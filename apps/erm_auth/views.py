# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import stripe

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.views.generic.edit import DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import (login as auth_login,
                                 update_session_auth_hash)
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.http import HttpResponse
from django.db import transaction
from django.conf import settings

from djstripe.models import Event, Customer
from djstripe.signals import WEBHOOK_SIGNALS

from erm_auth.forms import UserRegistrationForm, UserUpdateForm
from users.forms import UserRoleForm
from erm_auth.models import Profile
from users.models import Employee
from erm_billing.forms import BillingForm
from erm_business.forms import BusinessForm
from users.models import UserRole
from custom_payments.forms import CardForm
from helpers.tokens import account_activation_token


@method_decorator(lambda x: login_required(
    x, login_url=reverse_lazy('user_login')), name='dispatch')
class BaseLoginRequired(View):
    pass


@login_required
def create_user(request, user_id=None):

    try:
        user = User.objects.get(id=user_id)
        form = UserUpdateForm(request.POST or None, instance=user)
    except User.DoesNotExist:
        user = None
        form = UserRegistrationForm(request.POST or None)
    try:
        role_form = UserRoleForm(request.POST or None,
                                 instance=user.profile.roles.first())
    except (Profile.DoesNotExist, AttributeError):
        role_form = UserRoleForm(request.POST or None)
    if form.is_valid():
        try:
            user_form = form.save()
            role_obj = role_form.save(commit=False)
            role_obj.user_profile = user_form.profile
            role_obj.save()
            try:
                employee_obj = Employee.objects.get(
                    employee=user_form.profile, parent=request.user.profile)
                employee_obj.employee = user_form.profile
                employee_obj.save()
            except (Employee.DoesNotExist, AttributeError):
                employee = Employee()
                employee.employee = user_form.profile
                employee.parent = request.user.profile
                employee.save()

            messages.success(request, _(
                'User was successfully added!'))
        except IntegrityError:
            messages.success(request, _(
                'Email already used! please add new email'))

        return redirect('users-settings-management')
    if user_id:
        return render(request, 'users/edit_user.html', {
            'form': form, 'role_form': role_form, 'user_id': user_id})
    return render(request, 'users/signup.html', {
        'form': form, 'role_form': role_form})


