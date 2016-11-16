from arche.utils import utcnow


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
    config.add_request_method(time_difference)
    config.add_request_method(add_and_start_entry)
    config.add_request_method(stop_entry)
    config.add_request_method(ongoing_entry, reify=True)
    config.add_request_method(entry_color_cls)
