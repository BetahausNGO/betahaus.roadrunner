from datetime import timedelta
from datetime import datetime

from decimal import Decimal
from math import ceil
from typing import Iterable

from pytz import utc

from arche.api import Base
from arche.interfaces import IIndexedContent
from persistent.list import PersistentList
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITimeEntry


def entries_to_consumed_hours(entries):
    # type: (Iterable[TimeEntry]) -> Decimal
    # Returns time entry hours, rounded to full half hours
    total = timedelta()
    for t in entries:
        total += t.timedelta
    if total:
        half_hours = Decimal(ceil(total.total_seconds() / 1800.0))
        return half_hours / 2


@implementer(ITimeEntry, IIndexedContent)
class TimeEntry(Base):
    type_name = "TimeEntry"
    type_title = _("Time entry")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-time"
    title = ""
    tariff_uid = ""
    stop_time = None
    bill_hours = None
    billed = False

    @property
    def creator(self): return getattr(self, '__creator__', ())
    @creator.setter
    def creator(self, value):
        if value:
            self.__creator__ = PersistentList(value)
        else:
            if hasattr(self, '__creator__'):
                delattr(self, '__creator__')

    @property
    def start_time(self):
        #Map to created and set via created. It makes sense to link it to that
        #attribute and use that catalog index.
        return self.created

    @property
    def timedelta(self):
        # type: () -> timedelta
        if self.bill_hours:
            return timedelta(minutes=int(self.bill_hours*60))
        if self.stop_time is None:
            # TODO Get real timezone, yo
            return datetime.now(utc) - self.start_time
        else:
            return self.stop_time - self.start_time


def includeme(config):
    config.add_content_factory(TimeEntry, addable_to = 'Task')
