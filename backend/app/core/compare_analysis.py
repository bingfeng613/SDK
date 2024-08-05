import json
from some_function import get_url_name_finall
from some_function import write_json
import re
from prompt import prompt_function
from prompt import prompt_function2
import csv
from prompt import prompt_data3
from prompt import prompt_data30
import os
from llm_jieguoguizehua import extract_substrings
#from third_sdk_handle import sdk_prompt_handle2
from ERNIE3_5_8K_qianfan_ import main_35
#from third_sdk_handle import sdk_prompt_handle3
from ERNIE3_5_8K_qianfan_ import decode_json
sdk_llm_result_path = "llm_result_n_tuple"
cut_save_json_path = "sdk_html_text_cut"
purpose_result_path = "llm_result_purpose_compare"
data_result_path = "llm_result_data_compare"
def read_json(filepath):
    with open(filepath,'r',encoding='utf-8')as f:
        data = json.load(f)
    f.close()
    return data
def spilt_str(result):
    rlist = []
    if result:
        if isinstance(result,str):
            r = re.split(r'[、,，()（）/,.；等\]】]', result)
            for i in r :
                if i and len(i)>1:
                    rlist.append(i)
        if isinstance(result,list):
            for a in result:
                tr = re.split(r'[、,，()（）/,.；等\]]】',a)
                for smtr in tr:
                    if smtr and len(smtr)>1:
                        rlist.append(smtr)
    return rlist
def purpose_handle(sdk_pp_llm_dict_list):
    #第三方隐私政策目的相同的，合并数据项。
    for pp_dict in sdk_pp_llm_dict_list:
        pp_dict['purpose'] = list(set(pp_dict['purpose']))
    return  sdk_pp_llm_dict_list
'''
def same_purpose_track(sdk_dict,sdk_pp_llm_dict_list):
    result_list = []
    #针对每个结果一一比较，这样比较耗费时间
    for i in sdk_pp_llm_dict_list:
        try:
            prompt_temp = prompt_purpose.format(str(i["purpose"]),sdk_dict['purpose'])
            llm_result = run_prompt(prompt_temp)
            if llm_result:
                result_list.append({"data":i["data"],"purpose":i["purpose"],"llm_result":llm_result})
        except Exception as e:
            print(e)
            print("三元组格式错误.")
    return result_list'''
'''
def same_purpose_track2(sdk_dict,sdk_pp_llm_dict_list):
    #将sdk三元组所有目的组合成一个字典，这样一个sdk只需要问一次。下面data_compare也要改
    result_list = []
    purpose_list = []
    temp_same_purpose_list=[]
    for i in sdk_pp_llm_dict_list:
        #######################################记得将目的处理一下，比如、和等。
        if i["purpose"] and i["purpose"] != 'None':
            if isinstance(i["purpose"],str):
                purpose_list.append(i["purpose"])
            if isinstance(i["purpose"],list):
                purpose_list.extend(i["purpose"])
    try:
        if purpose_list:
            prompt_temp = prompt_purpose2.format(str(purpose_list),sdk_dict['purpose'])
            llm_result = run_prompt(prompt_temp)
            if llm_result:
                try:
                    if llm_result["Y/N"] == 'Y':#按原格式写入
                        if isinstance(llm_result["similarStrings"], list):
                            temp_same_purpose_list.extend(llm_result["similarStrings"])
                        if isinstance(llm_result["similarStrings"], str):
                            temp_same_purpose_list.append(llm_result["similarStrings"])
                except Exception as e:
                    print(e)
                    print("目的对齐大模型出错，可能是格式问题，请检查,将直接返回大模型输出结果")
                    return llm_result
        else:
            print("目的合并为列表处理失败，请检查。")
    except Exception as e:
        print(e)
        print("目的对齐模块出问题，请检查。")
    if temp_same_purpose_list:
        for i in sdk_pp_llm_dict_list:
            if i["purpose"]:
                if isinstance(i["purpose"], str) and i["purpose"] in temp_same_purpose_list:
                    result_list.append({"data": i["data"], "purpose": i["purpose"], "llm_result": {"Y/N":'Y',"similarStrings":i["purpose"]}})
                if isinstance(i["purpose"],list):
                    intersection = list(set(i["purpose"]) & set(temp_same_purpose_list))
                    if intersection:
                        result_list.append({"data": i["data"], "purpose": i["purpose"],"llm_result": {"Y/N": 'Y', "similarStrings": i["purpose"]}})
                    else:
                        result_list.append({"data": i["data"], "purpose": i["purpose"],"llm_result": {"Y/N": 'N', "similarStrings": []}})
                else:
                    result_list.append({"data": i["data"], "purpose": i["purpose"],"llm_result": {"Y/N": 'N', "similarStrings": []}})
    return result_list'''
