import pika
import json

class YoutubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='main_queue')
        self.channel.queue_declare(queue='youtuber_queue')  # Add this line

        self.youtuber_subscribers = {}
        self.user_queues = {}

    def consume_user_requests(self, ch, method, properties, body):
        request = json.loads(body.decode())
        action = request.get("action", None)

        if action == "subscription":
            self.handle_subscription_request(request)
        elif action == "upload":
            self.handle_video_upload_request(request)
        else:
            print("Invalid action:", action)
    
    def handle_video_upload_request(self, request):
        youtuber = request["youtuber"]
        video_name = request["video_name"]
        self.notify_users(youtuber, video_name)
        print(f"{youtuber} uploaded {video_name}")

    def handle_subscription_request(self, request):
        user = request["user"]
        youtuber = request["youtuber"]
        subscribe = request["subscribe"]

        if youtuber not in self.youtuber_subscribers:
            self.youtuber_subscribers[youtuber] = []

        if subscribe:
            self.youtuber_subscribers[youtuber].append(user)
            print(f"{user} subscribed to {youtuber}")
        else:
            self.youtuber_subscribers[youtuber].remove(user)
            print(f"{user} unsubscribed from {youtuber}")

    def handle_login(self, user):
        self.user_queues[user] = self.channel.queue_declare(queue='', exclusive=True).method.queue
        print(f"{user} logged in")

    def consume_youtuber_requests(self, ch, method, properties, body):
        request = json.loads(body.decode())
        youtuber = request["youtuber"]
        video_name = request["video_name"]

        if youtuber not in self.youtuber_subscribers:
            self.youtuber_subscribers[youtuber] = []

        for user in self.youtuber_subscribers[youtuber]:
            self.channel.basic_publish(
                exchange='',
                routing_key=user,
                body=json.dumps({"youtuber": youtuber, "video_name": video_name})
            )

    def notify_users(self, youtuber, video_name):
        if youtuber in self.youtuber_subscribers:
            for user in self.youtuber_subscribers[youtuber]:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=user,
                    body=json.dumps({"youtuber": youtuber, "video_name": video_name})
                )

    def run(self):
        self.channel.basic_consume(queue='main_queue', on_message_callback=self.consume_user_requests, auto_ack=True)
        self.channel.basic_consume(queue='youtuber_queue', on_message_callback=self.consume_youtuber_requests, auto_ack=True)

        print("YoutubeServer is waiting for requests. To exit press CTRL+C")
        self.channel.start_consuming()

# Create an instance of YoutubeServer and run it
youtube_server = YoutubeServer()
youtube_server.run()
