from functools import partial

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

import markdown
import bleach
from bleach import css_sanitizer as cs


register = template.Library()


@register.filter
def django_markdownify(text, custom_settings="default"):

    try:
        django_markdownify_settings = settings.MARKDOWNIFY[custom_settings]
    except (AttributeError, KeyError):
        django_markdownify_settings = {}

    # Bleach settings
    whitelist_tags = django_markdownify_settings.get('WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = django_markdownify_settings.get('WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    whitelist_styles = django_markdownify_settings.get('WHITELIST_STYLES', cs.ALLOWED_CSS_PROPERTIES)
    whitelist_protocols = django_markdownify_settings.get('WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)

    # Markdown settings
    strip = django_markdownify_settings.get('STRIP', True)
    extensions = django_markdownify_settings.get('MARKDOWN_EXTENSIONS', [])
    extension_configs = django_markdownify_settings.get('MARKDOWN_EXTENSION_CONFIGS', {})

    # Bleach Linkify
    linkify = None
    linkify_text = django_markdownify_settings.get('LINKIFY_TEXT', {"PARSE_URLS": True})
    if linkify_text.get("PARSE_URLS"):
        linkify_parse_email = linkify_text.get('PARSE_EMAIL', False)
        linkify_callbacks = linkify_text.get('CALLBACKS', [])
        linkify_skip_tags = linkify_text.get('SKIP_TAGS', [])
        linkifyfilter = bleach.linkifier.LinkifyFilter

        linkify = [partial(linkifyfilter,
                           callbacks=linkify_callbacks,
                           skip_tags=linkify_skip_tags,
                           parse_email=linkify_parse_email
                           )]

    # Convert markdown to html
    html = markdown.markdown(text or "", extensions=extensions, extension_configs=extension_configs)

    # Sanitize html if wanted
    if django_markdownify_settings.get("BLEACH", True):
        css_sanitizer = bleach.css_sanitizer.CSSSanitizer(allowed_css_properties=whitelist_styles)
        cleaner = bleach.Cleaner(tags=whitelist_tags,
                                 attributes=whitelist_attrs,
                                 css_sanitizer=css_sanitizer,
                                 protocols=whitelist_protocols,
                                 strip=strip,
                                 filters=linkify,
                                 )

        html = cleaner.clean(html)

    return mark_safe(html)


def do_django_markdownify(parser, token):
    # Set up the nodelist and parse till we hit the enddjango_markdownify block
    nodelist = parser.parse(("enddjango_markdownify",))
    parser.delete_first_token()

    # Get the settings from the tag
    try:
        django_markdownify_settings = token.split_contents()[1]
    except IndexError:
        django_markdownify_settings = "default"

    return MarkDownifyNode(nodelist, django_markdownify_settings)


class MarkDownifyNode(template.Node):
    def __init__(self, nodelist, django_markdownify_settings):
        self.nodelist = nodelist
        self.django_markdownify_settings = django_markdownify_settings

    def render(self, context):

        # Build new nodelist with rendered and markdownified nodes
        node_list = []
        for node in self.nodelist:
            md_node = django_markdownify(node.render(context), custom_settings=self.django_markdownify_settings)
            node_list.append(md_node)

        return "".join(node_list)


register.tag("django_markdownify", do_django_markdownify)
