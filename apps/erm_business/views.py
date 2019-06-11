# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from erm_business.models import Business
from erm_auth.views import BaseLoginRequired
from erm_business.forms import BusinessForm


class BusinessCreate(BaseLoginRequired, View):
    template_name = "business/create_business.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            form = BusinessForm(request.POST or None,
                                instance=user.user_business)
        except (Business.user.RelatedObjectDoesNotExist, AttributeError):
            form = BusinessForm(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            form = BusinessForm(request.POST or None,
                                instance=user.user_business)
        except (Business.user.RelatedObjectDoesNotExist, AttributeError):
            form = BusinessForm(request.POST or None)
        if form.is_valid():
            obj_business = form.save(commit=False)
            obj_business.user = user
            obj_business.save()
            messages.success(
                request, 'Business info was successfully updated!')
            return redirect('account_settings')

        return render(request, self.template_name, {'form': form})
