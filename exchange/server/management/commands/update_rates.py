import urllib.request, json
from django.core.management import BaseCommand
from datetime import datetime
from exchange.server.models import *


class Command(BaseCommand):
    # CLI to update rates. Add it to daily cron
    api_key = "3832eda7590d6601dcdaba33e0d9cd18"
    currencies = ["USD", "EUR", "CZK", "PLN"]

    for c_from in currencies:
        api_url = "http://apilayer.net/api/live?access_key=%s&source=%s&currencies=%s&format=1" % (
            api_key, c_from, ','.join(currencies)
        )

        with urllib.request.urlopen(api_url) as url:
            data = json.loads(url.read().decode())
            # returns {'quotes': {'USDCZK': 20.523098, 'USDEUR': 0.810099, blahblahblah}}
            if 'quotes' in data:
                for cc, rate in data['quotes'].items():
                    c_to = cc[3:]

                    cr, created = CurrencyRate.objects.update_or_create(
                        code_from=c_from, code_to=c_to,
                        defaults={'rate': rate, 'last_update': datetime.today()}
                    )
                    cr.save()

    # free account only works for base=USD
    # so i'll just calculate rest values for testing purpose
    rest = currencies[:]
    rest.remove("USD")

    # CZKPLN = USDPLN / USDCZK
    for c_from in rest:
        for c_to in currencies:
            cr1 = CurrencyRate.objects.get(code_from="USD", code_to=c_from)
            cr2 = CurrencyRate.objects.get(code_from="USD", code_to=c_to)
            cr, created = CurrencyRate.objects.update_or_create(
                code_from=c_from, code_to=c_to,
                defaults={'rate': round(cr2.rate / cr1.rate, 6),
                          'last_update': min(cr1.last_update, cr2.last_update)}
            )
            cr.save()

    def handle(self, *args, **options):
        self.stdout.write("OK")
