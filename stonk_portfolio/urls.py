from django.urls import path
from django.conf.urls import url

from . import views
from stonk_portfolio.views import WatchList

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.login_view, name="login"),
     path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('watchlist/', WatchList.as_view(), name="watchlist"),
    path("search/", views.search, name="search"),
    path("stock/<str:symbol>", views.stock, name="stock"),
]