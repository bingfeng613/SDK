'''
    最初版 表格和陈列形式的简单提取
    陈列形式根据节点提取，提取的效果较差
'''

from bs4 import BeautifulSoup
from bs4 import Tag
import chardet
import os
import re
import json
import math
import bs4.element

from Utils.selenium_driver import driver
from urllib.parse import urlparse
from urllib.parse import urljoin

from .display_incise_extract_llm import single_txt_temp


table_false = 0
def text_format(text):
    text = text.replace(" ", '')
    text = text.replace("﻿", '')
    text = text.replace("\n", '')
    text = text.replace("\t", '')
    text = text.replace(" ", '')
    text = text.replace("•",'')
    return text
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
def check_elements(_str,str_list,max = None,min = None):
    '''
    :param str_list: 字符串列表
    :param _str: string
    :param max: 界限值
    :return: 若列表中超过max个元素在字符串中，则返回true
    '''
    if max ==None:
        max = 1
    if min == None:
        min = 100
    count = 0
    for item in str_list:
        if item in _str:
            count += 1
    if count > max:
        if count < min:
            return True
        else:
            return False
    else:
        return False
def get_html_soup(html_filename):
    '''
    :param html_filename:.html文件的路径
    :return:返回该html文件的soup对象
    '''
    with open(html_filename,'rb')as f:
        html = chardet.detect(f.read())
    f.close()
    with open(html_filename,'r',encoding=html['encoding'])as f:
        result = f.read()
    f.close()
    #print(html['encoding'])
    soup = BeautifulSoup(result,'html.parser')
    return soup
def rowspan_judge(table):
    if table:
        rows = table.find_all('tr')
        for row_index, row in enumerate(rows):
            cells = row.find_all(['td', 'th'])     # 每个单元格
            for cell_index, cell in enumerate(cells):#如果该值大于1，则表明发生行合并
                if 'rowspan' in cell.attrs:
                    try:
                        if int(cell.attrs['rowspan'])<2:
                            continue
                        else:
                            return True
                    except:
                        continue
    return False
def count_row_column(rows):
    '''
    计算一个表格中每一行的列数
    :param rows: 表格所有行
    :return:每行列数列表
    '''
    count_column = []
    for row in rows:
        tds = row.find_all('td')
        if tds:
            count_column.append(len(tds))
        else:
            ths = row.find_all('th')
            if ths:
                count_column.append(len(ths))
    if len(count_column)<=1:
        return count_column,0
    temp_c = count_column[:]
    min_value = min(temp_c)
    temp_c.remove(min_value)
    aver = math.floor(sum(temp_c)/len(temp_c))
    if aver == 1:
        return count_column, aver
    return count_column,aver-1
def colspan_judge(tds):
    '''
    :param row: 表格的一行中所有列元素列表
    :return: 如果该行进行了列合并，则返回true
    '''
    for td in tds:
        if 'colspan'in td.attrs:#如果该值大于1则表明发生了列合并
            #print("该行进行了列合并"+td.get_text())
            try:
                if int(td.attrs['colspan'])<2:
                    return False
                else:
                    return True
            except:
                return True
    return False
def table_headers_find(row,i,count_column,false_colspan = None):
    '''

    :param row: 表格的一行
    :param i: 表格第i行
    :param count_column: 表格每行的列数统计列表
    :return: 表头列表
    '''
    th_list = []
    th_td_list = []
    ths = row.find_all('th')
    if ths:
        for th in ths:
            th_list.append(text_format(th.get_text()))
        return th_list
    else:#无th的情况,
        tds = row.find_all('td')
        #判断该行是否是列合并，如果是列合并则要求下一行
        if tds:
            if i == 0:
                if count_column[i]<count_column[i+1] and colspan_judge(tds):#第一行情况
                    return ['colspan']
                else:#第一行为表头，非列合并
                    for td in tds:
                        th_td_list.append(text_format(td.get_text()))
                    if th_td_list and len(list(set(th_td_list))) == len(th_td_list):#防止明明是列合并，但colspan判断失效
                        return th_td_list
                    else:
                        return['false_colspan']
            else:
                if i+1 == len(count_column):
                    return []
                else:
                    try:
                        if count_column[i]>count_column[i-1] and count_column[i] == count_column[i+1]:#如果该行和前面行不一样列数，同时又和后面列数相同，则该行为表头
                            for td in tds:
                                th_td_list.append(text_format(td.get_text()))
                            if th_td_list and len(list(set(th_td_list))) == len(th_td_list):  # 防止明明是列合并，但colspan判断失效
                                return th_td_list
                            else:
                                return ['false_colspan']
                        elif count_column[i]<count_column[i-1] and count_column[i] == count_column[i+1]:
                            for td in tds:
                                th_td_list.append(text_format(td.get_text()))
                            if th_td_list and len(list(set(th_td_list))) == len(th_td_list):  # 防止明明是列合并，但colspan判断失效
                                return th_td_list
                            else:
                                return ['false_colspan']
                        elif false_colspan:#前一行判断为colspan，但列数一样的行
                            for td in tds:
                                th_td_list.append(text_format(td.get_text()))
                            if th_td_list and len(list(set(th_td_list))) == len(th_td_list):  # 防止明明是列合并，但colspan判断失效
                                temp_new_list_20 = [s for s in th_td_list if len(s)>20]
                                if temp_new_list_20:
                                    return []
                                temp_new_list_38 = [s for s in th_td_list if 3<len(s)<8]
                                if len(temp_new_list_38)>len(th_td_list)/2-1:
                                    return th_td_list
                            else:
                                return ['false_colspan']
                    except:
                        print("")
    return []
