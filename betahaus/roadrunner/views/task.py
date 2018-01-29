# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from arche.views.base import BaseView
from pyramid.view import view_defaults
from pyramid.view import view_config

from betahaus.roadrunner.interfaces import ITask


@view_defaults(context=ITask)
class ProjectView(BaseView):

    # TODO Define subpath somehow
    @view_config(renderer="json")
    def update_card(self):
        if self.request.GET.get('update_trello_card') and self.context.trello_card:
            card = self.request.trello_client.get_card(self.context.trello_card)
            # TODO Update card from trello (no cache) to update estimated time and name
            # TODO Then update consumed time on trello if differs from task hours
        return {}


def includeme(config):
    config.scan(__name__)
