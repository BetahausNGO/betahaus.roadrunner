import colander
import deform
from arche.schemas import tagging_widget
from arche.validators import supported_thumbnail_mimetype
from arche.widgets import FileAttachmentWidget

from betahaus.roadrunner import _


class BaseOrgSchema(colander.Schema):
    title = colander.SchemaNode(
        colander.String(),
        title=_("Title")
    )
    description = colander.SchemaNode(
        colander.String(),
        title=_("Description"),
        widget=deform.widget.TextAreaWidget(rows=3),
        missing=u""
    )
    tags = colander.SchemaNode(
        colander.List(),
        title=_("Tags or subjects"),
        missing="",
        widget=tagging_widget
    )
    image_data = colander.SchemaNode(
        deform.FileData(),
        missing=None,
        title=_(u"Image"),
        blob_key='image',
        validator=supported_thumbnail_mimetype,
        widget=FileAttachmentWidget()
    )
