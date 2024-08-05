# 第三方文本切割入口

import os
import json
import re

from thirdtext_incise import run_thirdtext_incise
from language_format import punctuation_C2E


def has_more_than_five_lines(text):
    # 定义匹配四个中文字符后跟换行符的正则表达式
    pattern = r'[\u4e00-\u9fff]{4}\n'
    # 使用findall找到所有匹配的子串
    matches = re.findall(pattern, text)
    # 检查匹配的数量是否超过5个
    return len(matches) > 6
def write_result_to_json(result, specific_file, json_folder):
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    # 去除文件名中的扩展名
    file_name = os.path.splitext(specific_file)[0]

    # 创建JSON文件路径
    json_file_path = os.path.join(json_folder, f"{file_name}.json")
    for i in result:
        if has_more_than_five_lines(i):
            #if "文档"in i or "产品" in i or "推荐" in i or "商务" in i or "常见问题" in i or "开发者" in i or "关于我们" in i or "中心" in i:
            if "产品试用" in i or "产品工具" in i or "更多产品" in i or "开发者平台" in i or "免责声明" in i or "常见问题" in i or "文档中心" in i or "帮助中心" in i or"开发文档" in i or "产品中心" in i or "人才招聘" in i or "商务合作" in i or "热门推荐" in i or "房产服务" in i:
                result.remove(i)
        #if len(i)>8000:
         #   print(file_name+"aaa")
          #  print(i)
    data = {
        "result-len": len(result),    # 列表里的文本段数
        "join-text": ' '.join(result),   # 组成一段文本
        "result-list": result
    }



    # 将结果写入JSON文件
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def extract_text_from_json_files(folder_path, specific_file=None, json_folder="Third_Party_Text"):
    extracted_texts = ""
    if specific_file:
        file_path = os.path.join(folder_path, specific_file)
        if os.path.exists(file_path) and file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                oridata = json.load(file)
                data = punctuation_C2E(oridata[0])
                result = run_thirdtext_incise(data)
                write_result_to_json(result, specific_file, json_folder)

                return data
    else:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    #print("正在处理:", file_path)
                    oridata = json.load(file)
                    data = punctuation_C2E(oridata[0])
                    result = run_thirdtext_incise(data)
                    write_result_to_json(result, file_name, json_folder)

    return extracted_texts

if __name__ == '__main__':

    # 运行单个文件
    #extracted_text = extract_text_from_json_files('D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result_确定为sdk隐私政策的文本', specific_file='163.com.pgbcorp163comgblegal.json')

    # 运行整个文件夹
    extract_text_from_json_files('D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result_确定为sdk隐私政策的文本')