def sdk_n_tuple_extract(sdk_pp_llm_dict_list):
    result = []
    if sdk_pp_llm_dict_list:
        for s_dict in sdk_pp_llm_dict_list:
            if s_dict["result"]:
                for llm_result_dict in s_dict["result"]:
                    if llm_result_dict:
                        if isinstance(llm_result_dict["llm-result"],dict):
                            n_tuple = {"data":llm_result_dict["llm-result"]["data"],"purpose":llm_result_dict["llm-result"]["purpose"],"scene/sdk":llm_result_dict["llm-result"]["scene/sdk"],"permission":llm_result_dict["llm-result"]["permission"]}
                            result.append(dict(n_tuple))
                        elif isinstance(llm_result_dict["llm-result"],str):
                            try:
                                temp_llm_result = extract_substrings(llm_result_dict["llm-result"])
                                llm_result_text_list = temp_llm_result
                                for llm_result_text in llm_result_text_list:
                                    llm_result = decode_json(llm_result_text)
                                    n_tuple = {"data": llm_result["data"],
                                               "purpose": llm_result["purpose"],
                                               "scene/sdk": llm_result["scene/sdk"],
                                               "permission": llm_result["permission"]}
                                    result.append(dict(n_tuple))
                            except:
                                print("注意：出现llm字符串的错误，请检查")
                        else:
                            print("注意：出现llm字符串以外的错误，请检查")
    return result
def same_function_track(sdk_dict,sdk_pp_llm_dict_list):
    result_list = []
    purpose_list = []
    temp_same_function_list = []
    sdk_pp_llm_list = sdk_n_tuple_extract(sdk_pp_llm_dict_list)
    for i in sdk_pp_llm_list:
        #######################################记得将目的处理一下，比如、和等。
        if i["purpose"] and i["purpose"] != 'None':
            if isinstance(i["purpose"], str):
                purpose_list.append(i["purpose"])
            if isinstance(i["purpose"], list):
                purpose_list.extend(i["purpose"])
    if purpose_list:
        purpose_list = list(set(purpose_list))
    try:
        if purpose_list:
            prompt_temp = prompt_function+prompt_function2.format(str(purpose_list), sdk_dict['purpose'])
            ori_llm_result = main_35(prompt_temp)
            try:
                llm_result = decode_json(ori_llm_result)
                if llm_result:
                    try:
                        if llm_result["Y/N"] == 'Y':  # 按原格式写入
                            if isinstance(llm_result["similarStrings"], list):
                                temp_same_function_list.extend(llm_result["similarStrings"])
                            if isinstance(llm_result["similarStrings"], str):
                                temp_same_function_list.append(llm_result["similarStrings"])
                    except Exception as e:
                        print(e)
                        print("目的对齐大模型出错，可能是格式问题，请检查,将直接返回大模型输出结果")
                        return llm_result
            except:
                temp_llm_result = extract_substrings(ori_llm_result)
                llm_result_text = temp_llm_result[0]
                llm_result = decode_json(llm_result_text)
                if llm_result:
                    try:
                        if llm_result["Y/N"] == 'Y':  # 按原格式写入
                            if isinstance(llm_result["similarStrings"], list):
                                temp_same_function_list.extend(llm_result["similarStrings"])
                            if isinstance(llm_result["similarStrings"], str):
                                temp_same_function_list.append(llm_result["similarStrings"])
                    except Exception as e:
                        print(e)
                        print("目的对齐大模型出错，可能是格式问题，请检查,将直接返回大模型输出结果")

        else:
            print("目的合并为列表处理失败，请检查。")
    except Exception as e:
        print(e)
        print("目的对齐模块出问题，请检查。")
    if temp_same_function_list:
        for i in sdk_pp_llm_list:
            if i["purpose"]:
                if isinstance(i["purpose"], str) and i["purpose"] in temp_same_function_list:
                    result_list.append({"data": i["data"], "purpose": i["purpose"],
                                        "llm_result": {"Y/N": 'Y', "similarStrings": i["purpose"]}})
                if isinstance(i["purpose"], list):
                    intersection = list(set(i["purpose"]) & set(temp_same_function_list))
                    if intersection:
                        result_list.append({"data": i["data"], "function": i["purpose"],
                                            "llm_result": {"Y/N": 'Y', "similarStrings":intersection}})
                    else:
                        result_list.append({"data": i["data"], "purpose": i["purpose"],
                                            "llm_result": {"Y/N": 'N', "similarStrings": []}})
                else:
                    result_list.append(
                        {"data": i["data"], "purpose": i["purpose"], "llm_result": {"Y/N": 'N', "similarStrings": []}})
            else:
                result_list.append({"data": i["data"], "function": i["purpose"], "llm_result": {"Y/N": 'N', "similarStrings": []}})
    else:
        result_list.append({"sdk-purpose":str(purpose_list), "app-purpose":sdk_dict['purpose'],"llm-reuslt":ori_llm_result})
    return result_list
