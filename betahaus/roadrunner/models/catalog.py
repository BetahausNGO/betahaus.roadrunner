# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from repoze.catalog.indexes.field import CatalogFieldIndex

from betahaus.roadrunner.interfaces import IProject


def get_trello_board(obj, default):
    """ Objects automatic id. """
    if IProject.providedBy(obj):
        return obj.trello_board and obj.trello_board or default
    return default


def includeme(config):
    indexes = {
        'trello_board': CatalogFieldIndex(get_trello_board),
    }
    config.add_catalog_indexes(__name__, indexes)
    config.scan(__name__)