def find_th_dict(table_dict_list,n = None):
    '''
    :param table_dict_list:  表格分析字典列表
    :param n: 找到含有 n 个 None 值的字典
    :return: 它会从列表的最后一个字典开始往前遍历，直到找到含有 n 个 None 值的字典，然后返回该字典。如果找不到满足条件的字典，则返回 []。
    '''
    for i in range(len(table_dict_list)-1, -1, -1):
        if list(table_dict_list[i].values()).count(None) >= n:
            return table_dict_list[i]
    return []
def table_td_extract(row):
    td_list = []
    tds = row.find_all('td')
    if tds:
        for td in tds:
            td_list.append(text_format(td.get_text()))
    url_list = []
    a_tag = row.find_all('a')
    for a in a_tag:
        url_list.append([a.get_text(),a.get('href')])
    return td_list,url_list
def td_dict_write(td_list,th_dict,i,count_column):
    try:
        if count_column[i] == count_column[i-1]:
            temp_dict = dict(th_dict)
            if len(td_list)+1 == len(th_dict):
                a= 0
                for key in temp_dict:
                    if key != 'url-list':
                        temp_dict[key] = td_list[a]
                        a += 1
                sdk_dict_td = dict(temp_dict)
                return sdk_dict_td
            else:
                return {}
    except:
        return False
    return {}
def table_headers_thead(thead):
    th_list = []
    tds = thead.find_all(['td', 'th'])
    if tds:
        for td in tds:
            th_list.append(td.get_text())
    return th_list
def table_handle_no_rowspan(table):     # 看这里
    table_dict_list = []
    rows = table.find_all('tr')
    count_column, aver = count_row_column(rows)
    thead_flag = 0
    th_list = []
    for i in range(0, len(rows)):
        sdk_dict = {}
        if thead_flag == 0:
            thead = table.find('thead')
            if thead:
                th_list = table_headers_thead(thead)
                thead_flag = 1
            else:
                thead_flag = -1
        if thead_flag == -1:
            if 'false_colspan' in th_list:
                # 表示发生了列合并，则该行不写，并且下一行作为新表头？这里有个问题是，我记得有的是中间断开了，但是并没有产生新的表
                th_list = table_headers_find(rows[i], i, count_column,false_colspan=True)# 该行为合并列行
            else:
                th_list = table_headers_find(rows[i], i, count_column)
        # if th_list and 'colspan' not in th_list and 'false_colspan' not in th_list:   #不知道是什么意思，先注释掉
        if th_list:
            for th in th_list:
                sdk_dict[th] = None
            sdk_dict['url-list'] = None
            if len(sdk_dict) > 1:  # 防止合并列的情况
                #生成字典列表  llm消息格式转化的参考
                table_dict_list.append(dict(sdk_dict))
                th_list = []
            else:
                print("表头只有一个值")
        else:
            if len(table_dict_list) > 0:
                td_list, url_list = table_td_extract(rows[i])

                # 这一段也先注释掉
                # 增加新的行的数据的判断，防止出现列合并，但colspan判断失败的现象
                # if td_list and len(list(set(td_list)))<len(td_list):
                #     th_list = ['false_colspan'] #发生了列合并
                #     continue

                # 找到最近的表头
                nearly_th_dict = find_th_dict(table_dict_list, aver)
                if len(nearly_th_dict) == 0:
                    nearly_th_dict = table_dict_list[0]
                sdk_dict_temp = td_dict_write(td_list, nearly_th_dict, i, count_column)
                if url_list:
                    sdk_dict_temp['url-list'] = url_list
                if sdk_dict_temp:
                    table_dict_list.append(dict(sdk_dict_temp))
                #else:
                 #   print("写入行数据失败")
    return table_dict_list