def first_data_handle(data):
    first_data_list = spilt_str(data)
    return first_data_list
def direct_data_handle(first_data_list,third_data_list):
    first_data_list = [x.upper() for x in first_data_list]
    third_data_list = [x.upper() for x in third_data_list]
    #使用集合去除相同元素
    set1 = set(first_data_list)
    set2 = set(third_data_list)
    #计算差集
    first_data_list = list(set1-set2)
    third_data_list = list(set2-set1)
    return first_data_list,third_data_list

def data_campare(sdk_dict,purpose_same_result):
    #把目的对齐的第三方数据声明提取出来
    third_data_list = []
    result = []
    first_data_list = first_data_handle(sdk_dict["data"])#第一方数据切割，这里暂时没有做更加细分的操作，因为不确定是否有用。
    third_same_purpose_list = []
    for i in purpose_same_result:
        if "sdk-purpose" in i:
            return []
        try:
            if i["llm_result"]["Y/N"] == 'Y':
                if isinstance(i["data"], list):
                    third_data_list.extend(i["data"])
                if isinstance(i["data"],str):
                    third_data_list.extend(first_data_handle(i["data"]))
                third_same_purpose_list.append(i)
        except Exception as e:
            print(e+"查找目的对齐字典失败，无法进行数据项对比")
    if third_data_list:
        #这里的第三方的data都没有做切割，所以需要切割？
        third_data_list = spilt_str(third_data_list)
        first_data_list,third_data_list = direct_data_handle(first_data_list,third_data_list)
        prompt_temp = prompt_data3+prompt_data30.format(str(first_data_list),str(third_data_list))
        ori_llm_result2 = main_35(prompt_temp)
        try:
            llm_result2 = decode_json(ori_llm_result2)
        except :
            try:
                temp_llm_result = extract_substrings(ori_llm_result2)
                llm_result_text = temp_llm_result[0]
                llm_result2 = decode_json(llm_result_text)
            except Exception as e:
                print(e)
                llm_result2 = ori_llm_result2
                print("数据对比结果有误，请检查")
        if llm_result2:
            result.append({"first-data-list":first_data_list,"third-data-list":third_data_list,'data-llm-result':llm_result2,"third-same-purpose-dict":third_same_purpose_list})
    return result
'''
def run_same_purpose_track():
    first_sdk_dict_list = read_json("first_sdk_dict_list_citic21.json")
    for sdk_dict in first_sdk_dict_list:
        third_name = get_url_name_finall(sdk_dict['url'])
        try:
            sdk_pp_llm_dict_list = read_json("sdk_text_llm_result\\"+third_name+".json")
            if sdk_pp_llm_dict_list:
                #print(third_name+"有"+str(len(sdk_pp_llm_dict_list))+"开始查询llm，目的对齐.")
                #purpose_same_result = same_purpose_track(sdk_dict,sdk_pp_llm_dict_list)
                #if purpose_same_result:
                # write_json("purpose_llm_result\\"+third_name+".json",purpose_same_result)
                try:
                    #third_name = "amap.com.pslbsamapcomhomeprivacy"
                    purpose_same_result = read_json("purpose_llm_result\\"+third_name+".json")
                    if purpose_same_result:
                        print(third_name + "开始数据对比分析")
                        #write_json("purpose_llm_result\\"+third_name+".json",purpose_same_result)
                        data_result = data_campare(sdk_dict,purpose_same_result)
                        write_json("data_llm_result\\"+third_name+".json",data_result)
                except Exception as e:
                    print(e)
                    print("无目的文件"+third_name)
        except Exception as e:
            print(e)
            #print("无"+third_name)'''
