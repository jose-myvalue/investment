# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('companies.html', views.companies, name='companies'),

    # Matches any html file 
    re_path(r'^.*\.*', views.pages, name='pages'),

]
