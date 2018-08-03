#-*- coding: utf-8 -*-
import xmltodict, json
import os
import sys
import urllib2
import urllib
from threading import Thread

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR_PATH)
sys.path.append(DIR_PATH + '/corelib')

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import helpers
from elasticsearch import NotFoundError

from optparse import OptionParser
#import log
import utils

reload(sys)
sys.setdefaultencoding('utf-8')

ES = None
ESIndicesClient = None
Hosts = []
Config = None
ConfigFName = ''

POI_XML_DATA_DIR = "/Users/gimminsang/work/practice/data/"
BASE_DIR = '/Users/gimminsang/work/practice/data/static'

totalProcCnt = 0
failDocs = []


def convertFile(tno):
    global totalProcCnt
    global failDocs

    with open(os.path.join(POI_XML_DATA_DIR, "temp.log"), "r") as fp:
        idx = 0
        index = 0
        docList = []
        dic = {"ticket_id":"","sort":"","coord.focus.type":"","coord.focus.radius":"",
                "referrer_code":"","f1.group":"","coord.user.y":"","coord.user.x":"",
                "rows":"","client_code":"","coord.focus.x":"","coord.focus.y":"",
                "coord.user.type":"","start":"","q":"","additional_results":"",
                "use_tdb":"","option":"","app_ver":"","area_name":"","time_slot":""}
        while (True):
            line = fp.readline()
            if not line: break
            time = line.split("]")
            time = time[0]
            time = time.split("[")
            time = time[1]
            time = time.split(" ")
            date = time[0]
            time = time[1].split(",")
            dic["time_slot"] = date+" "+time[0]
            line2 = line.split("?")
            line3 = line2[1].split("&")
            for i in line3:
                line4 = i.split("=")
                prop = line4[0]
                value = line4[1]
                if prop == "q":
                    value = urllib.unquote(value)
                if ")" in value:
                    value = value.split(")")
                    value = value[0]
                dic[prop] = value
            json_val = json.dumps(dic, ensure_ascii=False)
            index += 1
            print idx
            if idx > 0 and idx % 1000 == 0:
                try:
                    sys.stdout.flush()
                    helpers.bulk(ES, docList, request_timeout=50000)
                    totalProcCnt += len(docList)
                    #print str(tno) + " Thread - bulk process...", "log", ':',  "->", totalProcCn
                    docList = []
                except:
                    failDocs += docList
                    #print "bulk index timeout...", len(failDocs)
            try:
                # if True:
                indexObj = {}
                indexObj["_source"] = json.loads(json_val)
                indexObj["_index"] = "log-index"
                indexObj["_type"] = "logs"
                indexObj["_id"] = index

                docList.append(indexObj)

            except Exception, e:
                print e
            idx += 1
        line = fp.readline()

    try:
        helpers.bulk(ES, docList)
    except:
        failDocs += docList
        #print "bulk index timeout...", len(failDocs)
    totalProcCnt += len(docList)
    #print str(tno) + " Thread - bulk process...", "log", ':', "->", totalProcCnt


fList = []


def static_index():
    print "static"
    global failDocs

    for idx in range(9):
        t = Thread(target=convertFile, args=(idx,))
        t.start()

    with open('./errorDocs.json', "w") as fp:
        fp.write(json.dumps(fList))


def delete_index():
    #index = Config.ES_INDEX
    #log.debug('start to delete index(%s)', index)
    print "delete"

    try:
        ret = ESIndicesClient.delete(index="log-index")
        if ret.get('acknowledged', False):
            #log.debug('success to delete index(%s)', index)
            return True
    except NotFoundError, e:
        #log.debug('not existing index(%s)', index)
        return True
    except Exception, e:
        print(e)
        #log.error('failed to delete index(%s) : err(%s)', index, e)

    return False


def create_index():
    #index = Config.ES_INDEX
    #log.debug('start to create index(%s)', index)
    print "create"
    try:
        with open("/Users/gimminsang/work/practice/data/mapping.json",'r') as f:
            ret = ESIndicesClient.create(index="log-index", ignore = 400, body = f.read())
            f.close()
            # ret = ESIndicesClient.create(index=index)
        if ret.get('acknowledged', False) and ret.get('shards_acknowledged', False):
                #log.debug('success to create index(%s)', index)
            return True
    except Exception, e:
        print e
        #log.error('failed to create index(%s) : err(%s)', index, e)

    return False

def search_index():
    print "search"
    res = ES.search(index="log-index", body={"query":{"match":{"q":"파인애비뉴"}}})
    for hit in res['hits']['hits']:
        print (hit["_source"]["log"])



def cluster_allocation(enable='all'):
    url = 'http://localhost:9200/_cluster/settings'
    data = json.dumps({"persistent": {"cluster.routing.allocation.enable": enable}})
    timeout = 600
    ret = urllib2.Request(url, data, {'Content-Type': 'application/json'})




def init():
    global ES, ESIndicesClient, ESHosts, Config, ConfigFName
    
    ESHosts = ["localhost:9200"]
    
    try:
        ES = Elasticsearch(ESHosts, timeout=20)
        ESIndicesClient = IndicesClient(ES)
    except Exception, e:
        print e

    return True


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-s", "--service_name", dest="service_name",
                      help="tmap|tmap_dev", default="tmap_dev", type="string")
    parser.add_option("-a", "--action_type", dest="action_type",
                      help="STATIC_INDEX|DYNAMIC_INDEX|DELETE_INDEX|CREATE_INDEX|SEARCH_INDEX|STATUS", default="STATUS",
                      type="string")
    (options, args) = parser.parse_args()

    init()
    print options.action_type

    if options.action_type == 'DELETE_INDEX':
        #cluster_allocation('all')
        delete_index()
        #cluster_allocation('none')
    elif options.action_type == 'CREATE_INDEX':
        #cluster_allocation('all')
        delete_index()
        create_index()
        #cluster_allocation('none')
    elif options.action_type == 'STATIC_INDEX':
        static_index()
    elif options.action_type == 'SEARCH_INDEX':
        search_index()
