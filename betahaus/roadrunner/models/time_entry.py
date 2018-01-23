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
    title = ""
    tariff_uid = ""
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

    @property
    def start_time(self):
        #Map to created and set via created. It makes sense to link it to that
        #attribute and use that catalog index.
        return self.created

    @property
    def timedelta(self):
        return self.stop_time - self.start_time


def includeme(config):
    config.add_content_factory(TimeEntry, addable_to = 'Task')
