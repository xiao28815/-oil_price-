import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def fetch_price():
    url = "http://m.qiyoujiage.com/yunnan/chuxiong.shtml"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": "http://m.qiyoujiage.com/yunnan.shtml"
    }
    try:
        res = requests.get(url, headers=headers, timeout=8)
        res.encoding = "utf-8"
    except requests.exceptions.Timeout:
        return "请求超时"
    except requests.exceptions.ConnectionError:
        return "网络连接失败"

    soup = BeautifulSoup(res.text, "html.parser")

    # 按顺序找价格数字（网站固定顺序：92、95、98、柴油）
    labels = ["🟢 92号汽油", "🔵 95号汽油", "🟣 98号汽油", "🟡 0号柴油"]
    
    prices = []
    for tag in soup.find_all(text=re.compile(r"\d+\.\d{2}")):
        text = tag.strip()
        # 只要纯价格或"9.13(元)"这样的格式，过滤掉长文本
        if re.fullmatch(r"[\d.()元/升\s]+", text) and len(text) < 15:
            # 提取数字
            num = re.search(r"\d+\.\d{2}", text)
            if num:
                prices.append(num.group())

    # 去重保序
    seen = set()
    unique_prices = []
    for p in prices:
        if p not in seen:
            seen.add(p)
            unique_prices.append(p)

    if not unique_prices:
        return "未找到价格数据"

    # 拼接标号和价格
    lines = []
    for i, price in enumerate(unique_prices[:4]):
        label = labels[i] if i < len(labels) else f"油品{i+1}"
        lines.append(f"{label}：{price} 元/升")

    return "\n".join(lines)


def push_notify(title, message):
    url = "https://messagepush.luckfast.com/send/avF9zCcVsXs/4453fbdabe83c204f4a5c1e03cb29ee5"
    message = message[:200]
    params = {"title": title, "message": message}
    try:
        res = requests.get(url, params=params, timeout=10)
        print("推送结果：", res.text)
    except Exception as e:
        print("推送失败：", e)


if __name__ == "__main__":
    today = datetime.now().strftime("%m月%d日")
    price = fetch_price()
    print("抓取内容：\n", price)
    push_notify(f"⛽ 楚雄油价 {today}", price)
