from django.contrib.sessions import middleware
from django.conf import settings
from django.utils.importlib import import_module
from django.middleware import locale

from django.core.urlresolvers import is_valid_path
from django.http import HttpResponseRedirect
from django.utils.cache import patch_vary_headers
from django.utils import translation


class SubDomainSessionMiddleware(middleware.SessionMiddleware):
    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        if session_key is None:
            # Look for old cookie in request for auth purposes.
            session_key = request.COOKIES.get('sessionid', None)

        request.session = engine.SessionStore(session_key)


class LocaleMiddleware(locale.LocaleMiddleware):
    """ Override locale middleware process response.

    This middleware tries to reidrect to the i18n version of the url if
    the response has a 404 status.

    For us every i18n url will be valid, since it serves our ember application.
    So all 404 generated by the api will be redirected to our ember application.
    Here we make sure that if the 404 was generated by an existing view, we do
    not redirect. That way api calls that generate a 404 will be left alone.
    """
    def process_response(self, request, response):
        language = translation.get_language()
        language_from_path = translation.get_language_from_path(
            request.path_info, supported=self._supported_languages
        )
        if (response.status_code == 404 and not language_from_path
                and self.is_language_prefix_patterns_used()):
            urlconf = getattr(request, 'urlconf', None)
            language_path = '/%s%s' % (language, request.path_info)
            path_valid = is_valid_path(language_path, urlconf)

            if (not path_valid and settings.APPEND_SLASH
                    and not language_path.endswith('/')):
                path_valid = is_valid_path("%s/" % language_path, urlconf)

            # If the redirect path is valid, and the 404 was not generated
            # by a view, we redirect.
            if path_valid and not is_valid_path(request.path_info):
                language_url = "%s://%s/%s%s" % (
                    'https' if request.is_secure() else 'http',
                    request.get_host(), language, request.get_full_path())
                return HttpResponseRedirect(language_url)

        if not (self.is_language_prefix_patterns_used()
                and language_from_path):
            patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response


