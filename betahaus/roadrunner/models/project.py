from arche.api import Content
from arche.interfaces import IBlobs
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import IProject


@implementer(IProject)
class Project(Content):
    type_name = "Project"
    type_title = _("Project")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-road"
    blob_key = 'image'

    @property
    def image_data(self):
        blobs = IBlobs(self, None)
        if blobs:
            return blobs.formdata_dict(self.blob_key)
    @image_data.setter
    def image_data(self, value):
        IBlobs(self).create_from_formdata(self.blob_key, value)


def includeme(config):
    config.add_content_factory(Project, addable_to = 'Customer')
