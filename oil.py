import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def fetch_price():
    url = "http://www.qiyoujiage.com/yunnan/chuxiong.shtml"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"}
    res = requests.get(url, headers=headers, timeout=15)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table")
    if not table:
        return "未找到价格表格"

    rows = table.find_all("tr")
    lines = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        if cols:
            lines.append("  ".join(cols))
    return "\n".join(lines)

def push_notify(title, message):
    url = "https://messagepush.luckfast.com/send/avF9zCcVsXs/4453fbdabe83c204f4a5c1e03cb29ee5"
    params = {"title": title, "message": message}
    res = requests.get(url, params=params, timeout=10)
    print("推送结果：", res.text)

if __name__ == "__main__":
    today = datetime.now().strftime("%m月%d日")
    price = fetch_price()
    push_notify(f"⛽ 楚雄油价 {today}", price)
