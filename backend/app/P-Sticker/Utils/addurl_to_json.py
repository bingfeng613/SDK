# 把三百多个JSON里的链接添加到sdk_url_list里

import json
import os
import re


# 把统一后的JSON文件里的URL提出来放到set里
def extract_urls_from_json_files(folder_path):
    urls_set = set()

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 提取每个文件中所有字典中 key 为 "url" 的值
                for item in data:
                    if 'url' in item:
                        if isinstance(item['url'], dict):
                            item['url'] = list(item['url'].values())

                        if isinstance(item['url'], list):
                            print("item['url']: ", item['url'])
                            for i in item['url']:
                                url = re.findall(
                                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
                                # print("提取到的 URL：", url)
                                if len(url)>0:
                                    urls_set.add(url[0])
                        else:
                            print("item['url']: ", item['url'])
                            # 使用正则表达式提取 URL 部分
                            url = re.findall(
                                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item['url'])
                            # print("提取到的 URL：", url)
                            if len(url) > 0:
                                urls_set.add(url[0])

    return urls_set

if __name__ == '__main__':
    json_path = "../../data/Third_Party_Text/sdk_url_list.json"
    with open(json_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    # 将列表内容复制到一个Set中
    ini_url_set = set(data)
    # print("ini_url_set: ", ini_url_set)

    # 指定文件夹路径
    folder_path = '../../data/submit/no_batch_json_to_3keys'
    to3keys_urls_set = extract_urls_from_json_files(folder_path)
    # print(urls_set)

    # 合并两个 set 并去除重复部分
    merged_set = ini_url_set.union(to3keys_urls_set)
    print("合并后的 set 去重效果：", merged_set)

    merged_list = list(merged_set)
    result_path = "../../data/Third_Party_Text/merged_sdk_url_list.json"
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, 'w', encoding="utf-8") as file:
        json.dump(merged_list, file, indent=2, separators=(',', ': '))