
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.views.generic.base import RedirectView



urlpatterns = [ path('',views.Home),
                path('Signature_Verification/',views.Signature_Verfication),
                path('Account_Number/',views.Account_Number),
                path('api-auth/', include('rest_framework.urls')),
                path('Match_Signature/',views.Match_Signature),
                path('Add_Signature/',views.Add_Signature),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

