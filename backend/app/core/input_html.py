# 输入隐私政策 也就是总入口

import os
import json

from bs4 import BeautifulSoup

from First_Party.extract.display_table_extract_tradition import run_SDK_analysis
from compare_analysis import run_compare
from Utils.first_sdk_dict_handle import run_get_first_sdk_dict_list_singlefile

def run_First_extract(html_file):
    '''
    开始切割第一方政策
    '''
    print("--------------------------------")
    print("正在处理:" + str(html_file) + str(":"))

    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        result = run_SDK_analysis(url=None, soup=soup)
        # result = {}

    # 构造JSON文件名（去掉后缀的单纯文件名加上JSON后缀）
    # json_filename = os.path.splitext(filename)[0] + '.json'

    # 构造JSON文件的完整路径
    # result_json_path = os.path.join(json_folder, json_filename)
    current_path = os.path.dirname(os.path.abspath(__file__))

    # 初步四元组的位置
    result_json_path = os.path.join(current_path, "第一方提取四元组.json")

    # 检查文件是否存在
    if not os.path.exists(result_json_path):
        # 创建一个空的JSON对象
        empty_json = {}

        # 打开文件并写入空的JSON内容
        with open(result_json_path, 'x', encoding='utf-8') as file:
            json.dump(empty_json, file, ensure_ascii=False, indent=2)

    with open(result_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 把四元组转化为标准四元组
    standard_first_json = run_get_first_sdk_dict_list_singlefile(result_json_path)

    # 标准四元组的位置
    standard_first_json_path = os.path.join(current_path, "标准第一方四元组.json")
    if not os.path.exists(standard_first_json_path):
        empty_json = {}
        with open(standard_first_json_path, 'x', encoding='utf-8') as file:
            json.dump(empty_json, file, ensure_ascii=False, indent=2)
    with open(standard_first_json_path, 'w', encoding='utf-8') as f:
        json.dump(standard_first_json, f, ensure_ascii=False, indent=2)

    # 进行不一致分析
    path = run_compare(standard_first_json)
    return path

if __name__ == "__main__":
    # print("11111")
    file_path = input("请输入待检测隐私政策HTML文档的文件路径: ")
    print("你输入的文件路径是: ", file_path)
    run_First_extract(file_path)
