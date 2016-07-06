islykill2
========
Utility to parse and verify Islykill authentication, using SAML 2.0

Requirements
==============

`signxml <https://github.com/kislyuk/signxml>`_

Installation
==============

:code:`pip install islykill2`

Add islykill2 to your INSTALLED_APPS if using django.

Usage
==============

Example in django

    from django.contrib.auth import login
    from django.http import HttpResponseRedirect
    from islykill2 import AuthenticationError, parse_saml

    try:
        response = parse_saml(
            request.POST['token'],
            ip
        )
        username = get_username_by_kt(response.kt)
        user = User.objects.get(username=username)
        backend = 'django.contrib.auth.backends.ModelBackend'
        user.backend = backend
        login(request, user)
        return HttpResponseRedirect('/home')
    except AuthenticationError:
        return HttpResponse(401)

Testing
=========

Please write some