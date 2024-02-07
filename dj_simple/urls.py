"""
URL configuration for dj_simple project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.views import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.views'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads.views import ads as ads_view
from ads.views import category as cat_view
from ads.views import users as user_view
from ads.views import locations as loc_view

router = routers.SimpleRouter()
router.register("location", loc_view.LocationsListView)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),

    path('cat/', cat_view.CategoryListView.as_view()),
    path('cat/create/', cat_view.CategoryCreateView.as_view()),
    path('cat/<int:pk>/', cat_view.CategoryDetailView.as_view()),
    path('cat/<int:pk>/update/', cat_view.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', cat_view.CategoryDeleteView.as_view()),

    path('ads/', ads_view.AdsListView.as_view()),
    path('ads/<int:pk>/', ads_view.AdsDetailView.as_view()),
    path('ads/<int:pk>/update/', ads_view.AdsUpdateView.as_view()),
    path('ads/<int:pk>/delete/', ads_view.AdsDeleteView.as_view()),
    path('ads/<int:pk>/upload_images/', ads_view.AdsUploadImageView.as_view()),
    path('ads/create/', ads_view.AdsCreateView.as_view()),

    path('user/', user_view.UserListView.as_view()),
    path('user/create/', user_view.UserCreateView.as_view()),
    path('user/<int:pk>/', user_view.UserDetailView.as_view()),
    path('user/<int:pk>/update/', user_view.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', user_view.UserDestroyView.as_view()),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
