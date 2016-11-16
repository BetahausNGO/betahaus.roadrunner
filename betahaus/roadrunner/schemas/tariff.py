import colander

from betahaus.roadrunner import _


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
    config.add_content_schema('Tariff', TariffSchema, ('add', 'view', 'edit'))
