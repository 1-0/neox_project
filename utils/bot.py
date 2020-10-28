#!/usr/bin/env python3

import requests
import json
import io
from faker import Faker
from bot import config

FAKE_USERS = []


def fake_post(fake):
    title = fake.text(25)
    content = fake.text()
    return {
        'title': title,
        'content': content,
    }


def fake_user():
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password()
    fake_posts = []
    for i in range(config.MAX_POSTS_PER_USER):
        fake_posts.append(fake_post(fake))
    return {
        'first_name': first_name,
        'last_name': last_name,
        'username': '_'.join((first_name, last_name)),
        'email': email,
        'password': password,
        'fake_posts': fake_posts,
    }


def server_request(url, data, headers):
    i = 0
    res = None
    while i < config.NUMBER_OF_CONNECTION_RETRY:
        try:
            res = requests.post(
                url=url,
                data=data,
                headers=headers,
            )
            return res
        except:
            i += 1
    return res


def user_logout(token):
    data = json.dumps({
        'token': json.loads(token['login'])['key'],
    },)
    r = server_request(url=config.ENTER_POINT + r'rest-auth/logout/',
                       data=data,
                       headers={
                           'content-type': 'application/json',
                       },
                       )
    return r


def user_jwt_login(f_username, f_password):
    res = {}
    data = json.dumps({
               'username': f_username,
               'password': f_password,
           },)
    r = server_request(url=config.ENTER_POINT + r'token/',
                       data=data,
                       headers={
                           'content-type': 'application/json',
                       },
                       )
    res['tokens'] = json.loads(r.content)
    return res


def user_login(f_username, f_email, f_password):
    res = {}
    data = json.dumps({
               'username': f_username,
               'email': f_email,
               'password': f_password,
           },)
    r = server_request(url=config.ENTER_POINT + r'rest-auth/login/',
                       data=data,
                       headers={
                           'content-type': 'application/json',
                       },
                       )
    res['login'] = r.content
    return res


def add_post(f_username, f_password, title, content):
    res = {}
    token = user_jwt_login(f_username, f_password)
    data = json.dumps({
        'title': title,
        'content': content,
    })
    r = server_request(url=config.ENTER_POINT + r'post_data/',
                       data=data,
                       headers={
                           'content-type': 'application/json',
                           'Authorization': 'Bearer %s' % (token['tokens']['access'],),
                       },
                       )
    # user_logout(token)
    res['add_post'] = r.text
    return res


def add_rating(f_username, f_password, post_id, post_like):
    res = {}
    token = user_jwt_login(f_username, f_password)
    data = json.dumps({
        'post_id': post_like,
        'like': post_like,
    })
    r = server_request(url=config.ENTER_POINT + r'post_data/',
                       data=data,
                       headers={
                           'content-type': 'application/json',
                           'Authorization': 'Bearer %s' % (token['tokens']['access'],),
                       },
                       )
    # user_logout(token)
    res['add_post'] = r.text
    return res


def add_user(f):
    res = {}
    token = user_login(
               f_username=config.ADMIN_USERNAME,
               f_email=config.ADMIN_EMAIL,
               f_password=config.ADMIN_PASSWORD,
    )
    data = json.dumps({
        'username': f['username'],
        'email': f['email'],
        'password1': f['password'],
        'password2': f['password'],
    }, )
    r = server_request(url=config.ENTER_POINT + r'registration/',
                       data=data,
                       headers={
                           'content-type': 'application/json',
                       },
                       )

    user_logout(token)
    res['r'] = r.text
    return res


def add_posts(faker):
    posts = []
    for p in faker['fake_posts']:
        ap = add_post(
            f_username=faker['username'],
            f_password=faker['password'],
            title=p['title'],
            content=p['content'],
        )
        posts.append(ap)
    return posts


def main():
    for i in range(config.NUMBER_OF_USERS):
        f = fake_user()
        f['add_user'] = add_user(f)
        f['add_data'] = [add_posts(faker=f), ]
        FAKE_USERS.append(f)
    res = '''
FAKE_USERS += ''' + str(FAKE_USERS)

    with io.open(config.BOT_LOG_FILE, 'a+', encoding="utf-8") as log:
        log.write(res)

    return {
        'FAKE_USERS': FAKE_USERS,
    }


if __name__ == "__main__":
    main()
