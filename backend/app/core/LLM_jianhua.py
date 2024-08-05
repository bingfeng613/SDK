# 大模型-简化

import os
from some_function import read_json
# from ERNIE_3_5_8K_qianfan import main
from some_function import text_replace
from ERNIE3_5_8K_qianfan_ import main_35
from prompt import prompt_4
from prompt import prompt_0
from ERNIE3_5_8K_qianfan_ import decode_json
from ERNIE3_5_8K_qianfan_ import main_35
from some_function import write_json
path = "llm_result_judgment_text"
result_path = "llm_result_simplify"
def single_qianfan(pp_text):
    prompt = prompt_4 + prompt_0.format(pp=pp_text)
    ori_llm_result = main_35(prompt)
    result_dict = {"text":pp_text,"llm-result":None}
    #result_dict["llm-result"] = ori_llm_result
    try:
        llm_result = decode_json(ori_llm_result)
        result_dict["llm-result"] = llm_result
    except:
        result_dict["llm-result"]=ori_llm_result
    return dict(result_dict)
def judgment_track(result_dict):
    if result_dict["llm-result"]:
        if isinstance(result_dict["llm-result"],str):
            if 'yes'in result_dict["llm-result"]:
                return True
        if isinstance(result_dict["llm-result"],dict):
            if 'yes' in result_dict["llm-result"]["judgment"]:
                return True
    return False
def run_qianfan():
    filename_list = os.listdir(path)
    false_sdk_pp_name_list = []
    for i in filename_list:
        result_list = os.listdir(result_path)
        if i.endswith(".json") and i not in result_list:
            data = read_json(path +"\\"+ i)
            result_list = []
            if data:
                print(i+"开始处理")
                for llm_result_dict in data:
                    if judgment_track(llm_result_dict):
                        text = llm_result_dict["text"]
                        try:
                            result = single_qianfan(text)
                            result_list.append(dict(result))
                        except Exception as e:
                            print(e)
                            print("i"+"大模型处理有问题，请重新处理")
            if result_list:
                write_json(result_path+"\\"+i,result_list)
                print(i+"处理成功，结果已保存")
            else:
                false_sdk_pp_name_list.append(i)
                print(i+"处理失败，无结果")
    write_json("无数据声明的隐私政策目录.json",false_sdk_pp_name_list)
if __name__ == '__main__':
    run_qianfan()
