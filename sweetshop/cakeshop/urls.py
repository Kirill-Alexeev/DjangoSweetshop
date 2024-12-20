from django.urls import path, re_path
from cakeshop import views


urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^cakes/$", views.CakeListView.as_view(), name="cakes"),
    re_path(r"^cake/(?P<pk>\d+)$", views.CakeDetailView.as_view(), name="cake-detail"),
    # path('register/', views.RegisterUser.as_view(), name='register'),
]