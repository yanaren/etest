# -*- coding: utf8 -*-
import codecs
import json
import copy
import os
import re
import pprint
from xml.dom.minidom import parse

null = ''

def Str2Json(source_str):
    global null
    return eval(source_str)

class JsonUtil:
    @staticmethod
    def Loads(json_file_path='/tmp/tmp.json'):
        '''
        @return: (load_success, json_object)
        Load non-standard json file. E.g. services configuration file of alimail 
        '''
        json_dict = ''
        load_success = False
        json_object = {}
        #with open(json_file_path, encoding='utf-8') as a_file:
        with open(json_file_path) as a_file:
            for a_line in a_file:
                p = re.compile('\s\/\/')
                if p.split(a_line).__len__() > 1:
                    json_dict += p.split(a_line)[0] + '\n'
                else:
                    json_dict += a_line
        if json_dict != '':
            load_success = True
            json_dict = json_dict.replace('\n', '')
            json_dict = json_dict.replace('\r', '')
            json_dict = json_dict.replace('\t', '')
            json_object =json.loads(json_dict) 
        return (load_success, json_object)
    
    @staticmethod
    def ToPrettyStr(json_object={}):
        return json.dumps(json_object, sort_keys=True, indent=4)

class MTestGloabel:
    jsDecoder = json.JSONDecoder()
    jsEncoder = json.JSONEncoder()

class TValueGroup:
    def __init__(self, group_source, is_value=False, type_word='t', value_word='v'):
        tgs = group_source.__class__.__name__
        if tgs == 'TValueGroup':
            group_source = group_source.__prop__
        self.is_value = is_value
        self.type_Word = type_word
        self.value_Word = value_word

        self.init(group_source)

    def init(self, group_source):
        self.__prop__ = TValueGroup.to_jsonmap(group_source) if "" != group_source else {}

    @staticmethod
    def to_jsonmap(group_source, is_list=False):
        tgs = group_source.__class__.__name__
        if  tgs == 'str' or tgs == 'unicode':
            if os.path.exists(group_source):
                if group_source.endswith('.xml'):
                    doml = parse(group_source)
                    jsonmap = {}
                    for node in doml.getElementsByTagName('Property'):
                        tvg_name = node.getAttribute("name")
                        tvg_type = node.getAttribute("type")
                        tvg_value = node.getAttribute("value")
                        if tvg_name != "":
                            if is_list and jsonmap.__contains__(tvg_name):
                                listVal = jsonmap[tvg_name]
                                if type(listVal) == list:
                                    listVal.append(tvg_value)
                                else:
                                    jsonmap[tvg_name] = [listVal, tvg_value]
                                continue
                            if tvg_type == "":
                                jsonmap[tvg_name] = tvg_value
                            else:
                                jsonmap[tvg_name] = {"v":tvg_value, "t":tvg_type}
                    return jsonmap
                else:
                    with codecs.open(group_source, 'r') as jsonFile:
                        group_source = jsonFile.read()
            try:
                return MTestGloabel.jsDecoder.decode(group_source)
            except:pass
            raise ValueError('Bad JSON "%s"' % group_source)
        return copy.deepcopy(group_source) if group_source != None else {}

    def getjson_locator(self, key_locator, value_locator=None, match_key=None, max_range=100):
        if value_locator == None or match_key == None:
            return eval('self' + key_locator)
        else:
            for index in range(0, max_range):
                try:
                    if match_key == eval("self" + key_locator % index):
                        return eval("self" + value_locator % index)
                except:
                    return None

    @staticmethod
    def TryGetVal(jsonObj, jKey, defVal=None):
        try:
            return jsonObj[jKey]
        except:
            return defVal

    def __getitem__(self, typeKey, isValue=True):
        tempItem = self.__prop__[typeKey]

        if isValue and self.is_value:
            try:
                return tempItem[self.vWord]
            except:pass
        return tempItem

    def __delitem__(self, typeKey):
        self.__prop__.__delitem__(typeKey)

    def __setitem__(self, typeKey, value):
        self.__prop__[typeKey] = value

    def __len__(self):
        return len(self.__prop__)

    def __repr__(self):
        return str(self)

    def __str__(self, indent=2, isJsonFormat=False):
        if indent > 0:
            if isJsonFormat:
                MTestGloabel.jsEncoder.indent = indent
                return MTestGloabel.jsEncoder.encode(self.__prop__)
            return pprint.pformat(self.__prop__, indent=indent)
        else:
            return self.__prop__.__str__()

    def keys(self):
        return self.__prop__.keys()

    def __contains__(self, typeKey):
        return self.__prop__.__contains__(typeKey)

    def GetType(self, typeKey):
        tempItem = self.__prop__[typeKey]

        if self.is_value and ((type(tempItem) is dict and tempItem.__contains__(self.vWord)) 
                or hasattr(tempItem, self.tWord)):
            return tempItem[self.tWord]

        return None

    def GetInt(self, typeKey):
        return int(self[typeKey])

    def GetBool(self, typeKey):
        return self[typeKey].lower() == "true"

    def ToFormatString(self, tvValueHandler=None, seperator=";", props=[]):
        tempProp = []
        if(len(props) == 0):
            tempProp = self.keys()
        else:
            tempProp = props
        countProp = 0
        propLen = len(tempProp)
        outputStr = ""
        for tType in tempProp:
            countProp += 1
            if tvValueHandler != None:
                tempStr = tvValueHandler(tType, self[tType])
                if tempStr == None:
                    continue
            else:
                tempStr = '%s:%s' % (tType, self[tType])
            if countProp <= propLen and outputStr != "":
                outputStr += seperator
            outputStr += tempStr

        return outputStr

    def SetByJsonLocaotr(self, keyLocator, tValue, useAppend=False):
        if useAppend:
            eval('self' + keyLocator).append(tValue)
        else:
            exec('self' + keyLocator + " = tValue")
