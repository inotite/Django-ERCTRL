import json
import stripe
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.views import View
from djstripe.models import Plan
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils.decorators import method_decorator
from users.forms import PlanForm
from erm_auth.views import BaseLoginRequired
from helpers.decorators import superadmin_required


@method_decorator(superadmin_required, name='dispatch')
class TrackerDetailView(BaseLoginRequired, DetailView):
    template_name = "users/user_tracker_details.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(TrackerDetailView, self).get_context_data(**kwargs)
        context['base_portal'] = self.request.user.profile.get_base_portal()
        return context


@method_decorator(superadmin_required, name='dispatch')
class TrackerView(BaseLoginRequired, TemplateView):
    template_name = "users/tracker.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(TrackerView, self).get_context_data(**kwargs)
        tracker_list = self.request.user.profile.get_graph_source_data()
        context['base_portal'] = self.request.user.profile.get_base_portal()
        context["tracker_list"] = json.dumps(tracker_list)

        return context


class PricingView(TemplateView):
    template_name = "users/pricing.html"


@method_decorator(superadmin_required, name='dispatch')
class PlanCreateView(BaseLoginRequired, View):
    template_name = "users/create_plan.html"

    def get(self, request, *args, **kwargs):
        form = PlanForm(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        plans = Plan.objects.all()
        stripe_id = 1
        try:
            if plans:
                stripe_id = plans.first().id + 1
            plan_args = request.POST.dict()
            plan_args['stripe_id'] = stripe_id
            plan_args.pop('csrfmiddlewaretoken')
            plan_args['amount'] = int(plan_args['amount'])
            Plan.create(**plan_args)
            return redirect("users_plan_list")
        except stripe.error.InvalidRequestError as err:
            card_msg = err._message
            messages.error(self.request, _(card_msg))
            return redirect("users_plan_create")


@method_decorator(superadmin_required, name='dispatch')
class PlanListView(BaseLoginRequired, ListView):
    template_name = "users/plan_list.html"
    model = Plan

    def get_context_data(self, **kwargs):
        context = super(PlanListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        stripe.api_key = settings.STRIPE_LIVE_PUBLIC_KEY
        try:
            plan_list = stripe.Plan.list()
            plans = [Plan.sync_from_stripe_data(pl) for pl in plan_list['data']]
        except stripe.error.PermissionError:
            plans = []
        return plans