def table_handle_rowspan(table):   # 改了参数列表
    table_dict_list_row = []

    # print("修改前的table是：" + str(table))

  #  soup = BeautifulSoup(table, 'html.parser')

    if table:
        rows = table.find_all('tr')

        # rowspan_begin_index = 0
        rowspan_begin_index_list = []   # 开始行合并的行索引

        # rowspan_num = 0
        rowspan_num_list = []

        # rowspan_cell_index = 0   # 发生行合并也就是要插入新单元格的索引(在一行内的索引,列索引)
        rowspan_cell_index_list = []

        # rowspan_text = ''
        rowspan_text_list = []

        for row_index, row in enumerate(rows):   # 每一行

            if len(rowspan_begin_index_list) == 0:   # 还没有发生过行合并，还在等待第一个行合并的出现
                cells = row.find_all(['td', 'th'])  # 一行里的每个单元格
                for cell_index, cell in enumerate(cells):  # 如果该值大于1，则表明发生行合并

                    if 'rowspan' in cell.attrs:
                        try:
                            if int(cell.attrs['rowspan']) < 2:
                                continue
                            else:
                                # 检查是不是第一次检测到这一列的行合并现象
                                rowspan_cell_index = cell_index  # 发生合并的列索引
                                flag = 0
                                inserted_index = 0

                                # 合并的列索引插入列索引列表
                                if rowspan_cell_index in rowspan_cell_index_list:  # 值已经存在于列表中
                                    flag = 1
                                    inserted_index = rowspan_cell_index_list.index(rowspan_cell_index)
                                    # 值已经存在于列表中，获得索引，后面就是更新操作而不是插入操作了
                                    # print("值已经存在于列表中，索引为:", index)
                                else:
                                    # 值不存在于列表中，将其插入列表
                                    rowspan_cell_index_list.append(rowspan_cell_index)
                                    # print("值已插入到列表中")
                                # rowspan_cell_index_list.append(rowspan_cell_index)

                                rowspan_begin_index = row_index  # 开始合并(也就是当前的行索引)
                                if flag:  # 值已经存在于列表中
                                    rowspan_begin_index_list[inserted_index] = rowspan_begin_index

                                else:
                                    rowspan_begin_index_list.append(rowspan_begin_index)

                                rowspan_num = int(cell.attrs['rowspan'])  # 合并了的行数
                                if flag:  # 值已经存在于列表中
                                    rowspan_num_list[inserted_index] = rowspan_num

                                else:
                                    rowspan_num_list.append(rowspan_num)

                                # rowspan_num_list.append(rowspan_num)

                                if cell:
                                    rowspan_text = cell.get_text()  # 合并的内容
                                    if flag:  # 值已经存在于列表中
                                        rowspan_text_list[inserted_index] = rowspan_text

                                    else:
                                        rowspan_text_list.append(rowspan_text)

                                    # rowspan_text_list.append(rowspan_text)

                                del cell['rowspan']

                                # 如果有colspan也删一下
                                if cell.has_attr('colspan'):
                                    del cell['colspan']
                        except:
                            continue

            else:
                for rowspan_begin_index_list_index, rowspan_begin_index in enumerate(rowspan_begin_index_list):   # 检查这一行里有没有哪一列在合并范围里

                    if rowspan_begin_index < row_index < int(rowspan_begin_index) + int(rowspan_num_list[rowspan_begin_index_list_index]):
                        # 创建一个新的<td>标签
                        new_cell = Tag(name='td')
                        new_cell.string = rowspan_text_list[rowspan_begin_index_list_index]   # 要插入新单元格的内容

                        # 在指定位置插入新的<td>标签
                        cells = row.find_all('td')    # cells是一行内的每个单元格

                        rowspan_cell_index = rowspan_cell_index_list[rowspan_begin_index_list_index]
                        if rowspan_cell_index < len(cells):
                            cells[rowspan_cell_index].insert_before(new_cell)
                        else:
                            row.append(new_cell)

                    else:   # 新的行合并的开始
                        cells = row.find_all(['td', 'th'])     # 一行里的每个单元格
                        for cell_index, cell in enumerate(cells):#如果该值大于1，则表明发生行合并

                            if 'rowspan' in cell.attrs:
                                try:
                                    if int(cell.attrs['rowspan'])<2:
                                        continue
                                    else:
                                        # 检查是不是第一次检测到这一列的行合并现象
                                        rowspan_cell_index = cell_index       # 发生合并的列索引
                                        flag = 0
                                        inserted_index = 0

                                        # 合并的列索引插入列索引列表
                                        if rowspan_cell_index in rowspan_cell_index_list: # 值已经存在于列表中
                                            flag = 1
                                            inserted_index = rowspan_cell_index_list.index(rowspan_cell_index)
                                            # 值已经存在于列表中，获得索引，后面就是更新操作而不是插入操作了
                                            # print("值已经存在于列表中，索引为:", index)
                                        else:
                                            # 值不存在于列表中，将其插入列表
                                            rowspan_cell_index_list.append(rowspan_cell_index)
                                            # print("值已插入到列表中")
                                        # rowspan_cell_index_list.append(rowspan_cell_index)


                                        rowspan_begin_index = row_index        # 开始合并(也就是当前的行索引)
                                        if flag: # 值已经存在于列表中
                                            rowspan_begin_index_list[inserted_index] = rowspan_begin_index

                                        else:
                                            rowspan_begin_index_list.append(rowspan_begin_index)



                                        rowspan_num = int(cell.attrs['rowspan'])   # 合并了的行数
                                        if flag: # 值已经存在于列表中
                                            rowspan_num_list[inserted_index] = rowspan_num

                                        else:
                                            rowspan_num_list.append(rowspan_num)

                                        # rowspan_num_list.append(rowspan_num)



                                        if cell:
                                            rowspan_text = cell.get_text()   # 合并的内容
                                            if flag:  # 值已经存在于列表中
                                                rowspan_text_list[inserted_index] = rowspan_text

                                            else:
                                                rowspan_text_list.append(rowspan_text)


                                            # rowspan_text_list.append(rowspan_text)

                                        del cell['rowspan']
                                        # 如果有colspan也删一下
                                        if cell.has_attr('colspan'):
                                            del cell['colspan']
                                except:
                                    continue

    print("修改后的table是：" + str(table))
