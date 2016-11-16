from datetime import datetime

from persistent.list import PersistentList
from zope.interface import implementer
import pytz

from arche.api import Base
from arche.api import Content
from arche.interfaces import IBlobs, IIndexedContent
from arche.utils import utcnow

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITariff, IOrganisation, ICustomer, IProject, ITask, ITimeEntry


@implementer(IOrganisation)
class Organisation(Content):
    type_name = "Organisation"
    type_title = _("Organisation")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-home"

    @property
    def image_data(self):
        blobs = IBlobs(self, None)
        if blobs:
            return blobs.formdata_dict('image')
    @image_data.setter
    def image_data(self, value):
        IBlobs(self).create_from_formdata('image', value)


@implementer(ICustomer)
class Customer(Content):
    type_name = "Customer"
    type_title = _("Customer")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-briefcase"

    @property
    def image_data(self):
        blobs = IBlobs(self, None)
        if blobs:
            return blobs.formdata_dict('image')
    @image_data.setter
    def image_data(self, value):
        IBlobs(self).create_from_formdata('image', value)


@implementer(IProject)
class Project(Content):
    type_name = "Project"
    type_title = _("Project")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-road"


@implementer(ITask)
class Task(Content):
    type_name = "Task"
    type_title = _("Task")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-tasks"

    def get_time_entries(self):
        results = []
        for obj in self.values():
            if ITimeEntry.providedBy(obj):
                results.append(obj)
        return sorted(results, key = lambda x: x.start_time, reverse=True)


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


@implementer(ITariff, IIndexedContent)
class Tariff(Base):
    type_name = "Tariff"
    type_title = _("Tariff")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-usd"
    title = ""
    price = None
    currency = ""
    vat = None


def time_difference(request, start, end):
    if not end:
        return ''
    res = end - start
    #This is silly, is there no smarter way?
    return str(res).split('.')[0]

def add_and_start_entry(request, context):
    assert request.authenticated_userid
    profile = request.root['users'][request.authenticated_userid]
    factory = request.content_factories['TimeEntry']
    obj = factory(start_time = utcnow())
    context[obj.uid] = obj
    profile.ongoing_entry = obj.uid
    return obj


def stop_entry(request):
    assert request.authenticated_userid
    profile = request.root['users'][request.authenticated_userid]
    if profile.ongoing_entry:
        entry = request.resolve_uid(profile.ongoing_entry)
        entry.stop_time = utcnow()
        profile.ongoing_entry = ""
        return entry


def ongoing_entry(request):
    if request.authenticated_userid:
        profile = request.root['users'][request.authenticated_userid]
        if profile.ongoing_entry:
            return request.resolve_uid(profile.ongoing_entry)


def entry_color_cls(request, entry):
    if request.ongoing_entry == entry:
        return 'success'
    if entry.stop_time == None:
        return 'warning'


def includeme(config):
    from arche.api import User
    config.add_content_factory(Organisation, addable_to = 'Root')
    config.add_content_factory(Customer, addable_to = 'Organisation')
    config.add_content_factory(Project, addable_to = 'Customer')
    config.add_content_factory(Task, addable_to = 'Project')
    config.add_content_factory(TimeEntry, addable_to = 'Task')
    config.add_content_factory(Tariff, addable_to = ('Organisation', 'Customer', 'Project'))
    config.add_request_method(time_difference)
    config.add_request_method(add_and_start_entry)
    config.add_request_method(stop_entry)
    config.add_request_method(ongoing_entry, reify=True)
    config.add_request_method(entry_color_cls)
    User.ongoing_entry = ""
