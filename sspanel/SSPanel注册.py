#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gaochen on 2022/10/16
# SSPanel注册.py
import json

import requests

email = "gcwm99@gmail.com"
password = "1123lovewm"


def register(url: str):
    """
    注册

    :param url:
    :return:
    """

    data = {
        "email": email,
        "name": "小敏同志",
        "passwd": password,
        "repasswd": password,
        "code": 0
    }
    try:
        r = requests.post(url, data=data).json()
        print(f"{url} 注册完毕 {r}")
        if r["ret"] == 1:
            f1.write(f"{url},{email},{password}\n")
            f1.flush()
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    # register("https://eifa.cloud/auth/register")
    with open("dataset_2022-10-16.txt", "r", encoding="utf-8") as f:
        with open("注册成功.csv", "a") as f1:
            for line in f.readlines():
                register(line.strip())
