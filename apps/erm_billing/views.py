from __future__ import unicode_literals
import stripe
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from djstripe.models import Customer, Card
from erm_auth.views import BaseLoginRequired
from erm_billing.forms import BillingForm


class BillingUpdate(BaseLoginRequired, View):
    template_name = "billing/create_billing.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        customer, created = Customer.get_or_create(
            subscriber=user)
        try:
            cardId = customer.default_source.id
        except AttributeError:
            cardId = None

        form = BillingForm()
        publishable_key = settings.STRIPE_LIVE_PUBLIC_KEY
        return render(request, self.template_name, {
            'form': form, 'cardId': cardId,
            'publishable_key': publishable_key})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = BillingForm(request.POST or None)
        if form.is_valid():
            exp_month = request.POST.get('exp_month')
            exp_year = request.POST.get('exp_year')
            card_no = request.POST.get('card_no')
            cvc = request.POST.get('cvc')
            stripe.api_key = settings.STRIPE_LIVE_PUBLIC_KEY
            cardId = None
            customer_id = user.profile.stripe_id
            customer, created = Customer.get_or_create(
                subscriber=user)
            try:
                card_id = customer.default_source.stripe_id
                cardId = customer.default_source.id
                customer = stripe.Customer.retrieve(customer_id)
                card = customer.sources.retrieve(card_id)
                card.exp_month = exp_month
                card.exp_year = exp_year
                new_stripe_card = card.save()
                Card.sync_from_stripe_data(new_stripe_card)
                messages.success(
                    request, 'Billing info was successfully updated!')
            except stripe.error.CardError as err:
                card_msg = err._message
                messages.error(self.request, card_msg)
            except stripe.error.InvalidRequestError as err:
                card_msg = 'You can not add cards, you can update the card only.'
                messages.error(self.request, card_msg)
            except AttributeError as err:
                card_msg = err._message
                messages.error(self.request, card_msg)
            return redirect('update_billing')

        return render(request, self.template_name, {
            'form': form, 'cardId': cardId})
