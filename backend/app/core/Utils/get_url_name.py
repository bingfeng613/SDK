import re
from urllib.parse import urlparse
def is_valid_url(url):
    #判断url格式是否正常
    if url:
        pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        try:
            match = re.match(pattern, url)
            return bool(match)
        except:
            return False
    else:
        return False
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
def get_url_name_finall(url):
    if isinstance(url,str):
        url_name = get_domain_name(url)+"."+get_urlname(url)
        return url_name
    elif isinstance(url,list):
        for i in url:
            if is_valid_url(i):
                url_name = get_domain_name(url)+"."+get_urlname(url)
                return url_name
    return None
if __name__ == '__main__':
    print(get_url_name_finall("https://lbs.amap.com/pages/privacy/"))