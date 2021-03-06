from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django import forms

from waiflike.models import SitePage

def source(request, slug):
    p = get_object_or_404(SitePage, slug = slug)
    return render(request, 'waiflike/source.html',
        dictionary = { 'page': p, 'site_name': settings.SITE_NAME })

class EditForm(forms.Form):
    body = forms.CharField(widget = forms.Textarea)

@login_required
def edit(request, slug):
    p = get_object_or_404(SitePage, slug = slug)
    perms = p.permissions_for_user(request.user)
    if not perms.can_edit():
        raise PermissionDenied

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            p.body = form.cleaned_data['body']
            p.save()
            return HttpResponseRedirect(p.url)
    else:
        form = EditForm(initial = { 'body': p.body })

    return render(request, 'waiflike/edit.html',
        dictionary =  {
            'page': p,
            'form': form,
            'site_name': settings.SITE_NAME,
        })
