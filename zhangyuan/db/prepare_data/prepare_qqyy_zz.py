import json
def prepare_zz(file1,file2):
    list1 = []
    with open(file1,'r',encoding='utf-8') as file:
        content = file.read()
        json_data = json.loads(content,encoding='utf-8')['RECORDS']

        for every_dict in json_data:
            # print(every_dict['名称'])
            tmp={}
            tmp['名称'] = every_dict.get('标题','')
            tmp['图片'] = every_dict.get('图片','暂无数据')
            tmp['url'] = every_dict.get('url','暂无数据')
            tmp['别名'] = every_dict.get('别名','暂无数据')
            tmp['定义'] = every_dict.get('简述','暂无数据')
            tmp['部位'] = every_dict.get('部位','暂无数据').strip().split(' ')
            tmp['科室'] = every_dict.get('科室','暂无数据').strip().split(' ')
            tmp['相似症状'] = every_dict.get('相似症状','暂无数据').strip().split(' ')
            tmp['检查项目'] = every_dict.get('检查项目','暂无数据').strip().split(' ')
            tmp['疾病'] = every_dict.get('相关疾病','暂无数据').strip().split(' ')
            tmp['通用药品'] = every_dict.get('通用药品','暂无数据')
            tmp['药品'] = every_dict.get('药品','暂无数据').strip().split(' ')

            if tmp not in list1:
                list1.append(tmp)

    print(len(list1))
    with open(file2,'w',encoding='utf-8') as ffile:
        ffile.write(json.dumps(list1,ensure_ascii=False))




if __name__ == '__main__':
    prepare_zz('/Users/zhangyuan/work/爬虫数据/全球医院/qqyy-zhengzhuang.json','/Users/zhangyuan/work/爬虫数据/全球医院/qqyy_zhengzhuang_ready.json')