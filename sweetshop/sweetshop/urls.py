from django.contrib import admin
from django.urls import include, path

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cakeshop/", include("cakeshop.urls")),
    path("", RedirectView.as_view(url="/cakeshop/", permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