#    return table_dict_list_row
    return table

def tables_handle(soup):
    '''
    :param soup: 待处理页面
    :return: 字典列表
    '''
    all_table_dict_list = []
    rowspan_count = 0
    tables = soup.find_all('table')
    if tables:
        print("len(tables)=", str(len(tables)))
        for table in tables:

            # judge_result, row_index, cell_index = rowspan_judge(table)    # 改了返回值
            # 检查是不是关于SDK的内容
            flag = 0
            #     flag = 1
            head_rows = []
            rows = []

            # 暂时注释掉判断的模块
            try:  # 表头
                head_rows = table.find_all('tr')
                rows = table.find_all('tr')
            except:
                pass

            for head_row in head_rows:
                if flag:
                    break
                cells = head_row.find_all('th')
                if cells:
                    for cell in cells:
                        if flag:
                            break
                        text = cell.get_text()
                        if 'SDK' in text or '第三方' in text or '合作' in text:
                            # 找到目标字样，执行相应的操作
                            flag = 1
                            break
                else:
                    break


            if flag == 0:
                for row in rows:
                    if flag:
                        break
                    cells = row.find_all('td')
                    for cell in cells:
                        if flag:
                            break
                        text = cell.get_text()
                        if 'SDK' in text or '第三方' in text or '合作' in text:
                            # 找到目标字样，执行相应的操作
                            flag = 1
                            break


            if flag:
                # 判断并简单地删除列合并
                for row_index, row in enumerate(rows):
                    cells = row.find_all(['td', 'th'])  # 一行里的每个单元格
                    for cell_index, cell in enumerate(cells):  # 如果该值大于1，则表明发生行合并
                        if 'colspan' in cell.attrs:  # 暂时处理一下列合并(粗暴地删除这一行
                            colspan = int(cell.attrs['colspan'])
                            if colspan > 1:
                                row.extract()    # 删除整行

                v = 0
                v = rowspan_judge(table)
                if v:
                # if rowspan_judge(table):  # 判断是否有行合并
                    print("存在行合并")
                    rowspan_count += 1
                    table = table_handle_rowspan(table)
                else:
                    print("不存在行合并")

                temp_n_ro = table_handle_no_rowspan(table)[:]
                print("temp_n_ro=", str(temp_n_ro))
                all_table_dict_list.extend(temp_n_ro)

    return all_table_dict_list, rowspan_count
def find_a_tag(child):
    if isinstance(child,bs4.element.Tag):
        link_list =[]
        a_tags = child.find_all('a')
        for a in a_tags:
            try:
                temp_url = a['href']
                if is_valid_url(temp_url):
                    link_list.append(a['href'])
                elif is_valid_url(a.get_text()):
                    link_list.append(a.get_text())
            except:
                continue
        return link_list
    return False
def display_text_extract2(display_bs_point):
    display_list = []
    all_display_list = []
    for child in display_bs_point:
        temp_a_link = find_a_tag(child)
        if temp_a_link:
            try:
                for i in child:
                    temp_text = text_format(i.get_text())
                    if temp_text:
                        display_list.append(temp_text)
                display_list.append({'url': temp_a_link})
                all_display_list.append(display_list)
                display_list = []
            except:
                display_list.append(child.get_text())
                display_list.append({'url': temp_a_link})
                all_display_list.append(display_list)
                display_list = []
    return all_display_list
def point_text(child):
    result = []
    sdk_url_list = find_a_tag(child)
    if sdk_url_list:
        result.append({'url': sdk_url_list})
    if child.name == 'ul':
        for li in child:
            result.append(text_format(li.get_text()))
        return result
    return []     # 为什么如果不是ul就要清空  (如果是普通节点的话最后就会返回空，因为两个分支都进不去)
def display_text_extract(display_bs_point):
    '''
    :param display_bs_point: 包含所有display的父节点
    :return:
    '''
    # 这段代码的作用是遍历节点，提取文本信息并组织成列表返回。同时，还处理了一些特定条件下的情况，例如空文本、超长文本等。
    display_list = []
    all_display_list = []
    flag = 0
    flag2 = 0
    if display_bs_point:
        for child in display_bs_point:
            temp_text = text_format(child.get_text())
            if temp_text and flag:
                temp_list = point_text(child)
                if temp_list:
                    display_list.extend(temp_list)
                    all_display_list.append(display_list[:])
                    display_list = []
                else:
                    sdk_url_list = find_a_tag(child)
                    if sdk_url_list:
                        display_list.append({'url':sdk_url_list})
                    display_list.append(temp_text)
            elif temp_text == '':
                if child.name:
                    flag = 1#找到第一个空位
                    if display_list:
                        all_display_list.append(display_list[:])
                        display_list = []
            elif len(display_list) > 30:
                flag2 = 1
    #if flag2 and display_bs_point:
     #   print("切割存在问题！")
    if len(all_display_list) ==0:
        all_display_list = display_text_extract2(display_bs_point)
    return all_display_list
