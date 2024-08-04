'''
    陈列文本的切割
    切割后的文本接入llm
'''

#临时文件，用于分块之后分析隐私政策中sdk称述
import base64
import json
import re
import os
import time

import requests
from bs4 import BeautifulSoup, NavigableString

from First_Party.llm_api.extract_llm_api_tongyiqianwen import call_with_prompt_tongyi
from First_Party.llm_api.extract_llm_api_gpt import call_with_prompt_gpt
from Utils.LLMmessage_to_jsonlist import LLMmessage_to_jsonlist
from Utils.token_incise import token_incise

from Utils.language_format import punctuation_C2E

txt_file = ''

def subsection(text):
    #使用正则表达式匹配文本中的分段符号:一、
    pattern = r'[一二三四五六七八九十]+、|附录'
    #segments = re.split(pattern, text)[1:]
    segments = re.split(pattern,text)   # 本来去掉了第一个


    # if len(segments) == 0:
    #     pattern = r'[1234567890]+. |附录'
    #     segments = re.split(pattern, text)    # 匹配没有用大写数字来分段的政策，比如国金证券
    #
    # if len(segments) != 1:
    #     # 将分段符号添加到每个段落的开头
    #     segments = [re.findall(pattern, text)[i] + segment for i, segment in enumerate(segments)]



    #segments = [segment.replace(" ","") for segment in segments]

    # print("segments = " + str(segments))
    return segments
def subsection_2(text):
    #使用正则表达式匹配文本中的分段符号：（一）
    #pattern = r'（[一二三四五六七八九十]+）|第三方SDK.*?(?:[：:]|$)'    # 这个冒号可能需要改
    pattern = r'（[一二三四五六七八九十]+）|第三方SDK.*?说明'
    segments = re.split(pattern,text)[1:]
    # 将分段符号添加到每个段落的开头
    # segments = [re.findall(pattern, text)[i] + segment for i, segment in enumerate(segments)]
    #segments = [segment.replace(" ","") for segment in segments]
    return segments
def run_subsection(text):
    #分块运行函数
    seg_1 = subsection(text)
    segments = []
    for index, i in enumerate(seg_1):
        # print("str(len(" + str(index) + "))=" + str(len(i)) + ":")
        # print(i)
        temp = subsection_2(i)
        if temp:
            segments.extend(temp)
        else:
            segments.append(i)
    return segments
def check_string(string, ext=1): # ext=0说明是外链接

    if ext:   # 对第一方陈述的辨认规则
        # keywords = ["第三方", "关联方", "数据合作方", "授权","服务商","合作方","共享、转让、公开","合作伙伴","关联公司"]
        keywords = ["接入", "第三方", "SDK", "隐私", "政策", "链接", "共享", "收集个人信息"]
        count = 0
        for keyword in keywords:
            if keyword in string:
                count += 1

        colon_num = string.count(":") + string.count("：")
        SDK_num = string.count("SDK")
        keywords_num = string.count("合作方")

        if count >= 4 or SDK_num >= 2:
            if colon_num >= 7 and keywords_num <= 3:
                return True
            else:
                return False
        else:
            return False

    else:  # 对外链陈述的辨认规则
        keywords = ["接入", "第三方", "SDK", "收集个人信息"]
        count = 0
        for keyword in keywords:
            if keyword in string:
                count += 1

        SDK_num = string.count("SDK")
        colon_num = string.count(":") + string.count("：")
        if SDK_num >= 4 and colon_num >= 12:
            return True
        elif count >= 1 and colon_num >= 12:
            return True
        else:
            return False

def judge_sdk_segments(segments, ext):
    '''
    :param segments: 分块隐私政策列表
    :return: 描述分享、共享数据的段
    '''
    # print("可以到judge_sdk_segments")
    result = []
    for i in segments:
        if check_string(i, ext):   # 第一方是1，外链接是0
            print("能检测到check_string")
            result.append(i)
    return list(set(result))
