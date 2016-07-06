from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from islykill2 import AuthenticationError, parse_saml

from .utils import get_username_by_kt  # Assumed you have this somewhere


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def islykill_login(request):
    try:
        response = parse_saml(
            request.POST['token'],
            get_client_ip(request)
        )
        username = get_username_by_kt(response.kt)
        user = User.objects.get(username=username)
        backend = 'django.contrib.auth.backends.ModelBackend'
        user.backend = backend
        login(request, user)
        return HttpResponseRedirect('/home')
    except AuthenticationError:
        return HttpResponse(401)
