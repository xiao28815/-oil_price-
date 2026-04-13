import requests
from bs4 import BeautifulSoup

# ========= 配置 =========
url = "http://www.qiyoujiage.com/yunnan/chuxiong.shtml"
sendkey = "SCT337050TjH8PFrQdsHkgTlEkbCNBHUFy"
# ======================

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    price92 = ""
    price95 = ""

    # 👉 关键：找表格里的数据
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            text = row.get_text().strip()

            if "92号汽油" in text:
                price92 = text

            if "95号汽油" in text:
                price95 = text

    # 👉 清洗格式（去掉多余空格）
    price92 = " ".join(price92.split())
    price95 = " ".join(price95.split())

    # 👉 兜底
    if not price92:
        price92 = "92号汽油：获取失败"
    if not price95:
        price95 = "95号汽油：获取失败"

    msg = f"""
📊 今日油价（楚雄）

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