def find_parent_with_most_children(soup):
    max_child_count = 0
    parent_with_most_children = None

    def traverse(node):
        nonlocal max_child_count, parent_with_most_children
        if len(node.contents) > max_child_count:
            max_child_count = len(node.contents)
            parent_with_most_children = node
        for child in node.contents:
            if child.name is not None:
                traverse(child)
    traverse(soup)
    return parent_with_most_children
def positioning_display_div(soup):
    '''
    :param soup: sdk页面soup
    :return: 返回包含display声明的bs节点
    '''
    display_bs_point = find_parent_with_most_children(soup)
    if display_bs_point:
        return display_bs_point
    return False    # bs就是beautifulsoup
def sdk_title_judge(text):
    '''
    :param text: 待判定为描述sdk的短文本
    :return: 如果是描述sdk则返回True，否则返回False
    '''
    key_word = ["第三方","sdk","共享","合作","运营","关联"]
    #小写处理
    text = text.lower()
    if check_elements(text,key_word,0,6):
        return True
    return False
def rule_cut(s):
    delimiters = ["：",":"]
    result = {}
    for delimiter in delimiters:
        if delimiter in s:
            split_list = s.split(delimiter)
            if len(split_list)==2:
                result[split_list[0]] = split_list[1]
            elif len(split_list)>2:
                result[split_list[0]] = "".join(split_list[1:])
            break
    if result =={}:
        result['text'] = s
    return result
def has_url_dict(lst,string = None):
    '''
    :param lst: 列表
    :param string: 字典键
    :return: 如果列表中包含string为键的字典，返回该字典元素
    '''
    if string == None:
        string = 'url'
    for item in lst:
        if isinstance(item, dict) and string in item:
            return item
    return False
def display_list_change_dictlist(display_list):
    '''
    :param display_list: 保存陈述的二维列表
    :return:
    '''
    display_dict_list = []
    display_dict = {}
    judge_sentence = ['我们','。',',','我','，']
    for display in display_list:
        judge_count = 0
        for i in range(0,len(display)):#这里假定已经切割好了
            if check_elements(display[i],judge_sentence,3):#判断是否为正式句子而非陈列形式。
                judge_count +=1
            if judge_count>len(display)//2-1:
                display_dict = {}
                break
            else:
                if i ==0:
                    display_dict['name'] = display[i]
                elif isinstance(display[i],dict):
                    continue
                else:#按照规则切割，没有对应规则的键为’text'：
                    temp_dict = rule_cut(display[i])
                    if isinstance(temp_dict,dict) and temp_dict:
                        display_dict.update(dict(temp_dict))
        temp_item = has_url_dict(display)
        if temp_item:
            display_dict['url'] = temp_item['url'][:]
        if display_dict:
            display_dict_list.append(dict(display_dict))
            display_dict = {}
    return display_dict_list
def remove_duplicates(lst):
    '''
    :param lst: 字典列表
    :return: 去掉重复键'url'的字典
    '''
    unique_lst = []
    urls = set()
    for d in lst:
        if d.get('url') not in urls:
            urls.add(d.get('url'))
            unique_lst.append(d)
    return unique_lst

def remove_duplicates_list(list):
    '''

    :param list: 待去重的列表
    :return: 去重后的列表
    '''
    # 以下是去重，因为发现解析第一方页面的结果会重复很多次
    # 创建一个空集合
    unique_table_dict_set = set()

    # 遍历final_result['table-result']中的每个字典
    temp = list

    # 遍历temp中的每个字典
    for table_dict in temp:
        # print("type of table_dict:" + str(type(table_dict)))

        # 将字典转换为不可变的哈希值（hashable）元组
        table_tuple = tuple(table_dict.items())

        # 将哈希值元组添加到集合中
        try:
            unique_table_dict_set.add(table_tuple)
        except Exception as e:
            print("将哈希值元组添加到集合中的异常:" + str(e))

            return list   # 现在还不清楚这个异常是什么，所以先直接把原列表返回好了(目测已经找到了为什么会重复好几个表的原因)
            # print(e)
            continue

    # 将集合转换回列表
    unique_table_dict_list = [dict(table_tuple) for table_tuple in unique_table_dict_set]

    # 将去重后的列表返回
    return unique_table_dict_list

def relative_url_judge(base_url,relative_url):
    try:
        parsed_href = urlparse(relative_url)
        if not parsed_href.scheme:
            absolute_url = urljoin(base_url, relative_url)
        #print("相对路径")
            return absolute_url
        else:
            return relative_url
        #print("绝对路径")
    except:
        return relative_url

