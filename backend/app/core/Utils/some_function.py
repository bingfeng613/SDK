import re
from urllib.parse import urlparse
import json
import os
def get_domain_name(url):
    #url = 'http://blog.jp.goo.ne.jp/index.php'
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[-2] + '.' + parsed_url.netloc.split('.')[-1]
    #print(domain) # 输出：goo.ne.jp
    return domain
def get_urlname(url):
    url = url.strip('html')
    url = re.sub(r'[^\w\s]', '', url)
    if len(url[:])<40:
        return url[:]
    else:
        return url[-40:]
def read_json(filepath):
    with open(filepath,'r',encoding='utf-8')as f:
        data = json.load(f)
    f.close()
    return data
def is_valid_url(url):
    #判断url格式是否正常
    if url and isinstance(url,str):
        pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        try:
            match = re.match(pattern, url)
            return bool(match)
        except:
            return False
    else:
        return False
def get_url_name_finall(url):
    if isinstance(url,str):
        url = url.replace(" ","")
        url_name = get_domain_name(url)+"."+get_urlname(url)
        return url_name
    elif isinstance(url,list):
        for i in url:
            if is_valid_url(i):
                i = i.replace(" ", "")
                url_name = get_domain_name(i)+"."+get_urlname(i)
                return url_name
    return None
def write_json(filepath,data):
    try:
        with open(filepath, 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()
    except Exception as e:
        print("write_json出错: ", e)
def run_subsection(text):
    segments = subsection(text)
    if segments:
        for i in segments:
            if len(i)>6000:
                son_sub = subsection_3(i)
                if son_sub:
                    segments.remove(i)
                    segments.extend(son_sub)
    return segments
def subsection(text):
    #使用正则表达式匹配文本中的分段符号:一、
    pattern = r'[一二三四五六七八九十]+、|附录'
    segments = re.split(pattern,text)[1:]
    # 将分段符号添加到每个段落的开头
    #segments = [re.findall(pattern, text)[i] + segment for i, segment in enumerate(segments)]
    #segments = [segment.replace(" ","") for segment in segments]
    if segments and len(segments)>1:
        return segments
    else:
        segments_2 = subsection_2(text)
        if segments_2 and len(segments)>1:
            return segments_2
        else:
            segments_3 = subsection_3(text)
            return segments_3
def subsection_2(text):
    #使用正则表达式匹配文本中的分段符号：（一）
    pattern = r'（[一二三四五六七八九十]+）'
    segments = re.split(pattern,text)[1:]
    # 将分段符号添加到每个段落的开头
    #segments = [re.findall(pattern, text)[i] + segment for i, segment in enumerate(segments)]
    #segments = [segment.replace(" ","") for segment in segments]
    return segments
def subsection_3(text):
    #使用正则表达式匹配文本中的分段符号：（一）
    pattern = r'[123456789]'
    segments = re.split(pattern,text)[1:]
    # 将分段符号添加到每个段落的开头
    #segments = [re.findall(pattern, text)[i] + segment for i, segment in enumerate(segments)]
    #segments = [segment.replace(" ","") for segment in segments]
    return segments
def read_txt_str(txt_name):
    with open(txt_name, 'r',encoding='utf-8') as file:
        content = file.read()
    file.close
    return content
def dir_create(directory,i):
    # 指定目录
    #directory = '/path/to/directory'
    # 检查目录下是否存在文件夹'aa'
    if not os.path.exists(os.path.join(directory, i)):
        # 创建文件夹'aa'
        os.makedirs(os.path.join(directory, i))
        print("文件夹'aa'已创建成功")
    else:
        print("文件夹'aa'已存在")
if __name__ == '__main__':
    '''
    path = "D:\\中山\\隐私合规\\data_compare"
    #path = "D:\\中山\\隐私合规\\purpose_compare"
    #html_name ="D:\\中山\\隐私合规\\sdk_analysis_lh_11.15"
    html_name ="D:\\中山\\隐私合规\\ali_first_sdk\\first_sdk"
    filename_list = os.listdir(html_name)
    for i in filename_list:
        dir_create(path,i[:-5])'''
    print(get_url_name_finall("https://render.alipay.com/p/c/k2cx0tg8     "))
    print(is_valid_url("https://accounts.growingio.com/privacy"))