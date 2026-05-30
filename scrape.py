import os
import re
from playwright.sync_api import sync_playwright

def post_to_x_simulation(message):
    # 本番ではここにXへの送信命令が入ります
    print("------------------------------------------")
    print("📢 【X投稿シミュレーション】")
    print(message)
    print("------------------------------------------")

def run():
    last_data_file = "last_data.txt"
    old_data = ""
    if os.path.exists(last_data_file):
        with open(last_data_file, "r", encoding="utf-8") as f:
            old_data = f.read().strip()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        try:
            # 表が表示されるまで待機
            page.wait_for_selector('.tabulator-row', timeout=30000)
            rows = page.query_selector_all('.tabulator-row')
            
            if rows:
                new_reports = []
                for row in rows:
                    cells = row.query_selector_all('.tabulator-cell')
                    if len(cells) >= 3:
                        header = cells[0].inner_text() # 日時＋場所
                        detail = cells[2].inner_text() # 状況
                        
                        # 既読チェック
                        if header == old_data:
                            break
                        
                        # 日付整形（年 /26 を消す）
                        display_header = re.sub(r'/\d{2}\s', ' ', header)
                        
                        # あなたの「理想の形式」に組み立て
                        # 【新潟県クマ出没情報】
                        # 日時 場所
                        # 状況（改行して表示）
                        new_reports.append(f"【新潟県クマ出没情報】\n{display_header}\n{detail}")

                if new_reports:
                    print(f"★新着を {len(new_reports)} 件見つけました。")
                    # 古いものから順にログへ表示（シミュレーション）
                    for report in reversed(new_reports):
                        post_to_x_simulation(report)

                    # 最後に、今回取得した中で一番新しいものを保存（次回は「新着なし」になる）
                    latest_id = rows[0].query_selector('.tabulator-cell').inner_text()
                    with open(last_data_file, "w", encoding="utf-8") as f:
                        f.write(latest_id)
                else:
                    print("新着情報はありませんでした（前回から更新なし）。")
            else:
                print("原本サイトのデータが読み取れませんでした。")
        except Exception as e:
            print(f"エラー発生: {e}")
        browser.close()

if __name__ == "__main__":
    run()
