from django.urls import path, re_path
from cakeshop import views
from django.conf import settings
from django.conf.urls.static import static
from .views import register, UserLoginView, UserLogoutView


urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^cakes/$", views.CakeListView.as_view(), name="cakes"),
    re_path(r"^cake/(?P<pk>\d+)$", views.CakeDetailView.as_view(), name="cake-detail"),
    path('cake/<int:cake_id>/add_review/', views.add_review, name='add-review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit-review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete-review'),
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
