from admin import admin
from .models import Setting,Type

@admin.before_app_request
def add_settings():
    from app import app
    settings = app.config.copy()
    CACHED_SETTINGS = [
            'RECAPTCHA_PUBLIC_KEY',
            'RECAPTCHA_PRIVATE_KEY',
            'ADMIN_PER_PAGE',
            'CODEMIRROR_LANGUAGES',
            'CODEMIRROR_THEME',
            'BLUEPRINTS',
            'EXTENSIONS',
            'TEMPLATE_FILTERS',     
            'CONTEXT_PROCESSORS',
    ]
    for itm in CACHED_SETTINGS:
        setting = Setting.query.filter(Setting.name==itm).first()
        if setting is None:
            t = Type.query.filter(Type.name==type(settings[itm])).first()
            value = settings.get(itm,None)
            if value is None:
                value = ''
            if t is None:
                t = Type(type(settings[itm]))
                t.save()
            setting = Setting(
                    name=itm,type=t,value=value
            )
            setting.save()



