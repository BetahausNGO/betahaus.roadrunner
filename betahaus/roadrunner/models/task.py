# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from decimal import Decimal
from math import ceil

from arche.api import Content
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITask, ITimeEntry
from betahaus.roadrunner.models.time_entry import entries_to_consumed_hours


@implementer(ITask)
class Task(Content):
    type_name = "Task"
    type_title = _("Task")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-tasks"
    trello_card = ''
    card_estimated_hours = None
    card_consumed_hours = None

    def get_time_entries(self, only_unbilled=False):
        results = []
        for obj in self.values():
            if ITimeEntry.providedBy(obj) and not (only_unbilled and obj.billed):
                results.append(obj)
        return sorted(results, key=lambda x: x.start_time, reverse=True)

    @property
    def total_time(self):
        entries = self.get_time_entries()
        if entries:
            total = timedelta()
            for t in entries:
                total += t.timedelta
            return total

    @property
    def consumed_hours(self):
        # Returns time entry hours, rounded to full half hours
        return entries_to_consumed_hours(self.get_time_entries())

    @property
    def unbilled_hours(self):
        # Returns time entry hours, rounded to full half hours
        return entries_to_consumed_hours(self.get_time_entries(only_unbilled=True))

    def __str__(self):
        consumed_hours = self.consumed_hours
        return ''.join((
            self.card_estimated_hours and '({}) '.format(self.card_estimated_hours) or '',
            self.title,
            consumed_hours and ' [{}]'.format(consumed_hours) or '',
        ))


def includeme(config):
    config.add_content_factory(Task, addable_to = 'Project')
