from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def resize(context, image):

    from media_helper.resizer import resize
    from media_helper.settings import MEDIA_HELPER_DEFAULT 
    import os
    try:
        resolution = context['request'].session['resolution']
    except KeyError:
        resolution = str(MEDIA_HELPER_DEFAULT)


    path = context['MEDIA_URL']
    return os.path.join(path, resolution, image)

