from pyramid.renderers import render


def timer_component(context, request, va, **kw):
    return render('betahaus.roadrunner:templates/timer.pt', {}, request=request)


def includeme(config):
    config.add_view_action(timer_component, 'nav_right', 'timer', priority=1)
