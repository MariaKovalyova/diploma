from django.urls import path

from todolist.bot import views

urlpatterns = [
    path('verify', views.BotVerifyView.as_view()),
]

