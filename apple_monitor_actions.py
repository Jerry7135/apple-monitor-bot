import requests
import time
import json
import random
import re
import os

# --- 使用者設定區 (從 GitHub Secrets 讀取) ---
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
TARGET_URL = "https://www.apple.com/tw/shop/refurbished/mac"
KEYWORD_TARGET = "24 吋 iMac Apple M4 晶片" #13吋 MacBook Air M4
# ------------------

def send_line_message(msg):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    payload = {"messages": [{"type": "text", "text": msg}]}
    try:
        res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        print(f"LINE 發送狀態: {res.status_code}")
    except Exception as e:
        print(f"LINE 發送錯誤: {e}")

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

def main():
    print(f"🚀 Apple 雲端巡邏啟動 (單次掃描模式)")
    
    try:
        # 模擬真人隨機延遲，避免 GitHub 固定 IP 被 Apple 瞬間偵測
        time.sleep(random.uniform(2, 5))
        
        response = requests.get(TARGET_URL, headers=get_headers(), timeout=30)
        html_content = response.text
        
        if KEYWORD_TARGET.upper() in html_content.upper():
            print("🚨 發現目標！")
            
            # 挖出完整名稱
            full_name = KEYWORD_TARGET
            match = re.search(rf'"productTitle":"([^"]*{KEYWORD_TARGET}[^"]*)"', html_content, re.IGNORECASE)
            if match:
                full_name = match.group(1)
            
            msg = f"🔥 [雲端報] 官網出現目標！\n\n機型：{full_name}\n🛒 搶購連結：{TARGET_URL}"
            send_line_message(msg)
        else:
            print("❌ 尚未發現目標。")

    except Exception as e:
        print(f"⚠️ 掃描發生錯誤: {e}")

if __name__ == "__main__":
    main()
    print("✅ 巡邏任務完成，正在關閉雲端環境。")
