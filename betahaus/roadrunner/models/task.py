# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from decimal import Decimal
from math import ceil

from arche.api import Content
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITask, ITimeEntry


@implementer(ITask)
class Task(Content):
    type_name = "Task"
    type_title = _("Task")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-tasks"
    trello_card = ''
    card_estimated_hours = None
    card_consumed_hours = None

    def get_time_entries(self):
        results = []
        for obj in self.values():
            if ITimeEntry.providedBy(obj):
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
        total = self.total_time
        if total:
            half_hours = Decimal(ceil(total.total_seconds() / 1800.0))
            return half_hours / 2


def includeme(config):
    config.add_content_factory(Task, addable_to = 'Project')
