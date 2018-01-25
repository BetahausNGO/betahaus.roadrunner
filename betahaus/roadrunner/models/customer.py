from arche.api import Content
from arche.interfaces import IBlobs
from zope.interface import implementer

from betahaus.roadrunner import _
from betahaus.roadrunner.interfaces import ICustomer


@implementer(ICustomer)
class Customer(Content):
    type_name = "Customer"
    type_title = _("Customer")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-briefcase"
    blob_key = 'image'

    @property
    def image_data(self):
        blobs = IBlobs(self, None)
        if blobs:
            return blobs.formdata_dict(self.blob_key)
    @image_data.setter
    def image_data(self, value):
        IBlobs(self).create_from_formdata(self.blob_key, value)


def includeme(config):
    config.add_content_factory(Customer, addable_to='Root')
