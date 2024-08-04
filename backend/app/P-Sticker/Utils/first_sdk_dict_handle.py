import os
import re
from some_function import write_json
from some_function import read_json
from some_function import is_valid_url
def spilt_str(result):
    if result:
        r = re.split(r'[、，]', result)
        return r

def run_get_first_sdk_dict_list_singlefile(filepath):
    '''
    跑单个文件
    '''
    num = 0
    #print("开始获取"+url+"的第一方sdk声明字典")
    # filepath = "D:\\中山\\隐私合规\\sdk_analysis_lh_11.15"
    #filepath = "D:\\中山\\隐私合规\\ali_first_sdk\\ali"
    # filepath = "D:\\大创项目\\性能评估\\App_sdk数据集评估\\待处理\\sdk_analysis_lh_11.15"
    # filepath = "D:\\大创项目\\性能评估\\App_sdk数据集评估\\待处理\\sdk_analysislh_4.22_jiayue\\json"
    # first_save_path = "D:\\中山\\隐私合规\\sdk_analysislh_11.15_handle"
    # first_save_path = "D:\\大创项目\\性能评估\\App_sdk数据集评估\\finished"
    #first_save_path = "D:\\中山\\隐私合规\\ali_first_sdk\\first_sdk"
    # filename_list = os.listdir(filepath)

    # 存放标准三元组的路径
    current_path = os.path.dirname(os.path.abspath(__file__))
    result_json_path = os.path.join(current_path, "第一方提取四元组的标准四元组.json")

    first_sdk_dict_list = None
    # for i in filename_list:
    sdk_dict_list = []
    #i = "com.bokecc.dance_8.0.6_345_policy.json"
    # if not i == "cn.colorv_6.28.9_492_policy.json":
    #     continue
    try:
        temp_sdk_dict = read_json(filepath)
        if temp_sdk_dict:
            # 遍历sdk_dict。得到数据，数据使用目的，第三方隐私政策链接
            if temp_sdk_dict["display-result"]:
                sdk_dict_list.extend(temp_sdk_dict["display-result"])
            if temp_sdk_dict['table-result']:
                sdk_dict_list.extend(temp_sdk_dict['table-result'])
            #print("提取出的sdk_dict_list:")
            #print(sdk_dict_list)
        # sdk_dict_list是所有字典结果
        if sdk_dict_list:
            # if sdk_dict_list == ['使用场景', '使用目的', '获取设备权限', '个人信息类型', '个人信息字段', '去标识化传输', '第三方机构名称', '官方链接地址']:
            #     print("file--", i)
            print("sdk_dict_list----", sdk_dict_list)
            first_sdk_dict_list = get_first_sdk_dict_list(sdk_dict_list)
            # print("最终list----", first_sdk_dict_list)


            if first_sdk_dict_list and len(first_sdk_dict_list)>1:

                write_json(result_json_path, first_sdk_dict_list[:])
            elif len(first_sdk_dict_list)==1:
                # num += 1
                print("长度为一")
                print("first_sdk_dict_list,", first_sdk_dict_list)
                # print("file--",i)
                print("--------------------------------")
                # print("abcdefg")
    except Exception as e:
        # num = num+1
        print('e:',e)
        # print("第",num,"个写入失败")
        print("写入失败")
        print("--------------------------------")

    # 返回存标准四元组的位置，以备后续使用
    print("标准四元组位置：", result_json_path)
    return result_json_path