def run_single_first(first_sdk_dict_list,first_app):
    #单个跑完全流程,这里需要注意的是输入的第一方字典为处理好的，只有数据项、使用目的、url和url判断结果的。
    '''
    "url": [],
    "ori-url": "https://render.alipay.com/p/c/k2cx0tg8",
    "sdk-url": ["https://render.alipay.com/p/c/k2cx0tg8"],
    "url-judge": "是隐私政策",
    "sdk-url-judge": "是sdk隐私政策"
    '''
    for sdk_dict in first_sdk_dict_list:
        if "sdk-url" in sdk_dict and sdk_dict["sdk-url"]:#只处理判断为sdk链接的
            third_name = get_url_name_finall(sdk_dict['sdk-url'])
            # 这里注意，第三方sdk的结果获得也是处理好的。如果有结果，那就直接拿，没有结果就需要到数据库里拿了。
            try:  # 获取sdk隐私政策的三元组
                sdk_pp_llm_dict_list = read_json(sdk_llm_result_path + "\\" + third_name + ".json")
            except:
                if third_name+".json" in os.listdir("llm_result_simplify"):
                    sdk_dict["sdk-text-judgment"] = "该隐私政策虽然为sdk隐私政策，但无具体有效信息。"
                    continue
                elif third_name+".json" in os.listdir("llm_result_judgment_text"):
                    sdk_dict["sdk-text-judgment"] = "通过更细致的判断，该隐私政策不为sdk隐私政策"
                else:
                    sdk_dict["sdk-text-judgment"] = "待分析的sdk链接"
                sdk_pp_llm_dict_list = []
            if sdk_pp_llm_dict_list:
                print(first_app+"###"+third_name +"---"+sdk_dict["sdk-url"][0]+"---" +"开始查询llm，目的对齐.")
                try:
                    if os.path.exists(purpose_result_path+"\\"+first_app):  # 判断文件夹是否存在
                        single_purpose_llm_save_path = purpose_result_path+"\\"+first_app+"\\"+ third_name + ".json"
                    else:
                        os.makedirs(purpose_result_path+"\\"+first_app)  # 如果不存在，则创建该文件夹
                        single_purpose_llm_save_path = purpose_result_path + "\\" + first_app + "\\" + third_name + ".json"
                except Exception as e:
                    print(e)
                    print("大模型目的对齐结果保存存在问题")
                    continue
                try:
                    purpose_same_result = read_json(single_purpose_llm_save_path)
                except:
                    # purpose_same_result = same_purpose_track(sdk_dict, sdk_pp_llm_dict_list)
                    purpose_same_result = same_function_track(sdk_dict, sdk_pp_llm_dict_list)
                    if purpose_same_result:
                        write_json(single_purpose_llm_save_path, purpose_same_result)
                if purpose_same_result:
                    print(third_name + "开始数据对比分析")
                    # single_data_llm_save_path = data_result_path+"\\"+first_app+"_"+ third_name + ".json"

                    current_path = os.path.dirname(os.path.abspath(__file__))
                    single_data_llm_save_path = os.path.join(current_path, "数据对比结果.json")

                    if os.path.exists(single_data_llm_save_path):
                        continue
                    else:
                        data_result = data_campare(sdk_dict, purpose_same_result)
                        write_json(single_data_llm_save_path, data_result)
                        print("成功写入文件："+single_data_llm_save_path)
                else:
                    print("获取sdk三元组失败."+third_name)

