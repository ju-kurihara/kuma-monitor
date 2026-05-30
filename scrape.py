import os
import requests
from playwright.sync_api import sync_playwright

def run():
    ifttt_key = os.environ.get("IFTTT_KEY")
    last_data_file = "last_data.txt"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("原本サイトにアクセス中...")
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        print("データの読み込みを待っています...")
        try:
            page.wait_for_selector('.tabulator-cell', timeout=30000)
            cells = page.query_selector_all('.tabulator-cell')
            
            if cells:
                # 最新の1件分（最初の5セル分）を抽出
                new_data = " / ".join([cells[i].inner_text() for i in range(min(len(cells), 5))])
                print(f"取得したデータ: {new_data}")

                # 【新着判定】前回保存したデータと比較
                old_data = ""
                if os.path.exists(last_data_file):
                    with open(last_data_file, "r", encoding="utf-8") as f:
                        old_data = f.read().strip()

                if new_data != old_data:
                    print("★新着情報を発見しました！IFTTTへ送信します。")
                    # IFTTTに送信（Value1にテキストを入れる）
                    ifttt_url = f"https://maker.ifttt.com/trigger/kuma_alert/with/key/{ifttt_key}"
                    requests.post(ifttt_url, json={"value1": new_data})
                    
                    # 今回のデータを保存
                    with open(last_data_file, "w", encoding="utf-8") as f:
                        f.write(new_data)
                else:
                    print("新着はありませんでした。")
            else:
                print("データが見つかりませんでした。")
        except Exception as e:
            print(f"エラー: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