def sdk_link_judge(url,links):
    '''
    :param links: 标记为超链接的节点列表
    :return: 判定为sdk描述链接的列表
    '''
    url_dict = {'description':None,'url':None,'soup':None,'table-result':None,'display-result':None}
    sdk_word_url_dict_list = []
    for link in links:
        son_url = None
        if url!=None:
            son_url = relative_url_judge(url, link.get('href'))
        if son_url ==None:
            son_url = link.get('href')    # 获取链接
        if is_valid_url(son_url):
            title = link.get_text()
            # 通过链接的名字判断是不是，如果能判断，则
            if sdk_title_judge(title):
                url_dict['description'] = title
                url_dict['url'] = son_url
                temp = dict(url_dict)
                sdk_word_url_dict_list.append(temp)
            else:
                parent_tag = link.parent
                # 通过父节点中对链接的描述判断
                temp_p =parent_tag.get_text()
                if len(parent_tag.get_text())<45:
                    if sdk_title_judge(parent_tag.get_text()):
                        url_dict['description'] = parent_tag.get_text()
                        url_dict['url'] = son_url
                        temp = dict(url_dict)
                        sdk_word_url_dict_list.append(temp)
    sdk_word_url_dict_list = remove_duplicates(sdk_word_url_dict_list)
    #如果description与url相等，那么如果列表长度大于2，则删除该元素
    for d in sdk_word_url_dict_list:
        try:
            if d['description'] == d['url'] and len(sdk_word_url_dict_list)>1:
                sdk_word_url_dict_list.remove(d)
        except Exception as e:
            print(e)
    return sdk_word_url_dict_list
def sdk_soup_judge(links):
    '''
    :param links: 标记为超链接的节点列表
    :return: 判定为sdk描述页面soup的列表
    '''
    url_dict = {'description': None, 'url': None,'soup':None,'table-result':None,'display-result':None}
    url_list = []
    sdk_url_soup_dict_list = []
    key_word = ["第三方","sdk","共享","合作","运营","关联"]
    for link in links:
        if is_valid_url(link.get('href')):
            url_list.append(link.get('href'))
    if url_list:
        for url in url_list:
            if url == 'https://terms.alicdn.com/legal-agreement/terms/suit_bu1_other/suit_bu1_other202112201639_51546.html':
                print(url)
            try:
                soup = driver.get_privacypolicy_html(url)
                if soup:
                    temp = soup.get_text()
                    if check_elements(temp,key_word):
                        if "权限列表" in temp and "安卓" in temp:
                            continue
                        #增加一个不是隐私政策页面，也不是权限列表页面
                        if temp.count("儿童")>3:
                            continue
                        else:
                            url_dict['url'] = url
                            url_dict['soup'] = soup
                            sdk_url_soup_dict_list.append(dict(url_dict))
            except Exception as e:
                print(e)
    return sdk_url_soup_dict_list
def display_handle(soup):
    display_dict_list = []
    display_bs_point = positioning_display_div(soup)        # 找到最多子节点的父节点
    display_list = display_text_extract(display_bs_point)
    if display_list:
        display_dict_list = display_list_change_dictlist(display_list)
    return display_dict_list

'''llm解析'''
def display_handle_llm(soup, ext):
    '''
    :param soup: sdk陈述页面soup
    :return: 返回该页面表格提取字典列表
    '''
    # print("soup=" + str(soup))
    text = soup.get_text(separator="\n")
    # print("text=" + str(text))
    print("传到display_handle_llm里的text:", text)
    result = single_txt_temp(text, ext)

    return result

def run_table_handle(url=None,soup = None):
    '''
    :param url: sdk声明链接
    :param soup: sdk声明页面soup
    :return: 返回该页面表格提取字典列表
    '''
    table_dict_list_result = []
    if soup == None:
        soup = driver.get_privacypolicy_html(url)
        # table_soup = sdk_dict['soup']
        flag = 0
        while True:
            if soup or flag == 3:
                # print("flag==", str(flag))
                soup = link_addtext(soup)
                # print("读取到的soup==", str(soup))
                break
            else:
                soup = driver.get_privacypolicy_html(url)
                flag = flag + 1

    if soup:
        table_dict_list_result, rowspan_count = tables_handle(soup)
    #for i in table_dict_list_result:
     #   print(i)
    #if rowspan_count>0:
     #   print("行合并表格数："+str(rowspan_count))
    return table_dict_list_result
def run_display_handle(url=None,soup = None):
    display_dict_list_result = []
    ext = 1
    if soup == None:  # 说明是外链接陈述
       ext = 0
       try:
           soup = driver.get_privacypolicy_html(url)
           print("读取" + str(url) + "成功！")

           flag = 0
           while True:
               if soup or flag == 3:
                   print("flag==", str(flag))
                   print("读取到的soup==", str(soup))
                   break
               else:
                   soup = driver.get_privacypolicy_html(url)
                   flag = flag + 1

       except Exception as e:
            print("试图读取" + str(url) + "失败！")
            # print(e)

    if soup:
       # display_dict_list_result = display_handle(soup)     # 节点解析

       # url = "https://finance.sina.cn/app/SFASDKlist.shtml"
       # print("到run_display_handle")
       # soup = driver.get_privacypolicy_html(url)
       soup = link_addtext(soup)
       print("display_handle_llm")
       print("传到display_handle_llm里的soup:", soup)
       display_dict_list_result = display_handle_llm(soup, ext)   # llm解析

    #for i in display_dict_list_result:
     #   print(i)
    return display_dict_list_result

