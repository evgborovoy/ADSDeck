import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ads, User, Category


class AdsListView(ListView):
    model = Ads
    queryset = Ads.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('author').order_by('-price')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 0)
        page_object = paginator.get_page(page_number)

        ads = []
        for ad in page_object:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "author_id": ad.author_id,
                "description": ad.description,
                "price": ad.price,
                "is_published": ad.is_published,
                "images": ad.images.url if ad.images else None,
                "category_id": ad.category_id,
            })

        response = [{
            "items": ads,
            "num_pages": page_object.paginator.num_pages,
            "total": page_object.paginator.count,
        }]
        return JsonResponse(response, safe=False)



class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "author_id": ad.author_id,
            "description": ad.description,
            "price": ad.price,
            "is_published": ad.is_published,
            "images": ad.images.url if ad.images else None,
            "category_id": ad.category_id,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsCreateView(CreateView):
    model = Ads
    fields = ("name", "author", "price", "description", "is_published", "category")

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        # author = get_object_or_404(User, ad_data["author_id"])
        # category = get_object_or_404(Category, ad_data["category_id"])
        print(ad_data)
        new_ad = Ads.objects.create(
            name=ad_data["name"],
            author=get_object_or_404(User, pk=ad_data['author_id']),
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category=get_object_or_404(Category, pk=ad_data['category_id']),
        )
        return JsonResponse({
            "id": new_ad.id,
            "name": new_ad.name,
            "author": new_ad.author.username,
            "author_id": new_ad.author_id,
            "description": new_ad.description,
            "price": new_ad.price,
            "is_published": new_ad.is_published,
            "images": new_ad.images.url if new_ad.images else None,
            "category_id": new_ad.category_id,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ("name", "description", "price")

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.description = ad_data["description"]
        self.object.price = ad_data["price"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "author_id": self.object.author_id,
            "description": self.object.description,
            "price": self.object.price,
            "is_published": self.object.is_published,
            "images": self.object.images.url if self.object.images else None,
            "category_id": self.object.category_id,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({
            "status": "ok"
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsUploadImageView(UpdateView):
    model = Ads
    fields = ("images",)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.images = request.FILES.get('images', None)
        self.object.save()

        return JsonResponse({
            "status": "ok"
        })