from fanstatic import Library, Resource

from arche.fanstatic_lib import common_js
from arche.interfaces import IViewInitializedEvent, IBaseView
from deform_autoneed import need_lib


library = Library('roadrunner', 'static')

timer_js = Resource(library, 'timer.js', depends = (common_js,))
inline_edit_js = Resource(library, 'inline_edit.js', depends = (common_js,))


def inject(view, event):
    timer_js.need()
    inline_edit_js.need()
    need_lib('deform')
    need_lib('pickadate')


def includeme(config):
    config.add_subscriber(inject, [IBaseView, IViewInitializedEvent])
