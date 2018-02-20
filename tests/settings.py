SECRET_KEY = 'you_saw_nothing.'

context_processors = [
    'django.template.context_processors.i18n']

loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader']


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'OPTIONS': {
        'debug': True,
        'context_processors': context_processors,
        'loaders': loaders,
        'string_if_invalid': '<< MISSING VARIABLE: %s >>'}}]


INSTALLED_APPS = [
    'invoice_generator.apps.InvoiceGeneratorConfig'
]
