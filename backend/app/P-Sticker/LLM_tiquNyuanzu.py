# 大模型提取n元组

from prompt import prompt_7
from prompt import prompt_0
from prompt import prompt_8
from prompt import prompt_80
from ERNIE3_5_8K_qianfan_ import main_35
from ERNIE3_5_8K_qianfan_ import decode_json
from some_function import write_json
from some_function import read_json
import os
simplify_sentence_path = "llm_result_simplify"
llm_result_tuple_path = "llm_result_n_tuple"
def single_extract(simplify_list):
    result_list = []
    if simplify_list:
        for simplify_dict in simplify_list:
            if simplify_dict["llm-result"]:
                #由观察得到，当llm的结果无法解析为json时，这个句子往往存在一些问题，导致大模型会返回json结果之外的解释，导致格式错误解析失败，因此暂时不处理这一部分。这一部分绝大部分不对结果造成绝对性影响。
                if isinstance(simplify_dict["llm-result"],dict):
                    if simplify_dict["llm-result"]["judgement"] == "true":
                        result = {"text":simplify_dict["text"],"result":[]}
                        if simplify_dict["llm-result"]["data-practice"]:
                            for sentence in simplify_dict["llm-result"]["data-practice"]:
                                t_reuslt = {"data-practice":sentence, "llm-result":None}
                                #prompt = prompt_7 + prompt_0.format(pp=sentence)
                                prompt = prompt_8+prompt_80.format(data_practice=sentence,pp_text=simplify_dict["text"])
                                ori_llm_result = main_35(prompt)
                                try:
                                    llm_result = decode_json(ori_llm_result)
                                    t_reuslt["llm-result"] = llm_result
                                except:
                                    t_reuslt["llm-result"] = ori_llm_result
                                result["result"].append(dict(t_reuslt))
                        result_list.append(dict(result))
    return result_list

def run_extract():
    filename_list = os.listdir(simplify_sentence_path)
    false_sdk_pp_name_list = []
    for i in filename_list:
        result_path_list = os.listdir(llm_result_tuple_path)
        if i.endswith(".json") and i not in result_path_list:
            data = read_json(simplify_sentence_path + "\\" + i)
            if data:
                print(i + "开始处理")
                result_list = single_extract(data)
                if result_list:
                    write_json(llm_result_tuple_path + "\\" + i, result_list)
                    print(i + "处理成功，结果已保存")
                else:
                    false_sdk_pp_name_list.append(i)
                    print(i + "处理失败，无结果")
    write_json("无数据声明的隐私政策目录.json", false_sdk_pp_name_list)
if __name__ == '__main__':
    run_extract()