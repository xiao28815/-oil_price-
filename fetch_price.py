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

    # 只找包含价格数字（如 7.89）的文本，过滤掉JS和导航文字
    result = []
    fuel_types = ["92", "95", "98", "柴油"]
    
    for tag in soup.find_all(["td", "div", "p", "span", "li"]):
        text = tag.get_text(strip=True)
        # 必须同时包含油号关键词和价格数字
        has_fuel = any(f in text for f in fuel_types)
        has_price = re.search(r"\d+\.\d{2}", text)
        if has_fuel and has_price and len(text) < 30:
            result.append(text)

    if not result:
        # 兜底：直接找所有含小数的短文本
        for tag in soup.find_all(text=re.compile(r"\d+\.\d{2}")):
            text = tag.strip()
            if text and len(text) < 30:
                result.append(text)

    if not result:
        return "未找到价格数据"

    # 去重
    seen = set()
    final = []
    for l in result:
        if l not in seen:
            seen.add(l)
            final.append(l)

    return "\n".join(final[:10])  # 最多10条，控制长度


def push_notify(title, message):
    url = "https://messagepush.luckfast.com/send/avF9zCcVsXs/4453fbdabe83c204f4a5c1e03cb29ee5"
    # 截断防止再次 PayloadTooLarge
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
