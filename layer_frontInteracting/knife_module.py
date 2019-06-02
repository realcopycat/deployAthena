#'knife(利刃)' 查找模块
# design for "/knife"

from athena_App.layer_dataOperating.neo4j_search import neo4jQuery
from athena_App.layer_dataOperating.sy_module import senCompare

'''
    knife主控模块
'''
class knifeModule():
    
    def __init__(self, des, ctrl_code, Ltptool):
        '''
        des 接受用户的描述
        ctrl_code 控制码，控制查询类型
        '''
        self.des = des
        self.qcode = int(ctrl_code) 
        self.ltptool = Ltptool
        self.graphQuery = neo4jQuery()

    def taskDistribute(self):
        '''
        任务分配器
        '''
        print(type(self.qcode))
        
        if self.qcode == 100 or self.qcode == 200:
            #后向查询与前导查询
            result = self.normalSearch()
            print("{ + } normalSearch")
        elif self.qcode == 300:
            #流程查询
            result = self.completeSearch()
            print("{ + } completeSearch")
        else:
            #流程码无解的情况下使用默认流程查询
            result = self.completeSearch()
            print("{ + } fianl completeSearch")
        print("{ + }")
        print(str(result))
        return result

    def normalSearch(self):
        '''
        前导与后向查询函数
        '''
        result = self.graphQuery.procedureQuery(self.des, self.qcode)

        #开始解析结果,这里实际的解析模式是 子图解析 在这里解析的都是 Path
        node_data = []
        node_set = set()
        link_set = set()
        belong = ''
        text_data = {"operate": [], "obj": []}
        for record in result:
            #先解析node
            for i in range(0,len(record['p'].relationships)-1):
                #取出路径上的每一对元组，保证覆盖每个点
                startNodeName = record['p'].relationships[i].start_node['name']
                endNodeName = record['p'].relationships[i].end_node['name']
                if startNodeName not in node_set:
                    node_set.add(startNodeName)
                    nodeItem = {}
                    nodeItem['name'] = startNodeName
                    nodeItem['category'] = str(record['p'].relationships[i].start_node.labels)
                    node_data.append(nodeItem)
                if endNodeName not in node_set:
                    node_set.add(endNodeName)
                    nodeItem = {}
                    nodeItem['name'] = endNodeName
                    nodeItem['category'] = str(record['p'].relationships[i].end_node.labels)
                    node_data.append(nodeItem)
                
                link_item = (startNodeName, endNodeName)
                link_set.add(link_item)

                #注意 此处为临时做法，用于设置belong
                belong =  record['p'].relationships[0].end_node['belong'][0]
        
        link_data = []
        link_list = list(link_set)
        for item in link_list:
            linkItem = {}
            linkItem['source'] = item[0]
            linkItem['target'] = item[1]
            link_data.append(linkItem)

        for node in node_data:
            if node['category'] == ":Object":
                text_data["obj"].append(node['name'])
            else:
                text_data["operate"].append(node['name'])
        
        finalResult = {"links": link_data, "nodes": node_data, "procedureName": belong, "text_data":text_data}
        print(finalResult)
        return finalResult

    def completeSearch(self):
        '''
        流程查询函数
        '''
        result = self.graphQuery.procedureQuery(self.des, self.qcode)

        #这里解析的模式是 单节点解析 分别是(a)-[b]->(c)
        node_set = set()
        node_data = []
        link_set = set()
        belong = ''
        for record in result:
            startNode = record['a']['name']
            endNode = record['b']['name']
            if startNode not in node_set:
                node_set.add(startNode)
                nodeItem = {}
                nodeItem['name'] = startNode
                nodeItem['category'] = str(record['a'].labels)
                node_data.append(nodeItem)
            if endNode not in node_set:
                node_set.add(endNode)
                nodeItem = {}
                nodeItem['name'] = endNode
                nodeItem['category'] = str(record['b'].labels)
                node_data.append(nodeItem)
            
            link_item = (startNode, endNode)
            link_set.add(link_item)

            belong = record['a']['belong']
        
        link_data = []
        link_list = list(link_set)
        for item in link_list:
            linkItem ={}
            linkItem['source'] = item[0]
            linkItem['target'] = item[1]
            link_data.append(linkItem)

        finalResult = {"links": link_data, "nodes": node_data, "procedureName": belong}

        return finalResult