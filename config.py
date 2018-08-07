#!/usr/bin/python
# encoding: utf-8
# 사용 환경에 맞게 config 파일은 수정해서 쓰세요

import socket


SERVICE_NAME    = 'log'
ES_USER                 = 'eunheekim'
ES_HOST_LIST    = [
                    "d-tsch-os01",
                    "d-tsch-os02",
                    "d-tsch-os03",
                    "d-tsch-os04",
                    "d-tsch-os05",
]
ES_HTTP_PORT    = 9200
ES_INDEX                = 'log'
ES_DOC_TYPE             = 'log'
ES_MAPPING_PATH       = '/home/eunheekim/TmapSearchPkg/pkg_script/env/poi/mapping.json'
BASE_DIR = '/home/eunheekim/minsang/es-logAnalyzer/static'
DATA_DIR = '/home/eunheekim/minsang/es-logAnalyzer/data'
MAPPING_DIR = '/home/eunheekim/minsang/es-logAnalyzer/static/mapping.json'