def run_get_first_sdk_dict_list():
    '''
    filepath是文件夹路径
    '''
    num = 0
    #print("开始获取"+url+"的第一方sdk声明字典")
    filepath = "D:\\中山\\隐私合规\\sdk_analysis_lh_11.15"
    #filepath = "D:\\中山\\隐私合规\\ali_first_sdk\\ali"
    filepath = "D:\\大创项目\\性能评估\\App_sdk数据集评估\\待处理\\sdk_analysis_lh_11.15"
    # filepath = "D:\\大创项目\\性能评估\\App_sdk数据集评估\\待处理\\sdk_analysislh_4.22_jiayue\\json"
    # first_save_path = "D:\\中山\\隐私合规\\sdk_analysislh_11.15_handle"
    first_save_path = "D:\\大创项目\\性能评估\\App_sdk数据集评估\\finished"
    #first_save_path = "D:\\中山\\隐私合规\\ali_first_sdk\\first_sdk"
    filename_list = os.listdir(filepath)
    first_sdk_dict_list = None
    for i in filename_list:
        sdk_dict_list = []
        #i = "com.bokecc.dance_8.0.6_345_policy.json"
        # if not i == "cn.colorv_6.28.9_492_policy.json":
        #     continue
        try:
            temp_sdk_dict = read_json(filepath+"\\"+i)
            if temp_sdk_dict:
                # 遍历sdk_dict。得到数据，数据使用目的，第三方隐私政策链接
                if temp_sdk_dict["display-result"]:
                    sdk_dict_list.extend(temp_sdk_dict["display-result"])
                if temp_sdk_dict['table-result']:
                    sdk_dict_list.extend(temp_sdk_dict['table-result'])
                #print("提取出的sdk_dict_list:")
                #print(sdk_dict_list)
            # sdk_dict_list是所有字典结果
            if sdk_dict_list:
                # if sdk_dict_list == ['使用场景', '使用目的', '获取设备权限', '个人信息类型', '个人信息字段', '去标识化传输', '第三方机构名称', '官方链接地址']:
                #     print("file--", i)
                first_sdk_dict_list = get_first_sdk_dict_list(sdk_dict_list)
                if first_sdk_dict_list and len(first_sdk_dict_list)>1:
                    write_json(first_save_path+"\\"+i,first_sdk_dict_list[:])
                elif len(first_sdk_dict_list)==1:
                    num += 1
                    print("第", num, "个长度为一")
                    print("first_sdk_dict_list,",first_sdk_dict_list)
                    print("file--",i)
                    print("--------------------------------")
                    # print("abcdefg")
        except Exception as e:
            num = num+1
            print('e:',e)
            print("第",num,"个写入失败")
            print(i+"写入失败")
            print("--------------------------------")
    return first_sdk_dict_list
def get_first_sdk_dict_list(sdk_dict_list):
    '''
    :param sdk_dict_list: 初步爬取的sdk_dict
    :return: 返回分类好的，数据，目的，第三方隐私权政策链接
    '''
    purpose_key = '功能'
    data_key = '信息'
    url_key = '链接'
    name_key = ['name','SDK名称','产品','名称','第三方名称','SDK服务','合作方']
    name_ex_key = '公司名称'
    name_value_key = "SDK"
    first_sdk_dict_list = []
    if sdk_dict_list:
        try:
            for i in sdk_dict_list:
                temp_dict = {"name":None,"data":None,"purpose":[],"url":None}
                # 判断每个key是什么  data还是什么

                try:
                    # sdk_name
                    for key, value in i.items():
                        name_flag = False
                        # print("key:",key, "value:",value)
                        if isinstance(value, str) and isinstance(name_value_key, str):
                            if name_value_key.lower() in value.lower():
                                temp_dict["name"] = i[key]
                                break

                        # print("name_key:",name_key)
                        for nk in name_key:
                            # print("关键词: ",nk)
                            if name_ex_key in key:
                                break   # 这个键值对是公司名称，检查下一个键值对

                            if isinstance(nk, str) and isinstance(key, str):
                                # print("检查关键词 key:",key)
                                print("------------------------------------------------")
                                if nk.lower() in key.lower():
                                    temp_dict["name"] = i[key]
                                    name_flag = True
                                    break

                        if name_flag:
                            break

                except Exception as e:
                    # print("sdkname-file:", sdk_dict_list)
                    # print("sdkname:", e)
                    pass

                # name以外的键
                for key in i:   
                    #key = "第三方数据安全能力描述"

                    if data_key in key or "数据" in key:
                        if '权' not in key and '安全' not in key and is_valid_url(i[key]) is False and i[key]:
                            temp_dict["data"] = i[key]
                    if purpose_key in key or '目的' in key or "场景" in key:
                        if i[key]:
                            temp_dict["purpose"].extend(spilt_str(i[key]))
                    try:
                        if temp_dict['url'] == None:
                            if i["url"]:
                                temp_dict["url"] = i["url"][0]
                    except:
                        try:
                            if i["url-list"]:
                                temp_dict["url"] = i["url-list"][0]
                        except:
                            if url_key in key and i[key]:
                                temp_dict["url"] = i[key]
                if temp_dict["data"] and temp_dict["purpose"] and temp_dict["url"]:
                    first_sdk_dict_list.append(dict(temp_dict))
        except Exception as e:
            print(e)
    return first_sdk_dict_list
if __name__ == '__main__':
    run_get_first_sdk_dict_list()
    #temp_dict = {'data': '存储权限', 'purpose': ['用户购买增值服务'], 'url': 'https://render.alipay.com/p/c/k2cx0tg8'}
    #if temp_dict["data"] and temp_dict["purpose"] and temp_dict["url"]:
        #print("rrr")
    #需要把sdk名称，以及权限加进来吗。
