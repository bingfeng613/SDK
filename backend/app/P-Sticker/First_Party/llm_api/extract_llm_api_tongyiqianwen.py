# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
'''
目前切割后的文本接入的API
'''

import base64
from http import HTTPStatus
import dashscope

'''
通过prompt调用
'''
def call_with_prompt_tongyi(sentence):
    print("call_with_prompt--str(len(sentence))" + str(len(sentence)))
    dashscope.api_key = "sk-b8b1250359f4489dbd4584a7af0f125f"
 #   prompt_text_tmp = f"""提取下面这段话中的信息，并按照[{{\\"第三方\\":\"\",\"收集信息类型\":[\"\",...]}}形式输出结果,无则返回None：{sentence}"""
 #    prompt_text_tmp = "提取下面这段话中的信息，并按照[{'第三方SDK名称':a,'收集个人信息类型':b,'隐私政策链接':e},\n{'第三方SDK名称':c,'收集个人信息类型':d,'隐私政策链接':f}]这种形式输出结果,没有相关信息则返回None：" + sentence
    # text = "请注意一定要以我指定的格式输出，即输出结果应该是由多个{第三方SDK名称:a,收集个人信息类型:b,隐私政策链接:e}这种字典格式的单元组成的列表，且每个字典格式单元之间以一个逗号隔开；也不要出现我指定的格式以外的内容，比如绝对不能出现类似于’以下是您要求的信息‘ 这样的说明"
    text = "接下来你将按要求解析下面用三个横杠(即“---”)分隔的隐私政策文本，只需返回下文要求的文本分析的json格式结果，而不是代码步骤。请以里面的内容为基础，判断有无提到'''第三方SDK或第三方合作方'''，并提取原文中描述这些第三方的字句, 并以json格式提供以下keys:’第三方SDK名称‘,'功能',’收集的个人信息类型‘,'隐私政策链接' 分析通过以下步骤：步骤1：读取隐私政策文本。步骤2：理解三个单引号中分隔的关键字意义，步骤3：基于读取的隐私政策文本，判断是否声明使用三个单引号中分隔的关键字。步骤4：如果判断该隐私政策声明进行了这些“第三方”的声明，提取原文中描述这些“第三方”的字句；如果无，则不提取。步骤5：返回json格式结果。给你举个例子：假设我给你的文本是“支付宝SDK 功能：帮助用户完成付款 收集个人信息类型：设备信息 所属机构：浙江蚂蚁小微金融服务集团 隐私权政策链接：https://opendocs.alipay.com/open”, 那么返回的结果为JSON格式，即{’SDK名称‘：‘支付宝SDK’, '功能'：’帮助用户完成付款 收集个人信息类型：设备信息‘, '所属机构'：’浙江蚂蚁小微金融服务集团‘, '隐私权政策链接'：’https://opendocs.alipay.com/open‘}} 注意事项：-需要先读取整个文本再做判断。-只返回一个基于整个文本的最终判断结果，且不要返回指定之外的key值。-请聚焦分析三个单引号分隔的关键字。-请给出完整的解析结果   ---{"
    # prompt_text_tmp = prompt_text_tmp + text
    prompt_text_tmp = text + sentence + "}"
    result = ''

    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt_text_tmp
    )
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print("response.output:"+str(response.output['text']))  # The output text
        print("usage:" + str(response.usage))  # The usage information
        # print("response：")
        # print(response)
        result = response.output['text']

    else:
        print("response.status_code != HTTPStatus.OK")
        print("response.code=" + str(response.code))  # The error code.
        print("response.message=" + str(response.message))  # The error message.

    return result

def call_with_messages():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

