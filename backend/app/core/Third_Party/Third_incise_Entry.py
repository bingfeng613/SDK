# 第三方隐私政策切割入口

import os
import json
import re

from thirdtext_incise import run_thirdtext_incise

import sys
sys.path.append("..")

from Utils.language_format import punctuation_C2E

def write_result_to_json(result, specific_file, json_folder):
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    # 去除文件名中的扩展名
    file_name = os.path.splitext(specific_file)[0]

    # 创建JSON文件路径
    json_file_path = os.path.join(json_folder, f"{file_name}.json")

    data = {
        "result-len": len(result),    # 列表里的文本段数
        "join-text": ' '.join(result),   # 组成一段文本
        "result-list": result
    }

    # 将结果写入JSON文件
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def extract_text_from_json_files(folder_path, specific_file=None, json_folder="../../data/Third_Party_Text/cleaned_text"):
    extracted_texts = ""

    if specific_file:
        file_path = os.path.join(folder_path, specific_file)
        if os.path.exists(file_path) and file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                data = punctuation_C2E(data)
                result = run_thirdtext_incise(data)
                write_result_to_json(result, specific_file, json_folder)

                return data


    else:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    print("正在处理:", file_path)
                    data = json.load(file)
                    data = punctuation_C2E(data)
                    result = run_thirdtext_incise(data)
                    write_result_to_json(result, file_name, json_folder)

    return extracted_texts

if __name__ == '__main__':

    # 运行单个文件
    # extracted_text = extract_text_from_json_files('../../data/Third_Party_Text/sdk_html_text', specific_file='163.com.pgbcorp163comgblegal.json')

    # 运行整个文件夹
    extract_text_from_json_files('../../data/Third_Party_Text/sdk_html_text')