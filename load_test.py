from locust import HttpUser, TaskSet, task, between
import random

# Sample reviews for testing
sample_reviews = [
    "Great website! Very easy to use.",
    "I love the UI and smooth performance.",
    "The system is fast and responsive.",
    "Could improve the design, but works well.",
    "Awesome experience, highly recommend!"
]

class ReviewTasks(TaskSet):
    @task(2)
    def get_homepage(self):
        """Simulate users visiting homepage"""
        self.client.get("/")

    @task(3)
    def post_review(self):
        """Simulate users posting reviews"""
        review_text = random.choice(sample_reviews)
        data = {
            "user": f"user_{random.randint(1,10000)}",
            "review": review_text,
            "rating": random.randint(1, 5)  # assuming you have rating field
        }
        self.client.post("/submit-review/", data=data)

class WebsiteUser(HttpUser):
    tasks = [ReviewTasks]
    wait_time = between(1, 3)  # users wait 1–3 sec between tasks