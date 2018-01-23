# -*- coding: utf-8 -*-

from calendar import timegm

from arche.interfaces import IRoot
from arche.views.base import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_defaults(context = IRoot)
class ControlsView(BaseView):

    @view_config(renderer = 'json', route_name = 'timer_add_start')
    def add_and_start(self):
        task_uid = self.request.matchdict.get('task_uid', None)
        context = self.request.resolve_uid(task_uid)
        entry = self.request.add_and_start_entry(context)
        return self.get_entry_data(entry)

    @view_config(renderer = 'json', route_name = 'timer_stop')
    def stop(self):
        self.request.stop_entry()
        return {}

    @view_config(renderer = 'json', route_name = 'timer_read')
    def read(self):
        entry = self.request.ongoing_entry
        if entry:
            return self.get_entry_data(entry)
        return {}

    def get_entry_data(self, entry):
        return {
            'epoch': timegm(entry.start_time.timetuple()),
            'title': entry.title,
            'url': self.request.resource_url(entry), #Or project?
        }


def includeme(config):
    config.add_route('timer_add_start', '/timer_controls/add/${task_uid}')
    config.add_route('timer_stop', '/timer_controls/stop')
    config.add_route('timer_read', '/timer_controls/read')
    config.scan(__name__)
