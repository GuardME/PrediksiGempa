from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.core.serializers import serialize
from django.template.context import Context
import pandas as pd
from gempaBumiApp.models import Gempa, Prediksi_Gempa

# Create your views here.
def gempa_dataset(request):
    gempa = serialize('json', Gempa.objects.order_by("id")[:1000])
    return HttpResponse(gempa, content_type='json')

def gempa_dataset_prediksi(request):
    gempa_predict = serialize('json', Prediksi_Gempa.objects.all()[:1000])
    return HttpResponse(gempa_predict, content_type='json')


def gempa_dataset_pred_risk(request):
    quake_risk = serialize('json', Prediksi_Gempa.objects.filter(Mag__gt=6.5))
    return HttpResponse(quake_risk, content_type='json')

def pred_score():
    score = Prediksi_Gempa.objects.all()[0]
    ret_score = str(round(score.Score, 2))
    return ret_score

def home(request):
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'pred_score': pred_score()
        }
    )