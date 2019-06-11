# from django.shortcuts import render

# import stripe

# from django.conf import settings
# from django.core.urlresolvers import reverse_lazy
# from django.views.generic import FormView, TemplateView

# from djstripe.models import Customer

# from custom_payments.forms import CardForm


# class StripeMixin(object):
#     def get_context_data(self, kwargs):
#         context = super(StripeMixin, self).get_context_data(kwargs)
#         context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
#         return context


# class SuccessView(TemplateView):
#     template_name = 'payments/thank_you.html'


# class CustomerMixin(object):
#     def get_customer(self):
#         try:
#             return self.request.user.customer
#         except:
#             return Customer.create(self.request.user)


# class SubscribeView(StripeMixin, CustomerMixin, FormView):
#     template_name = 'payments/subscribe.html'
#     form_class = CardForm
#     success_url = reverse_lazy('thank_you')

#     def form_valid(self, form):
#         customer = self.get_customer()
#         customer.update_card(form.cleaned_data.get('stripe_token', None))
#         customer.subscribe('monthly')

#         return super(SubscribeView, self).form_valid(form)
