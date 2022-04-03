import pika
import json
from app.settings.settings import rabbitmb_settings


async def send_message(message):

    credentials = pika.PlainCredentials(
        rabbitmb_settings.RABBITMQ_USER,
        rabbitmb_settings.RABBITMQ_PASSWORD)

    connect = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmb_settings.RABBITMQ_HOST,
                                  port=rabbitmb_settings.RABBITMQ_PORT,
                                  credentials=credentials))

    channel = connect.channel()

    channel.queue_declare(queue='votes')
    channel.basic_publish(exchange='', routing_key='votes',
                          body=json.dumps(message))

    connect.close()
