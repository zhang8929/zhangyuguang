import requests

from lxml import etree
import json
from threading import Thread


class JiangKang():
  '''健康问答'''
  def __init__(self):
       self.url='https://www.jiankang.com/ask/k3/'

       self.headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                     }


  def fist_url(self):

      rep = requests.get(self.url)
      resp = rep.content
      html = etree.HTML(resp)
      list_url_index = html.xpath("//div[@class='first_class clearfix']/a/@href")

      return list_url_index


  def sencond_url(self,list_ur):
      sen=requests.get(list_ur)
      html=etree.HTML(sen.content)
      list_url_sencond=html.xpath("//div[@class='first_class clearfix']/a/@href")

      return list_url_sencond

  def tree_url(self,send_url):
      tre=requests.get(send_url)
      html=etree.HTML(tre.content)
      list_url_tree=html.xpath("//div[@class='all_quest clearfix']/ul/li[2]/a/@href")

      return list_url_tree[0]

  def solve_url(self,tre_url_str):

      list1 =[]

      next_url_str = tre_url_str
      print(next_url_str)
      n=1
      while n < 16:

          solve = requests.get(next_url_str)
          star=solve.status_code
          if star ==404:

              print('taic')
              break
          try:
              html = etree.HTML(solve.content)
              list_url_solve = html.xpath("//div[@class='tab_contant clearfix']/ul/li/a/@href")
              list1.append(list_url_solve)
              next_url = html.xpath("//ul[@class='page clearfix']/li/a/@href")[0]
              print(next_url)
              n+=1
              next_url_str=tre_url_str + '?p={}'.format(n)
              print(next_url_str)
          except:
              pass


      print(list1)
      return list1

  def centend_url(self,conten_url):
      dict1 = {}
      try:
          cen=requests.get(conten_url)
          html=etree.HTML(cen.content)

          dict1['url']=conten_url
          dict1['question '] = html.xpath("//div[@class='content']/span/h1/text()")[0]
          dict1['describe'] = html.xpath("//div[@class='content']/div/span[2]/em/p/text()")[0]
          dict1['answer'] = html.xpath("//div[@class='answer']/span/em/p/text()")[0]

      except:
          pass
      return dict1
  def save(self,dict1):

      dict1_json=json.dumps(dict1,ensure_ascii=False)
      print(dict1_json)
      fileOb = open('外科.json', 'a',encoding='utf-8')  # 打开一个文件，没有就新建一个

      fileOb.write(dict1_json+','+'\n')

      fileOb.close()

  def run(self):

          list_url_index=self.fist_url()
          print(list_url_index)
          for i in list_url_index:
               list_url='https://www.jiankang.com'+i
               sen_url=self.sencond_url(list_url)

               for j in sen_url:
                 send_url = 'https://www.jiankang.com' + j
                 tre_url=self.tree_url(send_url)
                 tre_url_str = 'https://www.jiankang.com' + tre_url


                 list1=self.solve_url(tre_url_str)
                 for k in list1:

                     for u in k:

                        conten_url = 'https://www.jiankang.com' + u
                        centend_dict =self.centend_url(conten_url)
                        self.save(centend_dict)


if __name__=='__main__':

      jangkang=JiangKang()

      jangkang.run()











