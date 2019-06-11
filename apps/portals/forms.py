from django import forms
from django.core.mail import BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage


class ContactForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    # phone_number = forms.RegexField(
    #     regex=r'^\+?1?\d{9,15}$',
    #     error_message=("Phone number must be entered in the format:"
    #                    "'+999999999'. Up to 15 digits allowed."))
    def send_contact_email(self, domain):
        if bool(self.data):
            subject = self.data.get('subject', '')
            message = self.data.get('message', '')
            first_name = self.data.get('first_name', '')
            last_name = self.data.get('last_name', '')
            contect_html = render_to_string('users/contact_email.html', {
                'first_name': first_name,
                'last_name': last_name,
                'message': message,
                'site_domain': domain,
                'STATIC_URL': settings.STATIC_URL,
            })
            from_email = self.data.get('email', '')
            to_email = 'dchau2401@gmail.com'
            if subject and message and from_email:
                try:
                    email = EmailMessage(subject, contect_html, from_email, [to_email])
                    email.content_subtype = "html"
                    email.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/thanks/')
            else:
                # In reality we'd use a form class
                # to get proper validation errors.
                return HttpResponse('Make sure all fields are entered and valid.')
