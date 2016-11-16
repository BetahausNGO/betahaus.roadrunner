import colander
import deform
from arche.schemas import tagging_widget

from betahaus.roadrunner import _


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
    tags = colander.SchemaNode(
        colander.List(),
        title=_("Tags or subjects"),
        missing="",
        widget=tagging_widget
    )


def includeme(config):
    config.add_content_schema('Task', TaskSchema, ('add', 'view', 'edit'))
