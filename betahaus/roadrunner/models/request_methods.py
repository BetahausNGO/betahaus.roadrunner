from calendar import timegm
from collections import OrderedDict

from arche.utils import utcnow
from datetime import timedelta
from pyramid.traversal import resource_path
from repoze.catalog.query import Eq, Gt, Any


_marker = object()


def time_difference(request, start, end):
    if not end:
        return ''
    res = end - start
    return format_delta(request, res)


def add_and_start_entry(request, context):
    assert request.authenticated_userid
    profile = request.root['users'][request.authenticated_userid]
    factory = request.content_factories['TimeEntry']
    obj = factory(created = utcnow())
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


def sum_time(request, context, userid=_marker):
    """ Build a dict with time summary
    """
    query = Eq('path', resource_path(context)) & Eq('type_name', 'TimeEntry')
    if userid == _marker:
        userid = request.authenticated_userid
    if userid:
        query &= Any('creator', [userid])
    docids = request.root.catalog.query(query)[1]
    results = {}
    for obj in request.resolve_docids(docids, perm=None):
        if obj.stop_time:
            creator = obj.creator[0]
            if creator not in results:
                results[creator] = timedelta()
            results[creator] += obj.stop_time - obj.start_time
    return results


def format_delta(request, value, asstr=True):
    """
    :param request:
    :param value:
    :type value: timedelta
    :param asstr: Return string rather than a tuple with integers
    :return: string or a tuple of integers
    """
    secs = value.seconds
    hours = secs // 3600
    secs = secs - (hours * 3600)
    minutes = secs // 60
    secs = secs - (minutes * 60)
    if asstr:
        return "%s:%02d:%02d" % (hours, minutes, secs)
    return hours, minutes, secs


def day_entries(request, context, day=None, userid=_marker):
    """
    :param request:
    :param context: Fetch everything within this contexts path (may be root)
    :param group: Group entries together within tasks
    :param day: Limit within this day
    :type day: date
    :param userid: User to fetch for. None means all
    :return: OrderedDict with Task uid as key and time entry objects in a list as value.
    """
    if userid == _marker:
        userid = request.authenticated_userid
    #FIXME: Fetch exactly one day and all entries for that day. Sort according to Tasks
    #min_created = utcnow() - timedelta(days=days)
    query = Eq('path', resource_path(context)) &\
            Eq('type_name', 'TimeEntry')
     #       Gt('created', timegm(min_created.timetuple()))
    if userid:
        query &= Any('creator', [userid])
    docids = request.root.catalog.query(query, sort_index='created', reverse=True)[1]
    results = OrderedDict()
    for obj in request.resolve_docids(docids):
        items = results.setdefault(obj.__parent__.uid, [])
        items.append(obj)
    return results


def includeme(config):
    config.add_request_method(time_difference)
    config.add_request_method(add_and_start_entry)
    config.add_request_method(stop_entry)
    config.add_request_method(ongoing_entry, reify=True)
    config.add_request_method(entry_color_cls)
    config.add_request_method(sum_time)
    config.add_request_method(format_delta)
    config.add_request_method(day_entries)
