import threading
import time
import requests

def keep_alive():
    while True:
        try:
            requests.get("https://apibabysteps-production.up.railway.app/")
            print("✅ Keep-alive ping sent")
        except Exception as e:
            print("❌ Keep-alive failed:", e)
        time.sleep(300)  # 5 minutes

threading.Thread(target=keep_alive, daemon=True).start()
