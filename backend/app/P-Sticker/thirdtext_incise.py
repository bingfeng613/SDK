import re

def subsection(text):
    #pattern = r'[一二三四五六七八九十]+\.|[一二三四五六七八九十]+、|附录'
    pattern = r'([一二三四五六七八九十]+(?:十一|十二|十三|十四|十五|十六|十七|十八|十九)*\.|[一二三四五六七八九十]+(?:十一|十二|十三|十四|十五|十六|十七|十八|十九)*、|附录)'
    segments = re.split(pattern,text)
    if not segments:
        segments = [text]

    return segments

def subsection_2(text):
    #pattern = r'\([一二三四五六七八九十]\)|（[一二三四五六七八九十]+）|第三方SDK.*?说明'
    pattern = r'\([一二三四五六七八九十]+(?:十一|十二|十三|十四|十五|十六|十七|十八|十九)*\)|（[一二三四五六七八九十](?:十一|十二|十三|十四|十五|十六|十七|十八|十九)*）|第三方SDK.*?说明'
    segments = re.split(pattern,text)[:]
    if not segments:
        segments = [text]

    return segments
def subsection3(text):
    pattern = r'[123456789]+[、.．]'
    segments = re.split(pattern,text)
    if not segments:
        segments = [text]

    return segments
def subsection_keyword_1(t):
    title = "目录"
    if title in t:
        return False

    if len(t) <= 30:
        return False

    word = 'Cookie'
    # occurrences = t.count(word)
    occurrences = t.lower().count(word.lower())

    if occurrences >= 3:
        return False

    keywords = ["如何存储和保护", "如何保护", "如何存储"]
    title_chars = t[:15]   # 前十五个字，也就是第一行字中有这些字
    for keyword in keywords:
        if keyword in title_chars:
            return False

    keywords = ["如何联系"]
    title_chars = t[:10]
    for keyword in keywords:
        if keyword in title_chars:
            return False

    phrase = '监护人'
    occurrences = t.count(phrase)
    if occurrences >= 3:
        return False

    phrases = ["政策", "修订"]
    word = "信息"

    flag = True
    for phrase in phrases:
        if phrase not in t:
            flag = False
            break
    if flag:
        return False

    return True

def run_thirdtext_incise(text):
    seg_1 = subsection(text)
    seg_2 = []
    for i in seg_1:
        if subsection_keyword_1(i):
            seg_2.append(i)

    seg_3 = []
    for i in seg_2:
        temp = subsection_2(i)
        if temp:
            seg_3.extend(temp)
        else:
            seg_3.append(i)
    seg_4 = []
    for i  in seg_3:
        temp = subsection3(i)
        if temp:
            seg_4.extend(temp)
        else:
            seg_4.append(i)
    result = []
    for i in seg_4:
        if subsection_keyword_1(i):
            i = i.replace(" ","")
            result.append(i)

    #for i in result:
     #   print(i)
      #  print("---------------------")

    return result
if __name__ == "__main__":

    s = " 1.帮助您连接智能设备您如希望将App与您所使用的智能设备相连接,2.您需要开启蓝牙权限,以使得我们能够搜索到您的智能设备.3、此外我们可能会收集您的Wi-Fi信息、4.位置信息、智能设备信息.这些信息将用于为您提供智能设备快连、连接、发现附近设备和设备管理的功能.如您拒绝提供上述信息,我们将无法帮助您连接智能设备,但不影响您正常使用喜马拉雅的其他功能.(十一)为您提供客户服务及处理争议当您向我们发起投诉、申诉或进行咨询时,为了您的账号与系统安全,我们可能需要您先行提供账号信息,并与您之前的个人信息相匹配以验证您的用户身份.同时,为了方便与您联系或帮助您解决问题,我们可能还需要您提供姓名、手机号码、电子邮件及其他联系方式等个人信息,并通过第三方客服系统保存通话录音,其中可能包含通信/通话记录,用于与您联系和帮助您解决问题,或记录相关问题的处理方案及结果.为确认交易状态及为您提供商品/服务的售后与争议解决服务,我们会通过您基于交易所选择的支付机构、支付方式等收集与交易相关的信息,包括iOS端IAP支付交易凭证和收费凭证.如您拒绝提供上述信息,我们将无法为您提供完整的客户服务及处理争议,但不影响您正常使用喜马拉雅的其他功能.(十二)为您提供安全保障功能为履行维护网络安全义务,提高您使用服务的安全性,确保操作环境安全,预防钓鱼网站、欺诈、网络漏洞、计算机病毒、网络攻击、网络侵入等安全风险,以预防、发现和调查潜在的违法违规或违反用户服务协议、政策或规则的行为,如会员账号活动异常、多端登录、流量异常、经常性退款请求或低价转让会员卡等,我们以及在应用程序中嵌入的应用安全SDK将在后台自动收集您的设备信息(包括设备型号、硬件序列号、设备MAC地址、操作系统版本、设备设置、唯一移动设备识别码(IMEI、Android ID、IDFA、IDFV、MEID、OAID、SIM卡序列号和IMSI信息)、UUID、必要的移动应用列表信息、运行中的进程信息、软硬件及设备、设备环境信息)、日志信息(包括您的搜索和浏览记录、关注、播放记录、访问量、播放时长、IP地址、WIFI扫描列表、WIFI名称、运营商信息、电信运营商网络、使用的语言、访问日期和时间),并可能使用或整合您的账户信息、交易信息、支付信息以及其他取得您授权或依据法律共享的信息,综合判断您账户及交易风险、完成身份验证、检测,防范安全事件,并依法采取必要的记录、审计、分析、处置措施,保护各方合法权益稳定不受侵害.(十三)其他附加服务"
    result = run_thirdtext_incise(s)
    for i in result:
        print(i)