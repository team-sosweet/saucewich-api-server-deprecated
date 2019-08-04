"""
Models to consume
"""

from sanic_openapi import doc


class User:
    username = doc.String('username of the user')
    nickname = doc.String('nickname of the user')

    exp = doc.Integer('experience points the user has')
    point = doc.Integer('the amount of points the user has')
    kill_stats = doc.Integer('the amount of kill points the user gained')
    death_stats = doc.Integer('the amount of death points the user gained')
    win_stats = doc.Integer('the amount of win points the user gained')
    defeat_stats = doc.Integer('the amount of defeat points the user gained')

    playtime = doc.Integer('the amount of playtime the user played')


class UserRegistration:
    username = doc.String('username of the user')
    password = doc.String('password of the user')
    nickname = doc.String('nickname of the user')


class UserAuthentication:
    username = doc.String('username of the user')
    password = doc.String('password of the user')


class Friend:
    friend_id = doc.Integer('user id of the friend')
    created_at = doc.DateTime('timestamp when the relationship was established')


class FriendCreation(Friend):
    user_id = doc.Integer('user id of the user')
    friend_id = doc.Integer('user id of the friend')


class FriendRequest:
    sender = doc.Integer('user id of the user requested')
    created_at = doc.DateTime('timestamp when the request was sent')


class FriendRequestCreation:
    sender = doc.Integer('user id of the sender')
    recipient = doc.Integer('user id of the recipient')
