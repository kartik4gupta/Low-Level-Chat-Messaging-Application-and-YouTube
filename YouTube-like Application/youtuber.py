import pika
import sys
import json

class Youtuber:
    def __init__(self, youtuber_name, video_name):
        self.youtuber_name = youtuber_name
        self.video_name = video_name

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def publish_video(self):
        self.channel.basic_publish(
            exchange='',
            routing_key='main_queue',
            body=json.dumps({"youtuber": self.youtuber_name, "video_name": self.video_name, "action": "upload"})
        )
        print("SUCCESS")

# Extract command line arguments
youtuber_name = sys.argv[1]
video_name = sys.argv[2]

# Create an instance of Youtuber and publish the video
youtuber = Youtuber(youtuber_name, video_name)
youtuber.publish_video()