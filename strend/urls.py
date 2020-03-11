"""strend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cbond import views as cbond_view
from stock import views as stock_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cbond/', cbond_view.CbondListView.as_view(), name='cbond_list'),
    path('api/cbond/<int:pk>', cbond_view.CbondDetailView.as_view(), name='cbond_detail'),
    path('api/repurchase/', stock_view.RepurchaseListView.as_view(), name='repurchase_list'),
    path('api/repurchase/<int:pk>', stock_view.RepurchaseDetailView.as_view(), name='repurchase_detail'),
    path('api/index/', stock_view.IndexListView.as_view(), name='index_list'),
    path('api/kdata/index/<str:tscode>/<str:start>/', stock_view.KdataIndex.as_view(), name='kdata_index'),
]
