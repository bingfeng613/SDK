import json
import os
import re


#
# 需要把json里面的数据项拆成列表形式
#
# 1.找到json里数据项对应的键
#     有两大类情况：
#     大部分键是“收集个人信息类型”
#     小部分是其他键，如“个人信息字段”、“获取信息”、“个人信息的类型”等等，需要造个识别它们的方法
#
# 2.将数据项拆开
#     现在发现需要特殊处理的情况：
#     顿号：如"设备生产厂商、设备型号、操作系统名称"，应拆为["设备生产厂商","设备型号","操作系统名称"]
#     逗号：如"设备生产厂商，设备型号，操作系统名称"，应拆为["设备生产厂商","设备型号","操作系统名称"]
#     括号：如"设备标识信息（AndroidID、IDFA、IDFV）"，应拆为["AndroidID","IDFA","IDFV"]
#     连接词：如"经纬度、GNSS信息、WiFi地址及信号强度信息"，应拆为["经纬度","GNSS信息","WiFi地址",信号强度信息"]
#     混合：如"设备标识信息（AndroidID、IDFA、IDFV）、经纬度、GNSS信息、WiFi地址及信号强度信息、IP地址、蓝牙信息和传感器信息（加速度，陀螺仪、方向、压力、旋转矢量、光照、磁力计）"
#

def find_key(key_list):
    '''
    :param key: 传入的json键列表
    :return: 找到的数据项对应的键
    '''

    for key in key_list:
        if "信息" in key:  # 捕获包含“信息”的键值
            return key
        elif "information" in key:
            return key
    return None


# 用于提取括号项的函数
def split_items(value_string):
    items = []
    # 将中文左括号替换为英文左括号
    if not isinstance(value_string,list):
        if value_string == None:
            pass
        else:
            value_string = value_string.replace('(', '（')
            # 将中文右括号替换为英文右括号
            value_string = value_string.replace(')', '）')
            value_string = value_string.replace('【', '（')
            # 将中文右括号替换为英文右括号
            value_string = value_string.replace('】', '）')

            stack = []  # 用于跟踪括号的栈
            current_item = ''  # 当前项的内容
            inside_parentheses = False  # 标记是否处于括号内

            for char in value_string:
                if char == '（':  # 遇到左括号
                    stack.append(char)
                    inside_parentheses = True
                    current_item += char
                elif char == '）' and stack:  # 遇到右括号且栈非空
                    stack.pop()
                    current_item += char
                    if not stack:  # 如果栈为空，表示所有左括号都已找到匹配的右括号
                        inside_parentheses = False
                        items.append(current_item)
                        current_item = ''
                elif inside_parentheses:  # 如果当前处于括号内，继续添加字符到当前项
                    current_item += char
                elif not inside_parentheses and char in ['、', '，', ',', '以及']:  # 如果处于括号外且遇到分隔符
                    if current_item:
                        items.append(current_item)
                        current_item = ''
                else:
                    current_item += char

            if current_item:  # 添加最后一个项
                items.append(current_item)

    return items


def break_value(value_string):
    '''
    :param key: 传入的数据项对应的值
    :return: 修改后数据项对应的列表形式的值
    '''
    print("原始内容:", value_string)
    all_items = []
    # 如果不是字典的格式 则进行括号项的提取
    if not isinstance(value_string,dict):
        all_items.extend(split_items(value_string))
    else:
        # 对于字典的格式 对value值进行提取
        for key ,value in value_string.items():
            all_items.extend(value)
    print("划分项之后的内容:", all_items)

    result = []
    # 下面开始拆括号
    for item in all_items:
        # print(item)
        # if not re.search(r'（|）', item):
        if not (re.search(r'（', item) and re.search(r'）', item)):
            # 不包含括号的项
            result.extend(re.split(r'及|和|以及|还有|:|：|;|；|。|如', item))
        else:
            # item中只包含“（”而不包含“）”，在item末尾添加一个“）”
            if re.search(r'（', item) and not re.search(r'）', item):
                item += '）'

            # 检查括号内的内容是否只包含一个信息项（没有分隔符）
            if not re.search(r'、|，|, |及|和|以及|还有|与|/|:|：|;|；|。|如', item):
                # 括号内只有单独的项目 说明是解释性的内容
                result.append(item)
            else:
                # 定义匹配括号内内容的正则表达式
                pattern = re.compile(r'（([^）]+)）')
                # pattern = re.compile(r'（([^）]+)）|【([^】]+)】')
                matches = pattern.findall(item)
                # print(matches)
                for match in matches:
                    # print(type(match))
                    result.extend(re.split(r'、|，|, |及|和|以及|还有|与|/|:|：|;|；|。|如', match))


    # 使用列表推导式去除result中的所有空字符串
    result = [x for x in result if x != '']
    print("最终结果:", result)
    print()

    return result


def data_item_format(input_data):
    '''
    :param input_data: 解析结果json
    :return: 修改数据项对应value值之后的json
    '''

    output_data = input_data

    # Process "display-result1" section
    for item in output_data.get("display-result1", []):
        key_list = item.keys()
        data_key = find_key(key_list)
        if data_key and item[data_key]:
            temple = []
            # 有可能是列表形式
            if isinstance(item[data_key], list):
                for t in item[data_key]:
                    temple.extend(break_value(t))
                item[data_key] = temple
            # 有可能是字典形式
            elif isinstance(item[data_key],dict):
                for key, value in item[data_key].items():
                    temple.extend(break_value(value))
                item[data_key] = temple
            # 普通形式
            else:
                item[data_key] = break_value(item[data_key])

    # Process "table-result1" section
    for item in output_data.get("table-result1", []):
        key_list = item.keys()
        data_key = find_key(key_list)
        if data_key and item[data_key]:
            temple = []
            # 有可能是列表形式
            if isinstance(item[data_key], list):
                for t in item[data_key]:
                    temple.extend(break_value(t))
                item[data_key] = temple
            # 有可能是字典形式
            elif isinstance(item[data_key], dict):
                for key, value in item[data_key].items():
                    temple.extend(break_value(value))
                item[data_key] = temple
            # 普通形式
            else:
                item[data_key] = break_value(item[data_key])

    return output_data


def process_single_json(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_data = json.load(file)

    processed_data = data_item_format(input_data)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)


def process_json_folder(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)
            process_single_json(input_file_path, output_file_path)


if __name__ == "__main__":
    pass
    # input_file_path = r"C:\Users\DELL\Desktop\nyh大创\result2_json格式错误_手工处理\com.car300.activity_5.2.1.02_52102_policy.json"
    # output_file_path = r"C:\Users\DELL\Desktop\nyh大创\result2_json格式错误_手工处理\com.car300.activity_5.2.1.02_52102_policy.json"
    # process_single_json(input_file_path, output_file_path)

    # input_folder_path = r"C:\Users\DELL\Desktop\nyh大创\表格替换后的json"
    # output_folder_path = r"/result1"
    # process_json_folder(input_folder_path, output_folder_path)
