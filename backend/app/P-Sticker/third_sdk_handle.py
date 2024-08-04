#获取第三方sdk三元组
from some_function import write_json
from some_function import read_json
from some_function import run_subsection
from some_function import get_domain_name
from some_function import get_urlname
from some_function import get_url_name_finall
import os
import re
from some_function import read_txt_str
sdk_url_list = read_json("sdk_url_list.json")
json_path = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_html_text"
LLM_save_path = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result"

cut_save_json_path = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_html_text_cut"
LLM_save_path2 = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result_确定为sdk隐私政策的文本_llm提取n元组结果"
def temp_sdk_text_list_get(sdk_url_name2):
    sdk_text_list = read_json(cut_save_json_path+"\\" + sdk_url_name2 + ".json")
    return sdk_text_list
def sdk_text_cut(sdk_text):
    return run_subsection(sdk_text)
def sdk_sentence_cut(sdk_text):
    '''
    将文本以句为单位切割，以便llm结果更精确
    :return: 返回句子列表
    '''
    sdk_text_list = []
    #先段落切割后，然后将段落再按照句子切割。
    subsection_list = sdk_text_cut(sdk_text)
    result = []
    if subsection_list:
        for i in subsection_list:
            if i and len(i)>35:
                temp_result = i.split(".")
                temp_result_dot = [s + "." for s in temp_result if s and len(s)>2]
                sdk_text_list.extend(temp_result_dot[:])
    for i in sdk_text_list:
        if biaotou_delete(i):
            result.append(i)
    return result
def third_url_handle(sdk_url):
    url_judge = False
    pp_judge = False
    sdk_text = None
    def sdk_text_handle(sdk_text):
        if sdk_text:
            sdk_text = sdk_text.replace("\n\n", "")
            sdk_text = sdk_text.replace(" ", " ")
            sdk_text = sdk_text.replace("  ", "")
            sdk_text = sdk_text.replace("\t\t\t", "")
        return sdk_text
    def get_third_sdk_text(sdk_url):
        #先查找这个链接是否在库里
        sdk_text =None
        sdk_url_name = get_domain_name(sdk_url) + "." + get_urlname(sdk_url)
        if sdk_url in sdk_url_list:
            try:
                sdk_text = read_json(json_path+"\\"+sdk_url_name+".json")
                print(sdk_url+"在库里")
            except:
                print(sdk_url+"不在库里或是不为隐私政策链接。")
        else:
            '''
            soup = url_analysis3_html(sdk_url,sdk_url_name,soup_or=True)
            if soup:
                sdk_text =soup.get_text()
                sdk_url_list.append(sdk_url)
                print("爬取了新的隐私政策："+sdk_url+"并存入库中.")
            else:
                false_url_list.append(sdk_url)
                print("爬取新隐私政策："+sdk_url+"失败，false_url_list增加一条记录")'''
            print("待爬取第三方隐私政策:"+sdk_url)
        return sdk_text_handle(sdk_text)
    return get_third_sdk_text(sdk_url)
def sdk_prompt_handle(sdk_text,sdk_url):
    #得到LLM第三方返回结果，处理
    LLM_result = None
    #如果字数超过，则将sdk_text切断。
    sdk_url_name = get_domain_name(sdk_url) + "." + get_urlname(sdk_url)
    if sdk_text and len(sdk_text)<1400:
        #LLM_result = run_prompt(prompt_sdk.format(sdk_text))
        print("成功保存结果："+sdk_url_name)
        #write_json(cut_save_json_path + "\\" + sdk_url_name + ".json", [sdk_text])
        if LLM_result:
            write_json(LLM_result+sdk_url_name+".json",LLM_result)
    elif sdk_text:
        print(sdk_url)
        sdk_text_list = sdk_text_cut(sdk_text)
        print(sdk_url_name)
        #write_json(cut_save_json_path+"\\"+sdk_url_name+".json",sdk_text_list)
        try:
            max = -1
            temp_sdk_text_list = temp_sdk_text_list_get(sdk_url_name)
            for i in temp_sdk_text_list:
                if len(i)>max:
                    #LLM_result = run_prompt(prompt_sdk.format(sdk_text))
                    #print(len(i))
                    max = len(i)
            print(max)
        except Exception as e:
            print(e)
            print("跳过"+sdk_url_name)
    return LLM_result
'''
def sdk_prompt_handle2(sdk_url_name = None,sdk_url = None):
    #得到LLM第三方返回结果，处理
    LLM_result_list = []
    #如果字数超过，则将sdk_text切断。
    if sdk_url_name == None:
        sdk_url_name = get_domain_name(sdk_url) + "." + get_urlname(sdk_url)
    if sdk_url_name:
        try:
            sdk_text_list = read_json(cut_save_json_path+"\\"+sdk_url_name+".json")
            for sdk_text in sdk_text_list:
                if sdk_text and len(sdk_text)>35:
                    try:
                        #print(prompt_sdk.format(sdk_text))
                        #LLM_result = None
                        LLM_result = run_prompt(prompt_sdk.format(sdk_text))
                        #print("成功保存结果：" + sdk_url_name)
                    #write_json(cut_save_json_path + "\\" + sdk_url_name + ".json", [sdk_text])
                        if isinstance(LLM_result,dict):
                            LLM_result_list.append(LLM_result)
                        if isinstance(LLM_result,list):
                            LLM_result_list.extend(LLM_result)
                    except Exception as e:
                        print(e)
                        print("大模型处理失败")
            write_json(LLM_save_path+"\\" + sdk_url_name + ".json", LLM_result_list)
            print('得到LLM结果'+sdk_url_name)
        except:
            print("无剪切结果")
    return LLM_result_list'''
