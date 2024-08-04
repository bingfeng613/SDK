import json
import os
import re

def LLMmessage_to_jsonlist(llm_message):
    '''
    :param: llm输出的结果
    :return: 去掉头尾后的列表
    '''

    # 去除头尾、\n、空格
    cleaned_message = llm_message.replace('\n', '').replace('```json', '').replace('```', '').replace(' ', '')
    # 提取{}之间的信息
    pattern = re.compile(r'{.*?}')
    valid_json_data = [json.loads(match.group()) for match in pattern.finditer(cleaned_message)]

    # print(valid_json_data) # [{'第三方SDK名称': '小米推送SDK', '功能': '用于推送消息', '收集的个人信息类型': '设备标识符（如AndroidID、OAID）、WLAN接入点（如SSID）', '隐私政策链接': 'https://dev.mi.com/console/doc/detail?pId=1822'}, {'第三方SDK名称': '华为推送SDK', '功能': '用于推送消息', '收集的个人信息类型': '应用基本信息、应用内设备标识符、设备的硬件信息、系统基本信息和系统设置信息', '隐私政策链接': 'https://developer.huawei.com/consumer/cn/doc/development/HMSCore-Guides/privacy-statement-0000001050042021'}, {'第三方SDK名称': 'OPPO推送SDK', '功能': '用于推送消息', '收集的个人信息类型': '设备标识符（如IMEI、OAID、硬件序列号/Serial、IMSI、AndroidID、GAID/AAID）、应用信息、网络信息、IP地址、设备信息', '隐私政策链接': 'https://open.oppomobile.com/new/developmentDoc/info?id=10288'}, {'第三方SDK名称': 'Vivo推送SDK', '功能': '用于推送消息', '收集的个人信息类型': '设备标识符（如IMEI、EmmCID、UFSID、ANDROIDID、GUID、GAID、OPENID、VAID、OAID、RegID、加密的AndroidID）、设备制造商、设备型号、应用信息（如应用包名、版本号、APPID、安装、卸载、恢复出厂设置、运行状态）、网络类型、消息发送结果、通知栏状态、锁屏状态', '隐私政策链接': 'https://dev.vivo.com.cn/documentCenter/doc/652#w1-12075822'}, {'第三方SDK名称': '魅族推送SDK', '功能': '用于推送消息', '收集的个人信息类型': '设备标识符（如IMEI、MEID、硬件序列号/Serial）、设备MAC地址、位置信息（如GPS）、WLAN接入点（如SSID、BSSID）', '隐私政策链接': 'https://www.meizu.com/legal.html'}, {'第三方SDK名称': '友盟SDK', '功能': '用于数据统计分析', '收集的个人信息类型': '设备标识符（Android如IMEI、AndroidID、硬件序列号/Serial、IMSI、GAID/AAID、OAID、MEID、ICCID）、设备MAC地址、位置信息', '隐私政策链接': 'https://www.umeng.com/page/policy'}, {'第三方SDK名称': '钉钉SDK', '功能': '实现分享至钉钉', '收集的个人信息类型': '联网信息、设备信息', '隐私政策链接': 'https://open.dingtalk.com/document/orgapp-client/share-SDK'}, {'第三方SDK名称': '微信开放平台SDK', '功能': '提供微信分享、登录、支付等功能', '收集的个人信息类型': '分享图片或内容、设备标识符（Android如IMEI、AndroidID、硬件序列号/Serial）、设备MAC地址、WLAN接入点（如SSID、BSSID）', '隐私政策链接': 'https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_agreement&s=privacy'}, {'第三方SDK名称': '微博开放平台SDK', '功能': '实现通过微博登录、分享内容至微博及支付服务', '收集的个人信息类型': '设备标识符（Android如IMEI、MEID、AndroidID、IMSI、硬件序列号/Serial、ICCID、OAID，iOS如IDFV、IDFA）、设备MAC地址、IP地址、WLAN接入点（如SSID、BSSID）、分享图片或内容、设备信息', '隐私政策链接': 'https://m.weibo.cn/c/privacy'}, {'第三方SDK名称': '支付宝SDK', '功能': '实现支付宝分享、支付', '收集的个人信息类型': '设备标识符包括IMEI、IMSI、MAC地址、设备序列号、硬件序列号、SIM卡序列号、ICCID、；AndroidID、OAID、SSID、BSSID；系统设置、系统属性、设备型号、设备品牌、操作系统；IP地址、网络类型、运营商信息、Wi-Fi状态、Wi-Fi参数、Wi-Fi列表；软件安装列表', '隐私政策链接': 'https://opendocs.alipay.com/open/54/01g6qm'}, {'第三方SDK名称': 'QQSDK', '功能': '实现分享内容至QQ', '收集的个人信息类型': '分享图片或内容、设备标识符（Android如IMEI、AndroidID、硬件序列号/Serial）、设备MAC地址、WLAN接入点（如SSID、BSSID）', '隐私政策链接': 'https://wiki.connect.qq.com/qq%e4%ba%92%e8%81%94sdk%e9%9a%90%e7%a7%81%e4%bf%9d%e6%8a%a4%e5%a3%b0%e6%98%8e'}]
    # print(type(valid_json_data)) # <class 'list'>
    # print(type(valid_json_data[0])) # <class 'dict'>

    # json_data = json.dumps(valid_json_data, indent=2, ensure_ascii=False)
    # print(type(json_data),json_data)

    # 把字符串转化为“字典组成的列表”，才能跟其它地方的添加形式一样

    # list_result = []
    list_result = valid_json_data

    final_result = {'sdk-url-list': [], 'table-result-len': None, 'table-url': [], 'table-result': [],
                    'display-result-len': None, 'display-url': [], 'display-result': [], 'false-url': []}
    final_result['display-result'].extend(list_result)

    result_json_path = 'test.json'
    if not os.path.exists(result_json_path):
        # 创建一个空的JSON对象
        empty_json = {}

        # 打开文件并写入空的JSON内容
        with open(result_json_path, 'x', encoding='utf-8') as file:
            json.dump(empty_json, file, ensure_ascii=False, indent=2)

    with open(result_json_path,'w',encoding='utf-8')as f:
        json.dump(final_result,f,ensure_ascii=False,indent=2)#盒马漏掉了一个sdk链接，陈列形式的。

    f.close()

    return list_result

