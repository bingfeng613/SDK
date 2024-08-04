import openai

def call_with_prompt_gpt(sentence):
    openai.api_key = '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'

    message_content_prompt = "接下来你将按要求解析下面用三个横杠(即“---”)分隔的隐私政策文本，只需返回下文要求的文本分析的json格式结果，而不是代码步骤。请以里面的内容为基础，判断有无提到'''第三方SDK或第三方合作方'''，并提取原文中描述这些第三方的字句, 并以json格式提供以下keys:’第三方SDK名称‘,'功能',’收集的个人信息类型‘,'隐私政策链接' 分析通过以下步骤：步骤1：读取隐私政策文本。步骤2：理解三个单引号中分隔的关键字意义，步骤3：基于读取的隐私政策文本，判断是否声明使用三个单引号中分隔的关键字。步骤4：如果判断该隐私政策声明进行了这些“第三方”的声明，提取原文中描述这些“第三方”的字句；如果无，则不提取。步骤5：返回json格式结果。给你举个例子：假设我给你的文本是“支付宝SDK 功能：帮助用户完成付款 收集个人信息类型：设备信息 所属机构：浙江蚂蚁小微金融服务集团 隐私权政策链接：https://opendocs.alipay.com/open/54/01g6qm#%E6%94%AF%E4%BB%98%E5%AE%9D%20App%20%E6%94%AF%E4%BB%98%E5%AE%A2%E6%88%B7%E7%AB%AF%20SDK%20%E9%9A%90%E7%A7%81%E6%94%BF%E7%AD%96 阿里云SDK：功能：提供域名解析服务，建立网络连接，加速网络访问；语音识别；视频播放器 收集个人信息类型：设备信息 所属机构：阿里云计算有限公司 隐私权政策链接： https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud202112071754_83380.html?spm=a2c4g.11186623.0.0.598730e5wsglWa”, 那么返回的结果为JSON格式，即{“SDK名称”：”支付宝SDK”, ”功能”：”帮助用户完成付款”, ”收集个人信息类型”：”设备信息”, ”所属机构”：”浙江蚂蚁小微金融服务集团”, ”隐私权政策链接”：”https://opendocs.alipay.com/open/54/01g6qm#%E6%94%AF%E4%BB%98%E5%AE%9D%20App%20%E6%94%AF%E4%BB%98%E5%AE%A2%E6%88%B7%E7%AB%AF%20SDK%20%E9%9A%90%E7%A7%81%E6%94%BF%E7%AD%96”},\n{”SDK名称”:”阿里云SDK”, ”功能”：”提供域名解析服务，建立网络连接，加速网络访问；语音识别；视频播放器”, ”收集个人信息类型”：”设备信息”,”所属机构”：”阿里云计算有限公司”, ”隐私权政策链接”： ”https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud202112071754_83380.html?spm=a2c4g.11186623.0.0.598730e5wsglWa”} 注意事项：-需要先读取整个文本再做判断。-只返回一个基于整个文本的最终判断结果，且不要返回指定之外的key值。-请聚焦分析三个单引号分隔的关键字。-请给出完整的解析结果   ---{"

    message_content = message_content_prompt + sentence + "}"

    response = openai.ChatCompletion.create(

      model="gpt-4",

      messages=[

            # {"role": "user", "content": ""},
          {"role": "user",
           "content": message_content},

        ]

      )

    print("api内的返回结果 = " + str(response['choices'][0]['message']['content']))

    # 查看key可用模型
    # models = openai.Model.list()
    # print(models)

    return response['choices'][0]['message']['content']


