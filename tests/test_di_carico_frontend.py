from locust import HttpUser, task, between

# Indirizzi IP
FRONTEND_URL = "https://172.213.194.22"
BACKEND_URL = "https://172.213.194.23"


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.verify = False

    @task
    def load_frontend(self):
        self.client.get("/")