def biaotou_delete(sdk_text):
    #删除掉爬取的表头
    if sdk_text.count("文档中心")>2:
        return False
    if sdk_text.count("常见问题")>2:
        return False
    if "我的消息" in sdk_text and "个人中心" in sdk_text:
        return False
    if sdk_text.count("桌面")>2:
        return False
    if sdk_text.count("目录")>2:
        return False
    if sdk_text.count("指南")>4:
        return False
    if sdk_text.count("人工客服")>1:
        return False
    return True
def keep_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    result = re.findall(pattern, text)
    return ''.join(result)
def sdk_cut(sdk_url_name = None,sdk_url = None):
    #将隐私政策文本按句切开并保存
    if sdk_url_name == None:
        sdk_url_name = get_domain_name(sdk_url) + "." + get_urlname(sdk_url)
    if sdk_url_name:
        try:
            #sdk_text_list = read_json(cut_save_json_path+"\\"+sdk_url_name+".json")
            #sdk_text_str = third_url_handle(sdk_url)
            if os.path.exists(cut_save_json_path+"\\"+sdk_url_name+".json"):
                sdk_text_list = read_json(cut_save_json_path + "\\" + sdk_url_name + ".json")
            else:
                sdk_text_str = read_json("D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result_确定为sdk隐私政策的文本"+"\\"+sdk_url_name+".json")[0]
                sdk_text_list = sdk_sentence_cut(sdk_text_str)
            path = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_html_cut_确定为sdk隐私政策的文本"
            write_json(path+"\\"+sdk_url_name + ".json",sdk_text_list)
        except Exception as e:
            print(e)

'''def sdk_prompt_handle3(sdk_url_name = None,sdk_url = None):

    #得到LLM第三方返回结果，处理
    LLM_result_list = []
    LLM_result_list_sentence = []#便于调试，可以看到对应句子。
    #如果字数超过，则将sdk_text切断。
    if sdk_url_name == None:
        sdk_url_name = get_domain_name(sdk_url) + "." + get_urlname(sdk_url)
    if sdk_url_name:
        try:
            #sdk_text_list = read_json(cut_save_json_path+"\\"+sdk_url_name+".json")
            #sdk_text_str = third_url_handle(sdk_url)
            if os.path.exists(cut_save_json_path+"\\"+sdk_url_name+".json"):
                sdk_text_list = read_json(cut_save_json_path + "\\" + sdk_url_name + ".json")
            else:
                print("暂未处理"+sdk_url_name)
                return False
                #sdk_text_str = read_json("D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result_确定为sdk隐私政策的文本"+"\\"+sdk_url_name+".json")[0]
                #sdk_text_list = sdk_sentence_cut(sdk_text_str)
            #print(len(sdk_text_list))
            #for i in sdk_text_list:
             #   print(str(len(i))+":   "+i)
            a=0
            for sdk_text in sdk_text_list:
                if sdk_text and len(keep_chinese(sdk_text))>20 and biaotou_delete(sdk_text):#根据观察，20个字的句子不会包含有用信息。
                    #print(str(a)+sdk_text)
                    a=a+1
                    try:
                        #print(prompt_sdk.format(sdk_text))
                        #LLM_result = None
                        LLM_result = run_prompt(prompt_sdk3.format(sdk_text))
                        #print("成功保存结果：" + sdk_url_name)
                    #write_json(cut_save_json_path + "\\" + sdk_url_name + ".json", [sdk_text])
                        if isinstance(LLM_result,dict):
                            LLM_result_list.append(LLM_result)
                        if isinstance(LLM_result,list):
                            LLM_result_list.extend(LLM_result)
                        LLM_result_list_sentence.append({"sentence":sdk_text,"llm-result":LLM_result})
                    except Exception as e:
                        print(e)
                        print("大模型处理失败")
            write_json(LLM_save_path2+"\\" + sdk_url_name + ".json", LLM_result_list)
            write_json(LLM_save_path2+"_加上句子版""\\" + sdk_url_name + ".json", LLM_result_list_sentence)
            print('得到LLM结果'+sdk_url_name)
        except Exception as e:
            print("无剪切结果")
            print(e)
    return LLM_result_list'''
def sdk_sentence_cut_get_json(sdk_url):
    sdk_text_str = third_url_handle(sdk_url)
    sdk_url_name = get_domain_name(sdk_url) + "." + get_urlname(sdk_url)
    if sdk_text_str:
        sdk_text_list = sdk_sentence_cut(sdk_text_str)
        #cut_save_json_path2 = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_html_text_cut待处理"
        path = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_html_cut_确定为sdk隐私政策的文本"
        write_json(path+"\\"+sdk_url_name+".json",sdk_text_list)
        print(sdk_url_name+"已完成")
        return None
    else:
        print(sdk_url+":处理失败")
        return sdk_url
if __name__ == '__main__':
    #sdk_prompt_handle3(sdk_url="https://terms.alicdn.com/legal-agreement/terms/suit_bu1_unification/suit_bu1_unification202005141916_91107.html")
    filepath = "D:\\中山\\隐私合规\\sdk_html处理\\sdk_LLM_result_确定为sdk隐私政策的文本"
    filename_list = os.listdir(filepath)
    for filename in filename_list:
        if filename.endswith(".json"):
            sdk_path = LLM_save_path2 + "\\" + filename
            if os.path.exists(sdk_path):
                continue
            else:
                print(filename)
                #sdk_prompt_handle3(sdk_url_name=filename[:-5])