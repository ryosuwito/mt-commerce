from django.contrib import admin
from .models import Article, Page

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    exclude = ['slug']

class PageAdmin(admin.ModelAdmin):
    model = Page
    exclude = ['slug']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Page, PageAdmin)