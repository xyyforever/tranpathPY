# -*- coding: gbk -*-
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api_view.ware_view_help import TaoBao

import json
@csrf_exempt
def api_taobao(request):
    try:
        ware = request.GET.get('ware', '乐高')
        print('ware', ware)
        price_start = request.GET.get('price_start', '10')
        print('price_start', price_start)
        price_end = request.GET.get('price_end', '1000')
        print('price_end', price_end)

        tb = TaoBao()
        datas = tb._request_ware(ware_name=ware, price_start=int(price_start), price_end=int(price_end))
        ware_list = tb._parse(datas)
        ware_pro = ['raw_title','detail_url','view_price','item_loc','view_sales','nick']
        wares = map(lambda x:dict([(key, x[key]) for key in ware_pro]), ware_list)
        result = json.dumps(list(wares), ensure_ascii=False)
        return HttpResponse(result)
    except Exception as e:
        return HttpResponse({'result', e})