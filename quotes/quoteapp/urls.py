from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:page>', views.main, name='main_paginate'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
    path('author/<str:author_name>/', views.author_info, name='author'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
]
