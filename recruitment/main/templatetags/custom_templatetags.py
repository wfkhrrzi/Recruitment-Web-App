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

@register.filter('split')
def split_string(string:str,arg:str):
    return string.split(arg)

@register.inclusion_tag("main/components/initscreening/eval_label_leads.html")
def show_eval_lead(lead):    
    return {"lead": lead,}

@register.inclusion_tag("main/components/initscreening/label_leads.html")
def show_pending_lead(lead):    
    return {"lead": lead,}

@register.inclusion_tag("main/components/initscreening/status_editable_field.html")
def show_status_editable_field(
    is_proceed:bool, 
    label = None, 
    proceed_label = "proceed", 
    reject_label = "reject", 
    attr_name = "status-edit",
    show_submit_btn = False,
    submit_name = "is_proceed",
):
    
    return {
        "label": label,
        "proceed_label": proceed_label,
        "reject_label": reject_label,
        "is_proceed": is_proceed,
        "attr_name": attr_name,
        "show_submit_btn": show_submit_btn,
        "submit_name": submit_name,
    }


