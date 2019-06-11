import json
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class TokenValidateView(View):

    def post(self, request, *args, **kwargs):
        if request.POST.get('session_key', None) == request.session.session_key:
            return HttpResponse(json.dumps({'status': True, 'messgae': 'Access token Validated'})
                                )
        else:
            return HttpResponse(json.dumps({'status': False, 'messgae': 'Invalid access Token'}))

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TokenValidateView, self).dispatch(request, *args, **kwargs)
