import os
from playwright.sync_api import sync_playwright

def run():
    # 練習モード：IFTTTへの送信をストップしています
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
                # データを抽出し、投稿用メッセージを組み立てる
                raw_text = [cells[i].inner_text() for i in range(min(len(cells), 5))]
                
                # ここで文章の見た目を調整できます
                # 例：「日時：〇〇 / 場所：〇〇」のように整形
                report_text = f"【新潟県クマ出没情報】\n日時：{raw_text[0]}\n場所：{raw_text[1]}\n詳細：{raw_text[3]}"
                
                print("------------------------------------------")
                print("★【SNS投稿シミュレーション】★")
                print("実際にXに投稿される予定の文章は以下です：")
                print("\n" + report_text + "\n")
                print("------------------------------------------")
                
                # 新着判定のロジックだけは生かしておきます
                print(f"（内部判定用）現在の最新データ: {raw_text[0]}")
            else:
                print("データが見つかりませんでした。")
        except Exception as e:
            print(f"エラー: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
