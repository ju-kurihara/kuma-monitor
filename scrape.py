import os
from playwright.sync_api import sync_playwright
import re

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
                    # 1行（1件）の中にある全てのセルを取得
                    cells = row.query_selector_all('.tabulator-cell')
                    if len(cells) >= 3:
                        header = cells[0].inner_text() # 日時＋場所
                        detail = cells[2].inner_text() # 状況
                        
                        # 既読チェック
                        if header == old_data:
                            break
                        
                        # 年(/26)をカット
                        display_header = re.sub(r'/\d{2}\s', ' ', header)
                        new_reports.append(f"【新潟県クマ出没情報】\n{display_header}\n{detail}")

                if new_reports:
                    print(f"★新着情報を {len(new_reports)} 件見つけました。")
                    # 古いものから順にシミュレーション表示
                    for report in reversed(new_reports):
                        print("------------------------------------------")
                        print("★【SNS投稿シミュレーション】★")
                        print(report)
                        print("------------------------------------------")

                    # 一番新しいデータを保存
                    latest_id = rows[0].query_selector('.tabulator-cell').inner_text()
                    with open(last_data_file, "w", encoding="utf-8") as f:
                        f.write(latest_id)
                else:
                    print("新着情報はありませんでした。")
            else:
                print("データが空でした。")
        except Exception as e:
            print(f"エラー: {e}")
        browser.close()

if __name__ == "__main__":
    run()
