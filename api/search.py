from elasticsearch import Elasticsearch,exceptions
from datetime import datetime
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections
import json

#es = Elasticsearch(hosts='https://localhost:9200', http_auth=('elastic', '4Vj*9LLjaqIAY-eI8-j1'), verify_certs=False)
es = connections.create_connection(hosts=['http://120.46.205.87:9200'],
                                       http_auth=('elastic'), timeout=40)


def get_results(response): 
    result_list = {"results":[]}
    for hit in response:
        print(hit)
        result_tuple = (hit.id,hit.name)
        result_list["results"].append(result_tuple)  
    return result_list

def searchAuthor(name):
    q = Q({"match": {"name" : name }})
    s = Search(using=es, index="author").query(q)
    response = s.execute()
    search = get_results(response)    
    return search

def get_paperResults(response): 
    result_list = {"results":[]}
    for hit in response:
        result_tuple = (hit.title,hit.authors)
        print(type(result_tuple))
        result_list["results"].append(result_tuple)  
    return result_list

def searchPaperAuthor(keyword):
    q = Q({"match": {"id" : keyword }})
    s = Search(using=es, index="title2").query(q)
    response = s.execute()
    search = get_paperResults(response) 
    tuple = search['results'][0]
    list = []
    for tmp in tuple:
        list.append(tmp)

    data=[]
    for tmp in list:
        data.append(tmp)
    return data   

def get_AuthorResults(response): 
    result_list = {"results":[]}
    for hit in response:
        result_dict= [hit.to_dict() for hit in response]
        result_list["results"].append(result_dict)  
    return result_list

def searchAuthor(keyword):
    q = Q({"match": {"id" : keyword }})
    s = Search(using=es, index="author").query(q)
    response = s.execute()
    search = get_AuthorResults(response)    
    return search