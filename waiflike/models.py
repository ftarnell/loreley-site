import re

from django.db import models
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel    
import markdownwl
from django.core.exceptions import ObjectDoesNotExist
from wagtail import wagtailimages

def sub_image(fname, optstr):
    opts = {}

    opts['spec'] = 'width-500'
    opts['classname'] = 'left'

    for opt in optstr:
        bits = opt.split('=', 1)
        opt = bits[0]
        value = ''

        if len(bits) > 1:
            value = bits[1]

        if opt == 'left':
            opts['classname'] = 'left'
        elif opt == 'right':
            opts['classname'] = 'right'
        elif opt == 'full':
            opts['classname'] = 'full-width'
        elif opt == 'width':
            try:
                opts['spec'] = "width-%d" % int(value)
            except ValueError:
                pass
    try:
        image = wagtailimages.models.get_image_model().objects.get(title = fname)
    except ObjectDoesNotExist:
        return '[image %s not found]' % (fname,)

    url = image.file.url
    formatter = wagtailimages.formats.Format('', '', opts['classname'], opts['spec'])
    return '<a href="%s" data-toggle="lightbox" data-type="image">%s</a>' % (image.file.url, formatter.image_to_html(image, ''))

def sub_page(name, optstr):
    try:
        text = name
        if len(optstr):
            text = optstr[0]

        page = SitePage.objects.get(title = name)
        url = page.url
        return '<a href="%s">%s</a>' % (url, text)
    except ObjectDoesNotExist:
        return '[page %s not found]' % (name,)

def wl_markdown(s):
    return markdownwl.markdownwl(s, MARKDOWN_EXTRAS)

MARKDOWN_EXTRAS = {
    '__default__': sub_page,
    'page:': sub_page,
    'image:': sub_image
}

class SitePage(Page):
    body = models.TextField()
    search_name = "Text page"

    indexed_fields = ('body', )

    @property
    def rendered(self):
        return mark_safe(wl_markdown(self.body))

SitePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]
