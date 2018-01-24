# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from trello import TrelloClient


def read_trello_credentials(config):
    with open(config.registry.settings['roadrunner.trello_api_file']) as tf:
        trello_keys = json.load(tf)
        assert trello_keys.keys() == {'api_key', 'api_secret', 'token', 'token_secret'}
        config.registry.settings['trello_keys'] = trello_keys


def get_trello_client(request):
    keys = request.registry.settings['trello_keys']
    return TrelloClient(**keys)


def includeme(config):
    config.include(read_trello_credentials)
    config.add_request_method(get_trello_client)
