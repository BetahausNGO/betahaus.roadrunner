import colander
import deform
from arche.schemas import tagging_widget
from pyramid.traversal import find_interface

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import IProject
from betahaus.roadrunner.models.task import Task


@colander.deferred
def trello_card_widget(node, kw):
    context = kw['context']
    project = find_interface(context, IProject)
    values = [('', '- Inget kort -')]
    if project.trello_board:
        board = kw['request'].get_trello_client().get_board(project.trello_board)
        current_task = isinstance(context, Task) and context or None
        used_cards = project.other_used_cards(current_task)
        for l in board.list_lists():
            for card in l.list_cards():
                if card.id not in used_cards:
                    values.append((card.id, card.name))
    return deform.widget.Select2Widget(values=values, multiple=False)


class TaskSchema(colander.Schema):
    title = colander.SchemaNode(
        colander.String(),
        title=_("Title")
    )
    description = colander.SchemaNode(
        colander.String(),
        title=_("Description"),
        widget=deform.widget.TextAreaWidget(rows=3),
        missing=""
    )
    trello_card = colander.SchemaNode(
        colander.String(),
        title=_('Trello card'),
        missing='',
        widget=trello_card_widget,
    )
    tags = colander.SchemaNode(
        colander.List(),
        title=_("Tags or subjects"),
        missing="",
        widget=tagging_widget
    )


def includeme(config):
    config.add_content_schema('Task', TaskSchema, ('add', 'view', 'edit'))
