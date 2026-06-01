import os
import re
from playwright.sync_api import sync_playwright

def run():
    last_data_file = "last_data.txt"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("原本サイトにアクセス中...")
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        try:
            print("データの読み込みを待っています...")
            page.wait_for_selector('.tabulator-row', timeout=30000)
            rows = page.query_selector_all('.tabulator-row')
            
            if rows:
                print(f"合計 {len(rows)} 件のデータの中から最新3件を表示します：\n")
                
                for i in range(min(len(rows), 3)):
                    row = rows[i]
                    # セルを全て取得し、中身があるものだけを抽出
                    cells = row.query_selector_all('.tabulator-cell')
                    texts = [c.inner_text().strip() for c in cells if c.inner_text().strip()]
                    
                    if len(texts) >= 2:
                        # texts[0]が日時・場所、texts[1]が詳細であることが多いです
                        header = texts[0]
                        detail = texts[1]
                        
                        # 年(/26)をカット
                        clean_header = re.sub(r'/\d{2}\s', ' ', header)
                        
                        print(f"--- 【{i+1}件目】 ---")
                        print(f"【新潟県クマ出没情報】")
                        print(f"{clean_header}")
                        print(f"{detail}\n")
                
                # エラー回避のため、空のファイルを作っておく
                with open(last_data_file, "w", encoding="utf-8") as f:
                    f.write("TEST_MODE")
            else:
                print("データが見つかりませんでした。")
        except Exception as e:
            print(f"エラー発生: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
