# 爬取第三方隐私政策html
import json
import os

from selenium_driver import driver
from get_url_name import get_url_name_finall

def run_get_html():
    result_folder = "../../data/Third_Party_Text/re_get_third_html/html"
    failed_urls = []
    # json_path = "../../data/Third_Party_Text/sdk_url_list.json"
    json_path = "../../data/Third_Party_Text/re_get_third_html/failed_url.json"
    with open(json_path, "rb") as file:
        url_list = json.load(file)

    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    for url in url_list:
        url_name = get_url_name_finall(url)
        files_in_folder = os.listdir(result_folder)
        # temp = [os.path.splitext(file)[0] for file in files_in_folder]
        # print(temp)
        if url_name in [os.path.splitext(file)[0] for file in files_in_folder]:
            print("爬取过：", url_name)
            print("----------------------------")
            continue         # 如果是已经爬取了的文件就跳过

        print("正在爬取：", url)
        print("文件名为：", url_name)
        html = None
        try:
            html = driver.get_privacypolicy_html(url, False)
        except Exception as e:
            print("读取" + str(url) + "异常：")
            html = None
            print(e)

        if html:
            url_name = get_url_name_finall(url)
            html_file_path = os.path.join(result_folder, url_name + ".html")
            if not os.path.exists(html_file_path):
                os.makedirs(os.path.dirname(html_file_path), exist_ok=True)
            with open(html_file_path, "w", encoding="utf-8") as file:
                file.write(html)
            print("---------------------------------------------------------")
        else:
            print("无法爬取：", url)
            failed_urls.append(url)
            print("---------------------------------------------------------")

    return failed_urls

if __name__ == '__main__':
    failed_urls = run_get_html()
    failed_url_json = "../../data/Third_Party_Text/re_get_third_html/failed_url.json"
    os.makedirs(os.path.dirname(failed_url_json), exist_ok=True)
    with open(failed_url_json, "w") as file:
        json.dump(failed_urls, file, indent=2, separators=(',', ': '))
