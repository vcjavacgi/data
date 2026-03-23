import requests
import json
from datetime import datetime

# 所有可能用到的股票（自动覆盖你的 exportCategories）
tickers = ["0981.HK", "1211.HK", "0175.HK", "2333.HK", "300750.SZ"]

url = f"https://query1.finance.yahoo.com/v6/finance/quote?symbols={','.join(tickers)}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    quotes = {}
    for q in data.get("quoteResponse", {}).get("result", []):
        quotes[q["symbol"]] = q
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quotes": quotes
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新成功！共抓取 {len(quotes)} 只股票，时间 {result['timestamp']}")
except Exception as e:
    print(f"❌ 抓取失败: {e}")
