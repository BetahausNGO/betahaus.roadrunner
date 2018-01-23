# -*- coding: utf-8 -*-

from arche.views.base import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults

from betahaus.roadrunner.interfaces import IProject
from betahaus.roadrunner.interfaces import ITask


@view_defaults(context = IProject)
class ProjectView(BaseView):

    @view_config(renderer = "betahaus.roadrunner:templates/project.pt")
    def main(self):
        return {'tasks': tuple(self.get_tasks())}

    def get_tasks(self):
        for obj in self.context.values():
            if ITask.providedBy(obj):
                yield obj


def includeme(config):
    config.scan(__name__)
