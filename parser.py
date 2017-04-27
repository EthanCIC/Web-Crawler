# pylint: disable=I0011,C0103
"""
Python Web Crawler Practice
"""

import requests
import os
from lxml import html

for pages in range(2100, 2153):
    get_beauty = requests.get("https://www.ptt.cc/bbs/Beauty/index" + str(pages) + ".html")
    tree = html.fromstring(get_beauty.content)
    beauty = tree.xpath('//div[@class="r-ent"]')
    print("Now downloading page:", pages)

    beauty_data = []
    for i in range(20):
        try:
            beauty_push = int(beauty[i][0].text_content())
        except ValueError:
            if beauty[i][0].text_content() == "爆":
                beauty_push = 999
            else:
                beauty_push = 0
        # beauty_push = beauty[i][0].text_content()
        beauty_title = str(beauty[i][2].text_content()).strip()
        beauty_url = str(list((beauty[0]).iterlinks())[0][2])
        beauty_data.append([beauty_push, beauty_title, beauty_url])

    for row_data in beauty_data:
        if row_data[0] > 80:

            # 解析 html ，並抽取出 url
            get_beauty_html = requests.get("https://www.ptt.cc" + row_data[2])
            tree = html.fromstring(get_beauty_html.content)
            beauty_pics = tree.xpath('//div[@class="bbs-screen bbs-content"]//@href')

            # 取得標題
            folder_name = row_data[1]

            # 建立資料夾並下載圖片
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            no = 1
            for i, pic_url in enumerate(beauty_pics):
                # 判斷此網址是否為圖片，是的話存入電腦
                if ".jpg" in pic_url:
                    pic = requests.get(pic_url)
                    file_name = str(no) + ".jpg"
                    file_path = os.path.join(folder_name, file_name)
                    with open(file_path, 'wb') as picture:
                        picture.write(pic.content)
                    no += 1
                