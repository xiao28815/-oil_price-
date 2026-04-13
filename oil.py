import requests
from bs4 import BeautifulSoup
import re

# ========= 配置区域 =========
# 修改为你的城市页面
url = "http://www.qiyoujiage.com/yunnan/chuxiong.shtml"

# Server酱 SendKey
sendkey = "SCT337050TjH8PFrQdsHkgTlEkbCNBHUFy"
# ==========================

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()

    # ========= 正则提取价格（核心修复） =========
    match92 = re.search(r"92号汽油.*?([\d\.]+)元/升", text)
    match95 = re.search(r"95号汽油.*?([\d\.]+)元/升", text)

    if match92:
        price92 = f"92号汽油：{match92.group(1)}元/升"
    else:
        price92 = "92号汽油：获取失败"

    if match95:
        price95 = f"95号汽油：{match95.group(1)}元/升"
    else:
        price95 = "95号汽油：获取失败"

    # ========= 组织推送内容 =========
    msg = f"""
📊 今日油价

{price92}
{price95}
"""

except Exception as e:
    msg = f"油价获取失败：{str(e)}"

# ========= 推送 =========
push_url = f"https://sctapi.ftqq.com/{sendkey}.send"

requests.get(push_url, params={
    "title": "今日油价提醒",
    "desp": msg
})
