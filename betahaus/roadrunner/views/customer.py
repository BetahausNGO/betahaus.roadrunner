# -*- coding: utf-8 -*-
from arche.security import PERM_VIEW
from arche.views.base import BaseView
from pyramid.traversal import resource_path
from pyramid.view import view_config
from repoze.catalog.query import Eq

from betahaus.roadrunner.interfaces import ICustomer


@view_config(context=ICustomer, name='view',
             permission=PERM_VIEW,
             renderer='betahaus.roadrunner:templates/customer.pt')
class CustomerView(BaseView):

    def __call__(self):
        return {'projects': self.get_projects()}

    def get_projects(self):
        query = Eq('type_name', 'Project') & Eq('path', resource_path(self.context))
        docids = self.request.root.catalog.query(query, sort_index='sortable_title')[1]
        return self.request.resolve_docids(docids)


def includeme(config):
    config.scan(__name__)
