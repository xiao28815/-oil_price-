import requests

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

    text = res.text

    price92 = ""
    price95 = ""

    # 👉 核心：逐行筛选
    for line in text.split("\n"):
        line = line.strip()

        if "92号汽油" in line and "元/升" in line:
            price92 = line

        if "95号汽油" in line and "元/升" in line:
            price95 = line

    # 👉 二次清洗（去HTML标签）
    import re
    clean = lambda x: re.sub("<.*?>", "", x)

    price92 = clean(price92)
    price95 = clean(price95)

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
