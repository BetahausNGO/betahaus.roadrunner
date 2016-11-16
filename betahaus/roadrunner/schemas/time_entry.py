import colander
import deform
from arche.schemas import LocalDateTime
from repoze.folder import IFolder

from betahaus.roadrunner.interfaces import ITariff
from betahaus.roadrunner import _


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
        widget=deform.widget.DateTimeInputWidget(time_options={'interval': 5}),
        title=_("Start time")
    )
    stop_time = colander.SchemaNode(
        LocalDateTime(),
        missing=None,
        widget=deform.widget.DateTimeInputWidget(time_options={'interval': 5}),
        title=_("End time")
    )


def includeme(config):
    config.add_content_schema('TimeEntry', TimeEntrySchema, ('add', 'view', 'edit'))
