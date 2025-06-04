import pika
import os
from datetime import datetime
import time
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin123')
RABBITMQ_QUEUE = 'messages'
OUTPUT_DIR = '/app/messages'

def connect_rabbitmq():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )
    return pika.BlockingConnection(parameters)

def process_message(ch, method, properties, body):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{OUTPUT_DIR}/message_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(body.decode())
        
        logger.info(f"Message saved to {filename}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

def setup_queue(channel):
    """Declaración consistente de la cola"""
    channel.queue_declare(
        queue=RABBITMQ_QUEUE,
        durable=True
    )
    channel.basic_qos(prefetch_count=1)

def main():
    try:
        connection = connect_rabbitmq()
        channel = connection.channel()
        
        setup_queue(channel)
        
        channel.basic_consume(
            queue=RABBITMQ_QUEUE,
            on_message_callback=process_message,
            auto_ack=False
        )
        
        logger.info("Worker started. Waiting for messages...")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == '__main__':
    while True:
        main()
        logger.info("Restarting worker in 5 seconds...")
        time.sleep(5)
