from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from erm_auth.models import Profile
from portals.forms import ContactForm


def landpage(request):
    user = request.user
    # next_url = request.GET.get('next', '')
    if not user.is_authenticated():
        return redirect("erctrl_home")
    if user.is_superuser:
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile()
        profile.user = user
        profile.save()
        return redirect("landpage_administration")

    # if next_url:
    #     return redirect("tablet_live_rooms")

    if user.profile.is_administrator():
        return redirect("landpage_administration")

    if user.profile.is_normal_user():
        return redirect("landpage_user")

    return redirect("landpage_guest")


def landpage_administration(request):
    return redirect("dashboard_rooms")


def landpage_user(request):
    return redirect("dashboard_user_rooms")


def landpage_guest(request):
    if request.user.profile.is_administrator():
        base_portal = "portals/base_administration_portal.html"
    else:
        base_portal = "portals/base_user_portal.html"
    ctx = {'base_portal': base_portal}
    return render(request, "portals/guest/landpage.html", ctx)


class ContactView(FormView):
    template_name = 'landing/contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        domain = self.request.environ.get('HTTP_ORIGIN')
        form.send_contact_email(domain)
        return super().form_valid(form)