# llm_message = '```json\n[\n    {\n        "第三方SDK名称": "小米推送SDK",\n        "功能": "用于推送消息",\n        "收集的个人信息类型": "设备标识符（如Android ID、OAID）、WLAN接入点（如SSID）",\n        "隐私政策链接": "https://dev.mi.com/console/doc/detail?pId=1822"\n    },\n    {\n        "第三方SDK名称": "华为推送SDK",\n        "功能": "用于推送消息",\n        "收集的个人信息类型": "应用基本信息、应用内设备标识符、设备的硬件信息、系统基本信息和系统设置信息",\n        "隐私政策链接": "https://developer.huawei.com/consumer/cn/doc/development/HMSCore-Guides/privacy-statement-0000001050042021"\n    },\n    {\n        "第三方SDK名称": "OPPO推送SDK",\n        "功能": "用于推送消息",\n        "收集的个人信息类型": "设备标识符（如IMEI、OAID、硬件序列号/Serial、IMSI、Android ID、GAID/AAID）、应用信息、网络信息、IP地址、设备信息",\n        "隐私政策链接": "https://open.oppomobile.com/new/developmentDoc/info?id=10288"\n    },\n    {\n        "第三方SDK名称": "Vivo推送SDK",\n        "功能": "用于推送消息",\n        "收集的个人信息类型": "设备标识符（如IMEI、EmmCID、UFSID、ANDROIDID、GUID、GAID、OPENID、VAID、OAID、RegID、加密的Android ID）、设备制造商、设备型号、应用信息（如应用包名、版本号、APPID、安装、卸载、恢复出厂设置、运行状态）、网络类型、消息发送结果、通知栏状态、锁屏状态",\n        "隐私政策链接": "https://dev.vivo.com.cn/documentCenter/doc/652#w1-12075822"\n    },\n    {\n        "第三方SDK名称": "魅族推送SDK",\n        "功能": "用于推送消息",\n        "收集的个人信息类型": "设备标识符（如IMEI、MEID、硬件序列号/Serial）、设备MAC地址、位置信息（如GPS）、WLAN接入点（如SSID、BSSID）",\n        "隐私政策链接": "https://www.meizu.com/legal.html"\n    },\n    {\n        "第三方SDK名称": "友盟SDK",\n        "功能": "用于数据统计分析",\n        "收集的个人信息类型": "设备标识符（Android如IMEI、Android ID、硬件序列号/Serial、IMSI、GAID/AAID、OAID、MEID、ICCID）、设备MAC地址、位置信息",\n        "隐私政策链接": "https://www.umeng.com/page/policy"\n    },\n    {\n        "第三方SDK名称": "钉钉SDK",\n        "功能": "实现分享至钉钉",\n        "收集的个人信息类型": "联网信息、设备信息",\n        "隐私政策链接": "https://open.dingtalk.com/document/orgapp-client/share-SDK"\n    },\n    {\n        "第三方SDK名称": "微信开放平台SDK",\n        "功能": "提供微信分享、登录、支付等功能",\n        "收集的个人信息类型": "分享图片或内容、设备标识符（Android如IMEI、Android ID、硬件序列号/Serial）、设备MAC地址、WLAN接入点（如SSID、BSSID）",\n        "隐私政策链接": "https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_agreement&s=privacy"\n    },\n    {\n        "第三方SDK名称": "微博开放平台SDK",\n        "功能": "实现通过微博登录、分享内容至微博及支付服务",\n        "收集的个人信息类型": "设备标识符（Android如IMEI、MEID、Android ID、IMSI、硬件序列号/Serial、ICCID、OAID，iOS如IDFV、IDFA）、设备MAC地址、 IP地址、WLAN接入点（如SSID、BSSID）、分享图片或内容、设备信息",\n        "隐私政策链接": "https://m.weibo.cn/c/privacy"\n    },\n    {\n        "第三方SDK名称": "支付宝SDK",\n        "功能": "实现支付宝分享、支付",\n        "收集的个人信息类型": "设备标识符包括IMEI、IMSI、MAC 地址、设备序列号、硬件序列号、SIM卡序列号、ICCID、；Android ID、OAID、SSID、BSSID；系统设置、系统属性、设备型号、设备品牌、操作系统；IP 地址、网络类型、运营商信息、Wi-Fi 状态、Wi-Fi 参数、Wi-Fi 列表；软件安装列表",\n        "隐私政策链接": "https://opendocs.alipay.com/open/54/01g6qm"\n    },\n    {\n        "第三方SDK名称": "QQ SDK",\n        "功能": "实现分享内容至QQ",\n        "收集的个人信息类型": "分享图片或内容、设备标识符（Android如IMEI、Android ID、硬件序列号/Serial）、设备MAC地址、WLAN接入点（如SSID、BSSID）",\n        "隐私政策链接": "https://wiki.connect.qq.com/qq%e4%ba%92%e8%81%94sdk%e9%9a%90%e7%a7%81%e4%bf%9d%e6%8a%a4%e5%a3%b0%e6%98%8e"\n    },\n    // ... more SDK entries would follow similar structure ...\n]\n```'
# list_result = LLMmessage_to_jsonlist(llm_message)