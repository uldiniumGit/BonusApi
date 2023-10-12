from django.urls import path
from .views import RandomBonusView

app_name = 'bonusAPIapp'

urlpatterns = [
    path('random-bonus/', RandomBonusView.as_view()),
]
