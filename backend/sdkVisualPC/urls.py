"""
URL configuration for sdkVisualPC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from app.views import AppListView, AppSearchView, AppDeleteView, AppExcelView, AppDownloadView, LoginView, \
    PasswordChangeView, UserRegistrationView, AppUploadView, StatisticsView, StatisticsExcelView

urlpatterns = [
    # path("admin/", admin.site.urls),
    # todo：账号写成django自带的 改成数据库里的
    # path('login/', LoginView.as_view(), name='login'),
    # path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    # path('register/', UserRegistrationView.as_view(), name='register'),
    # 上传文件
    path('upload-app/', AppUploadView.as_view(), name='upload-app'),
    # 已解析库
    path('apps/list/', AppListView.as_view(), name='app-list'),
    path('apps/search/', AppSearchView.as_view(), name='app_search_list'),
    path('apps/delete/', AppDeleteView.as_view(), name='app_delete_list'),
    path('apps/excel/', AppExcelView.as_view(), name='app_excel_export'),
    path('apps/download/', AppDownloadView.as_view(), name='app_html_download'),
    # 统计数据
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('statistics/excel/', StatisticsExcelView.as_view(), name='statistics-excel'),


]
