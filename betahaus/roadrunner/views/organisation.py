# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from arche.security import PERM_VIEW
from arche.views.base import BaseView
from pyramid.traversal import resource_path
from pyramid.view import view_config
from repoze.catalog.query import Eq

from betahaus.roadrunner.interfaces import IOrganisation


@view_config(context=IOrganisation, name='view',
             permission=PERM_VIEW,
             renderer='betahaus.roadrunner:templates/organisation.pt')
class OrganisationView(BaseView):

    def __call__(self):
        return {'customers': self.get_customers()}

    def get_customers(self):
        query = Eq('type_name', 'Customer') & Eq('path', resource_path(self.context))
        docids = self.request.root.catalog.query(query, sort_index='sortable_title')[1]
        return self.request.resolve_docids(docids)


def includeme(config):
    config.scan(__name__)
