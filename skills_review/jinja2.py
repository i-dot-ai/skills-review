import jinja2
import pypugjs
from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse
from markdown_it import MarkdownIt

markdown_converter = MarkdownIt()

DEFAULT = object()


@pypugjs.register_filter("markdown")
def markdown(text, ast):
    return markdown_converter.render(text)


def finalize(thing):
    if thing is None:
        return ""
    else:
        return thing


def is_empty_selected(data, name):
    if data.get(name) in ("", None):
        return "selected"
    else:
        return ""


def is_selected(data, name, value):
    if data.get(name) is value:
        return "selected"
    else:
        return ""


def environment(**options):
    extra_options = {"autoescape": True}
    env = jinja2.Environment(
        finalize=finalize,
        **{
            **options,
            **extra_options,
        },
    )
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "is_selected": is_selected,
            "is_empty_selected": is_empty_selected,
            "DEFAULT": DEFAULT,
            "get_messages": messages.get_messages,
        }
    )
    return env
