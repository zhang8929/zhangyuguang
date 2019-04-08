import json
def prepare_zz(file1,file2):
    list1 = []
    with open(file1,'r',encoding='utf-8') as file:
        content = file.read()
        json_data = json.loads(content,encoding='utf-8')['RECORDS']

        for every_dict in json_data:
            # print(every_dict['名称'])
            tmp={}
            tmp['名称'] = every_dict.get('名称','')
            tmp['图片'] = every_dict.get('图片','暂无数据')
            tmp['url'] = every_dict.get('url','暂无数据')
            tmp['别名'] = every_dict.get('别名','暂无数据')
            tmp['定义'] = every_dict.get('定义','暂无数据')
            tmp['部位'] = every_dict.get('部位','暂无数据').strip().split(' ')
            tmp['相似症状'] = every_dict.get('相似症状','暂无数据').strip().split(' ')
            tmp['检查项目'] = every_dict.get('检查项目','暂无数据').strip().split(' ')
            tmp['通用药品'] = every_dict.get('通用药品','暂无数据')
            tmp['药品'] = every_dict.get('药品','暂无数据').strip().split(' ')
            tmp['饮食保健'] = every_dict.get('饮食注意','暂无数据')
            jb_list = []
            ks_list = []
            for jb in json.loads(every_dict.get('可能疾病')):
                jb_list.append(jb.get('可能疾病','暂无数据'))
                ks_list+=(jb.get('急诊科室','暂无数据').strip().split(' '))
            tmp['疾病'] = jb_list
            # tmp['科室'] = list(set(ks_list))
            tmp['科室'] = ['暂无数据']

            if tmp not in list1:
                list1.append(tmp)

    with open(file2,'w',encoding='utf-8') as ffile:
        ffile.write(json.dumps(list1,ensure_ascii=False))




if __name__ == '__main__':
    prepare_zz('/Users/zhangyuan/work/爬虫数据/9939/9939-zhengzhuang.json','/Users/zhangyuan/work/爬虫数据/9939/9939_zhengzhuang_ready.json')