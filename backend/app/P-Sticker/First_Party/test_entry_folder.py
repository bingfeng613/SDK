# 第一方隐私政策 跑文件夹
import os
import json

from bs4 import BeautifulSoup
from extract.display_table_extract_tradition import run_SDK_analysis

def entry(html_folder):
    # 获取html_folder的父文件夹路径
    parent_folder = os.path.dirname(html_folder)

    # 在父文件夹路径下创建result文件夹
    json_folder = os.path.join(parent_folder, 'json_result')

    # json_folder = '../data/first_display/json_result'  # 第一方页面中陈述

    # 创建结果文件夹（如果不存在）
    os.makedirs(json_folder, exist_ok=True)

    # 遍历HTML文件夹中的所有文件
    for filename in os.listdir(html_folder):
        if filename.endswith('.html'):
            # 构造HTML文件的完整路径
            html_file = os.path.join(html_folder, filename)

            print("--------------------------------")
            print(html_file + str(":"))

            # 读取HTML文件内容进行操作
            with open(html_file, 'r', encoding='utf-8') as file:
                content = file.read()

                soup = BeautifulSoup(content, 'html.parser')
                result = run_SDK_analysis(url=None, soup=soup)

            # 构造JSON文件名（去掉后缀的单纯文件名加上JSON后缀）
            json_filename = os.path.splitext(filename)[0] + '.json'

            # 构造JSON文件的完整路径
            result_json_path = os.path.join(json_folder, json_filename)

            # 检查文件是否存在
            if not os.path.exists(result_json_path):
                # 创建一个空的JSON对象
                empty_json = {}

                # 打开文件并写入空的JSON内容
                with open(result_json_path, 'x', encoding='utf-8') as file:
                    json.dump(empty_json, file, ensure_ascii=False, indent=2)

            with open(result_json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    html_folder = '../data/incised_data_privacy_html/Batch_35/html'
    entry(html_folder)





