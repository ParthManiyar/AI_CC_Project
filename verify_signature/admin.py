from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Slip
from django.contrib.auth.models import Group

class Slip_Admin(admin.ModelAdmin):
    list_display=('Account_Number','Signature',)
    search_fields=('Account_Number',)
    

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Add,Update or Delete Record'}
        return super(Slip_Admin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(Slip,Slip_Admin)
admin.site.unregister(Group)
admin.site.site_header = "Bank Administration"
admin.site.site_title="Bank Dashboard"
admin.site.index_title = ""
admin.site.change_title=""

