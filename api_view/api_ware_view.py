from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_view.ware_view_help import TaoBao

@csrf_exempt
def api_taobao(request):
    ware = request.get('ware', '')
    price_start = request.get('price_start', '')
    price_end = request.get('price_end', '')

    url = 'https://s.taobao.com/search?q=%s&filter=reserve_price%5B%s%%2C%s%%5D&s=' %(ware, price_start, price_end)
    tb = TaoBao(tb_url=url)
    data = tb._request()
