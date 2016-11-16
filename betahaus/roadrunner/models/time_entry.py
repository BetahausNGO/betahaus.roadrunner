from arche.api import Base
from arche.interfaces import IIndexedContent
from persistent.list import PersistentList
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITimeEntry


@implementer(ITimeEntry, IIndexedContent)
class TimeEntry(Base):
    type_name = "TimeEntry"
    type_title = _("Time entry")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-time"
    creator = ""
    title = ""
    tariff_uid = ""
    start_time = None
    stop_time = None

    @property
    def creator(self): return getattr(self, '__creator__', ())
    @creator.setter
    def creator(self, value):
        if value:
            self.__creator__ = PersistentList(value)
        else:
            if hasattr(self, '__creator__'):
                delattr(self, '__creator__')


def includeme(config):
    config.add_content_factory(TimeEntry, addable_to = 'Task')
