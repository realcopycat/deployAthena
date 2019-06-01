#'knife(利刃)' 查找模块
# design for "/knife"

from athena_App.layer_dataOperating.neo4j_search import neo4jQuery
from athena_App.layer_dataOperating.sy_module import senCompare

'''
    knife主控模块
'''
class knife():
    def __init__(self, des, ctrl_code, Ltptool):
        '''
        des 接受用户的描述
        ctrl_code 控制码，控制查询类型
        '''
        self.des = des
        self.qcode = ctrl_code 
        self.ltptool = Ltptool
        self.graphQuery = neo4jQuery()

    def taskDistribute(self):
        '''
        任务分配器
        '''

        if self.qcode == 100:
            #后向查询
            result = self.backSearch()
        elif self.qcode == 200:
            #前导查询
            result = self.forwardSearch()
        elif self.qcode == 300:
            #流程查询
            result = self.completeSearch()
        else:
            #流程码无解的情况下使用默认流程查询
            result = self.completeSearch()
        
        return result

    def backSearch(self):
        '''
        后向查询函数
        '''
        node_list, link_list = self.graphQuery.entityQuery(self.des)
        #务必注意

        finalResult = {}
        finalResult['userNode'] = self.des
        finalResult['targetNode'] = node_list
        finalResult['link_list'] = link_list

        return finalResult


    def forwardSearch(self):
        '''
        前导查询函数
        '''

        return finalResult

    def completeSearch(self):
        '''
        流程查询函数
        '''
   
        return finalResult