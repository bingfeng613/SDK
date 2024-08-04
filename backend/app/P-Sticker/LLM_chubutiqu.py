# 大模型_初步提取

import os
from some_function import read_json
from ERNIE3_5_8K_qianfan_ import main_35
from some_function import text_replace
from prompt import prompt_5
from prompt import prompt_0
from ERNIE3_5_8K_qianfan_ import decode_json
from some_function import write_json
path = "Third_Party_Text"
result_path = "llm_result_judgment_text"
def single_qianfan(pp_text):
    prompt = prompt_5 + prompt_0.format(pp=pp_text)
    ori_llm_result = main_35(prompt)
    result_dict = {"text":pp_text,"llm-result":None}
    result_dict["llm-result"] = ori_llm_result
    '''
    try:
        llm_result = decode_json(ori_llm_result)
        result_dict["llm-result"] = llm_result
    except Exception as e:
        print(e)
        result_dict["llm-result"]=ori_llm_result
        '''
    return dict(result_dict)

def run_qianfan():
    filename_list = os.listdir(path)
    for i in filename_list:
        result_list = os.listdir(result_path)
        if i.endswith(".json") and i not in result_list:
            data = read_json(path +"\\"+ i)
            result_list = []
            pp_text_list = data["result-list"][:]
            if pp_text_list:
                print(i+"开始处理")
                for text in pp_text_list:
                    if text:
                        try:
                            result = single_qianfan(text)
                            result_list.append(dict(result))
                        except Exception as e:
                            print(e)
            if result_list:
                write_json(result_path+"\\"+i,result_list)
                print(i+"处理成功，结果已保存")
            else:
                print(i+"处理失败，无结果")
if __name__ == '__main__':
    run_qianfan()
