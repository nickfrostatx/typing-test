from random import choice
from redis import StrictRedis
from uuid import uuid4
from bcrypt import hashpw, gensalt

r = StrictRedis(host='localhost')

def create_uuid():
    return str(uuid4())

def create_session_key(l=32):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    key = ''
    while len(key) < l:
        key += choice(letters)
    return key

def rkey(*args):
    return 'maestro:' + ':'.join(args)

def create_user(email=''):
    uid = create_uuid()
    r.hmset(rkey(uid), {
            'email': email,
        })
    return uid

def create_auth(email, password, uid):
    try:
        password_hash = hashpw(password, gensalt())
    except Exception as e:
        print(e)
    r.hmset(rkey('auth', email), {
            'password': password_hash,
            'uid': uid,
        })
    return True

def auth(email, password):
    password_hash, uid = r.hmget(rkey('auth', email), 'password', 'uid')
    password_hash = password_hash.decode('utf-8')
    uid = uid.decode('utf-8')
    if hashpw(password, password_hash) == password_hash:
        return uid
    return None

def create_session(uid):
    key = create_session_key()
    r.hmset(rkey('session', key), {
            'uid': uid,
        })
    return key

def get_session_uid(key):
    uid = r.hget(rkey('session', key), 'uid')
    if not uid:
        return None
    uid = uid.decode('utf-8')
    return uid