def data_contract(first_data_list,third_data_list,data_llm_result):
    #mohu_data = []
    duoshuo_data = None
    tobe_data = None
    '''
    try:
        if data_llm_result["similarData2"]:
            mohu_data.append(data_llm_result["data1"])
    except Exception as e:
        print(e)
        mohu_data.append("llm返回结果格式错误。")
    '''
    try:
        if isinstance(data_llm_result["data1"],str):
            duoshuo_data = [x for x in first_data_list if x !=data_llm_result["data1"]]
        if isinstance(data_llm_result["data1"],list):
            duoshuo_data =list(set(first_data_list)-set(data_llm_result["data1"]))
        else:
            duoshuo_data = []
    except Exception as e:
        print(e)
        duoshuo_data=["llm返回结果格式错误。"]
    try:
        if data_llm_result["similarData2"]:
            if isinstance(data_llm_result["similarData2"],str):
                tobe_data = [x for x in third_data_list if x !=data_llm_result["similarData2"]]
            if isinstance(data_llm_result["similarData2"],list):
                tobe_data =list(set(third_data_list)-set(data_llm_result["similarData2"]))
            else:
                tobe_data = []
    except Exception as e:
        print(e)
        tobe_data=["llm返回结果格式错误。"]
    return duoshuo_data,tobe_data
def purpose_count(third_dict_list):
    purpose_list = []
    for i in third_dict_list:
        purpose_list.extend(i["llm_result"]["similarStrings"])
    return list(set(purpose_list))
def temp_line_buquan(temp_line):
    if len(temp_line) == 3:
        temp_line.extend(['', '', '', '', '', ''])
    if len(temp_line) == 4:
        temp_line.extend(['', '', '', '', ''])
    if len(temp_line) == 5:
        temp_line.extend(['', '', '', ''])
    if len(temp_line) == 6:
        temp_line.extend(['', '', ''])
    if len(temp_line) == 7:
        temp_line.extend(['', ''])
    if len(temp_line) == 8:
        temp_line.extend([''])
    return temp_line
def write_csv(first_sdk_list,first_app):
    data = []
    #title = ["第三方名称","第三方隐私政策链接","第一方数据项","第一方目的","第三方对齐目的","第三方对齐后数据项","第一方模糊数据项","第一方多说数据项","第一方该说未说数据项"]
    #data.append(title)
    false_data = []
    url_data = []
    no_purpose_data = []
    zhengque_data = []
    #false_data.append(title)
    #citic21 = read_json("first_sdk_dict_list_citic21.json")
    #for sdk_dict in citic21:
    count = 0
    count1 = 0
    duoshuo_data_count = 0
    tobe_data_count = 0
    for sdk_dict in first_sdk_list:
        if "sdk-url" in sdk_dict and sdk_dict["sdk-url"]:#只处理判断为sdk链接的
            count +=1
            third_name = get_url_name_finall(sdk_dict['sdk-url'])
            temp_line = [first_app, third_name, sdk_dict['sdk-url']]
            try:  # 获取sdk隐私政策的三元组
                #sdk_pp_llm_dict_list = read_json(sdk_llm_result_path + "\\" + third_name + ".json")
                single_data_llm_save_path = data_result_path + "\\" + first_app + "_" + third_name + ".json"
                data_llm_result = read_json(single_data_llm_save_path)
                if data_llm_result:
                    temp_line.append(str(data_llm_result[0]["first-data-list"]))
                    temp_line.append(str(sdk_dict["purpose"]))
                    temp_line.append(str(purpose_count(data_llm_result[0]["third-same-purpose-dict"])))
                    temp_line.append(str(data_llm_result[0]["third-data-list"]))
                    duoshuo_data, tobe_data = data_contract(data_llm_result[0]["first-data-list"],
                                                                       data_llm_result[0]["third-data-list"],
                                                                       data_llm_result[0]["data-llm-result"])
                    temp_line.append(str(duoshuo_data))
                    duoshuo_data_count +=len(duoshuo_data)
                    #temp_line.append(str(tobe_data))
                    temp_line.append(tobe_data)
                    tobe_data_count +=len(tobe_data)
                    if len(duoshuo_data) ==0 and len(tobe_data) == 0:
                        zhengque_data.append(temp_line[:])
                        continue
                    if len(duoshuo_data) ==0 and isinstance(tobe_data,str) and tobe_data == 'None':
                        zhengque_data.append(temp_line[:])
                        continue
                    data.append(temp_line[:])
                else:
                    temp_line.append(str(sdk_dict["data"]))
                    temp_line.append(str(sdk_dict["purpose"]))
                    if third_name+".json" in os.listdir("llm_result_purpose_compare\\"+first_app):
                        temp_data = read_json("llm_result_purpose_compare\\"+first_app+"\\"+third_name+".json")
                        if temp_data:
                            if "sdk-purpose" in temp_data[0]:
                                temp_line.append("无相同目的")
                            else:
                                temp_line.append("数据对比分析出错，请检查")
                        else:
                            temp_line.append("使用目的对比分析出错，请检查")
                        no_purpose_data.append(temp_line_buquan(temp_line[:])[:])
                        continue
                    elif third_name + ".json" in os.listdir("llm_result_simplify"):
                        temp_line.append("该隐私政策虽然为sdk隐私政策，但无具体有效信息。")
                    elif third_name + ".json" in os.listdir("llm_result_judgment_text"):
                        temp_line.append("通过更细致的判断，该隐私政策不为sdk隐私政策")
                    else:
                        temp_line.append("待分析的sdk链接")
                        #false_data.append(temp_line_buquan(temp_line[:]))
                        #continue
                    url_data.append(temp_line_buquan(temp_line[:])[:])
            except:
                if third_name+".json" in os.listdir("llm_result_simplify"):
                    temp_line.append("该隐私政策虽然为sdk隐私政策，但无具体有效信息。")
                elif third_name+".json" in os.listdir("llm_result_judgment_text"):
                    temp_line.append("通过更细致的判断，该隐私政策不为sdk隐私政策")
                else:
                    temp_line.append("链接不为隐私政策链接")
                    #false_data.append(temp_line_buquan(temp_line[:]))
                    #continue
                url_data.append(temp_line_buquan(temp_line[:]))
        else:
            third_name = get_url_name_finall(sdk_dict['url'])
            temp_line = [first_app, third_name, sdk_dict['url']]
            if "url-judge" in sdk_dict:
                temp_line.append(sdk_dict["url-judge"])
            if "sdk-url-judge" in sdk_dict:
                temp_line.append(sdk_dict["sdk-url-judge"])
            if len(temp_line) == 3:
                temp_line.extend(['链接不为隐私政策链接', '', '', '', '', ''])
                #false_data.append(temp_line[:])
                count1 +=1
                url_data.append(temp_line[:])
            else:
                url_data.append(temp_line_buquan(temp_line[:]))
    return data,false_data,url_data,no_purpose_data,zhengque_data,count,count1,duoshuo_data_count,tobe_data_count
