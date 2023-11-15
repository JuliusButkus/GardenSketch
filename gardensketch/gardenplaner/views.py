from typing import Any
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from . import models, forms
from django.views.decorators.csrf import csrf_protect


def index(request: HttpRequest):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }
    return render(request, 'gardenplaner/index.html', context)
