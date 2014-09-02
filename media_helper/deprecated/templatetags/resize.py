from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def resize(context, image):
    ''' This is no longer used, but im waiting before I delete it '''
    
    from media_helper.resizer import resize
    from media_helper.settings import Settings
    import os
    try:
        resolution = context['request'].session['resolution']
    except KeyError:
        resolution = str(Settings().default)


    path = context['MEDIA_URL']
    return os.path.join(path, resolution, image)

