from django.contrib import admin
from django.urls import path, include
from users.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('users/', include('users.urls')),
    path('appeals/', include('appeals.urls')),
]
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))