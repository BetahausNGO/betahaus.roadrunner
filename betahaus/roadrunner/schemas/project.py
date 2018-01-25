import colander
import deform
from repoze.catalog.query import Eq

from betahaus.roadrunner.models.project import Project
from betahaus.roadrunner.schemas.base import BaseOrgSchema
from betahaus.roadrunner import _


@colander.deferred
def trello_board_widget(node, kw):
    request = kw['request']
    values = [('', '- Ingen tavla -')]
    for board in request.get_trello_client().list_boards():
        if request.root.catalog.query(Eq('trello_board', board.id))[0].total == 0 or \
           isinstance(kw['context'], Project) and board.id == kw['context'].trello_board:
            values.append((board.id, board.name))
    return deform.widget.Select2Widget(values=values, multiple=False)


class ProjectSchema(BaseOrgSchema):
    trello_board = colander.SchemaNode(
        colander.String(),
        title=_('Trello board '),
        widget=trello_board_widget,
        missing="",
    )


def includeme(config):
    config.add_content_schema('Project', ProjectSchema, ('add', 'view', 'edit'))
