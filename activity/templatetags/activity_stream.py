from django import template

register = template.Library()

def safe_get(model, *attrs):
    # To do : improve this
    for attr in attrs:
        try:
            model = getattr(model, attr)
        except ValueError:
            return ""
    return model


def activity_stream_heading(activity):
    content_type = activity.content_type.name
    output = {
        'card': {
            'property': ['name'],
            'str': ' card named "{}"'
        },
        'list': {
            'property': ['name'],
            'str': ' a list named "{}"'
        },
        'column': {
            'property': ['name'],
            'str': ' a column named "{}"'
        },
        'referral': {
            'property': ['email'],
            'str': ' invited "{}"'
        },
        'board member': {
            'property': ['board', 'name'],
            'str':  ' joined "{}"'
        },
        'board': {
            'property': ['name'],
            'str': ' a board named "{}"'
        },
        'card member': {
            'property': ['board_member','user', 'username'],
            'str': ' {} to a card'
        },
        'card comment': {
            'property': ['comment'],
            'str': ' a comment "{}" on  a card'
        }
    }
    # * makes *args know that you are passing a list
    val = safe_get(activity.content_object,*output[content_type]['property'])
    return output[content_type]['str'].format(val)

register.filter('activity_stream_heading', activity_stream_heading)