from django.core.exceptions import PermissionDenied
from maestro.lib.jsonwrap.decorators import view
from .decorators import auth_view
from maestro.lib.jsonwrap.exceptions import BadRequest
from . import util

@view(['GET'])
def root(request):
    return {'msg': 'This is the Maestro API.'}

@view(['POST'])
def create_user(request):
    email = request.POST['email']
    password = request.POST['password']
    uid = util.create_user(email)
    util.create_auth(email, password, uid)
    return {'success': True}

@view(['POST'])
def login(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        uid = util.auth(email, password)
        if uid is None:
            raise PermissionDenied('Invalid email and/or password.')
    except KeyError:
        uid = util.create_user()
    key = util.create_session(uid)
    return {'key': key}

@auth_view(['POST'])
def new_story(request):
    story = ('Tonight imagine me gown and all, fetchingly draped against the '
        'wall, the picture of sophisticated grace. I suddenly see him '
        'standing there, a beautiful stranger, tall and fair. I wanna stuff '
        'some chocolate in my face. But then we laugh and talk all evening, '
        'which is totally bizarre. Nothing like the life I\'ve lead so far. '
        'For the first time in forever, there\'ll be magic, there\'ll be fun. '
        'For the first time in forever, I could be noticed by someone. And I '
        'know it is totally crazy to dream I\'d find romance. But for the '
        'first time in forever, at least I\'ve got a chance.')
    story = ('This is some text, please type it.')
    return {
            'story': story,
            'sid': 1,
        }
