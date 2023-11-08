from locust import HttpUser, task, between
import json


class Payload(HttpUser):
    @task
    def payload(self):
        res = self.client.get('/api/v2/demo/limit')
        res = json.loads(res.content)
