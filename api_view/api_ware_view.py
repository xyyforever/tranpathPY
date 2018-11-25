from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_view.ware_view_help import TaoBao

import json
@csrf_exempt
def api_taobao(request):
    try:
        ware = request.get('ware', '')
        price_start = request.get('price_start', '')
        price_end = request.get('price_end', '')

        tb = TaoBao()
        datas = tb._request_ware(ware,price_start,price_end)
        ware_list = tb._parse(datas)
        ware_pro = ['raw_title','detail_url','view_price','item_loc','view_sales','nick']
        wares = map(lambda x:dict([(key, x[key]) for key in ware_pro]), ware_list)

        return JsonResponse(json.dumps(list(wares)))
    except Exception as e:
        return JsonResponse(e)