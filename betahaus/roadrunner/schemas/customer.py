from betahaus.roadrunner.schemas.base import BaseOrgSchema


class CustomerSchema(BaseOrgSchema):
    pass


def includeme(config):
    config.add_content_schema('Customer', CustomerSchema, ('add', 'view', 'edit'))