def csv_data_pinggu(lists):
    #more_data = []#过度声明
    less_data = []#缺失声明
    i=0
    for row in lists:
        if i ==0:
        # 在这里处理每一行，例如打印出来
            less_data_0 = row[:7]
            less_data_0.append("缺失声明数据项")
            less_data.append(less_data_0)
        else:
            result_lists = []
            less_data_0 = row[:7]
            numbers_to_add = row[8]
            if numbers_to_add:
                result_lists = [[*less_data_0, number] for number in numbers_to_add]
            if result_lists:
                less_data.extend(result_lists)
        i +=1
    with open('csv/data_2024.6.1_less_data_eval.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(less_data)
    file.close()
def run_write_csv():
    #first_sdk_dict_path = "D:\\中山\\隐私合规\\sdk_analysislh_11.15_handle"
    first_sdk_dict_path = "D:\\中山\\隐私合规\\sdk_analysislh_3.11_handle"
    filename_list = os.listdir(first_sdk_dict_path)
    data = []
    title = ["第一方名称","第三方名称","第三方隐私政策链接","第一方数据项","第一方目的","第三方对齐目的","第三方对齐后数据项","第一方多说数据项","第一方该说未说数据项"]
    data.append(title)
    false_data = []
    url_data=[]
    no_purpose_data= []
    false_data.append(title)
    first_data_name = []
    zhengque_data = []
    count = 0
    count1 =0
    first_sdk_count,duoshuo_data_count,tobe_data_count = 0,0,0
    for i in filename_list:
        first_sdk_dict_list = read_json(first_sdk_dict_path + "\\" + i)
        first_sdk_count +=len(first_sdk_dict_list)
        try:
            temp_data,temp_false_data,temp_url_data,temp_no_purpose_data,temp_zhengque_data,temp_count,temp_count1,temp_duoshuo_data_count,temp_tobe_data_count =write_csv(first_sdk_dict_list, i[:-5])
            if temp_data:
                data.extend(temp_data[:])
            if temp_false_data:
                false_data.extend(temp_false_data[:])
            if temp_url_data:
                url_data.extend(temp_url_data)
            if temp_no_purpose_data:
                no_purpose_data.extend(temp_no_purpose_data)
            if temp_zhengque_data:
                zhengque_data.extend(temp_zhengque_data)
            count +=temp_count
            count1 += temp_count1
            duoshuo_data_count +=temp_duoshuo_data_count
            tobe_data_count +=temp_tobe_data_count
        except Exception as e:
            print(e)
    for i in range(1,len(data)):
        first_data_name.append(data[i][0])
    first_data_name = list(set(first_data_name))
    print("是sdk链接的109个的字典有"+str(count))
    print("count1:"+str(count1))
    print("109个app总共有sdk字典："+str(first_sdk_count))
    print("确定有数据项问题的first-data-count:"+str(len(first_data_name)))
    print("多说数据项："+str(duoshuo_data_count))
    print("忽略说数据项:"+str(tobe_data_count))
    #print("完全合规项："+str(len(zhengque_data)))
    with open('csv/data_2024.6.1-data.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    file.close()
    csv_data_pinggu(data)
    print("data:"+str(len(data)))
    with open('csv/data_2024.4.29-url_data.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(url_data)
    file.close()
    print("url-data:" + str(len(url_data)))

    with open('csv/data_2024.4.29-zhengque_data.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(zhengque_data)
    file.close()
    print("zhengque-data:"+str(len(zhengque_data)))
    '''
    print("false-data:" + str(len(false_data)))
    with open('csv/data_2024.4.29-url_data.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(url_data)
    file.close()'''

    with open('csv/data_2024.4.29-no_purpose_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(url_data)
    file.close()
    print("no_purpose-data:" + str(len(no_purpose_data)))

    csv_path = 'csv/data_2024.4.29-no_purpose_data.csv'

    path = csv_to_json(csv_path)

    return path


def csv_to_json(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)

    json_data = json.dumps(rows, indent=4, ensure_ascii=False)

    result_json_dir = os.path.join(os.path.dirname(csv_file_path), 'result_json')
    os.makedirs(result_json_dir, exist_ok=True)
    json_filename = os.path.splitext(os.path.basename(csv_file_path))[0] + '.json'
    json_file_path = os.path.join(result_json_dir, json_filename)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    return json_file_path

def run_all(first_sdk_dict_path):
    first_sdk_dict_path_list = []
    # first_sdk_dict_path_list.append(first_sdk_dict_path)
    #first_sdk_dict_path = "D:\\中山\\隐私合规\\sdk_analysislh_11.15_handle"
    # first_sdk_dict_path = "D:\\中山\\隐私合规\\sdk_analysislh_3.11_handle"
    # filename_list = os.listdir(first_sdk_dict_path)
    # for i in filename_list:
    #     first_sdk_dict_list = read_json(first_sdk_dict_path+"\\"+i)
    #     run_single_first(first_sdk_dict_list,i[:-5])
    filename = os.path.basename(first_sdk_dict_path)   #提取JSON文件名
    print("JSON文件名是：", filename)
    run_single_first(first_sdk_dict_path, filename[:-5])

def run_compare(first_sdk_dict_path):
    #data = read_json("sdk_text_llm_result\\alicdn.com.onsuit_bu1_unification202005141916_91107.json")
   # run_same_purpose_track()
    '''
    最后给出的表格的表头为：第一方三元组，第三方隐私政策二元组，第三方目的一致二元组，第一方模糊数据项，第一方多说数据项，第一方该说未说数据项
    '''
    #print(spilt_str("设备标识符（IMEI、MAC、BSSID、SSID、AndroidID）、运营商信息"))
    run_all(first_sdk_dict_path)
    #spilt_str("版本号[仅ANDROID] 宿主应用的进程名称")
    run_write_csv()
    '''
    列表1：第一方数据
    列表2：第三方数据
    要找的是，第一方多说的，和第一方模糊的
    我需要llm找列表2中和列表1意义相似的数据项，返回意义相似的第一方数据和对应的第三方数据项。
    1.排除掉直接匹配
    2.找到了意义相似的数据，那么暂且把这个第一方数据项划为模糊数据项。
    3.除此之外的第一方数据项都是多说的。
    4.减掉2中第三方数据项，剩余的都是该说的没说。'''
