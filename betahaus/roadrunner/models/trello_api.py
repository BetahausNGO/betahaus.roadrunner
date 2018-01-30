# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
import json
import re

from trello import TrelloClient
from trello.card import Card


def get_trello_client(request):
    client = request.registry.settings['trello_client']
    client.cache_override(False)
    return client


def to_decimal(self, str):
    if str is not None and str != '?':
        return Decimal(str)


def new_card_init(self, parent, card_id, name=''):
    self.original_init(parent, card_id, name)

    name_split = self.scrum_split.match(name).groups()
    self.name = name_split[2]
    self.estimated_hours = self.to_decimal(name_split[1])
    self.consumed_hours = self.to_decimal(name_split[4])


# Monkey patch the Trello cards to add Scrum for Trello attributes (estimated points, etc)
def monkeypatch_card():
    Card.original_init = Card.__init__
    Card.__init__ = new_card_init
    Card.to_decimal = to_decimal
    Card.scrum_split = re.compile('^(\((\?|\d+\.?\d?)\)\s)?(.*?)(\s\[(\?|\d+\.?\d?)\])?$')


class CachedTrelloClient(TrelloClient):
    cache_storage = {}
    _cache_override = False

    def fetch_json(self, uri_path, **kwargs):
        method = kwargs.get('http_method', 'GET')
        if self._cache_override or method != 'GET' or uri_path not in self.cache_storage:
            self.cache_storage[uri_path] = super(CachedTrelloClient, self).fetch_json(uri_path, **kwargs)
        return self.cache_storage[uri_path]

    def cache_override(self, state=True):
        self._cache_override = state

    def clear_cache(self):
        self.cache_storage.clear()


def includeme(config):
    with open(config.registry.settings['roadrunner.trello_api_file']) as tf:
        trello_keys = json.load(tf)
    assert set(trello_keys.keys()) == {'api_key', 'api_secret', 'token', 'token_secret'}
    config.add_settings(trello_client=CachedTrelloClient(**trello_keys))
    config.add_request_method(get_trello_client, name='trello_client', property=True)
    monkeypatch_card()
