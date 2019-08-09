"""Utilities for unlocking media URLs."""

import re
from django.conf import settings

SRC_REGEX = re.compile("src=\"(?P<url>.+?)\"")


def update_media_links_in_rich_text(html_string):
    """Replace locked media image URLs with Django static tag.

    Args:
        html_string (str): String of HTML to check.

    Returns:
        String of updated HTML.
    """
    updated_html = re.sub(SRC_REGEX, replace_url, html_string)
    return updated_html


def replace_url(match):
    """Replace locked media image URL with Django static tag if required.

    Args:
        match (re.Match): Regular expression match object.

    Returns:
        Return string to replace match with.
    """
    url = match.group('url')
    url_prefix = settings.get('GS_BUCKET_NAME')
    if url_prefix and url.startswith(url_prefix):
        return '{% static "{}" %}'.format(url[len(url_prefix):])
    else:
        return match.group(0)
