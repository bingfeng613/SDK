#该代码用于将llm的结果规则化。
import os
from some_function import write_json
from some_function import read_json
import re
from prompt import prompt_8
from prompt import prompt_80
from ERNIE3_5_8K_qianfan_ import main_35
from ERNIE3_5_8K_qianfan_ import decode_json
def extract_substrings(string):
    pattern = r"\{[^{}]+\}"
    substrings = re.findall(pattern, string)
    return substrings
def run_simplify(path):
    filename_list = os.listdir(path)
    str_list_true = []
    str_list_false = []
    name_list = []
    result2_list = []
    for i in filename_list:
        flag = 1
        if i.endswith(".json"):
            data = read_json(path + "\\" + i)
            try:
                llm_data = read_json("llm_result_n_tuple"+"\\"+i)
            except:
                llm_data = []
            for simplify_dict in data:
                if isinstance(simplify_dict["llm-result"], str):
                    if "true" in simplify_dict["llm-result"]:
                        str_list_true.append(simplify_dict["llm-result"])
                        temp_result = extract_substrings(simplify_dict["llm-result"])
                        result2 = []
                        try:
                            for ine in temp_result:
                                result2.append(decode_json(ine))
                        except:
                            result2.append("wrong!")
                            print(i)
                        if len(result2)>1:
                            print(len(result2))
                        result2_list.append({"text":simplify_dict["text"],"ori": i})
                        simplify_dict["llm-result"] = result2
                        '''
                        if simplify_dict["llm-result"]["judgement"] == "true":
                            result = {"text": simplify_dict["text"], "result": []}
                            if simplify_dict["llm-result"]["data-practice"]:
                                for sentence in simplify_dict["llm-result"]["data-practice"]:
                                    t_reuslt = {"data-practice": sentence, "llm-result": None}
                                    # prompt = prompt_7 + prompt_0.format(pp=sentence)
                                    prompt = prompt_8 + prompt_80.format(data_practice=sentence,
                                                                         pp_text=simplify_dict["text"])
                                    ori_llm_result = main_35(prompt)
                                    try:
                                        llm_result = decode_json(ori_llm_result)
                                        t_reuslt["llm-result"] = llm_result
                                    except:
                                        t_reuslt["llm-result"] = ori_llm_result
                                    result["result"].append(dict(t_reuslt))
                            llm_data.append(dict(result))
                        
                        flag = 0
                    else:
                        str_list_false.append(simplify_dict["llm-result"])
            write_json("llm_result_n_tuple"+"\\"+i,llm_data)
            '''
        if flag == 0:
            #write_json(path + "\\" + i,data)
            name_list.append(i)
    write_json("json\\待规则化字符串.json",result2_list)
    write_json("json\\待重跑文件名单.json",name_list)
    print(len(name_list))
if __name__ == '__main__':
    path = "llm_result_simplify_old"
    run_simplify(path)