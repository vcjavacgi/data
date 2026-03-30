import requests
import json
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

tickers = ["0981.HK", "1211.HK", "0175.HK", "2333.HK", "300750.SZ"]

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[403, 429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

url = f"https://query1.finance.yahoo.com/v6/finance/quote?symbols={','.join(tickers)}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://finance.yahoo.com/"
}

try:
    response = session.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    quotes = {}
    for q in data.get("quoteResponse", {}).get("result", []):
        quotes[q["symbol"]] = q
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quotes": quotes,
        "status": "success"
    }
    print(f"✅ 更新成功！共抓取 {len(quotes)} 只股票")
except Exception as e:
    print(f"❌ Yahoo 请求失败: {str(e)}")
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quotes": {},
        "status": "error",
        "error": str(e)
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
    
print("📁 data.json 已写入（即使失败也会生成）")
