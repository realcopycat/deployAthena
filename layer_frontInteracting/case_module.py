#案件查找模块

from athena_App.layer_dataOperating.es_search import searchInEs
from athena_App.layer_dataOperating.neo4j_search import neo4jQuery
#在views里直接实例化本工具
#from athena_App.layer_dataOperating.textParse_module import TripleExtractor
from athena_App.layer_dataOperating.sy_module import senCompare
from athena_App.layer_dataOperating.mongo_search import mongoSearch
import re

class caseQuery():

    def __init__(self, des, tripletool):
        '''初始化模块'''

        self.graphQuery=neo4jQuery()
        #self.ltpTools=Ltptool
        print('{ + } 案例分析加载模型')
        self.parser=tripletool

        self.index='case_data'
        self.docType='caseText'
        self.key='plainText'
        self.res_limit=10
        self.des=des
        self.searchMongo=mongoSearch()

        #达到一定的分数就属于“核心相关关系”
        #“coreRela”
        self.rela_score=0.25
        #达到标准分数就不再检索，直接返回答案，加快速度
        self.score_standard=0.8

    def es_preSearch(self):
        '''ES预搜索'''

        result=searchInEs(self.des,self.index,self.docType,self.key,self.res_limit)

        title_list=[]
        for res in result:
            title_list.append(res['_source']['title'])

        return title_list

    def destriptionParse(self):
        '''解析传入的描述'''

        return self.parser.triples_main(self.des)

    def titlePick(self):
        '''挑一个最好的title'''

        try:
            relaPick=self.destriptionParse()[1]
            if isinstance(relaPick,list):
                relaPick=relaPick[1]

        #为了防止三元组解析失效，
        except Exception as e:
            print(e)
            relaPick=self.des

        highestScore=0
        highestTitle=''
        relative_relation=set()
        for title in self.es_preSearch():
            result=self.graphQuery.attrQuery('belong',title)

            title_score=0
            for record in result:
                tmp_score=senCompare(record["b"].type,relaPick)
                if title_score<tmp_score:
                    title_score=tmp_score

                if tmp_score>self.rela_score:
                    relative_relation.add(record["b"].type)

            if title_score>highestScore:
                highestScore=title_score
                highestTitle=title

            if title_score>self.score_standard:
                break
        #为了getTextData可以访问,特地设置成员
        self.bestTitle=highestTitle
        self.bestScore=highestScore

        return highestTitle,list(relative_relation)

    def pickBestGraph(self):
        '''
            调用后输出画图数据
        '''
        #提取案例名称
        coreTitle,coreRela=self.titlePick()
        graphData=self.graphQuery.attrQuery('belong',coreTitle)
        #设定画图数据集
        node_list=[]
        link_list=[]
        #控制节点大小
        node_count={}
        #统计匹配的关系数
        link_pick=0
        #记录直接相关的关键节点
        coreNode=[]
        sub_coreNode=[]

        for record in graphData:
            #取出node标签数据
            tmpNode1=record["a"]._properties["text"]
            tmpNode2=record["c"]._properties["text"]
            node_list.append(tmpNode1)
            node_list.append(tmpNode2)
            #抽出linkType数据
            tmpLink=record["b"].type
            print(tmpLink)
            linkItem={}
            linkItem["source"]=tmpNode1
            linkItem["target"]=tmpNode2
            linkItem["value"]=tmpLink
            #设置样式
            linkItem["label"]={}
            linkItem["label"]["normal"]={}
            linkItem["label"]["normal"]["show"]=True
            linkItem["label"]["normal"]["formatter"]=tmpLink
            #判断是否为核心关系数据，设置更加显眼的样式
            if tmpLink in coreRela:
                linkItem["lineStyle"]={}
                linkItem["lineStyle"]["normal"]={}
                linkItem["lineStyle"]["normal"]["color"]="#34E52D"
                linkItem["label"]["normal"]["color"]="#34E52D"
                #为统计的需要计数
                link_pick+=1
                #作为核心关系所链接的节点，做特殊标记
                coreNode.append(tmpNode1)
                coreNode.append(tmpNode2)
            else:
                #如果不在核心关系之内，检测是否其中一个节点与核心节点相联系
                if tmpNode1 in coreNode:
                    sub_coreNode.append(tmpNode2)
                if tmpNode2 in coreNode:
                    sub_coreNode.append(tmpNode1)
            #最后加入数据集
            link_list.append(linkItem)
            #每个节点拥有的链接计数
            try:
                node_count[tmpNode1] +=1
            except:
                node_count[tmpNode1]=0
            #设置被接入的节点
            if tmpNode2 not in node_count:
                node_count[tmpNode2]=0
        
        #取集合以保证节点唯一性
        coreNode=list(set(coreNode))
        sub_coreNode=list(set(sub_coreNode))
        sub_coreNode=[s for s in sub_coreNode if s not in coreNode]
        node_set=list(set(node_list))
        node_data=[]
        #数据统计部分：node
        node_short=0
        node_long=0
        node_text=0
        #数据统计部分：link
        link_A=0
        link_B=0
        link_C=0
        link_D=0
        #对节点数据遍历，做统计分析
        for node in node_set:
            data={}
            data["name"]=node
            data["draggable"]=True
            #节点分级
            if node_count[node]>=10:
                link_A+=1
            elif ((node_count[node]>=6)&(node_count[node]<10)):
                link_B+=1
            elif ((node_count[node]>=3)&(node_count[node]<6)):
                link_C+=1
            elif ((node_count[node]>=0)&(node_count[node]<3)):
                link_D+=1
            #节点分类
            if len(node)>=15:
                data["category"]="text"
                node_text=node_text+1
            elif ((len(node)>=7)&(len(node)<15)):
                data["category"]="long"
                node_long=node_long+1
            elif ((len(node)>0)&(len(node)<7)):
                data["category"]="short"
                node_short=node_short+1
            #添加新分类
            if node in coreNode:
                data["category"]='Core'
            elif node in sub_coreNode:
                data["category"]='subCore'
            #根据链接数目设置节点大小
            if node_count[node]==0:
                data["symbolSize"]=30
            else:
                data["symbolSize"]=30+node_count[node]*3
                if data["symbolSize"]>=60:
                    data["symbolSize"]=60
            #写入数据
            node_data.append(data)

        #数据统计部分:node
        nodeStat=[{"value":node_short,"name":'短文本节点'},
                 {"value":node_long,"name":'长文本节点'},
                 {"value":node_text,"name":'描述性节点'}]
        print(nodeStat)

        #数据统计部分：link
        linkStat=[{"name":'A级节点',"value":link_A},
                  {"name":'B级节点',"value":link_B},
                  {"name":'C级节点',"value":link_C},
                  {"name":'D级节点',"value":link_D},]
        print(linkStat)

        #数据统计部分：All
        node_total=node_long+node_short+node_text
        link_total=link_A+link_B+link_C+link_D
        allStat=[self.res_limit,node_total,link_total,node_short,node_long,node_text,link_pick]

        final={"data":node_data,"links":link_list,"nodeAnalyse":nodeStat,
               "linkAnalyse":linkStat,"totalStat":allStat}

        return final

    '''
        获取数据的主函数
    '''
    def getData(self):
        '''
            试图综合画图数据以及文字标签数据
        '''
        #由于存在对象内成员的动态定义
        #这三个函数的位置切勿随意调换
        addup = dict()
        addup['graphData']=self.pickBestGraph()
        addup['tagData']=self.getTextData()
        addup['lawData']=self.getLawData()
        return addup

    '''
        解析标签数据
    '''
    def getTextData(self):
        '''
            根据es预选的结果
            给出匹配度
            给出可能的判决
            给出可能相关的法条
        '''
        #以下函数的参数决定于数据库设置,注意这里对于嵌套字典的索引方式
        
        singleDoc=self.searchMongo.singleFieldSearch('spider_data','lawText','judgement.title',self.bestTitle)

        textDataDict=dict()
        #相似度计算，算法待优化
        textDataDict["相似度"]=self.bestScore
        #现成的基本信息
        try:
            textDataDict["判决日期"]=singleDoc['judgement']['judgeDate']
        except:
            pass
        try:
            textDataDict["审理法院"]=singleDoc['judgement']['court']
        except:
            pass
        try:
            textDataDict['案例标题']=singleDoc['judgement']['title']
        except:
            pass
        try:
            textDataDict['案例编号']=singleDoc['judgement']['caseNo']
        except:
            pass
        #以下cause作为成员供法条查询使用
        try:
            self.cause=singleDoc['judgement']['cause'][0]
            textDataDict['涉及的违法或犯罪行为']=singleDoc['judgement']['cause'][0]
        except:
            self.cause=False

        try:
            defedantParse_tmp=singleDoc['judgement']['litigants']
            for each in defedantParse_tmp:
                if each['type']=='Defedant':
                    textDataDict['被告人'].append(each['name'])
                if each['type']=='Plaintiff':
                    textDataDict['起诉方']=each['name']
        except:
            pass

        #需要RE解析的信息
        puretext=singleDoc['judgement']['plaintext']
        pattern_forLaw=re.compile('((?<=依照).*?(?=之规定))|((?<=依照).*?(?=的规定))|((?<=依照).*?(?=规定))|((?<=根据).{4,25}?(?=规定))')
        textDataDict['案例涉及的法律法规']=re.findall(pattern_forLaw,puretext)

        return textDataDict

    '''
        从Es中获取相关的法律法条
    '''
    def getLawData(self):
        '''
            由ES引擎给出相关的具体法条
        '''

        #下列参数与具体的数据库相关,
        #根据标题返回五个法条
        resOfLaw1 = searchInEs(self.bestTitle,'law_data','line','line',5)

        #下列参数与具体数据库相关
        set=0
        if self.cause:
            resOfLaw2 = searchInEs(self.cause,'law_data','line','line',5)
            set=1

        #包装相关法条
        lawLine = list()
        for line in resOfLaw1:
            lawLine.append(line['_source'])
        if set == 1:
            for line in resOfLaw2:
                lawLine.append(line['_source'])
        
        return lawLine