from atexit import register
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('twojprofil', views.twojprofil, name = 'twojprofil'),
    path('', views.base, name = 'base'),
    path('szukajlekarzy', views.szukajlekarzy, name = 'szukajlekarzy'),
    path('umowwizyte', views.umowwizyte, name = 'umowwizyte'),
    path('wizyta', views.wizyta, name = 'wizyta'),
    path('twojewizyty', views.twojewizyty, name = 'twojewizyty'),
    path('recenzje', views.recenzje, name = 'recenzje'),
    path('twojerecenzje', views.twojerecenzje, name = 'twojerecenzje'),
    path('wykresrecenzji', views.wykresrecenzji, name = 'wykresrecenzji'),
    path('dodajrecenzje', views.dodajrecenzje, name = 'dodajrecenzje'),
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('api/data', views.get_chart_data, name='get_chart_data'),
    path('wykresrecenzji', views.wykresrecenzji, name='wykresrecenzji'),
    path('save_to_csv', views.save_to_csv, name='save_to_csv'),
]