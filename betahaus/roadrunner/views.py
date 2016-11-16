from calendar import timegm

from colander import Invalid
from pyramid.view import view_config, view_defaults

from arche.interfaces import IRoot
from arche.utils import get_content_schemas
from arche.views.base import BaseView,BaseForm

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import IProject, ITask, ITimeEntry


class EntryMixin(object):

    def get_entry_data(self, entry):
        return {
            'epoch': timegm(entry.start_time.timetuple()),
            'title': entry.title,
            'url': self.request.resource_url(entry), #Or project?
        }


class SchemaMixin(object):

    def json_validate(self, type_name = None, schema_name = 'edit'):
        if not type_name:
            type_name = self.context.type_name
        schema = get_content_schemas(self.request.registry)[type_name][schema_name]
        schema = schema()
        if 'tariff_uid' in schema:
            del schema['tariff_uid']
        schema = schema.bind(context = self.context, request = self.request, view = self)
        try:
            print schema.deserialize(self.request.POST)
        except Invalid as exc:
            return exc.asdict()
    #        event = SchemaCreatedEvent(self.schema, view = self, context = context, request = request)


@view_defaults(context = IProject)
class ProjectView(BaseView):

    @view_config(renderer = "templates/project.pt")
    def main(self):
        return {'tasks': tuple(self.get_tasks())}

    def get_tasks(self):
        for obj in self.context.values():
            if ITask.providedBy(obj):
                yield obj

# @view_config(name = 'edit_partial', renderer = "arche:templates/form.pt")
# class TimeEntryPartialEdit(BaseForm):
#     schema_name = "edit"
#     type_name = "TimeEntry"
#
#     _ajax_options = """
#         {success:
#           function (rText, sText, xhr, form) {
#             var loc = xhr.getResponseHeader('X-Relocate');
#             if (loc) {
#               document.location = loc;
#             };
#            }
#         }
#     """
#
#     buttons = (BaseForm.button_save,)
#
#     def get_schema(self):
#         """ Return either an instantiated schema or a schema class.
#             Use either this method or get_schema_factory.
#         """
#         schema = self.get_schema_factory(self.type_name, self.schema_name)
#         field = self.request.GET.get('f')
#         schema = schema()
#         names = [x.name for x in schema]
#         for name in names:
#             if name != field:
#                 del schema[name]
#         return schema
#
#     def save_success(self, appstruct):
#         print appstruct

@view_defaults(context = ITimeEntry)
class TimeEntryView(BaseView, EntryMixin, SchemaMixin):

    @view_config(name = "update", renderer = "json")
    def update_view(self):
        title = self.request.POST.get('title', '')
        errors = self.json_validate()
        if errors:
            return {'errors': errors}
        else:
            self.context.update(title = title)
            return self.get_entry_data(self.context)

    # @view_config(renderer = "templates/project.pt")
    # def main(self):
    #     return {'tasks': tuple(self.get_tasks())}
    #
    # def get_tasks(self):
    #     for obj in self.context.values():
    #         if ITask.providedBy(obj):
    #             yield obj


@view_defaults(context = IRoot)
class ControlsView(BaseView, EntryMixin):

    @view_config(renderer = 'json', route_name = 'timer_add_start')
    def add_and_start(self):
        task_uid = self.request.matchdict.get('task_uid', None)
        context = self.request.resolve_uid(task_uid)
        entry = self.request.add_and_start_entry(context)
        return self.get_entry_data(entry)

    @view_config(renderer = 'json', route_name = 'timer_stop')
    def stop(self):
        self.request.stop_entry()
        return {}

    @view_config(renderer = 'json', route_name = 'timer_read')
    def read(self):
        entry = self.request.ongoing_entry
        if entry:
            return self.get_entry_data(entry)
        return {}


def includeme(config):
    config.add_route('timer_add_start', '/timer_controls/add/${task_uid}')
    config.add_route('timer_stop', '/timer_controls/stop')
    config.add_route('timer_read', '/timer_controls/read')
    config.scan()
