from django.urls import path
from source.views.api import ApiView

urlpatterns = [
    path('stocks/', ApiView.as_view()),
]
