from arche.api import Content
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITask, ITimeEntry


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


def includeme(config):
    config.add_content_factory(Task, addable_to = 'Project')