def run_LLM(segments):
    '''
    :param segments: 判定为描述第三方的块列表
    :return: 返回处理好的LLM第三方字典结果
    '''

    json_result = []   # 然后extend LLMmessage_to_jsonlist函数返回的列表之后，就是最后要的整个文本的displayresult了，就可以去extend final_result['display-result']

    for sentence in segments:
        # 比如在两个地方有两大段声明
    #    result = test_from_ali(sentence)
        print("sentence=" + str(sentence))
        # 所以接下来需要把这“一大段”再划分为两到三块，可以在这里计算字数然后分块然后再放到llm
        sentence_list = token_incise(sentence, 3000)
        # print("sentence_list=" + str(sentence_list[0]))
        incise_num = len(sentence_list)
        print("切割段数为：" + str(incise_num))
        if incise_num == 0:
            continue

        index = 0
        for incised_sentence in sentence_list:


            # 记录一次调LLM的时间戳
            current_timestamp = time.time()

            # 与上一次调用的时间戳比较  睡眠
            if hasattr(run_LLM, 'last_timestamp'):
                time_diff = current_timestamp - run_LLM.last_timestamp
                if time_diff < 6:
                    sleep_time = 6 - time_diff
                    print(f"距离上一次调用的时间间隔为：{time_diff}秒，小于6秒，休眠 {sleep_time} 秒")
                    time.sleep(sleep_time)

            result_to_list = []

            print("------------------")
            try:
                print("调用第" + str(index+1) + "个sentence")
                print("在这里要放进llm的子段落是：")
                print(incised_sentence)
                # result = call_with_prompt_gpt(incised_sentence)
                # result = call_with_prompt_tongyi(incised_sentence)

                # 尝试连LLM  如果网络中断之类的就(休眠后)重新发起操作
                while True:
                    try:
                        # result = call_with_prompt_gpt(incised_sentence)
                        result = call_with_prompt_tongyi(incised_sentence)
                        # 执行其他操作
                        break  # 如果没有异常，跳出循环
                    except Exception as e:
                        # 处理异常
                        print("try分支连接LLM时出错:", str(e))
                        # 继续循环，休眠后重复执行动作
                        time.sleep(5)

                index = index + 1
                run_LLM.last_timestamp = current_timestamp

            except Exception as e:
                print("调用LLM接口的异常:" + str(e))

            try:
                result_to_list = LLMmessage_to_jsonlist(result)  # 目前理想是result_to_list是列表
            except Exception as e:
                print("调用回复——json的异常:" + str(e))

            try:
                # 获取所有的键并转换为列表
                keys_list = list(result_to_list[0].keys())

                # 访问列表中的第一个键和第二个键
                first_key = keys_list[0]
                second_key = keys_list[1]

                if result_to_list[0][first_key] == result_to_list[0][second_key]:
                    result_to_list = []

                # json_result.append(result)
                json_result.extend(result_to_list)
            except Exception as e:
                print("改成空列表的异常:" + str(e))

    return json_result     # 这个是所有结果的汇总，是一列表，也就是extend到final_result['display-result']的东西

'''
接口不能用了
'''
def test_from_ali(sentence):
    url = 'http://47.106.173.151:6006/qwen'
    headers = {
        'Content-Type': 'application/json'
    }
    prompt_text_tmp = f"""提取下面这段话中的信息，并按照[{{\\"第三方SDK名称\\":\"\",\"收集个人信息的类型\":[\"\",...]}}形式输出结果,无则返回None：{sentence}"""
    data = {'prompt_text': str(base64.b64encode(prompt_text_tmp.encode('utf-8')))}
    response = requests.post(url, data=json.dumps(data, ensure_ascii=True), headers=headers)

    # 获取响应结果
    result = response.text.encode().decode("unicode_escape")

    # print('result:\n{}'.format(result))
    return 'result:\n{}'.format(result)


