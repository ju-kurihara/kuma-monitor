import os
from playwright.sync_api import sync_playwright
import re

def run():
    last_data_file = "last_data.txt"
    # 前回保存した「最後に投稿した日付＋場所」を読み込む
    old_data = ""
    if os.path.exists(last_data_file):
        with open(last_data_file, "r", encoding="utf-8") as f:
            old_data = f.read().strip()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        try:
            page.wait_for_selector('.tabulator-cell', timeout=30000)
            cells = page.query_selector_all('.tabulator-cell')
            
            if cells:
                new_reports = []
                # リストを上（最新）から順に確認
                for i in range(0, len(cells), 3):
                    if i + 2 >= len(cells): break
                    
                    header = cells[i].inner_text() # 日時＋場所
                    detail = cells[i+2].inner_text() # 状況
                    
                    # このデータが「前回保存したもの」と同じなら、これ以降は全て既読
                    if header == old_data:
                        break
                    
                    # 年(/26)をカットして整形
                    display_header = re.sub(r'/\d{2}\s', ' ', header)
                    new_reports.append(f"【新潟県クマ出没情報】\n{display_header}\n{detail}")

                if new_reports:
                    print(f"★新着情報を {len(new_reports)} 件見つけました。")
                    # 最新順に並んでいるので、古い順（下から順）に投稿予約
                    for report in reversed(new_reports):
                        print("------------------------------------------")
                        print("★【SNS投稿シミュレーション】★")
                        print(report)
                        # ここで実際には投稿命令を送ります
                        print("------------------------------------------")

                    # 一番新しい（リストの先頭の）データを次回のために保存
                    latest_id = cells[0].inner_text()
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
