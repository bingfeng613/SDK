#import requests
import json

import requests

from some_function import text_replace
from prompt import prompt_4
from prompt import prompt_0
from some_function import write_json
from some_function import read_json
API_KEY = "N8dICKkgAvaC8wC0J0brEAkC"
SECRET_KEY = "iirmORoNYjv0iC3TOX7ZfXI8xIRIjmCp"


def main_35(prompt):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": 'json_object'
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    try:
        result = response.json().get("result")
    except:
        result = response.text
    return result


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
def decode_json(json_str):
    # 解析JSON字符串为Python对象，比如说字典，列表之类的
    obj = json.loads(json_str, strict=False)
    # 将Python对象转换为JSON格式的编码字符串（中文不转义）
    #decoded_str = json.dumps(obj, ensure_ascii=False)
    return obj

if __name__ == '__main__':
    text = "用了号码认证，参考如下内容：使用的SDK名称：号码认证服务类型：实现本机号码一键登录和认证收集的各个信息类型：网络类型、切换wifi和蜂窝网络通道、设备信息（含IP地址、设备制造商、设备型号、手机操作系统、SIM卡信息SIM State）。SDK隐私政策链接：https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud202112211045_86198.html请务必做延迟初始化配置，确保用户授权《隐私权政策》后再初始化号码认证3.      请务必在您的《隐私政策》中向用户明确告知，号码认证SDK服务集成三大运营商SDK，三大运营商如何处理用户个人信息，详见如下及隐私政策。                                     中移互联网移动认证                  运营主体:中移互联网有限公司                  功能:识别用户的手机号码快速登录，以及查询、分析和风险控制。                  收集个人信息类型:网络类型、网络地址、运营商类型、本机号码信息、SIM卡状态、手机设备类型、手机操作系统、硬件厂商。                  隐私权政策链接:https://wap.cmpassport.com/resources/html/contract.html                  中国联通手机号一键登录                  运营主体:中国联合网络通信集团有限公司                  功能:识别用户的手机号码快速登录，以及实现业务风控                  收集个人信息类型:网络类型、网络地址、运营商类型、本机手机号、手机设备类型、手机操作系统、硬件厂商。                   隐私政策链接:https://opencloud.wostore.cn/authz/resource/html/disclaimer.html?spm=a2c4g.11186623.0.0.41f1633eHxMLkQ&fromsdk=true                   天翼账号认证SDK                   运营主体:天翼数字生活科技有限公司                   功能:识别用户的手机号码快速登录，以及实现业务风控                   收集个人信息类型: 注册手机号码、本机号码、网络连接类型、网络状态信息、网络地址、运营商类型、手机设备类型、手机设备厂商、手机操作系统类型及版本。"
    text = text_replace(text)
    prompt = prompt_4 + prompt_0.format(pp=text)
    llm_result = main_35(prompt)
    print(llm_result)
    print(type(decode_json(llm_result)))
    #llm_result = {"id":"as-zf8wsmfc45","object":"chat.completion","created":1713108501,"result":"{\n    \"judgement\": \"true\",\n    \"data-practice\": [\n        \"使用号码认证服务SDK，我们收集网络类型、切换wifi和蜂窝网络通道、设备信息（含IP地址、设备制造商、设备型号、手机操作系统、SIM卡信息SIM State）等数据，用于实现本机号码一键登录和认证\",\n        \"使用号码认证SDK服务集成中移互联网移动认证SDK，收集网络类型、网络地址、运营商类型、本机号码信息、SIM卡状态、手机设备类型、手机操作系统、硬件厂商等信息，用于识别用户的手机号码快速登录，以及查询、分析和风险控制\",\n        \"使用中国联通手机号一键登录SDK，收集网络类型、网络地址、运营商类型、本机手机号、手机设备类型、手机操作系统、硬件厂商等信息，用于识别用户的手机号码快速登录，以及实现业务风控\",\n        \"使用天翼账号认证SDK，收集注册手机号码、本机号码、网络连接类型、网络状态信息、网络地址、运营商类型、手机设备类型、手机设备厂商、手机操作系统类型及版本等信息，用于识别用户的手机号码快速登录，以及实现业务风控\"\n    ]\n}","is_truncated":False,"need_clear_history":False,"finish_reason":"normal","usage":{"prompt_tokens":961,"completion_tokens":253,"total_tokens":1214}}

