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
            tmp['名称'] = every_dict.get('标题','')
            tmp['英文名'] = every_dict.get('英文名','暂无数据')
            tmp['定义'] = every_dict.get('疾病介绍','暂无数据')
            tmp['别名'] = ['暂无数据']
            ks = every_dict.get('就诊科室：','暂无数据').strip().split(' ')
            tmp['科室']=[]
            for i in ks:
                if i.strip()[1:-1] not in tmp['科室']:
                    tmp['科室'].append(i.strip()[1:-1])
            print(tmp['科室'])
            tmp['部位'] = every_dict.get('发病部位：','暂无数据').strip().split(' ')
            tmp['症状'] = every_dict.get('相关症状：','暂无数据').strip().split(' ')
            tmp['病因'] = every_dict.get('病因','暂无数据').replace('\\','\\\\')
            tmp['多发人群'] = every_dict.get('多发人群：','暂无数据')
            tmp['检查项目'] = every_dict.get('检查项目：','暂无数据').strip().split(' ')
            tmp['并发疾病'] = every_dict.get('相关疾病：','暂无数据').strip().split(' ')
            tmp['治疗方法'] = every_dict.get('治疗方法：','暂无数据').strip().replace('   ',',').replace(' ','').split(',')
            tmp['治疗方法详述'] = every_dict.get('治疗','暂无数据')
            tmp['治疗费用'] = every_dict.get('治疗费用','暂无数据')
            tmp['医保'] = every_dict.get('是否属于医保：','暂无数据').strip()
            tmp['通用药品'] = every_dict.get('通用药品','暂无数据').strip().split(' ')
            tmp['药品'] = every_dict.get('常用药品：','暂无数据').strip().split(' ')
            tmp['传染性'] = every_dict.get('传染性：','暂无数据')
            tmp['传染方式'] = every_dict.get('传播途径：','暂无数据')
            tmp['患病比例'] = every_dict.get('患病比例','暂无数据')
            tmp['患病比例值'] = every_dict.get('患病比例值','暂无数据')
            tmp['治愈率'] = every_dict.get('治愈率','暂无数据')
            tmp['治愈率值'] = every_dict.get('治愈率值','暂无数据')
            tmp['治疗周期'] = every_dict.get('治疗周期','暂无数据')
            tmp['温馨提示'] = every_dict.get('温馨提示','暂无数据')
            tmp['鉴别详述'] = every_dict.get('鉴别','暂无数据')
            tmp['预防详述'] = every_dict.get('预防','暂无数据')
            tmp['饮食保健'] = every_dict.get('饮食保健','暂无数据')
            tmp['检查内容详述'] = every_dict.get('检查','暂无数据')
            tmp['病症详述'] = every_dict.get('症状','暂无数据')
            tmp['护理详述'] = every_dict.get('护理详述','暂无数据')
            tmp['流行度'] = every_dict.get('流行度','暂无数据')
            tmp['url'] = every_dict.get('url','暂无数据')

            # print(tmp)
    #
            if tmp not in list1:
                list1.append(tmp)

    print(len(list1))
    with open(file2,'w',encoding='utf-8') as ffile:
        ffile.write(json.dumps(list1,ensure_ascii=False))




if __name__ == '__main__':
    prepare_jb('/Users/zhangyuan/work/爬虫数据/名医在线/mingyizaixian-jibing.json','/Users/zhangyuan/work/爬虫数据/名医在线/myzx_jb_ready.json')
