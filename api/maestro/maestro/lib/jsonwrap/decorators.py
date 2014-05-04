from django import http
from django.core.exceptions import PermissionDenied
from django.core.signals import got_request_exception
from django.core.handlers.base import BaseHandler
from functools import wraps
from .exceptions import BadRequest
from json import dumps

def view(methods=[]):
    def _inner(func):

        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            try:
                status = 200
                headers = {
                        'Access-Control-Allow-Origin': '*',
                    }

                if len(methods) > 0 and request.method not in methods:
                    data = http.HttpResponseNotAllowed('')
                else:
                    # Call the view
                    data = func(request, *args, **kwargs)

                # Isn't thrown as an exception, but instead returned
                if isinstance(data, http.HttpResponseNotAllowed):
                    return http.HttpResponse(dumps({
                            'error': 405,
                            'msg': 'HTTP method not allowed.',
                        }), status=405, content_type='application/json')

                # Allow for multiple results
                if isinstance(data, tuple):
                    if len(data) == 2:
                        data, status = data
                    elif len(data) == 3:
                        data, status, headers = data
                    else:
                        raise Exception('Too many return values from view')

                if not isinstance(data, dict):
                    raise Exception('Expected dictionary')

                resp = http.HttpResponse(dumps(data), status=status, content_type='application/json')
                for h in headers:
                    resp[h] = headers[h]

            except Exception as e:
                if isinstance(e, BadRequest):
                    resp = http.HttpResponseBadRequest(dumps({
                            'error': 400,
                            'msg': str(e),
                        }), content_type='application/json')
                elif isinstance(e, PermissionDenied):
                    resp = http.HttpResponseForbidden(dumps({
                            'error': 403,
                            'msg': str(e),
                        }), content_type='application/json')
                elif isinstance(e, http.Http404):
                    resp = http.HttpResponseNotFound(dumps({
                            'error': 404,
                            'msg': str(e),
                        }), content_type='application/json')
                else:
                    got_request_exception.send(sender=BaseHandler, request=request)
                    resp = http.HttpResponseServerError(dumps({
                            'error': 500,
                            'msg': 'Internal server error.',
                        }), content_type='application/json')

            return resp
        return _wrapped
    return _inner
