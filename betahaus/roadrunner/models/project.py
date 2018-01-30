from arche.api import Content
from arche.interfaces import IBlobs
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import IProject
from betahaus.roadrunner.models.task import Task


@implementer(IProject)
class Project(Content):
    type_name = "Project"
    type_title = _("Project")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-road"
    blob_key = 'image'
    trello_board = ""

    def other_used_cards(self, task=None):
        other_tasks = filter(lambda t: t != task, self.tasks_with_card())
        return [t.trello_card for t in other_tasks]

    @property
    def used_cards(self):
        return self.other_used_cards()

    def tasks_with_card(self):
        return filter(lambda t: isinstance(t, Task) and t.trello_card, self.values())

    @property
    def image_data(self):
        blobs = IBlobs(self, None)
        if blobs:
            return blobs.formdata_dict(self.blob_key)
    @image_data.setter
    def image_data(self, value):
        IBlobs(self).create_from_formdata(self.blob_key, value)

    def consumed_hours(self, only_unbilled=True):
        pass


def includeme(config):
    config.add_content_factory(Project, addable_to='Customer')
