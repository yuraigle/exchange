from django.http import JsonResponse
from exchange.server.models import *


def read_rate(request):
    try:
        c_from = request.GET.get("from", "").strip().upper()
        c_to = request.GET.get("to", "").strip().upper()
        c_amount = float(request.GET.get("amount", ""))
        cr = CurrencyRate.objects.get(code_from=c_from, code_to=c_to)
    except ValueError:
        return JsonResponse({"err": "Numerical amount expected"})
    except CurrencyRate.DoesNotExist:
        return JsonResponse({"err": "No data for this currency"})

    data = {'currency': c_to, 'amount': cr.rate * c_amount}
    return JsonResponse(data)
