import json
import os
import re

def token_incise(input_message, max_token):
    '''
    :param input_message: 等待输入模型的字符串
    :param max_token: 模型最大输出token
    :return: 按字数分段后的字符串列表
    '''

    list_message = []
    max_words = max_token / 2 * 0.9  # 对应的字符数(可以用len计算的)
    print("最大token数对应的字符数：" + str(max_words))
    print("输入对应的字符数：" + str(len(input_message)))


    if len(input_message) < max_words:
        list_message.append(input_message)
        return list_message

    # 按url分段
    text_lines = input_message.split('\n')
    current_section = ''
    sections = []
    flag = 1

    for line in text_lines:
        current_section += (line + '\n')
        if 'http' or "点击查看" in line:
            flag = 0
            sections.append(current_section.strip())
            current_section = ''

    if flag:
        # sections.append(current_section.strip())
        return sections

    # for section in sections:
    #     print(section)
    #     print('-'*50)

    # 按字数合并段
    current_segment = ''
    words_count = 0

    for section in sections:
        words_len = len(section)
        if words_len >= max_words:
            return list_message
        if words_count + words_len <= max_words:
            current_segment += section + '\n'
            words_count += words_len
        else:
            list_message.append(current_segment)
            current_segment = section + '\n'
            words_count = words_len

    list_message.append(current_segment)

    return list_message

