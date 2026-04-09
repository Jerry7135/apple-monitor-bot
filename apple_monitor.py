import requests
import time
import json
import random
import re
import os  # 新增這一行

# --- GitHub使用者設定區 ---
# 改成從系統環境變數讀取，這樣 Token 才不會外洩
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN") 
# ------------------

# --- 電腦版使用者設定區 ---
#LINE_ACCESS_TOKEN = "0mA1KRI9KSo1bO+HaKinfSeBjLB0xVkWJKOmCzhaWaOPQSX5Ht5OfncK0cmEpnHi6mUW2o4U3m65SkiOsBZCUE5JXa4naeB8F/ZtQh2XA5yNz68XbF49Aear1nailQRa25x+lTZ9wHgg0wPrh7N0AAdB04t89/1O/w1cDnyilFU="

# ⚠️ 注意：網址已經拿掉 ?format=json，直接鎖定一般網頁
TARGET_URL = "https://www.apple.com/tw/shop/refurbished/mac"

# 關鍵字設定
KEYWORD_TARGET = "13吋 MacBook Air M4 整修品" #"14 吋 MacBook Pro"

# 檢查頻率（秒）：1800 秒 = 30 分鐘 (若要搶手動改為 300)
CHECK_INTERVAL = 600 
# ------------------

def send_line_message(msg):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    payload = {"messages": [{"type": "text", "text": msg}]}
    try: requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    except: pass

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
    print(f"🚀 Apple 破窗硬幹版啟動")
    print(f"📍 目標: {KEYWORD_TARGET}")
    
    session = requests.Session()
    
    # 狀態紀錄開關：避免連續半小時都發通知
    is_currently_in_stock = False
    
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] 🕵️ 正在讀取網頁原始碼...")
            # 增加隨機微小延遲
            time.sleep(random.uniform(1.5, 4.0))
            
            response = session.get(TARGET_URL, headers=get_headers(), timeout=20)
            html_content = response.text
            
            # 最暴力的解法：直接搜尋字串
            if KEYWORD_TARGET.upper() in html_content.upper():
                
                if not is_currently_in_stock:
                    print("🚨 發現目標！立刻發送通知！")
                    
                    # 嘗試用正規表達式挖出完整的商品名稱 (挖不到也沒關係)
                    full_name = KEYWORD_TARGET
                    match = re.search(rf'"productTitle":"([^"]*{KEYWORD_TARGET}[^"]*)"', html_content, re.IGNORECASE)
                    if match:
                        full_name = match.group(1)
                    
                    msg = f"🔥 警報！官網出現目標！\n\n發現機型：{full_name}\n\n🛒 點擊立刻前往搶購：\n{TARGET_URL}"
                    send_line_message(msg)
                    
                    # 標記為已在架上，下次巡邏如果是同一批貨就不再通知
                    is_currently_in_stock = True
                else:
                    print("🎯 目標仍在架上 (已通知過，保持靜默)")
                    
            else:
                if is_currently_in_stock:
                    print("📉 目標已從網頁消失 (售完)，重置監控開關。")
                    is_currently_in_stock = False # 重置，等待下次補貨
                else:
                    print("❌ 網頁原始碼中未發現目標...")

        except Exception as e:
            print(f"⚠️ 連線發生錯誤: {e}")

        # 隨機化巡邏頻率
        wait_time = CHECK_INTERVAL + random.randint(-60, 60)
        print(f"💤 休息 {wait_time // 60} 分鐘後再次更新頁面...\n")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
