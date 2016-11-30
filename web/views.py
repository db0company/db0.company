# -*- coding: utf-8 -*-
from __future__ import division
import random, math
from django.core.urlresolvers import resolve
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
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
    context['percent_stats'] = 100 / int(total / int(math.ceil(total / 4)))
    return render(request, 'project.html', context)

def social(request):
    context = globalContext(request)
    context['socials'] = models.SocialLink.objects.all().order_by('small', '-importance', 'name')
    for (link, color) in zip(context['socials'], utils.getRainbowFromSize(len(context['socials']))):
        link.color = color
    return render(request, 'social.html', context)

def tags(request):
    context = globalContext(request)
    context['hide_nav'] = True
    context['back'] = '/projects/'
    context['tags'] = models.Tag.objects.all().order_by('?')
    return render(request, 'tags.html', context)
