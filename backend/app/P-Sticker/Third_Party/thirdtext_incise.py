import re
import sys
sys.path.append("..")
from First_Party.extract.display_incise_extract_llm import run_subsection
from First_Party.extract.display_incise_extract_llm import subsection
from First_Party.extract.display_incise_extract_llm import subsection_2

def subsection_keyword_1(t):
    title = "目录"
    if title in t:
        return False

    if len(t) <= 25:
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
    # else:
    #     flag = True
    #     phrases = ["联系我们", "回复"]
    #     for phrase in phrases:
    #         if phrase not in t:
    #             flag = False
    #             break
    #     if flag:
    #         return False

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

    # segments = run_subsection(text)
    seg_2 = []
    result = []

    for i in seg_1:
        # print(i)
        # print("---------------------")
        if subsection_keyword_1(i):
            seg_2.append(i)

    seg_3 = []
    for i in seg_2:
        temp = subsection_2(i)
        if temp:
            seg_3.extend(temp)
        else:
            seg_3.append(i)

    result = []
    for i in seg_3:
        # print(i)
        # print("---------------------")
        if subsection_keyword_1(i):
            result.append(i)

    for i in result:
        print(i)
        print("---------------------")

    return result