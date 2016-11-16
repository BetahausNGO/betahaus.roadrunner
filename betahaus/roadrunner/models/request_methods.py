from arche.utils import utcnow
from datetime import timedelta
from pyramid.traversal import resource_path
from repoze.catalog.query import Eq


def time_difference(request, start, end):
    if not end:
        return ''
    res = end - start
    return format_delta(request, res)


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


def sum_time(request, context):
    """ Build a dict with time summary
    """
    query = Eq('path', resource_path(context)) & Eq('type_name', 'TimeEntry')
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
    secs = value.seconds
    hours = secs // 3600
    secs = secs - (hours * 3600)
    minutes = secs // 60
    secs = secs - (minutes * 60)
    if asstr:
        return "%s:%02d:%02d" % (hours, minutes, secs)
    return hours, minutes, secs


def includeme(config):
    config.add_request_method(time_difference)
    config.add_request_method(add_and_start_entry)
    config.add_request_method(stop_entry)
    config.add_request_method(ongoing_entry, reify=True)
    config.add_request_method(entry_color_cls)
    config.add_request_method(sum_time)
    config.add_request_method(format_delta)
