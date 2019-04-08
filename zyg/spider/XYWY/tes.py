# with open('./url.json','r')as f:
#     a = (f.read()).strip()
#     # for i in a :
#     print(a)
#     # print(f.read())
#
with open('./bk.json','r') as f:
    content = f.read().splitlines()
    a = set(content)

    print(len(list(a)))