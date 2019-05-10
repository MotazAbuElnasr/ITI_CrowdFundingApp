from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
# those imports are for the static files
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import  settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)