# -*- coding: utf-8 -*-
from arche.interfaces import IRoot
from arche.security import PERM_VIEW
from arche.views.base import BaseView
from pyramid.view import view_config


@view_config(context=IRoot, name='view', permission=PERM_VIEW, renderer='betahaus.roadrunner:templates/root.pt')
class RootView(BaseView):
    """ Overview of current stats """

    def __call__(self):
        return {}


def includeme(config):
    config.scan(__name__)