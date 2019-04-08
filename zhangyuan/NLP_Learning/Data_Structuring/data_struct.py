import requests,json

text = """
慢性咽炎容易与哪些疾病混淆?
因病程发展缓慢，病变部位隐蔽，故往往早期不易明确诊断。根据临床表现，仔细检查咽部，对于咽反向敏感或不能配合检查的病人采⽤用纤维⿐咽镜检查。必要时做活检，以明确诊断， 排队⿐鼻咽咽肿瘤。摄颅底X线⽚片及颅脑CT或磁共振检查有助于鉴别诊断。
一、是慢性单纯性咽咽炎。表现为咽咽部粘膜慢性充⾎;
⼆、是肥厚性咽咽炎。主要表现为咽咽部粘膜充⾎血肥厚，粘膜下有⼴广泛的结缔组织及淋淋巴组织增生;
三、是慢性萎缩性咽咽炎。主要表现为粘膜层及粘膜下层萎缩变薄，咽咽后壁有痂⽪皮附着，分泌减少。"""

url = 'http://154.8.214.203:5555/fenci?words='+text  #分词结果
result = requests.get(url=url)
res = result.content.decode('utf-8')
data = json.loads(res)['result']  #list
# print(data)

words_list= []
for ll in data:
    if ll[1]=='d' or ll[1]=='uj' or ll[1]=='x':
        continue
    else:
        words_list.append(ll)

# print(words_list)

sentence_list = text.split('。')
print(len(sentence_list))

for sentence in sentence_list:
    print(sentence)
    url = 'http://154.8.214.203:5555/jufafenxi?words='
    url += sentence
    res = requests.get(url=url)
    print(res.content.decode())

