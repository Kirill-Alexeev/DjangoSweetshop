from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^cakes/$", views.CakeListView.as_view(), name="cakes"),
    re_path(r"^cake/(?P<pk>\d+)$", views.CakeDetailView.as_view(), name="cake-detail"),
    re_path(r"^reviews/$", views.ReviewListView.as_view(), name="reviews"),
    path('register/', views.RegisterUser.as_view(), name='register'),
]

# Добавляет URLConf для создания, редактирования и удаления отзыва
urlpatterns += [
    path('review/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/update/', views.ReviewUpdate.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', views.ReviewDelete.as_view(), name='review-delete'),
]

urlpatterns += [
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/<int:id>/', views.cart, name='cart'),
    path('order_success/', views.order_success, name='order_success'),
]