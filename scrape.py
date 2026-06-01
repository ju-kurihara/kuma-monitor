import os
import re
import time
from playwright.sync_api import sync_playwright

def run():
    last_data_file = "last_data.txt"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 画面サイズを大きめにして、表が隠れないようにします
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        
        print("原本サイトにアクセス中...")
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        try:
            print("データの読み込みを待っています（最大30秒）...")
            page.wait_for_selector('.tabulator-row', timeout=30000)
            
            # さらに5秒、文字が流れてくるのをじっと待ちます
            print("文字が表示されるまで少し待機します...")
            time.sleep(5)
            
            rows = page.query_selector_all('.tabulator-row')
            
            if rows:
                print(f"合計 {len(rows)} 件のデータが見つかりました。\n")
                
                for i in range(min(len(rows), 3)):
                    row = rows[i]
                    # 行の中にあるすべての文字を強引に取得します
                    full_text = row.inner_text().strip()
                    
                    # 取得したテキストを行ごとに分割
                    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                    
                    if len(lines) >= 2:
                        # 日時・場所
                        header = lines[0]
                        # 状況（2行目以降を合体させる）
                        detail = " ".join(lines[1:])
                        
                        # 日付の「/26（年）」を消して整形
                        clean_header = re.sub(r'/\d{2}\s', ' ', header)
                        
                        print(f"--- 【{i+1}件目】 ---")
                        print(f"【新潟県クマ出没情報】")
                        print(f"{clean_header}")
                        print(f"{detail}\n")
                
                # エラー回避用ファイルの作成
                with open(last_data_file, "w", encoding="utf-8") as f:
                    f.write("TEST_MODE")
            else:
                print("データが見つかりませんでした。")
        except Exception as e:
            print(f"エラー発生: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
