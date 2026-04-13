import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

def fetch_price():
    # 用移动版页面，结构更简单
    url = "http://m.qiyoujiage.com/yunnan/chuxiong.shtml"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": "http://m.qiyoujiage.com/yunnan.shtml"
    }
    res = requests.get(url, headers=headers, timeout=15)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    lines = []

    # 方法1：找所有包含"汽油"或"柴油"的文本节点
    for tag in soup.find_all(text=re.compile(r"(汽油|柴油|元/升)")):
        text = tag.strip()
        if text:
            lines.append(text)

    # 方法2：找 table（备用）
    if not lines:
        table = soup.find("table")
        if table:
            for row in table.find_all("tr"):
                cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
                if cols:
                    lines.append("  ".join(cols))

    # 方法3：找含价格数字的 div/p
    if not lines:
        for tag in soup.find_all(["div", "p", "span", "li"]):
            text = tag.get_text(strip=True)
            if re.search(r"\d+\.\d+", text) and ("油" in text or "元" in text):
                lines.append(text)

    if not lines:
        # 兜底：打印前2000字符用于调试
        return "解析失败，页面内容片段：\n" + soup.get_text()[:500]

    # 去重并合并
    seen = set()
    result = []
    for l in lines:
        if l not in seen:
            seen.add(l)
            result.append(l)

    return "\n".join(result[:20])  # 最多取前20条


def push_notify(title, message):
    url = "https://messagepush.luckfast.com/send/avF9zCcVsXs/4453fbdabe83c204f4a5c1e03cb29ee5"
    params = {"title": title, "message": message}
    res = requests.get(url, params=params, timeout=10)
    print("推送结果：", res.text)


if __name__ == "__main__":
    today = datetime.now().strftime("%m月%d日")
    price = fetch_price()
    print("抓取内容：\n", price)  # GitHub Actions 日志里可以看到
    push_notify(f"⛽ 楚雄油价 {today}", price)
