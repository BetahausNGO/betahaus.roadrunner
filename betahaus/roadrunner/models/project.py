from arche.api import Content
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import IProject


@implementer(IProject)
class Project(Content):
    type_name = "Project"
    type_title = _("Project")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-road"


def includeme(config):
    config.add_content_factory(Project, addable_to = 'Customer')
