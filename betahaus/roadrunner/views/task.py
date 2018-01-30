# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from arche.views.base import BaseView
from pyramid.view import view_defaults
from pyramid.view import view_config

from betahaus.roadrunner.interfaces import ITask


@view_defaults(context=ITask)
class TaskView(BaseView):
    update_fields = {
        'title': 'name',
        'card_estimated_hours': 'estimated_hours',
        'card_consumed_hours': 'consumed_hours',
    }

    # TODO Define subpath somehow
    @view_config(name='update_card', renderer="json")
    def update_card(self):
        response = {
            'updated_fields': {},
            'trello_updated': False
        }
        if self.context.trello_card:
            trello = self.request.trello_client
            task = self.context
            trello.cache_override()
            card = trello.get_card(task.trello_card)

            for field in self.update_fields:
                value = getattr(card, self.update_fields[field])
                if getattr(task, field) != value:
                    setattr(task, field, value)
                    response['updated_fields'][field] = str(value)

            consumed_hours = task.consumed_hours
            if card.consumed_hours != consumed_hours:
                card.set_name(''.join((
                    task.card_estimated_hours and '({}) '.format(task.card_estimated_hours) or '',
                    task.title,
                    consumed_hours and ' [{}]'.format(consumed_hours) or '',
                )))
                response['updated_fields']['consumed_hours'] = str(consumed_hours)
                response['updated_trello'] = True
        return response


def includeme(config):
    config.scan(__name__)
