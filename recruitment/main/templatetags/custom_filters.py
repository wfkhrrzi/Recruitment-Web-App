from django import template

register = template.Library()

@register.filter
def format_card_title(value):
    words = value.split('_')
    capitalized_words = [word.capitalize() for word in words]
    formatted_string = ' '.join(capitalized_words)
    return formatted_string
