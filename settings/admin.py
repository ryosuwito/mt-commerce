from django.contrib import admin
from .models import HeaderLink, FooterLink, HomeLink

class HeaderLinkAdmin(admin.ModelAdmin):
    model = HeaderLink

class FooterLinkAdmin(admin.ModelAdmin):
    model = FooterLink

class HomeLinkAdmin(admin.ModelAdmin):
    model = HomeLink

admin.site.register(HeaderLink, HeaderLinkAdmin)
admin.site.register(FooterLink, FooterLinkAdmin)
admin.site.register(HomeLink, HomeLinkAdmin)