#coding=utf-8
#encoding='utf-8'
#py2neo test script

from py2neo import Graph 

graph = Graph(password = 'neo123')

result = graph.run("MATCH p=(b)-[*1..4]->(a:Object {name:'" + "可疑账号" + "'}) return p").data()

#print(result)

for record in result:
    print(record)
    # print(type(record["a"]))
    # print(record['a']['name'])
    # print(record['b'])
    # print(record['c']['belong'])
    # print(str(record['a'].labels))
    # print(record['a'].keys())
    # print(record['p'].nodes)
    # print(type(record['p'].relationships))
    # print(record['p'].relationships)
    # print(type(record['p'].relationships[0]))#遍历
    # print(dir(record['p'].relationships[0]))
    # print(type(record['p'].relationships[0].start_node))
    # print(record['p'].relationships[0].end_node['name'])#str
    # print(record['p'].relationships[0].end_node['belong'])#list
    # print(record['p'].relationships[0].start_node['name'])#str
    # print(record['p'].relationships[0].start_node['belong'])#str
    # print(str(record['p'].relationships[0].start_node.labels))#str
    # print(str(record['p'].relationships[0].end_node.labels))#str
    print(record['p'])#str
    print(len(record['p'].relationships))