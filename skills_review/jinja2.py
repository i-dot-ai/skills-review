import jinja2
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify


def environment(**options):
    extra_options = dict()
    env = jinja2.Environment(
        **{
            **options,
            **extra_options,
        }
    )
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "slugify": slugify,
        }
    )
    return env
