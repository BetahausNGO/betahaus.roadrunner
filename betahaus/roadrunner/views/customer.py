# -*- coding: utf-8 -*-
from datetime import timedelta

from arche.security import PERM_VIEW
from arche.views.base import BaseView
from pyramid.traversal import resource_path
from pyramid.view import view_config, view_defaults
from repoze.catalog.query import Eq

from betahaus.roadrunner.interfaces import ICustomer


@view_defaults(context=ICustomer,
               permission=PERM_VIEW)
class CustomerView(BaseView):

    @view_config(renderer='betahaus.roadrunner:templates/customer.pt')
    def main(self):
        return {'projects': self.get_projects()}

    def get_projects(self):
        query = Eq('type_name', 'Project') & Eq('path', resource_path(self.context))
        docids = self.request.root.catalog.query(query, sort_index='sortable_title')[1]
        return self.request.resolve_docids(docids)

    @view_config(name='report', renderer='betahaus.roadrunner:templates/customer_report.pt')
    def report(self):
        unbilled_time_query = Eq('type_name', 'TimeEntry') & Eq('path', resource_path(self.context))
        unbilled_count, unbilled_time_entries = self.request.root.catalog.query(unbilled_time_query)
        total_time = timedelta()
        for time_entry in self.request.resolve_docids(unbilled_time_entries):
            total_time += time_entry.timedelta
        return {'total_time': total_time}



def includeme(config):
    config.scan(__name__)
