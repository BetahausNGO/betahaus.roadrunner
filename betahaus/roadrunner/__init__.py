from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('betahaus.roadrunner')



def includeme(config):
    config.include('.models')
    config.include('.schemas')
    config.include('.views')
    config.include('.fanstatic_lib')
    config.override_asset(to_override='arche:templates/',
                          override_with='betahaus.roadrunner:templates/overrides/')
