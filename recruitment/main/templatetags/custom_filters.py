from django import template
import math

register = template.Library()

@register.filter
def format_card_title(value):
    words = value.split('_')
    capitalized_words = [word.capitalize() for word in words]
    formatted_string = ' '.join(capitalized_words)
    return formatted_string

@register.filter
def any_ds_leads(lst_lead, bool_val):
    return any([True if lead['eval_is_proceed'] == bool_val else False for lead in lst_lead])

@register.filter
def all_ds_leads(lst_lead, bool_val):
    return all([True if lead['eval_is_proceed'] == bool_val else False for lead in lst_lead])
