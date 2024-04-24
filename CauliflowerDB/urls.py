"""
URL configuration for CauliflowerDB project.

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from revproxy.views import ProxyView

from appcaulie import views

app_patterns = [
    path('home/', views.home),
    path('genome/', views.genome),
    path('sampleinfo/', views.sampleinfo),
    path('snpseek/', views.SnpSeek.as_view()),
    path('consensusseq/', views.ConsensusSeq.as_view()),
    path('search/', views.Search.as_view()),
    path('searchbyid/', views.SearchById.as_view()),
    path('batch/', views.Batch.as_view()),
    path('target/', views.Target.as_view()),
    path('download/', views.download),
    path('downloadfile/<str:filename>/', views.downloadfile),
    re_path(r'jbrowse/(?P<path>.*)$', ProxyView.as_view(upstream='http://taascr.myddns.me:7250/static/jbrowse/')),
    re_path(r'blast/(?P<path>.*)$', ProxyView.as_view(upstream=f'http://taascr.myddns.me:7253/')),  # 反向代理到blast
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cauliflowerdb/', include(app_patterns)),
    re_path(r'(?P<path_param>[\w-]+)$', views.revblast),  # 处理blast查询的返回参数
]