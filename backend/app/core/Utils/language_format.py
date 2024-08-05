import re

def punctuation_C2E(string):
    C_pun = u'~！@#￥%…&*（）—+·={}|：“《》？【】；’，。、*'
    E_pun = u' !      *()_+ ={}|:"<>?[];\',..*'

    table= {ord(f):ord(t) for f,t in zip(C_pun,E_pun)}
    string = string.translate(table)

    # 减少换行符
    pattern = r'\n+'
    replacement = '\n'
    processed_text = re.sub(pattern, replacement, string)

    # 减少空格
    pattern = r'\s{2,}'
    replacement = '  '
    processed_text = re.sub(pattern, replacement, processed_text)

    return processed_text

if __name__ == "__main__":
    s1 = '这里包含中文字符~！@#￥%…&*（）—+·={}|：“《》？【】、；’，。、*\n\n\n\n\n\n这里包含中文字符'
    s2 = punctuation_C2E(s1)
    print(s2)

