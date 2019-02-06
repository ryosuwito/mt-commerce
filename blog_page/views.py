from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from catalog.models import Product
from settings.models import HeaderLink, FooterLink

from .models import Page, Article

import random

def blog_index(request):
    return HttpResponse(Article.objects.all().count())

def page(request, page_slug):
    article =  get_object_or_404(Page, slug=page_slug)
    return render_article(request, article)

def article(request, article_slug):
    article =  get_object_or_404(Article, slug=article_slug)
    return render_article(request, article)

def render_article(request, article):
    header_links = HeaderLink.objects.all()
    hlinks = {}
    for link in header_links :
        if not link.page:
            hlinks['%s'%link.pos] = {
                'addr':link.addr, 
                'name':link.name
            }
        else:
            hlinks['%s'%link.pos] = {
                'addr':link.page.get_url(), 
                'name':link.page.title
            }
    flinks = FooterLink.objects.all()
    all_product = Product.objects.filter(is_archived=False)
    all_article = Article.objects.filter(is_published=True).exclude(slug=article.slug)
    if len(all_product) >= 5:
        other_product = random.sample(list(all_product), 4)
    else:
        other_product = random.sample(list(all_product), len(all_product))

    if len(all_article) >= 4:
        other_article = random.sample(list(all_article), 3)
    else:
        other_article = random.sample(list(all_article), len(all_article))

    return render(request, 'blog_page/blog_detail.html', 
            {"article":article,
             'hlinks':hlinks,
             'flinks':flinks, 
             'other_article':other_article,
             'other_product':other_product})
