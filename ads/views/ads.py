import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ads


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):
    def get(self, request):
        if request.method == "GET":
            ads = Ads.objects.all()
            response = []
            for ad in ads:
                response.append({
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price
                })
            return JsonResponse(response, safe=False)

    def post(self, request):
        ads_data = json.loads(request.body)
        ads = Ads()
        ads.name = ads_data["name"]
        ads.price = ads_data["price"]
        ads.author = ads_data["author"]
        ads.description = ads_data["description"]
        ads.address = ads_data["address"]
        ads.is_published = True
        ads.save()
        return JsonResponse({
            "id": ads.id,
            "price": ads.price,
            "author": ads.author,
            "description": ads.description,
            "address": ads.address,
            "name": ads.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsDetailView(DetailView):
    model = Ads

    def get(self, *args, **kwargs):
        ad = self.get_object()
        response = ({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price
        })
        return JsonResponse(response, safe=False)
