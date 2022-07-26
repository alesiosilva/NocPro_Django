from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls'), name='home'),
    path('centreon/', include('apps.centreon.urls')),
    path('acionamentos/', include('apps.acionamentos.urls')),
    path('topdesk/', include('apps.topdesk.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

]