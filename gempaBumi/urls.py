"""gempaBumi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls import url
import django.contrib.auth.views
import gempaBumiApp.views
from gempaBumiApp.views import gempa_dataset, gempa_dataset_prediksi, gempa_dataset_pred_risk


urlpatterns = [
    url(r'^$', gempaBumiApp.views.home, name='home'),
    url(r'^gempa_dataset/', gempa_dataset, name='gempadataset'),
    url(r'^gempa_dataset_pred/', gempa_dataset_prediksi, name='gempadatasetpred'),
    url(r'^gempa_dataset_pred_risk/', gempa_dataset_pred_risk, name='gempadatasetpredrisk'),
    path('admin/', admin.site.urls),
]
