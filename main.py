# -*- coding: utf-8 -*-
import re
import MeCab
import sys
import io
import time

class TFIDF:
    def tf(self, terms, document):
        tf_values = [document.count(term) for term in terms]
        return list(map(lambda x: x/sum(tf_values), tf_values))

    # idf値算出メソッド定義
    def idf(self, terms, documents):
        import math
        return [math.log10(len(documents)/sum([bool(term in document) for document in documents])) for term in terms]

    # tf-idf値算出メソッド定義
    def calc_tfidf(self, terms, documents):
        return [[_tf*_idf for _tf, _idf in zip(self.tf(terms, document), self.idf(terms, documents))] for document in documents]

def getDocs(documents):
    m='((http|https).+?($|\n|\z))|(@.+?(:| |\n))'
    documents = [re.sub(m, "", text) for text in documents]
    return documents


def getTerms(text,speech):
    # tagger = MeCab.Tagger('-Ochasen -d /usr/lib/mecab/mecab-dict-gen')
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')

    node = tagger.parseToNode(text)
    print(len(text))
    print(speech)
#    print(node)
    ignore_str = "…。ーー@/:._ ？？✨✨*】❗♪｡ﾟ❗?♪　⇨*)５☃☆*。??？？？ｩｗｗｗwwwwszeznwwwwwniconewsOCSPA!DD３ZEgtRIｼｪﾙﾝ20年後てんsh"
    terms=[]
    while node:
#        print(node.surface)
        if (node.surface not in ignore_str and node.surface not in terms):
            if (node.feature.split(",")[0] in speech):
                terms.append(node.surface)
#                print (node.surface)                 # 表層形
#                print (node.feature.split(",")[0])   # 品詞
#                print (node.feature.split(",")[1])   # 品詞細分類1
#                print (node.feature.split(",")[2])   # 品詞細分類2
#                print (node.feature.split(",")[3])   # 品詞細分類3
        node = node.next
    return terms


def getIndex(result_top, result):
    result_top_index = []
    for rows_result_top in result_top:
        for row in rows_result_top:
            for i, d_result in enumerate(result):
                for j, td_result in enumerate(d_result):
                    if td_result == row:
                        if [i,j] not in result_top_index:
                            result_top_index.append([i,j])
            print(row)
            print(result_top_index,"\n")
    return result_top_index

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Here

    dataP = ""
    dataE = ""
    dataN = ""
    f = open('./input-files/sample_PN.txt')
    line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
    while line:
#        print(line)
        if (int(line.split('\t')[0]) > 0):
            dataP += (line.split('\t')[1]) + " "
        elif(int(line.split('\t')[0]) == 0):
            dataE += (line.split('\t')[1]) + " "
        elif(int(line.split('\t')[0]) < 0):
            dataN += (line.split('\t')[1]) + " "
        else:
            print("**Error**")
        line = f.readline()
    f.close
    documents=[dataP, dataN]

    terms = getTerms(" ".join(documents), ["名詞", "形容詞", "動詞"])
    print (documents)
    print (terms)

    tfidf = TFIDF()
    result = tfidf.calc_tfidf(terms, documents)
    print(result,"\n")

    result_sorted = []
    for row in result:
        result_sorted.append(list(reversed(sorted(row))))
    print(result_sorted)
    result_top = []
    for row in result_sorted:
        result_top.append(row[0:100])
    result_top_index = getIndex(result_top, result)

    print("＊＊TEXT番号＊＊", "＊＊重要語＊＊", "＊＊TFIDF値＊＊", "\n")
    for row in result_top_index:
        print(row[0], terms[row[1]], result[row[0]][row[1]])



    f = open('./output-files/'+time.strftime("%Y%m%d%H%M%S")+'.txt','a')

    for i in range(len(result)):
        for j in range(len(result[i])):
            f.write(str(i)+"\t"+str(j)+"\t"+str(result[i][j])+"\n")

    for i in range(len(documents)):
        f.write(str(i)+"\t"+documents[i]+"\n")
    for i in range(len(terms)):
        f.write(str(i)+"\t"+terms[i]+"\n")

    f.close()