def single_txt_temp(t, ext):
    # 单个调试
    # file = open('Privacypolicy_txt/com.taobao.litetao.txt', 'r', encoding='utf-8')
    # t = file.read()
    segments = run_subsection(t)   # 应该是拆分后的段
    for i in segments:
        print(i)
        print("---------------------")
        print("到judge_sdk_segments前")
        # pass
    result_segments = judge_sdk_segments(segments, ext)

    print("提取的关键文本：")
    # print("---------------------")

    for i in result_segments:
        print(i)
        # print("到for i in result_segments:")
        print("---------------------")

    json_rusult = run_LLM(result_segments)

    # json_rusult = str(json_rusult)
    # json_rusult = r"{}".format(json_rusult)
    print("llm识别结果：")
    print(json_rusult)

    '''
    txt记录JSON信息
    '''

    global txt_file

    # folder_name = "txt_record"
    #
    # if not os.path.exists(folder_name):
    #     os.makedirs(folder_name)
    #
    # file_path = os.path.join(folder_name, txt_file)
    #
    # with open(file_path, 'w') as file:
    #     for content in json_rusult:
    #         if type(content) is str:
    #             file.write(content)

    return json_rusult

def piliang_text_temp():
    #批量调试
    filepath = "Privacypolicy_txt"
    filename_list = os.listdir(filepath)
    for i in filename_list:
        if i.endswith(".txt"):
            file = open(filepath+"/"+i, 'r', encoding='utf-8')
            t = file.read()
            segments = run_subsection(t)
            result = judge_sdk_segments(segments, ext)   # 描述分享、共享数据的段
            try:
                if result:
                    with open('segments_temp_result/' + i[:-4] + '.json', 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    f.close()
                else:
                    pass
                    # print(i+"无相关片段")
            except:
                print(i+"写入失败")

if __name__ == '__main__':
    #single_txt_temp()
    #piliang_text_temp()
    #菜鸟裹裹：
    url = "https://page.cainiao.com/cn/docs/?spm=tars.cms-article.0.0.5b395b8975T9Li#/content/cainiaoapp_privacy_updated"
    #墨迹天气：
    url = "https://html5.moji.com/tpd/agreement/privacy-zh_CN.html"
    #先用规则定位到大致几个段落，然后从中抽一句话询问llm这段是否是关于第三方分享信息的，如果返回结果是则继续

    data_path = "../data/data_privacy_html/"

    file_path = 'cn.dictcn.android.digitize.swg_xhzd_21003_3.0.15_306_policy.html'  # 原页面—陈述 新华字典 最规整
    # file_path = 'cn.damai_8.5.5_6000169_policy.html'  # 原页面—陈述 大麦  在一大段附录后面
#    file_path = 'cn.com.pansky.sxzgyl_2.1.71_118_policy.html'  # 原页面—陈述 陕西养老保险APP  识别到的SDK名称会合到一起，怎么修改prompt
#    file_path = 'cn.com.lzb.mobilebank.per_6.2.7_6133_policy.html'  # 兰州银行等银行 非常不规整
#     file_path = 'cn.com.gzbank.mbank_5.0.8_102_policy.html'  # 广银信用卡
#     file_path = 'cn.com.drivedu.chexuetang_5.5.4_290_policy.html'  # 原页面—陈述 国金证券

    file_path = data_path + file_path

    '''
    要不要让llm自己提取字段名,
    返回的结果再来根据关键字提取
    '''

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    new_file_path = file_path.rsplit('.', 1)[0] + '.json'
    # print(new_file_path)

    #global txt_file
    # txt_file = new_file_path


    soup = BeautifulSoup(content, 'html.parser')

    text = soup.get_text(separator="\n")
    # print("html_text:")
    # print(text)

    json_rusult = single_txt_temp(text)

    folder_name = "../data/json_result"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, txt_file)

    with open(file_path, 'w') as file:
        for content in json_rusult:
            if type(content) is str:
                file.write(content)


