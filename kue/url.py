from django.urls import path
from kue.views import Home, Result, Predict
app_name = 'kue'

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('predict', Predict.as_view(), name='predict'),
    path('predict/<str:pk>', Result.as_view(), name='result'),
]