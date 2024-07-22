import pika
import sys
import json

class User:
    def __init__(self, user_name, action=None, youtuber=None):
        self.user_name = user_name
        self.action = action
        self.youtuber = youtuber

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.user_name)
        self.personal_queue = self.user_name

    def perform_action(self):
        if self.action == "s" or self.action == "u":
            self.update_subscription()
        else:
            print(f"{self.user_name} logged in")

    def update_subscription(self):
        if self.action == "s":
            subscribe = True
            print(f"{self.user_name} subscribed to {self.youtuber}")
        elif self.action == "u":
            subscribe = False
            print(f"{self.user_name} unsubscribed from {self.youtuber}")

        self.channel.queue_declare(queue='main_queue')
        self.channel.basic_publish(
            exchange='',
            routing_key='main_queue',
            body=json.dumps({"user": self.user_name, "action": "subscription", "youtuber": self.youtuber, "subscribe": subscribe})
        )
        print("SUCCESS")

    def receive_notifications(self, ch, method, properties, body):
        notification = json.loads(body.decode())
        print(f"New Notification: {notification['youtuber']} uploaded {notification['video_name']}")

    def run(self):
        self.perform_action()

        if self.action is None:
            self.channel.basic_consume(queue=self.personal_queue, on_message_callback=self.receive_notifications, auto_ack=True)

            print(f"{self.user_name} is waiting for notifications. To exit press CTRL+C")
            self.channel.start_consuming()

# Extract command line arguments
user_name = sys.argv[1]
action = sys.argv[2] if len(sys.argv) > 2 else None
youtuber = sys.argv[3] if len(sys.argv) > 3 else None

# Create an instance of User and run it
user = User(user_name, action, youtuber)
user.run()
