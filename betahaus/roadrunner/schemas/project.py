import colander

from betahaus.roadrunner.schemas.base import BaseOrgSchema
from betahaus.roadrunner import _
from betahaus.roadrunner.widgets import TrelloBoardSelectWidget


class ProjectSchema(BaseOrgSchema):
    trello_boards = colander.SchemaNode(
        colander.List(),
        title=_('Trello boards'),
        widget=TrelloBoardSelectWidget(),
    )


def includeme(config):
    config.add_content_schema('Project', ProjectSchema, ('add', 'view', 'edit'))
