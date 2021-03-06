import re
import string
import random
from urlparse import urljoin
from flask import request, url_for, session, flash, redirect
from functools import wraps


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def extract_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("", tags)
    tags_array = nowhite.split(',')

    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)

    return cleaned


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = random_string()
    return session['_csrf_token']


def make_external(url):
    return urljoin(request.url_root, url)


def login_required():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get('user'):
                flash('You must be logged in..', 'error')
                return redirect(url_for('main.login'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def single_keyword(str_key):
    from blog_app.application import settingsClass
    str_key = str_key.replace('  ', ' ').replace(',,', ',').split(',')
    static_str = settingsClass.get_config().get('BLOG_DESCRIPTION')
    if static_str not in str_key:
        str_key.insert(0, static_str)

    str_key = map(lambda x: x.strip(), str_key)
    str_key = set(str_key)

    if '' in str_key:
        str_key.remove('')

    str_key = ','.join(str_key).replace('#', ' ')
    return str_key


def format_datetime_filter(input_value, format_="%Y%m%d %H:%M"):
    return input_value.strftime(format_)


