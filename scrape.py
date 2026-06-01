import os
import re
from playwright.sync_api import sync_playwright

def run():
    # テスト用：前回の記憶を無視して、今サイトにある最新3件を必ず表示します
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("原本サイトにアクセス中...")
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        try:
            # 1. サイトの「行」が表示されるまでじっくり待つ
            print("データの読み込みを待っています...")
            page.wait_for_selector('.tabulator-row', timeout=30000)
            
            # 2. 全ての「行」を取得
            rows = page.query_selector_all('.tabulator-row')
            
            if rows:
                print(f"合計 {len(rows)} 件のデータを見つけました。最新3件を表示します：\n")
                
                # 3. 最新の3件分をループして表示
                for i in range(min(len(rows), 3)):
                    row = rows[i]
                    # 行の中にある「セル（箱）」を取得
                    cells = row.query_selector_all('.tabulator-cell')
                    
                    if len(cells) >= 3:
                        header = cells[0].inner_text()  # 日付＋場所
                        detail = cells[2].inner_text()  # 状況
                        
                        # 日付の「/26（年）」を消して「5/30」などの形に整形
                        clean_header = re.sub(r'/\d{2}\s', ' ', header)
                        
                        print(f"--- 【{i+1}件目】 ---")
                        print(f"【新潟県クマ出没情報】")
                        print(f"{clean_header}")
                        print(f"{detail}\n")
            else:
                print("行（row）が見つかりませんでした。")
        except Exception as e:
            print(f"エラー発生: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
if __name__ == "__main__":
    run()
