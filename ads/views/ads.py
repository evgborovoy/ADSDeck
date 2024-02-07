import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView

from ads.models import Ads, User, Category
from ads.serializers import AdsListSerializer, AdsDetailSerializer, AdsDestroySerializer


class AdsListView(ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsListSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat", None)
        if categories:
            self.queryset = self.queryset.filter(
                category_id__in=categories
            )
        text = request.GET.get("text", None)
        if text:
            self.queryset = self.queryset.filter(
                name__icontains=text
            )
        location = request.GET.get("location", None)
        if location:
            self.queryset = self.queryset.filter(
                author__locations__name__icontains=location
            )
        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        if price_from:
            self.queryset = self.queryset.filter(
                price__gte=price_from
            )
        if price_to:
            self.queryset = self.queryset.filter(
                price__lte=price_to
            )

        return super().get(request, *args, **kwargs)


class AdsDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDetailSerializer

    # model = Ads
    #
    # def get(self, request, *args, **kwargs):
    #     ad = self.get_object()
    #
    #     return JsonResponse({
    #         "id": ad.id,
    #         "name": ad.name,
    #         "author": ad.author.username,
    #         "author_id": ad.author_id,
    #         "description": ad.description,
    #         "price": ad.price,
    #         "is_published": ad.is_published,
    #         "images": ad.images.url if ad.images else None,
    #         "category_id": ad.category_id,
    #     })


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



class AdsDeleteView(DestroyAPIView):
    queryset = AdsDestroySerializer
    serializer_class = AdsDestroySerializer



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
