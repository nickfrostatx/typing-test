from django.core.exceptions import PermissionDenied
from functools import wraps
from . import util
from maestro.lib.jsonwrap.decorators import view

def auth_view(methods):
    def _inner(func):

        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            try:
                key = request.GET['key']
            except KeyError:
                try:
                    key = request.POST['key']
                except KeyError:
                    raise PermissionDenied('Must supply a session key.')
            uid = util.get_session_uid(key)
            if not uid:
                raise PermissionDenied('Invalid session key.')
            request.uid = uid
            return func(request)

        return view(methods)(_wrapped)

    return _inner
