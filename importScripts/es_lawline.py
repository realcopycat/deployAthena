#coding=utf-8
#导入法条到es
#未编写完成！！

import time
from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import bulk
from pymongo import MongoClient as MG

class dataImporter():
    '''用于在mongodb和elastic之间转接导入数据'''

    def __init__(self):
        '''初始化设置'''

        #可修改：定c义索引名称
        self._index=""

        #可修改，但一般不需要，定义es服务器设置
        self.es=ES([{"host":"localhost","port":9200}])

        #可修改：定义文档类型
        self.doc_type="case"

        #无需修改，链接mongodb
        self.MGclient=MG("mongodb://reader:reader@localhost:27017")

        #可修改，指定数据库名称
        self.db=self.MGclient.spider_data

        #可修改,指定collection的名称
        self.collect=self.db.tagged_case

