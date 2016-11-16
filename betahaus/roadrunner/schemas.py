import colander
import deform
from arche.schemas import LocalDateTime
from arche.schemas import tagging_widget
from arche.validators import supported_thumbnail_mimetype
from arche.widgets import FileAttachmentWidget
from repoze.folder import IFolder

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITariff


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


class OrganisationSchema(BaseOrgSchema):
    pass


class CustomerSchema(BaseOrgSchema):
    pass


class ProjectSchema(BaseOrgSchema):
    pass


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


@colander.deferred
def selectable_tariff_radio(node, kw):
    values = [('', _("N/A"))]
    context = kw['context']
    while context.__parent__:
        if IFolder.providedBy(context):
            for obj in context.values():
                if ITariff.providedBy(obj):
                    values.append((obj.uid, obj.title))
        context = context.__parent__
    return deform.widget.RadioChoiceWidget(values=values)


def datetime_widget(*args):
    return deform.widget.DateTimeInputWidget(time_options={'interval': 5})


class TimeEntrySchema(colander.Schema):
    title = colander.SchemaNode(
        colander.String(),
        title=_("Title")
    )
    tariff_uid = colander.SchemaNode(
        colander.String(),
        title=_("Tariff"),
        missing="",
        widget=selectable_tariff_radio,
    )
    start_time = colander.SchemaNode(
        LocalDateTime(),
        missing=None,
        widget=datetime_widget(),
        title=_("Start time")
    )
    stop_time = colander.SchemaNode(
        LocalDateTime(),
        missing=None,
        widget=datetime_widget(),
        title=_("End time")
    )


class TariffSchema(colander.Schema):
    title = colander.SchemaNode(
        colander.String(),
        title=_("Title")
    )
    price = colander.SchemaNode(
        colander.Decimal(),
        title=_("Price"),
        default=0
    )
    currency = colander.SchemaNode(
        colander.String(),
        title=_("Currency"),
        missing=""
    )
    vat = colander.SchemaNode(
        colander.Int(),
        title=_("VAT in integer percentage"),
        default=0
    )


def includeme(config):
    config.add_content_schema('Organisation', OrganisationSchema, ('add', 'view', 'edit'))
    config.add_content_schema('Customer', CustomerSchema, ('add', 'view', 'edit'))
    config.add_content_schema('Project', ProjectSchema, ('add', 'view', 'edit'))
    config.add_content_schema('Task', TaskSchema, ('add', 'view', 'edit'))
    config.add_content_schema('TimeEntry', TimeEntrySchema, ('add', 'view', 'edit'))
    config.add_content_schema('Tariff', TariffSchema, ('add', 'view', 'edit'))
