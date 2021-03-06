# -*- coding: utf-8 -*-
from __future__ import division
import random, math
from django.core.urlresolvers import resolve
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, Count
from django.conf import settings
from web import models, utils
from web.constants import *

def globalContext(request, nav=NAV):
    rainbow = utils.getRainbowFromSize(len(nav))
    return {
        'current': resolve(request.path_info).url_name,
        'static_url': (settings.STATIC_FULL_URL + settings.STATIC_URL).replace('//static', '/static'),
        'site_name': 'db0.company',
        'site_description': 'Deby Lepage Official Website',
        'debug': settings.DEBUG,
        'static_files_version': '3',
        'rainbow': [(
            (index * (100/len(RAINBOW))),
            ((index + 1) * (100 / (len(RAINBOW)))),
            color,
        ) for index, color in enumerate(RAINBOW)],
        'nav': [tuple(list(info) + [rainbow[index]]) for index, info in enumerate(nav)],
    }

def generic(request):
    context = globalContext(request)
    return render(request, context['current'] + u'.html', context)

def index(request):
    context = globalContext(request, nav=NAV[1:])
    context['hide_nav'] = True
    return render(request, 'index.html', context)

def projects(request):
    context = globalContext(request)
    context['projects'] = models.Project.objects.all().order_by('-current', '-end', '-beginning')
    if 'tags' in request.GET:
        context['hide_nav'] = True
        context['back'] = '/tags/' if 'project' not in request.GET else request.GET['project']
        context['tags'] = []
        for tag in request.GET['tags'].split(','):
            context['tags'].append(tag)
            context['projects'] = context['projects'].filter(tags__name=tag)
        if not context['projects']:
            context['tags'] = []
        context['tags'] = ' - '.join(context['tags'])
    return render(request, 'projects.html', context)

def project(request, id):
    context = globalContext(request)
    context['hide_nav'] = True
    context['back'] = '/projects/'
    context['project'] = get_object_or_404(models.Project.objects.all().prefetch_related(Prefetch('stats', to_attr='all_stats'), Prefetch('tags', to_attr='all_tags')), id=id)
    total = len(context['project'].all_stats)
    context['percent_stats'] = 100 / int(total / int(math.ceil(total / 4))) if total else 0
    return render(request, 'project.html', context)

def social(request):
    context = globalContext(request)
    context['socials'] = models.SocialLink.objects.all().order_by('small', '-importance', 'name')
    context['show_tags'] = 'show_tags' in request.GET
    if context['show_tags']:
        context['socials'] = context['socials'].prefetch_related(Prefetch('tags', to_attr='all_tags'))
    if 'tags' in request.GET:
        context['hide_nav'] = True
        context['back'] = '/socialtags/'
        context['tags'] = []
        for tag in request.GET['tags'].split(','):
            context['tags'].append(tag)
            context['socials'] = context['socials'].filter(tags__name=tag)
        if not context['socials']:
            context['tags'] = []
        context['tags'] = ' - '.join(context['tags'])
    for (link, color) in zip(context['socials'], utils.getRainbowFromSize(len(context['socials']))):
        link.color = color
        if context['show_tags']:
            link.tags_string = u', '.join([tag.name for tag in link.all_tags])
    return render(request, 'social.html', context)

def faq(request):
    context = globalContext(request)
    context['questions'] = models.FAQ.objects.all().order_by('-importance')
    for (question, color) in zip(context['questions'], utils.getRainbowFromSize(len(context['questions']))):
        question.color = color
    return render(request, 'faq.html', context)

def tags(request):
    context = globalContext(request)
    context['hide_nav'] = True
    context['back'] = '/projects/'
    context['filter_url'] = '/projects/'
    context['tags'] = models.Tag.objects.all().order_by('?')
    return render(request, 'tags.html', context)

def socialtags(request):
    context = globalContext(request)
    context['hide_nav'] = True
    context['back'] = '/social/'
    context['filter_url'] = '/social/'
    context['tags'] = models.SocialTag.objects.all().order_by('?')
    return render(request, 'tags.html', context)

def public(request):
    context = globalContext(request)
    context['publics'] = models.Public.objects.all().order_by('-modification')
    context['show_tags'] = 'show_tags' in request.GET
    context['ajax'] = 'ajax' in request.GET
    context['page'] = int(request.GET.get('page', 0))
    if not request.user.is_superuser:
        context['publics'] = context['publics'].filter(private=False)
    if context['show_tags']:
        context['publics'] = context['publics'].prefetch_related(Prefetch('tags', to_attr='all_tags'))
    if 'tags' in request.GET:
        context['hide_nav'] = True
        context['back'] = '/publictags/'
        context['tags'] = []
        for tag in request.GET['tags'].split(','):
            context['tags'].append(tag)
            context['publics'] = context['publics'].filter(tags__name=tag)
        if not context['publics']:
            context['tags'] = []
        context['tags'] = ' - '.join(context['tags'])
    if 'search' in request.GET:
        context['hide_nav'] = True
        context['back'] = '/publictags/'
        context['search'] = request.GET['search']
        context['publics'] = context['publics'].filter(name__icontains=context['search'])
    context['next_page'] = context['page'] + 20
    context['publics'] = context['publics'][context['page']:context['next_page']]
    for (public, color) in zip(context['publics'], utils.getRainbowFromSize(len(context['publics']))):
        public.color = color
        if context['show_tags']:
            public.tags_string = u', '.join([tag.name for tag in public.all_tags])
    context['extends'] = 'ajax.html' if context['ajax'] else 'base.html'
    return render(request, 'public.html', context)

def publictags(request):
    context = globalContext(request)
    context['hide_nav'] = True
    context['back'] = '/public/'
    context['filter_url'] = '/public/'
    context['tags'] = models.PublicTag.objects.all().order_by('?')
    context['allow_search'] = True
    return render(request, 'tags.html', context)
