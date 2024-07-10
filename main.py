###################################
# Author: Jerry.Chen
# Last Updated: YYYY-MM-DD
# Description:
# Usage:
###################################

import pandas as pd

# import requests
from bs4 import BeautifulSoup

# 目標網頁URL
url = "https://coscup.org/2024/zh-TW/session"
file_path = "session.html"


def main():
    print("Hello World")
    # 發送HTTP請求獲取網頁內容
    # response = requests.get(url)
    # response.encoding = "utf-8"
    # html_content = response.text

    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 找到日程表的表格
    schedule_tables = soup.find_all("table", class_="schedule-table")
    # 確認找到了幾個class="schedule-table"的表格
    print(f"Found {len(schedule_tables)} tables with class 'schedule-table'")
    # 初始化存儲議程資訊的列表
    sessions = []

    # 遍歷每個表格
    for table in schedule_tables:
        # 找到tbody元素
        tbody = table.find("tbody", class_="table-body")
        if tbody:

            for row in tbody.find_all("tr"):
                session_info = {}
                # 找到每個議程項目
                schedule_item = row.find("a", class_="schedule-item")

                if schedule_item:
                    session_info["track"] = schedule_item.find("h4", class_="track").text.strip() if schedule_item.find("h4", class_="track") else ""
                    session_info["time"] = schedule_item.find("h4", class_="period").text.strip() if schedule_item.find("h4", class_="period") else ""
                    session_info["title"] = schedule_item.find("h2", class_="title").text.strip() if schedule_item.find("h2", class_="title") else ""
                    session_info["speakers"] = (
                        schedule_item.find("h3", class_="speaker-list").text.strip() if schedule_item.find("h3", class_="speaker-list") else ""
                    )
                    session_info["tags"] = schedule_item.find("div", class_="tag-list").text.strip() if schedule_item.find("div", class_="tag-list") else ""

                    # 將議程信息添加到列表中
                    sessions.append(session_info)
    # 將列表轉換為DataFrame
    df = pd.DataFrame(sessions)

    # 將DataFrame輸出為CSV檔案
    df.to_csv("conference_schedule.csv", index=False, encoding="utf-8-sig")

    print("CSV檔案已生成：conference_schedule.csv")


if __name__ == "__main__":
    main()