if __name__ == '__main__':
    input_message = '''1） SDk名称：BUGLySDK
    第三方公司名称：深圳市腾讯计算机系统有限公司
    第三方收集个人信息的目的：用于检测App稳定性并进行故障诊断、崩溃上报，以便帮助用户快速解决异常情况
    第三方收集个人信息的类型：设备MAC、设备IMEI、设备地理位置
    隐私政策链接：https://static.bugly.qq.com/bugly-sdk-privacy-statement.pdf
    2） SDk名称：友盟+SDK
    第三方公司名称：友盟同欣（北京）科技有限公司
    第三方收集个人信息的目的：我们的产品集成友盟+SDK，友盟+SDK需要手机您的设备MAC地址，IP地址以提供统计分析服务，并通过地理位置校准报表数据准确性，提供基础反作弊能力。
    第三方收集个人信息的类型：设备信息（设备序列号、Android_Id、IMEI、MAC、IDFA、OpenUDID、GUID、SIM 卡 IMSI 信息、地理位置、Ip地址）
    隐私政策链接：https://www.umeng.com/page/policy
    
    3）SDk名称：铠甲sdk
    第三方公司名称：厦门铠甲网络股份有限公司
    第三方收集个人信息的目的：广告服务
    第三方收集个人信息的类型：收集个人信息类型：设备信息、应用版本信息、网络信息、位置信息、设备唯一标识符
    隐私政策链接：https://mssp.kaijia.com/privacyPolicy.html
    4）SDk名称：穿山甲sdk
    第三方公司名称：北京巨量引擎网络技术有限公司
    第三方收集个人信息的目的：广告服务
    第三方收集个人信息的类型：
    收集个人信息：【双端】设备品牌、设备序列号、型号、软件系统版本、分辨率、网络信号强度、IP地址、设备语言、传感器信息等基础信息
    【仅Android】AndroidID
    【仅iOS】手机系统重启时间、磁盘总空间、系统总内存空间、CPU数目等基础信息、IDFV
    您可以基于广告投放效果优化的目的需要选择是否向穿山甲提供如下信息：
    【双端】无线网SSID名称、WiFi路由器MAC地址、设备的MAC地址（如为iOS端，则仅适用于IOS3200以下版本）
    【仅Android】设备标识符（如IMEI、OAID、IMSI、ICCID、GAID（仅GMS服务）、MEID、设备序列号build_serial，具体字段因软硬件版本不同而存在差异）
    【仅iOS】设备标识符（如IDFA，具体字段因软硬件版本不同而存在差异）
    使用权限：读取手机设备标识等信息、获取位置信息、允许应用程序访问有关Wi-Fi 网络的信息、允许应用程序写入外部存储、允许应用程序读取外部存储、获取应用软件列表、麦克风权限
    隐私政策链接：https://www.csjplatform.com/privacy
    
    5）SDk名称：优量汇sdk
    第三方公司名称：深圳市腾讯计算机系统有限公司
    第三方收集个人信息的目的：广告服务
    第三方收集个人信息的类型：
    【设备信息】：系统版本名、系统版本号、设备型号、分辨率、屏幕DPI设备生产商、网络类型、系统语言、时区、时间戳、User Agent信息、屏幕方向;
    【应用信息】当前应用包名、应用版本名、应用版本信息
    【设备标识信息】设备id(android_id)、IMEI（用户授权才收集）、OAID、Mac地址、IDFA
    地理位置信息、广告交付数据
    隐私政策链接：https://imgcache.qq.com/gdt/cdn/adn/uniondoc/ylh_sdk_privacy_statement.html
    6）SDk名称：ADmobile Suyiad SDK
    第三方公司名称：杭州魔厨科技有限公司及其子公司杭州艾狄墨搏信息服务有限公司
    第三方收集个人信息的目的：广告服务
    第三方收集个人信息的类型：
    【设备信息】：系统版本名、系统版本号、设备型号、分辨率、屏幕DPI、设备生产商、网络类型、系统语言、时区、时间戳、User Agent信息、屏幕方向;
    【应用信息】当前应用包名、应用版本名、应用版本信息
    【设备标识信息】设备id(android_id)、IMEI（用户授权才收集）、OAID、Mac地址、IDFA
    地理位置信息（用户授权才收集）、广告交互数据
    隐私政策链接：https://www.admobile.top/privacyPolicy.html
    7）SDk名称：支付宝sdk
    第三方公司名称：支付宝(中国)网络技术有限公司
    第三方收集个人信息的目的：帮助您顺利完成交易、保障您的交易安全、查询订单信息、提供客户服务。在支付过程中，我们可能会收集您的第三方支付账号(包括Apple Store账号、支付宝账号)，以实现原路径退款、售后服务
    第三方收集个人信息的类型：交易商品或服务信息、收货人信息（收货人姓名、收货地址及其联系电话）（个人敏感信息）、交易金额、下单时间、订单商户、订单编号、订单状态、支付方式、支付账号、支付状态（个人敏感信息）、OpenUUId (iOS)
    隐私政策链接：https://render.alipay.com/p/c/k2cx0tg8
    8）SDk名称：腾讯浏览器
    第三方公司名称：深圳市腾讯计算机系统有限公司
    第三方收集个人信息的目的：广告浏览
    第三方收集个人信息的类型：设备信息（IMEI/MAC/Android ID/IDFA/OpenUDID/GUID/SIM 卡 IMSI 信息）
    隐私政策链接：https://x5.tencent.com/tbs/guide/develop.html#5
    9）SDk名称：微信支付
    第三方公司名称：深圳市腾讯计算机系统有限公司
    第三方收集个人信息的目的：帮助您顺利完成交易、保障您的交易安全、查询订单信息、提供客户服务。在支付过程中，我们可能会收集您的第三方支付账号(包括Apple Store账号、微信账号)，以实现原路径退款、售后服务
    第三方收集个人信息的类型：交易商品或服务信息、收货人信息（收货人姓名、收货地址及其联系电话）（个人敏感信息）、交易金额、下单时间、订单商户、订单编号、订单状态、支付方式、支付账号、支付状态（个人敏感信息）、OpenUUId (iOS)
    隐私政策链接：https://pay.weixin.qq.com/
    10）SDk名称：百度定位SDK
    第三方公司名称：百度在线网络技术（北京）有限公司
    第三方收集个人信息的目的：用于定位用户位置，提供基于地理位置信息的服务
    第三方收集个人信息的类型：获取粗略位置，获取精确位置，网络访问，获取WiFi状态，改变网络状态，写入外部存储，读取外部存储，设备标识信息【MAC地址信息、imei、imsi或oaid、Android Id 、CPU ID 序列号、OpenUUId (iOS)】
    隐私政策链接：http://lbsyun.baidu.com/index.php?title=android-locsdk
    11）SDk名称：百度统计SDK
    第三方公司名称：百度在线网络技术（北京）有限公司
    第三方收集个人信息的目的：数据分析
    第三方收集个人信息的类型：网络访问，设备标识信息【MAC地址信息、imei、imsi或oaid、Android Id 、CPU ID 序列号、OpenUUId (iOS)】，地理位置信息、应用程序列表信息
    隐私政策链接：https://mtj.baidu.com/web/welcome/login
    12）SDk名称：茜昂科技移动广告产品
    第三方公司名称：上海茜昂信息科技有限公司
    第三方收集个人信息的目的：广告服务
    第三方收集个人信息的类型：收集个人信息类型：设备信息、应用版本信息、网络信息、位置信息、设备唯一标识符
    隐私政策链接：http://ssp.tenetengine.com/privacy.html
    13）SDk名称：MobSDK服务
    第三方公司名称：上海游昆信息技术有限公司
    第三方收集个人信息的目的：广告服务
    第三方收集个人信息的类型：收集个人信息类型：设备信息、应用版本信息、网络信息、位置信息、设备唯一标识符
    隐私政策链接：https://www.mob.com/wiki/detailed?wiki=437&id=296
    14）SDK名称：移动推送 TPNS SDK
    第三方名称：深圳市腾讯计算机系统有限公司
    SDK用途：在移动终端设备进行消息推送
    收集个人信息类型：设备信息(手机型号，系统类型、系统版本等)用于标签化推送以及识别是否是真机、网络信息(网络类型)支持根据不同网络类型进行不同类型推送、账号绑定信息(根据您所选用的不同推送渠道，QQ号、微信Union ID、 手机号、邮箱等)用于根据账号信息进行推送。
    数据处理方式：通过去标识化、加密传输及其他安全方式
    官网链接：https://cloud.tencent.com/product/tpns
    隐私政策链接：https://privacy.qq.com/document/preview/8565a4a2d26e480187ed86b0cc81d727
    15）SDK名称：获得场景视频SDK
    第三方公司名称： 创盛视联数码科技（北京）有限公司
    SDK用途：云点播
    隐私政策链接：https://hdgit.bokecc.com/ccvideo/VOD_Android_SDK/-/wikis/%E5%90%88%E8%A7%84%E6%8C%87%E5%8D%97
    16）
    第三方公司名称：广州太平洋电脑信息咨询有限公司
    服务：H5页面，广告服务
    隐私政策链接：https://www1.pcauto.com.cn/app/20190909/privacyPolicy.html
    17）SDK名称：BeiZi SDK
    服务：广告服务
    收集信息：
    [Android和iOS公共信息]
    设备品牌、设备型号、设备时区、设备语言、系统版本、开发者应用名、应用版本号、应用包名、网络类型、UserAgent信息、网络状态、崩溃信息、性能数据、屏幕高宽、屏幕方向、屏幕DPI信息、系统更新时间、开机时间、电池电量、USB调试模式、基站个数、运营商、cpu
    [Android独有信息]
    设备ID（OAID、GAID）（IMEI 用户授权才收集）
    [iOS独有信息]
    设备ID（IDFA 用户授权才收集）、IDFV
    获取信息（未收集）：
    传感器信息（例如：重力传感器、加速度传感器、方向传感器、陀螺仪、光线传感器、压力传感器、重力传感器、线性加速度传感器等）、掠过手势内容。
    获取权限：
    [Android]
    访问互联网、网络状态、手机WiFi状态、安装应用
    [iOS]
    网络权限、设备信息（IDFA
    收集信息的目的：基于用户设备信息调整广告投放策略
    基于用户设备信息提供统计分析服务
    基于用户设备信息进行基础的反作弊分析
    基于用户设备信息实现广告正常显示与交互功能的实现
    通过崩溃信息，以此来优化代码缺陷，最大程度减少App崩溃
    通过收集SDK运行过程中性能数据，以优化SDK的性能
    统计广告数据，以用于广告主统计投放结果。包括不限于：请求、展示 、点击 、转化等，用于广告流程分析
    隐私政策链接：http://sdkdoc.beizi.biz/#/zh-cn/guide/UsePrivacy
    18）SDK名称：腾讯云视立方播放器
    包名：com.tencent
    SDK厂家：深圳市腾讯计算机系统有限公司
    服务：视频播放
    收集个人信息：设备型号、wifi状态、操作系统、ip地址、连接的wifi、录音、传感器
    使用权限：存储权限 蓝牙权限
    收集的用户信息及权限说明详见隐私政策链接：https://cloud.tencent.com/document/product/881/65679'''

    list_message = token_incise(input_message, 3000)

    for i, segment in enumerate(list_message):
        print(f"Segment {i + 1}:\n{segment}\n")





