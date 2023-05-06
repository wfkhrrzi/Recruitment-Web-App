from django.urls import reverse
from django.http import HttpRequest
from main.models import Candidate
from django.apps import apps
from django.db.models import Q, Case, When, Value, Count, OuterRef, Subquery, F, CharField, Prefetch


# load sidebar

SB_URLS = ( 
    reverse('main:initscreening.index.default'),
    reverse('main:prescreening.index.default'),
    reverse('main:cbi.index.default'),
)
SB_DISABLED = {'fill_color':'#FFFFFF','stroke_color':'#5B5B5B','disabled':True}
SB_ONGOING = {'fill_color':'#CCECEB','stroke_color':'#00635B',}
SB_PROCEED = {'fill_color':'#00A19C','stroke_color':'#00635B',}
SB_FAILED = {'fill_color':'#D42626','stroke_color':'#AC0C0C',}

app = apps.get_app_config('main')

def get_stage(key):
    return key.split(':')[0]

def sidebar(request:HttpRequest):
    found = False
    for sb_url in SB_URLS:
        if sb_url in request.path:
            found = True
    if not found:
        return {}

    # initialize sidebar
    dict_sidebar={
        'initial screening':{
            'overall':SB_DISABLED,
        },
        'prescreening':{
            'overall':SB_DISABLED,
            'instruction sent':SB_DISABLED,
            'assessment submitted':SB_DISABLED,
            'assessment validated':SB_DISABLED,
        },
        'cbi':{
            'overall':SB_DISABLED,
            'interview scheduled':SB_DISABLED,
            'interview conducted':SB_DISABLED,
            'interview assessed':SB_DISABLED,

        },
        'hiring':{
            'overall':SB_DISABLED,
            'joining confirmation':SB_DISABLED,
        },    
    }
    
    # retrieve candidate 
    stage,stage_id = tuple(request.path.strip('/').split('/'))
    stage_model = app.get_model(stage).objects.get(id=stage_id)
    
    # fetch status of stages
    dict_status = list(Candidate.objects.filter(id=stage_model.candidate.id).values(
        initialscreening_status=F('initialscreening__status__codename'),
        prescreening_status=F('prescreening__status__codename'),
        cbi_status=F('cbi__status__codename'),
        overall_status_ = F('overall_status__codename')
    ))[0]

    # return {"dict_status":dict_status}

    # dict_sidebar['overall_status_']=dict_status['overall_status_']

    # parse status
    if 'initscreening' in dict_status['overall_status_']:
        dict_sidebar['initial screening']['overall'] = SB_ONGOING

        return {'sidebar':dict_sidebar}

    for x in ['prescreening','cbi',]:
        if x in dict_status['overall_status_']:
            for stage in dict_sidebar:
                if stage != x:
                    dict_sidebar[stage] = {phase:SB_PROCEED for phase,v in dict_sidebar[stage].items()}
                else:
                    dict_sidebar[stage] = {phase:SB_ONGOING for phase,v in dict_sidebar[stage].items()}
                    break

    # return {'sidebar':dict_sidebar}

    if 'cbi' in dict_status['overall_status_']:
        if 'proceed' in dict_status['cbi_status']:
            dict_sidebar['cbi'] = {phase:SB_PROCEED for phase,v in dict_sidebar[stage].items()}
            if 'not proceed' in dict_status['cbi_status']:
                dict_sidebar['cbi']['overall'] = SB_FAILED

        elif 'interview' in dict_status['cbi_status']:
            dict_sidebar['cbi']['interview scheduled'] = SB_PROCEED

        elif 'result' in dict_status['cbi_status']:
            dict_sidebar['cbi']['interview scheduled'] = SB_PROCEED
            dict_sidebar['cbi']['interview conducted'] = SB_PROCEED

    if 'prescreening' in dict_status['overall_status_']:
        if 'proceed' in dict_status['prescreening_status']:
            dict_sidebar['prescreening'] = {phase:SB_PROCEED for phase,v in dict_sidebar[stage].items()}
            if 'not proceed' in dict_status['prescreening_status']:
                dict_sidebar['prescreening']['overall'] = SB_FAILED

        elif 'submission' in dict_status['prescreening_status']:
            dict_sidebar['prescreening']['instruction sent'] = SB_PROCEED

        elif 'submitted' in dict_status['prescreening_status']:
            dict_sidebar['prescreening']['instruction sent'] = SB_PROCEED
            dict_sidebar['prescreening']['assessment submitted'] = SB_PROCEED


    return {
        'sidebar':dict_sidebar
    }

