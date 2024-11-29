from django.contrib import admin
from django.contrib.admin.sites import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Elected"
    site_title = "My Admin"
    index_title = "ElectEd"

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = ['admin/custom_admin.css']
        return context
    
admin_site = CustomAdminSite()


