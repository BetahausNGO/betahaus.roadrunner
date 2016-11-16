from betahaus.roadrunner.schemas.base import BaseOrgSchema


class OrganisationSchema(BaseOrgSchema):
    pass


def includeme(config):
    config.add_content_schema('Organisation', OrganisationSchema, ('add', 'view', 'edit'))
