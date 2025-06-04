from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import pika
import os
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuración RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin123')
RABBITMQ_QUEUE = 'messages'

security = HTTPBasic()

class Message(BaseModel):
    content: str

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    correct_password = os.getenv('API_PASSWORD', 'admin123')
    if username != "admin" or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username

@app.post("/message")
async def create_message(message: Message, username: str = Depends(get_current_username)):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Declaración consistente de la cola
        channel.queue_declare(
            queue=RABBITMQ_QUEUE,
            durable=True
        )
        
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=message.content,
            properties=pika.BasicProperties(
                delivery_mode=2  # Mensaje persistente
            )
        )
        connection.close()
        logger.info(f"Message published to queue: {message.content}")
        return {"status": "Message published to RabbitMQ"}
    except Exception as e:
        logger.error(f"Error publishing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
