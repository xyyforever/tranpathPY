from django.core import serializers
import json
from system.helpClass import formatStr
#queryset对象转成列表
def queryset_to_list(queryset_obj):
    data_json = serializers.serialize('json',queryset_obj)
    data_dict = json.loads(data_json)

    data_list = []
    for data in data_dict:
        data['fields']['id'] = data['pk']
        data_list.append(data['fields'])
        for key in data['fields']:
            data['fields'][key] = formatStr(data['fields'][key])
    return data_list
    