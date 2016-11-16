from betahaus.roadrunner.schemas.base import BaseOrgSchema


class ProjectSchema(BaseOrgSchema):
    pass


def includeme(config):
    config.add_content_schema('Project', ProjectSchema, ('add', 'view', 'edit'))
