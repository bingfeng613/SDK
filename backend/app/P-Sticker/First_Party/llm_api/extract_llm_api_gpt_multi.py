import openai

def call_with_prompt_gpt_multi(sentence, times, iffinished = 0):
    '''
    :param sentence: 次数为0时为空
    :param times: 发送的次数，0为multi_prompt_0
    :param iffinished: 是否为最后一段，是1，否0
    :return: 解析结果
    '''

    openai.api_key = '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'

    multi_prompt_0 = "现在将给你发送一个指示，由于指示内容的字数太多，我需要分批发送给你，你要分批接收，接收结束后将这些内容拼接起来，再做分析。一定要严格按照下面几点要求执行。1、内容会用[]圈起来，以便让你识别。2、每发送一批内容，你收到后不要做任何处理。3、内容全部发送完后我会明确告诉你，“发送结束”。4、收到“发送结束”的指令后，你要把所有内容拼接起来，按照接下来给你的指示进行输出。"

    multi_prompt_1 = "[接下来你将按要求解析下面用三个横杠(即“---”)分隔的隐私政策文本，只需返回下文要求的文本分析的json格式结果，而不是代码步骤。请以里面的内容为基础，判断有无提到'''第三方SDK或第三方合作方'''，并提取原文中描述这些第三方的字句, 并以json格式提供以下keys:’第三方SDK名称‘,'功能',’收集的个人信息类型‘,'隐私政策链接' 分析通过以下步骤：步骤1：读取隐私政策文本。步骤2：理解三个单引号中分隔的关键字意义，步骤3：基于读取的隐私政策文本，判断是否声明使用三个单引号中分隔的关键字。步骤4：如果判断该隐私政策声明进行了这些“第三方”的声明，提取原文中描述这些“第三方”的字句；如果无，则不提取。步骤5：返回json格式结果。给你举个例子：假设我给你的文本是“支付宝SDK 功能：帮助用户完成付款 收集个人信息类型：设备信息 所属机构：浙江蚂蚁小微金融服务集团 隐私权政策链接：https://opendocs.alipay.com/open/54/01g6qm#%E6%94%AF%E4%BB%98%E5%AE%9D%20App%20%E6%94%AF%E4%BB%98%E5%AE%A2%E6%88%B7%E7%AB%AF%20SDK%20%E9%9A%90%E7%A7%81%E6%94%BF%E7%AD%96 阿里云SDK：功能：提供域名解析服务，建立网络连接，加速网络访问；语音识别；视频播放器 收集个人信息类型：设备信息 所属机构：阿里云计算有限公司 隐私权政策链接： https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud202112071754_83380.html?spm=a2c4g.11186623.0.0.598730e5wsglWa”, 那么返回的结果为JSON格式，即{’SDK名称‘：‘支付宝SDK’, '功能'：’帮助用户完成付款 收集个人信息类型：设备信息‘, '所属机构'：’浙江蚂蚁小微金融服务集团‘, '隐私权政策链接'：’https://opendocs.alipay.com/open/54/01g6qm#%E6%94%AF%E4%BB%98%E5%AE%9D%20App%20%E6%94%AF%E4%BB%98%E5%AE%A2%E6%88%B7%E7%AB%AF%20SDK%20%E9%9A%90%E7%A7%81%E6%94%BF%E7%AD%96‘},\n{'SDK名称':‘阿里云SDK’, '功能'：'提供域名解析服务，建立网络连接，加速网络访问；语音识别；视频播放器', '收集个人信息类型'：'设备信息','所属机构'：'阿里云计算有限公司', '隐私权政策链接'： 'https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud202112071754_83380.html?spm=a2c4g.11186623.0.0.598730e5wsglWa'} 注意事项：-需要先读取整个文本再做判断。-只返回一个基于整个文本的最终判断结果，且不要返回指定之外的key值。-请聚焦分析三个单引号分隔的关键字。-请给出完整的解析结果   ---{"

    multi_prompt_1 = multi_prompt_1 + sentence + "}]"

    multi_prompt_final = "---{" + sentence + "}]"

    fin_sign = "发送结束"

    message_content = ""
    if times == 0:
        message_content = multi_prompt_0
    elif times == 1:
        message_content = multi_prompt_1
    else:
        message_content = multi_prompt_final

    if iffinished:
        message_content = message_content + fin_sign

    response = openai.ChatCompletion.create(

      model="gpt-4",

      messages=[

            # {"role": "user", "content": ""},
          {"role": "user",
           "content": message_content},

        ]

      )

    print("返回结果 = " + str(response['choices'][0]['message']['content']))

    return response['choices'][0]['message']['content']


t1 = "1.腾讯 BuglySDK SDK类型：日志跟踪 公司名称：深圳市腾讯计算机系统有限公司 业务场景：更真实地为开发者还原Crash场景服务 收集的信息或申请的权限：Crash信息及线程堆栈，ROM/RAM/SD卡容量、网络/语言等状态包名、版本、所属进程名，Android id，用于判断Crash设备做统计 链接地址：https://bugly.qq.com/v2/downloads 2.BoltsTasks SDK类型：开源框架 "

t2 = "公司名称：BoltsFramework 业务场景：UI线程中运行任何耗时操作，避免阻塞UI线程 收集的信息或申请的权限：无 链接地址：https://github.com/BoltsFramework/Bolts-Android 3.小米推送 SDK类型：推送通知 公司名称：小米科技有限责任公司 业务场景："

t3 = "对小米品牌手机进行消息推送 收集的信息或申请的权限：设备型号、APP版本、IMEI/MEID、设备存储、地区、APP运行进程信息 链接地址：https://dev.mi.com/console/doc/detail?pId=41"

call_with_prompt_gpt_multi("", 0)
call_with_prompt_gpt_multi(t1, 1)
call_with_prompt_gpt_multi(t2, 2)
call_with_prompt_gpt_multi(t3, 3)