class UserListView(BaseLoginRequired, ListView):
    template_name = "users/user_list.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            # user_ids = Profile.objects.filter(
            #     stripe_id__isnull=False).values_list("user", flat=True)

            users = User.objects.filter(is_superuser=False)
            business_user_ids = [
                user.id for user in users if user.profile.is_administrator()]
            business_users = User.objects.filter(id__in=business_user_ids)
            return business_users
        user_employees = self.request.user.profile.user_parent_employee.values_list(
            "employee__user", flat=True)
        return User.objects.filter(id__in=user_employees, is_superuser=False)


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/dashboard/rooms/'
    form_class = AuthenticationForm
    template_name = "users/login.html"

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        _next = request.GET.get('next', '')
        if request.user.is_authenticated():
            if _next and 'tablet' in _next:
                redirect_to = 'tablet_live_rooms'
            else:
                redirect_to = 'main_dashboard'
            # redirect_to = '%s?next=%s' % ('/', _next) if _next and len(_next) > 0 else 'main_dashboard'
            return redirect(redirect_to)
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # if not form.get_user().profile.subscribed:
        #     messages.success(self.request, _(
        #         "You haven't subscribe plan"))
        #         return redirect("login")
        auth_login(self.request, form.get_user())
        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        if self.request.user.is_authenticated():
            next_parameter = self.request.environ.get('QUERY_STRING')
            if next_parameter and 'tablet' in next_parameter and len(next_parameter) > 0:
                redirect_to = 'tablet_live_rooms'
            else:
                redirect_to = 'main_dashboard'
            return redirect(redirect_to)

        return super(LoginView, self).form_valid(form)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _(
                'Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)

    if request.user.is_superuser or request.user.profile.is_administrator():
        base_portal = "portals/base_administration_portal.html"
    else:
        base_portal = "portals/base_user_portal.html"
    return render(request, 'users/change_password.html', {
        'form': form,
        'base_portal': base_portal
    })


class UserDeleteView(BaseLoginRequired, DeleteView):
    template_name = "users/user_confirm_delete.html"
    model = User
    success_url = reverse_lazy('users-settings-management')
    permission_required = 'user.delete'


class UserSignupWithSubscription(FormView):
    template_name = 'users/user_signup.html'
    form_class = UserRegistrationForm

    # On successful form submission
    def get_success_url(self):
        return reverse('user_login')

    # Validate forms
    def form_valid(self, form):
        stripe.api_key = settings.STRIPE_LIVE_PUBLIC_KEY
        ctx = self.get_context_data()
        form_billing = ctx['form_billing']
        form_business = ctx['form_business']
        form_stripe = ctx['form_stripe']
        plan_id = self.kwargs.get("plan_id")
        coupon_code = self.request.POST.get('coupon_code')
        if form_stripe.is_valid() and form_billing.is_valid() and form_business.is_valid() and form.is_valid():
            try:
                with transaction.atomic():
                    self.object = form.save()  # saves Father and Children
                    customer = Customer.create(
                        subscriber=self.object)
                    customer.add_card(form_stripe.cleaned_data.get(
                        'stripe_token', None))
                    customer.subscribe(plan_id, coupon=coupon_code)
                    self.object.profile.stripe_id = customer.stripe_id
                    self.object.profile.last_4_digits = form_stripe.cleaned_data['last_4_digits']
                    self.object.profile.subscribed = self.object.profile.has_active_subscription
                    self.object.profile.save()
                    customer._sync_invoices()
                    customer._sync_charges()
                    customer._sync_cards()
            except IntegrityError:
                # form.addError(form.cleaned_data['email'] + ' is already a member')
                messages.error(self.request, _(
                    form.cleaned_data['email'] + ' is already a member'))
                return self.render_to_response(
                    self.get_context_data(form=form))
            except stripe.error.CardError as err:
                card_msg = 'Invalid card entry:' + err._message
                messages.error(self.request, _(card_msg))
                return self.render_to_response(
                    self.get_context_data(form=form))
            except stripe.error.InvalidRequestError as err:
                card_msg = 'Invalid coupon entry:' + err._message
                messages.error(self.request, _(card_msg))
                return self.render_to_response(
                    self.get_context_data(form=form))
            else:
                business = form_business.save(commit=False)
                business.user = self.object
                business.save()
                UserRole.objects.create(
                    role='admin', user_profile=self.object.profile)
                superusers = User.objects.filter(is_superuser=True)
                if superusers:
                    Employee.objects.create(
                        employee=self.object.profile,
                        parent=superusers.first().profile)
                # return reverse('djstripe:subscribe')
                # Email activation feature
                # current_site = get_current_site(self.request)
                mail_subject = 'Activate your escaperoom account.'
                message = render_to_string('users/account_active_email.html', {
                    'user': self.object,
                    # 'domain': current_site.domain,
                    'domain': self.request.environ.get('HTTP_ORIGIN'),
                    'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
                    'token': account_activation_token.make_token(self.object),
                })
                to_email = form.cleaned_data.get('email')
                send_mail(
                    mail_subject,
                    message,
                    'no-reply@example.com',
                    [to_email],
                    fail_silently=False,
                )
                messages.success(self.request, _(
                    'Thank You for subscribing! Please activate your account.')
                )
                return redirect(self.get_success_url())
        else:
            return super(UserSignupWithSubscription, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserSignupWithSubscription, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_LIVE_PUBLIC_KEY
        context['plan_id'] = self.kwargs.get('plan_id')
        if self.request.POST:
            context['form'] = UserRegistrationForm(self.request.POST)
            context['form_billing'] = BillingForm(self.request.POST)
            context['form_business'] = BusinessForm(self.request.POST)
            context['form_stripe'] = CardForm(self.request.POST)
        else:
            context['form'] = UserRegistrationForm()
            context['form_billing'] = BillingForm()
            context['form_business'] = BusinessForm()
            context['form_stripe'] = CardForm()
        return context


def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@method_decorator(csrf_exempt)
@receiver(WEBHOOK_SIGNALS['charge.succeeded'])
def charges_succeeded(sender, **kwargs):
    event_json = json.loads(sender.body.decode('utf-8'))
    # req = event_json['request']
    stripe_id = event_json['data']['object'].get('id')
    type_t = event_json.get('type', '')
    livemode = int(event_json.get('livemode', 0))
    customer_id = event_json['data']['object'].get('customer', '')
    description = event_json['data']['object'].get('description', '')
    received_api_version = event_json.get('api_version', '')
    request_id = event_json['request'].get('id', 1)
    # stripe_timestamp = event_json.get('created')
    # idempotency_key = req.get('idempotency_key', '')
    # created = event_json.get('created')

    #get primery key for customer:
    # try:
    if type_t == 'charge.succeeded':
        try:
            customer_pk_id = Customer.objects.get(stripe_id=customer_id)
            signup_user = Profile.objects.get(stripe_id=customer_id)
            Event.objects.create(
                stripe_id=stripe_id, type=type_t, livemode=livemode,
                webhook_message='Payment successfull', processed=True,
                description=description,
                received_api_version=received_api_version,
                request_id=request_id, customer_id=customer_pk_id.id)
            send_payement_confirmation_email(
                'Your payment has been successfully completed', signup_user)
        except:
            HttpResponse(status=422)
    return HttpResponse(status=200)


def send_payement_confirmation_email(webhook_message,user):
        user_in = User.objects.get(id=user.user_id)
        mail_subject = 'Payment successfull'
        message = render_to_string('users/webhookresponse.html', {
            'user': user_in.username,
            'msg': "Hi %s, %s" % (user_in.username, webhook_message)
        })

        to_email = user_in.email
        return send_mail(
            mail_subject,
            message,
            'from@example.com',
            [to_email],
            fail_silently=False,
        )


@method_decorator(csrf_exempt)
@receiver(WEBHOOK_SIGNALS['customer.subscription.created'])
def subscription_created(sender, **kwargs):
    print('===============================customer.subscription.created')
    return HttpResponse(status=200)
