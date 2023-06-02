from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import time
import json
from django_celery_results.models import TaskResult
from main.utils import get_active_tasks

class WSResumeParserNotification(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.return_active_tasks()

    def receive(self,text_data):
        self.return_active_tasks()

    def return_active_tasks(self):
        # Fetch active tasks
        active_tasks = get_active_tasks()

        # return the active tasks
        if active_tasks:

            self.send(json.dumps({'lst_task':active_tasks}))
        
        else:
            self.send(json.dumps({'lst_task':None}))
