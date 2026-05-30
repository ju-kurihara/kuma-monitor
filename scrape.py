import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # ブラウザを起動（人間と同じ動きを再現）
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("原本サイトにアクセス中...")
        page.goto("https://www.arcgis.com/apps/dashboards/20b4d06fb3b34776959a4e69c7a8511a")
        
        # サイトが重いので、リスト（表）が表示されるまで最大30秒待つ
        print("データの読み込みを待っています（最大30秒）...")
        try:
            page.wait_for_selector('.tabulator-cell', timeout=30000)
            
            # データの1行目を取得
            cells = page.query_selector_all('.tabulator-cell')
            if cells:
                # 最初の数個のセル（日付、市町村など）を結合
                data = [cells[i].inner_text() for i in range(min(len(cells), 5))]
                result = " / ".join(data)
                print(f"--- 【成功】取得データ ---\n{result}")
            else:
                print("データが見つかりませんでした。")
        except Exception as e:
            print(f"読み込み失敗（タイムアウト）: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
