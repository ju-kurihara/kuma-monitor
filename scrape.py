import os
import re
from playwright.sync_api import sync_playwright
import tweepy # X投稿用のライブラリ

def post_to_x(message):
    # GitHubの金庫から鍵を取り出す
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    # Xに接続して投稿
    client = tweepy.Client(
        consumer_key=api_key, consumer_secret=api_secret,
        access_token=access_token, access_token_secret=access_secret
    )
    client.create_tweet(text=message)

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
                        
                        # 既読チェック（前回の最新と同じなら終了）
                        if header == old_data:
                            break
                        
                        # 年(/26)をカットして理想の形式に整形
                        display_header = re.sub(r'/\d{2}\s', ' ', header)
                        new_reports.append(f"【新潟県クマ出没情報】\n{display_header}\n{detail}")

                if new_reports:
                    print(f"新着を {len(new_reports)} 件見つけました。")
                    # 古いものから順にXへ投稿
                    for report in reversed(new_reports):
                        print(f"投稿中: {report}")
                        post_to_x(report)

                    # 今回の最新データを保存
                    latest_id = rows[0].query_selector('.tabulator-cell').inner_text()
                    with open(last_data_file, "w", encoding="utf-8") as f:
                        f.write(latest_id)
                else:
                    print("新着なし。投稿をスキップしました。")
            else:
                print("データが空でした。")
        except Exception as e:
            print(f"エラー発生: {e}")
        browser.close()

if __name__ == "__main__":
    run()
