
from django.contrib import admin
from django.urls import path, include
from flip import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flip.urls')),
    path('accounts/registration/', views.Registration, name='registration'),
    path('accounts/authentication/', views.Authentications, name='authentications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)