import re
import json
def prepare_jb(file1,file2):
    list1 = []
    with open(file1,'r',encoding='utf-8') as file:
        content = file.read()
        json_data = json.loads(content,encoding='utf-8')['RECORDS']

        for every_dict in json_data:
            # print(every_dict['名称'])
            tmp={}
            mc = every_dict.get('标题','')
            b = re.search('(.*)(（.*）)',mc)
            if b is None:
                tmp['名称'] = mc
                tmp['别称'] = []
            else:
                tmp['名称'] = b.group(1)
                tmp['别称'] = b.group(2).strip()[1:-1].replace('，',',').replace(' ',',').strip().split(',')
            print(tmp['别称'])
            tmp['英文名'] = every_dict.get('英文名','暂无数据')
            tmp['定义'] = every_dict.get('简介','暂无数据')

            tmp['科室'] = every_dict.get('就诊科室：','暂无数据').strip().split(' ')
            tmp['部位'] = every_dict.get('发病部位：','暂无数据').strip().split(' ')
            tmp['症状'] = every_dict.get('典型症状：','暂无数据').strip().split(' ')
            tmp['病因'] = every_dict.get('病因','暂无数据')
            tmp['多发人群'] = every_dict.get('易感人群：','暂无数据')
            tmp['检查项目'] = every_dict.get('检查项目：','暂无数据').strip().split(' ')
            tmp['并发疾病'] = every_dict.get('并发疾病','暂无数据').strip().split(' ')
            tmp['治疗方法'] = every_dict.get('治疗方法：','暂无数据').strip().replace('   ',',').replace(' ','').split(',')
            tmp['治疗方法详述'] = every_dict.get('治疗','暂无数据')
            tmp['治疗费用'] = every_dict.get('治疗费用：','暂无数据')
            tmp['医保'] = every_dict.get('是否医保：','暂无数据').strip()
            tmp['通用药品'] = every_dict.get('通用药品','暂无数据').strip().split(' ')
            tmp['药品'] = every_dict.get('常用药品：','暂无数据').strip().split(' ')
            tmp['传染性'] = every_dict.get('是否传染：','暂无数据')
            tmp['传染方式'] = every_dict.get('传染方式：','暂无数据')
            tmp['患病比例'] = every_dict.get('患病比例：','暂无数据')
            tmp['患病比例值'] = every_dict.get('患病比例值','暂无数据')
            tmp['治愈率'] = every_dict.get('治愈率：','暂无数据')
            tmp['治愈率值'] = every_dict.get('治愈率值','暂无数据')
            tmp['治疗周期'] = every_dict.get('治疗周期：','暂无数据')
            tmp['温馨提示'] = every_dict.get('温馨提示','暂无数据')
            tmp['鉴别详述'] = every_dict.get('鉴别详述','暂无数据')
            tmp['预防详述'] = every_dict.get('预防详述','暂无数据')
            tmp['饮食保健'] = every_dict.get('饮食保健','暂无数据')
            tmp['检查内容详述'] = every_dict.get('检查','暂无数据')
            tmp['病症详述'] = every_dict.get('症状','暂无数据')
            tmp['护理详述'] = every_dict.get('护理','暂无数据')
            tmp['流行度'] = every_dict.get('流行度','暂无数据')
            tmp['url'] = every_dict.get('url','暂无数据')

            # print(tmp)
    #
            if tmp not in list1:
                list1.append(tmp)

    with open(file2,'w',encoding='utf-8') as ffile:
        ffile.write(json.dumps(list1,ensure_ascii=False))




if __name__ == '__main__':
    prepare_jb('/Users/zhangyuan/work/爬虫数据/健康一线/jkyx-jibing.json','/Users/zhangyuan/work/爬虫数据/健康一线/jkyx_jibing_ready.json')