def run_sdk_link_judge(url=None,soup = None):
    '''
    :param soup: 隐私政策soup文件
    :return: 判定为sdk子链接的soup文件列表
    '''

    sdk_dict_list = []

    if soup == None:
        soup = driver.get_privacypolicy_html(url)

    if soup:
        links = soup.find_all('a')

        sdk_dict_list = sdk_link_judge(url, links)
        try:
            if sdk_dict_list:#从原页面链接描述判定
                for d in sdk_dict_list:
                    sdk_soup = driver.get_privacypolicy_html(d['url'])
                    if sdk_soup:
                        d['soup'] = sdk_soup
            else:
            #从子页面文本描述判定
                sdk_dict_list.extend(sdk_soup_judge(links))
        except Exception as e:
            print(e)
        return sdk_dict_list

link_result = []

def link_addtext(soup):   # 将sdk声明的"点击查看"这种变一下
    # 遍历所有的超链接节点
    # print("对点击查看进行处理")

    try:
        for link in soup.find_all('a'):
            # 获取超链接的显示文本和链接地址
            link_text = link.get_text()
            link_url = link['href']

            # 判断显示文本与链接地址是否不一致
            if link_text != link_url:
                # 构造新的显示文本
                new_link_text = f"{link_text}({link_url})"

                # 替换超链接的显示文本
                link.string.replace_with(new_link_text)
    except Exception as e:
        print("对点击查看进行处理的异常:", str(e))

    return soup


def run_SDK_analysis(url = None,soup = None):
    '''
    :param url: 隐私政策链接
    :param soup: 隐私政策页面soup
    :return: 返回sdk字典形式列表
    '''
    final_result = {'sdk-url-list':[],'table-result-len':None,'table-url':[],'table-result':[],'display-result-len':None,'display-url':[],'display-result':[],'false-url':[]}
    if soup == None:
        soup = driver.get_privacypolicy_html(url)
    if soup:#隐私政策链接
        sdk_dict_list = run_sdk_link_judge(url, soup)           # 拿到SDK描述链接的列表
        # print("sdk_dict_list = ")
        # for link in sdk_dict_list:
        #     print(link)
        sdk_dict_list = remove_duplicates(sdk_dict_list)
        # sdk_dict_list = remove_duplicates_list(sdk_dict_list)
        if sdk_dict_list:#判断有无sdk子链接(也就是说SDK描述链接的列表有可能是空的，不是说接下来开始判断是不是子链接的意思)  有子链接的话：
            for sdk_dict in sdk_dict_list:
                try:
                    final_result["sdk-url-list"].append({'description':sdk_dict['description'],'url':sdk_dict['url']})
                except:
                    final_result["sdk-url-list"].append({'description':None, 'url': sdk_dict['url']})
                    # table处理
                try:
                    # print(sdk_dict['url'])
                    # table_soup = None
                    # if sdk_dict['soup']:
                    #     table_soup = sdk_dict['soup']
                    #     table_soup = link_addtext(table_soup)
                    # print("table_soup=", str(table_soup))
                    table_dict_list = run_table_handle(url = sdk_dict['url'],soup = None)#解析子链接soup文件：表格解析
                    # print("table_dict_list = ", str(table_dict_list))

                    if table_dict_list:
                        try:
                            final_result['table-url'].append({'description':sdk_dict['description'],'url':sdk_dict['url']})
                        except:
                            final_result['table-url'].append({'description':None, 'url': sdk_dict['url']})

                        final_result['table-result'].extend(table_dict_list)
                        # 去重，先注释掉
                        # list = final_result['table-result']
                        # final_result['table-result'] = remove_duplicates_list(list)

                    else:# 不是，则判断是否为陈列形式
                        # display_dict_list = run_display_handle(url = url,soup = sdk_dict['soup'])

                        display_dict_list = run_display_handle(url=sdk_dict['url'], soup=None)

                        # print("display_dict_list的类型是：" + str(type(display_dict_list)))
                        if display_dict_list:
                            try:
                                final_result['display-url'].append({'description':sdk_dict['description'],'url':sdk_dict['url']})
                            except:
                                final_result['display-url'].append({'description':None, 'url': sdk_dict['url']})

                            final_result['display-result'].extend(display_dict_list)
                            list = final_result['display-result']
                            final_result['display-result'] = remove_duplicates_list(list)

                        else:
                            # 返回的陈述解析结果是空的(也可能是URL读不了)
                            try:
                                final_result['false-url'].append({'description':sdk_dict['description'],'url':sdk_dict['url']})
                            except:
                                final_result['false-url'].append({'description':None, 'url': sdk_dict['url']})

                except Exception as e:
                    print(e)

        try: #无sdk子链接    没有appendNone，URL的value留空
            #llm模块
            # 把这个第一方页面接上llm
            # soup = driver.get_privacypolicy_html(url)
            table_dict_list = run_table_handle(url=url, soup=soup)  # 解析第一方soup文件：表格解析
            if table_dict_list:

                # 以下是去重，因为发现解析第一方页面的结果会重复很多次
                # 创建一个空集合
                # unique_table_dict_set = set()
                #
                # # 遍历final_result['table-result']中的每个字典
                # temp = final_result['table-result']
                #
                # for pre in temp:
                #     print("type of pre:" + str(type(pre)))
                #     # 将字典转换为不可变的哈希值（hashable）元组
                #     pre_tuple = tuple(pre.items())
                #
                #     # 将哈希值元组添加到集合中
                #     unique_table_dict_set.add(pre_tuple)
                #
                # # 遍历table_dict_list中的每个字典
                # for table_dict in table_dict_list:
                #     print("type of table_dict:" + str(type(table_dict)))
                #
                #     # 将字典转换为不可变的哈希值（hashable）元组
                #     table_tuple = tuple(table_dict.items())
                #
                #     # 将哈希值元组添加到集合中
                #     try:
                #         unique_table_dict_set.add(table_tuple)
                #     except Exception as e:
                #         print("将哈希值元组添加到集合中的异常:" + str(e))
                #         # print(e)
                #         continue
                #
                # # 将集合转换回列表
                # unique_table_dict_list = [dict(table_tuple) for table_tuple in unique_table_dict_set]
                #
                # # 将去重后的列表赋值给final_result['table-result']
                # final_result['table-result'] = unique_table_dict_list

                final_result['table-result'].extend(table_dict_list)

            display_dict_list_result = run_display_handle(url=None, soup=soup) # 进行第一方解析
            # display_dict_list_result = display_handle_llm(soup)  # llm进行第一方解析

            if display_dict_list_result:
                final_result['display-result'].extend(display_dict_list_result)
                list = final_result['display-result']
                final_result['display-result'] = remove_duplicates_list(list)

            print("直接解析第一方页面！")

        except Exception as e:
            print("解析第一方页面时异常：")
            print(e)

    else:
        print("隐私政策sdk分析失败！错误链接")

    final_result['table-result-len'] = len(final_result['table-result'])
    final_result['display-result-len'] = len(final_result['display-result'])

    return final_result
