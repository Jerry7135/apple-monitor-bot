import requests
import time
import json
import random
import re
import os

# --- 雲端版使用者設定區 ---
# 從 GitHub Secrets 讀取 Token
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN") 

TARGET_URL = "https://www.apple.com/tw/shop/refurbished/mac"

# 目標關鍵字
KEYWORD_TARGET = "13 吋 MacBook"#"24 吋 iMac Apple""13 吋 MacBook"
# ------------------

def send_line_message(msg):
    if not LINE_ACCESS_TOKEN:
        print("❌ 致命錯誤：找不到 LINE_ACCESS_TOKEN！請確認 GitHub Secrets 是否有正確設定。")
        return

    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    payload = {"messages": [{"type": "text", "text": msg}]}
    
    try: 
        print("準備發送 LINE 通知...")
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            print("✅ LINE 廣播發送成功！")
        else:
            print(f"❌ LINE 發送失敗，錯誤碼: {response.status_code}, 內容: {response.text}")
    except Exception as e: 
        print(f"⚠️ 發送 LINE 時發生網路異常: {e}")

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "close"  # 💡 雲端防護升級：打帶跑戰術，問完就走
    }

def main():
    print(f"🚀 Apple 雲端破窗版啟動 (單次掃描打帶跑)")
    print(f"📍 目標: {KEYWORD_TARGET}")
    
    try:
        print(f"[{time.strftime('%H:%M:%S')}] 🕵️ 正在讀取網頁原始碼...")
        # 增加隨機微小延遲，避免被防火牆秒殺
        time.sleep(random.uniform(1.5, 4.0))
        
        # 💡 戰術改變：直接使用 requests.get，不建立 session
        response = requests.get(TARGET_URL, headers=get_headers(), timeout=20)
        html_content = response.text
        
        if KEYWORD_TARGET.upper() in html_content.upper():
            print("🚨 發現目標！準備執行發報程序！")
            
            full_name = KEYWORD_TARGET
            match = re.search(rf'"productTitle":"([^"]*{KEYWORD_TARGET}[^"]*)"', html_content, re.IGNORECASE)
            if match:
                full_name = match.group(1)
            
            msg = f"🔥 [雲端警報] 官網出現目標！\n\n發現機型：{full_name}\n\n🛒 點擊立刻前往搶購：\n{TARGET_URL}"
            send_line_message(msg)
                
        else:
            print("❌ 網頁原始碼中未發現目標...")
            title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
            if title_match:
                print(f"💡 (雲端機器人目前看到的網頁標題是: {title_match.group(1)})")

    except Exception as e:
        print(f"⚠️ 連線發生錯誤: {e}")

if __name__ == "__main__":
    main()
    print("✅ 巡邏任務完成，雲端容器即將關閉。")
