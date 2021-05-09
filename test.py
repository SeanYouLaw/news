#   coding=utf-8
from stanfordcorenlp import StanfordCoreNLP
import json

class StanfordNLP:
    def __init__(self, host='https://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=15000)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'zh',
            'outputFormat': 'json'
        }

    def __init__(self):
        self.nlp = StanfordCoreNLP(r'D:\study 2021(1)\数据新闻\stanfordcorenlp\stanford-corenlp-full-2018-10-05', lang='zh')   # , lang='zh' , quiet=False, logging_level=logging.DEBUG)

        self.props = {
            'annotators': 'tokenize,ssplit,pos',
            'pipelineLanguage': 'zh',
            'outputFormat': 'json'
        }


    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))


def Print(list1, list2):
    max = len(list2)
    for item in list1:
        m = item[1]
        n = item[2]
        if m < max and n < max:
            a = item[0] + " : " + list2[m-1] + " | " + list2[n-1]
            print(a)
    return 0


if __name__ == '__main__':
    sNLP = StanfordNLP()

    title = '距“限行”不到1小时！印度超级富豪花近百万元飞英国'
    content = '当地时间25日，印度报告新增新冠肺炎确诊病例接近35万例，再创新高。印度政府当天表示，预计这一波新冠疫情可能将于5月中旬达到峰值，届时印度每天新增确诊病例可能将高达50万例。面对持续涌入的病人，印度多个城市的医疗系统已不堪重负、接近崩溃的边缘。有印度医生说，这波疫情就像是一场海啸，冲垮了印度的医疗系统，而由于缺乏有效应对，印度疫情最糟糕的时候“恐怕还远还没有到来。'
    print("标题：", title)
    print("初始：", content)

    sentence = content

    print('\n分词:')
    title_lst = sNLP.word_tokenize(title)
    word_lst = sNLP.word_tokenize(sentence)
    print("  ".join(str(x) for x in title_lst))
    print("  ".join(str(x) for x in word_lst))



    #print('\n词性标注:')
    title_pos_lst = sNLP.pos(title)
    pos_lst = sNLP.pos(sentence)
    #print(title_pos_lst)
    #print(pos_lst)



    # 基于词汇重复确认词汇链
    print('\n词汇链：')
    total_pos_lst = title_pos_lst + pos_lst
    cword_lst = []
    #获取去除标点的所有分得词语
    for i in total_pos_lst:
        if i[1] == 'NR' or i[1] == 'NN' or i[1] == 'VV' or i[1] == 'JJ':
            cword_lst.append(i[0])

    set1 = set(cword_lst)
    dict = {}
    for item in set1:
        dict.update({item:cword_lst.count(item)})
    dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    for i in range(5):
        print(dict[i][0], end='  ')
    print('\n')



    #基于词性标注获得长NP
    print('NP:')
    npcnt = len(title_pos_lst) - 1
    npi = 0
    np_lst = []
    while npi <= npcnt:
            npstr = ''
            while npi <= npcnt:
                if title_pos_lst[npi][1] == 'NR' or title_pos_lst[npi][1] == 'NN' or title_pos_lst[npi][1] == 'JJ':
                    npstr = npstr + title_pos_lst[npi][0]
                    npi = npi + 1
                else:
                    npi = npi + 1
                    break
            if npstr != '':
                np_lst.append(npstr)

    npcnt = len(pos_lst) - 1
    npi = 0
    while(npi <= npcnt):
            npstr = ''
            while(npi <= npcnt):
                if pos_lst[npi][1] == 'NR' or pos_lst[npi][1] == 'NN' or pos_lst[npi][1] == 'JJ':   #or pos_lst[npi][1] =='DEG'
                    npstr = npstr + pos_lst[npi][0]
                    npi = npi + 1
                else:
                    npi = npi + 1
                    break
            if npstr != '':
                np_lst.append(npstr)

    print("  ".join(np_lst))



    #最长np
    print('\n最长NP：')
    setnp = set(np_lst)
    dictnp = {}
    for item in setnp:
        dictnp.update({item:len(item)})
    dictnp = sorted(dictnp.items(), key=lambda d: d[1], reverse=True)

    npi = 0
    print(dictnp[npi][0], end='  ')
    while(1):
        npi = npi + 1
        if dictnp[npi][1] == dictnp[npi - 1][1]:
            print(dictnp[npi][0], end='  ')
        else:
            break
    print(' ')



    #print('\n命名实体识别:')
    ner_lst = sNLP.ner(sentence)
    #print(ner_lst)

    #抽取人名，地名，组织名、时间要素
    print('\n要素识别:')
    print('人名',end=': ')
    person_lst = []
    for item in ner_lst:
        if item[1] == 'PERSON':
            person_lst.append(item[0])
    setp = set(person_lst)
    print("、".join(str(x) for x in setp))

    print('地名', end=': ')
    location_lst = []
    for item in ner_lst:
        if item[1] == 'CITY' or item[1] == 'COUNTRY' or item[1] == 'LOCATION' or item[1] == 'GPE':
            location_lst.append(item[0])
    setl = set(location_lst)
    print("、".join(str(x) for x in setl))

    print('组织名', end=': ')
    orgna_lst = []
    for item in ner_lst:
        if item[1] == 'ORGANIZATION':
            orgna_lst.append(item[0])
    seto = set(orgna_lst)
    print("、".join(str(x) for x in seto))

    print('时间', end=': ')
    time_lst = []
    for item in ner_lst:
        if item[1] == 'DATE':
            time_lst.append(item[0])
    sett = set(time_lst)
    print("、".join(str(x) for x in sett))



    #print('\n句法分析:')
    #parse_lst = sNLP.parse(sentence)




    #“后”是“前”的什么角色
    #print('\n依存关系分析:')
    dependency_parse_lst = sNLP.dependency_parse(sentence)
    title_dependency_parse_lst = sNLP.dependency_parse(title)
    #Print(title_dependency_parse_lst, title_lst)
    #Print(dependency_parse_lst, word_lst)



    #根据标题依存关系，分析主要事件链
    print('\n主要事件链:')
    re = []
    for i in title_dependency_parse_lst:
        if i[0] == 'nsubj':
            dobj_word = ''
            nn_word = ''
            assmod_word = ''
            ccomp_word = ''
            for k in title_dependency_parse_lst:
                if k[0] == 'dobj' and k[1] == i[1]:
                    dobj_word = ' ' + title_lst[k[2]-1]
            for k1 in title_dependency_parse_lst:
                if k1[0] == 'compound:nn' and k1[1] == i[2]:
                    nn_word = ' ' + title_lst[k1[2]-1]
            for k2 in title_dependency_parse_lst:
                if k2[0] == 'nmod:assmod' and k2[1] == i[2]:
                    assmod_word = ' ' + title_lst[k2[2]-1]
            for k3 in title_dependency_parse_lst:
                if k3[0] == 'ccomp' and k3[1] == i[1]:
                    ccomp_word = ' ' + title_lst[k3[2]-1]
            sstr = assmod_word + nn_word + title_lst[i[2]-1] + ' ' + title_lst[i[1]-1] + dobj_word + ccomp_word
            re.append(sstr)

    re_str = ''
    for n in re:
        if n == re[-1]:
            re_str = re_str + n
        else:
            re_str = re_str + n + ' --> '

    print(re_str)



    #根据依存关系，分析事件要素
    print('\n内容事件要素:')
    re = []
    for i in dependency_parse_lst:
        if i[0] == 'nsubj':
            dobj_word = ''
            nn_word = ''
            assmod_word = ''
            ccomp_word = ''
            for k in dependency_parse_lst:
                if k[0] == 'dobj' and k[1] == i[1]:
                    dobj_word = ' ' + word_lst[k[2]-1]
            for k1 in dependency_parse_lst:
                if k1[0] == 'compound:nn' and k1[1] == i[2]:
                    nn_word = ' ' + word_lst[k1[2]-1]
            for k2 in dependency_parse_lst:
                if k2[0] == 'nmod:assmod' and k2[1] == i[2]:
                    assmod_word = ' ' + word_lst[k2[2]-1]
            for k3 in dependency_parse_lst:
                if k3[0] == 'ccomp' and k3[1] == i[1]:
                    ccomp_word = ' ' + word_lst[k3[2]-1]
            sstr = assmod_word + nn_word + word_lst[i[2]-1] + ' ' + word_lst[i[1]-1] + dobj_word + ccomp_word
            re.append(sstr)

    re_str = ''
    for n in re:
        if n == re[-1]:
            re_str = re_str + n
        else:
            re_str = re_str + n + ' --> '

    print(re_str)

    print("------------------------------------------------")
    sNLP.nlp.close()