if __name__ == '__main__':
    '''
    start_time = time.time()
    random_50()
    end_time = time.time()
    total_time = end_time - start_time
    print("程序运行时间：", total_time, "秒") '''
    #单个隐私政策提取sdk调试
    test_url = 'https://www.jiguang.cn/license/privacy'    # 极光
#    test_url = 'https://docs.getui.com/privacy/'  # 个推   没有识别出来
#    test_url = 'https://www.mob.com/about/policy'  # 秒验SDK(MobTech)
#     test_url = 'https://www.umeng.com/page/policy'  # 友盟
#    result = run_SDK_analysis(url ='https://terms.alicdn.com/legal-agreement/terms/suit_bu1_alibaba_hema/suit_bu1_alibaba_hema202203300948_54070.html?spm=hemdefault.11124225.6429453315.1')

    test_html_folder_path = '../../../data/data_privacy_html/'
    test_path = 'cn.com.yunma.school.app_5.2.4_524_policy.html'  # 易校园 本地路径
    test_path = 'cn.com.sina.finance_6.25.0.1_878_policy.html'  # 北京新浪财经 本地路径
    # file_path = 'temp_sdk_result/yixiaoyuan.json'
    # file_path = 'temp_sdk_result/caijing.json'

    result_json_path = test_path.rsplit('.', 1)[0] + '_test.json'

    test_path = test_html_folder_path + test_path


    result_json_folder_name = '../data/data_privacy_html_result_json'


    if not os.path.exists(result_json_folder_name):
        os.makedirs(result_json_folder_name)

    result_json_path = os.path.join(result_json_folder_name, result_json_path)

    with open(test_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    result = run_SDK_analysis(url=None, soup=soup)

    # write_to_json(result, result_json_path)

    # 检查文件是否存在
    if not os.path.exists(result_json_path):
        # 创建一个空的JSON对象
        empty_json = {}

        # 打开文件并写入空的JSON内容
        with open(result_json_path, 'x', encoding='utf-8') as file:
            json.dump(empty_json, file, ensure_ascii=False, indent=2)

    with open(result_json_path,'w',encoding='utf-8')as f:
        json.dump(result,f,ensure_ascii=False,indent=2)#盒马漏掉了一个sdk链接，陈列形式的。

    f.close()


  #  url = 'https://www.jiguang.cn/license/accessPartner'
    # 隐私政策sdk子链接提取：
   # run_sdk_link_judge(url, soup=None)
   # table_dict_list = run_table_handle(url=url, soup=None)  # 解析子链接soup文件：表格解析