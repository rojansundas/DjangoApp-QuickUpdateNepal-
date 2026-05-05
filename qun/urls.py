
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('news-details/<slug:slug>/', views.newsDetails, name="news-details"),
    path('latestnews/',views.LatestNews,name='latestnews'),
    path('category/<slug>',views.categoryDetails,name='category-details'),
    path('category/',views.category_list,name='category'),
    path('search/',views.search,name='search'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'),
    path('logout/',views.account_logout,name='logout'),
    path('register/', views.register,name='register'),
    path('profile/',views.profile,name='profile'),

]
