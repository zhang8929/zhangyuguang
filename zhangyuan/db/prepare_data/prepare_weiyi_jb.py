import json

import json
def prepare_jb(file1,file2):
    list1 = []
    with open(file1,'r',encoding='utf-8') as file:
        content = file.read()
        json_data = json.loads(content,encoding='utf-8')['RECORDS']

        for every_dict in json_data:
            # print(every_dict['名称'])
            tmp={}
            tmp['名称'] = every_dict.get('标题','').strip()
            tmp['定义'] = every_dict.get('概述','暂无数据')
            basic_inf = json.loads(every_dict.get('基本信息',''))
            for dict in basic_inf:
                tmp[list(dict.keys())[0]] = list(dict.values())[0]

            tmp['科室'] = tmp.get('科室','暂无数据').strip().split(' ')
            tmp['部位'] = tmp.get('部位','暂无数据').strip().split(' ')
            tmp['症状'] = tmp.get('症状','暂无数据').strip().split(' ')
            tmp['治疗方法'] = tmp.get('治疗方法','暂无数据').strip().split(' ')
            tmp['英文名'] = tmp.get('英文名','暂无数据').strip()
            tmp['多发人群']=tmp.get('多发人群','暂无数据').strip()

            tmp['病因'] = every_dict.get('病因','暂无数据').strip()
            tmp['检查项目'] = every_dict.get('检查项目：','暂无数据').strip().split(' ')
            tmp['并发疾病'] = tmp.get('并发疾病','暂无数据').strip().split(' ')
            tmp['治疗方法详述'] = every_dict.get('治疗','暂无数据').strip()
            tmp['治疗费用'] = every_dict.get('治疗费用','暂无数据').strip()
            tmp['医保'] = every_dict.get('是否属于医保：','暂无数据').strip()
            tmp['通用药品'] = every_dict.get('通用药品','暂无数据').strip().split(' ')
            tmp['药品'] = every_dict.get('常用药品：','暂无数据').strip().split(' ')
            tmp['传染性'] = every_dict.get('传染性：','暂无数据').strip()
            tmp['传染方式'] = every_dict.get('传播途径：','暂无数据').strip()
            tmp['患病比例'] = every_dict.get('患病比例','暂无数据').strip()
            tmp['患病比例值'] = every_dict.get('患病比例值','暂无数据').strip()
            tmp['治愈率'] = every_dict.get('治愈率','暂无数据').strip()
            tmp['治愈率值'] = every_dict.get('治愈率值','暂无数据').strip()
            tmp['治疗周期'] = every_dict.get('治疗周期','暂无数据').strip()
            tmp['温馨提示'] = every_dict.get('温馨提示','暂无数据').strip()
            tmp['鉴别详述'] = every_dict.get('诊断','暂无数据').strip()
            tmp['预防详述'] = every_dict.get('预防','暂无数据').strip()
            tmp['饮食保健'] = every_dict.get('饮食保健','暂无数据').strip()
            tmp['检查内容详述'] = every_dict.get('检查','暂无数据').strip()
            tmp['病症详述'] = every_dict.get('症状','暂无数据').strip()
            tmp['护理详述'] = every_dict.get('护理详述','暂无数据').strip()
            tmp['流行度'] = every_dict.get('流行度','暂无数据').strip()
            tmp['url'] = every_dict.get('url','暂无数据').strip()

            # print(tmp)
    #
            if tmp not in list1:
                list1.append(tmp)

    with open(file2,'w',encoding='utf-8') as ffile:
        ffile.write(json.dumps(list1,ensure_ascii=False))




if __name__ == '__main__':
    prepare_jb('/Users/zhangyuan/work/爬虫数据/健康度和微医/weiyi.json','/Users/zhangyuan/work/爬虫数据/健康度和微医/weiyi_ready.json')