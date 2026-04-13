import requests
from bs4 import BeautifulSoup

# 修改为你的城市页面
url = "http://www.qiyoujiage.com/yunnnan/chuxiong.shtml"

# Server酱KEY
sendkey = "SCT337050TjH8PFrQdsHkgTlEkbCNBHUFy"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, "html.parser")
text = soup.get_text()

price92 = ""
price95 = ""

for line in text.split("\n"):
    if "92号汽油" in line:
        price92 = line.strip()
    if "95号汽油" in line:
        price95 = line.strip()

msg = f"""
今日油价

{price92}
{price95}
"""

push_url = f"https://sctapi.ftqq.com/{sendkey}.send"

requests.get(push_url, params={
    "title": "今日油价提醒",
    "desp": msg
})
