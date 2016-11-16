from arche.api import Base
from arche.interfaces import IIndexedContent
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ITariff


@implementer(ITariff, IIndexedContent)
class Tariff(Base):
    type_name = "Tariff"
    type_title = _("Tariff")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-usd"
    title = ""
    price = None
    currency = ""
    vat = None


def includeme(config):
    config.add_content_factory(Tariff, addable_to = ('Organisation', 'Customer', 'Project'))
