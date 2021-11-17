import os
import sys

import requests

requests.packages.urllib3.disable_warnings()

hostname = "https://www.kejiwanjia.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
}


# 签到
def checkin():
    s = requests.session()
    s.headers.update({"authorization": "Bearer " + get_token()})
    url = f"{hostname}/wp-json/b2/v1/userMission"
    print(headers)
    r = s.post(url, headers=headers).json()
    try:
        bean = int(r.replace("\"", ""))
        print(f"您今天已经签到，获得{bean}个积分")
    except (TypeError, ValueError):
        print(f"签到成功，获得{r['credit']}个积分，连续签到{r['mission']['tk']['days']}天，剩余积分{r['mission']['my_credit']}")


def get_token():
    token = os.getenv("KJWJ_TOKEN")
    if token is None:
        print("请先添加环境变量：KJWJ_TOKEN")
        sys.exit(-1)
    return token


if __name__ == '__main__':
    checkin()
