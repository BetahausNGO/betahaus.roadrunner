# -*- coding: utf-8 -*-

from arche.views.base import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults

from betahaus.roadrunner.interfaces import IProject
from betahaus.roadrunner.interfaces import ITask
from betahaus.roadrunner.models.task import Task


@view_defaults(context=IProject)
class ProjectView(BaseView):

    @view_config(renderer="betahaus.roadrunner:templates/project.pt")
    def main(self):
        if self.request.GET.get('tasks_from_trello') and self.context.trello_board:
            trello = self.request.trello_client
            trello.cache_override()
            board = trello.get_board(self.context.trello_board)
            used_cards = self.context.used_cards
            for l in board.list_lists():
                for card in l.list_cards():
                    if card.id in used_cards:
                        continue
                    new_task = Task(
                        title=card.name,
                        trello_card=card.id,
                        card_estimated_hours=card.estimated_hours,
                        card_consumed_hours=card.consumed_hours,
                    )
                    self.context[new_task.uid] = new_task

        if self.request.GET.get('sync_trello_cards'):
            trello = self.request.trello_client
            trello.cache_override()
            for task in self.context.tasks_with_card():
                card = trello.get_card(task.trello_card)
                task.title = card.name
                task.card_estimated_hours = card.estimated_hours
                task.card_consumed_hours = card.consumed_hours

                consumed_hours = task.consumed_hours
                if card.consumed_hours != consumed_hours:
                    card.set_name(str(task))

        return {'tasks': tuple(self.get_tasks())}

    def get_tasks(self):
        for obj in self.context.values():
            if ITask.providedBy(obj):
                yield obj


def includeme(config):
    config.scan(__name__)
