import os
from pathlib import Path
from django import template
from django.contrib.staticfiles import finders
from djangollmapi.settings import STATIC_VERSIONS
from django.templatetags.static import StaticNode

BASE_DIR = Path(__file__).resolve().parent.parent.parent
register = template.Library()


@register.simple_tag
def v_static(format_string):
    # {% v_static css/components/bottombar.css %}
    # should result in "/static/css/components/bottombar.css?v=1632137649"

    path = StaticNode.handle_simple(format_string)

    if path in STATIC_VERSIONS:
        v = STATIC_VERSIONS[path]
    else:
        try:
            fn = finders.find(format_string)
            t = os.path.getmtime(fn)
        except Exception as e:
            print('v_static cannot find this file: ', format_string)
            raise e

        v = int(t)
        STATIC_VERSIONS[path] = v

    path = f"{path}?v={v}"
    return path
