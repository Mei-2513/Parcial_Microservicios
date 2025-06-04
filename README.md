SECCIÓN 1: CONCEPTOS TEÓRICOS:

1.1 RabbitMQ
● Explique qué es RabbitMQ y cuándo se debe utilizar una cola frente a un
exchange tipo fanout

RabbitMQ es un sistema de mensajería que permite que diferentes partes de una aplicación se comuniquen entre sí enviando mensajes. 
Este nos sirve cuando queremos que los servicios trabajen de forma independiente y asincrónica, es decir, sin tener que esperar unos a otros
y se usa un exchange fanout cuando queremos enviar el mismo mensaje a varios servicios al mismo tiempo. No importa el contenido del mensaje ni a quién va dirigido: todos los que estén conectados lo reciben.

● ¿Qué es una Dead Letter Queue (DLQ) y cómo se configura en RabbitMQ?

Una Dead Letter Queue (DLQ) es una cola especial donde se envían los mensajes que no se pudieron procesar correctamente. Esto puede pasar cuando el mensaje es rechazado por el consumidor. 
Este se configura enlazando una cola principal con otra cola secundaria usando argumentos

1.2 Docker y Docker Compose
● Diferencia entre un volumen y un bind mount con ejemplos.

Volumen: Docker guarda los datos por su cuenta.
un ejemplo seria

volumes:
  - mydata:/app/data
este guarda datos de /app/data dentro de Docker, aunque borres el contenedor.

Bind mount: Usás una carpeta de tu compu directamente.
un ejemplo
volumes:
  - ./mi-carpeta:/app/data

esto es lo que pongo en ./mi-carpeta aparece dentro del contenedor.

● ¿Qué implica usar network_mode: host en un contenedor?.

Significa que el contenedor comparte la red directamente con la computadora (host).

1.3 Traefik
● Función de Traefik en una arquitectura de microservicios.

este funciona como un reverse proxy y balanceador de carga, es como la puerta de los microservicios.

● ¿Cómo se puede asegurar un endpoint usando certificados TLS automáticos
en Traefik?

Traefik puede obtener y renovar certificados HTTPS automáticamente usando Let's Encrypt.

SECCIÓN 2: DESARROLLO PRÁCTICO

usamos docker-compose up --build -d
para construir las imagenes y levantar los contonedores juntos y -d para que corran en segundo plano

luego mplementamos la arquitectura de microservicios que incluya:

● Una API REST en Flask o FastAPI
● Un worker que consuma mensajes desde RabbitMQ
● Traefik como reverse proxy
● Toda la solución orquestada con Docker Compose

Creamos un archivo docker-compose.yml que incluya los servicios:
● api
● worker
● rabbitmq
● traefik
![image](https://github.com/user-attachments/assets/1b17c4a0-2156-45f8-a991-a18c229edd5e)

2.2 API productora de mensajes
lo implementamos:
![image](https://github.com/user-attachments/assets/36e86195-5c02-45bc-b6f9-dbc6f128d911)

2.3 Worker consumidor

creamos un worker que escuche los mensajes:

![image](https://github.com/user-attachments/assets/124efc1c-765b-4ddc-b09c-000d721b3da0)

2.4 Configuración de Traefik
Configuramos /api:c 
![image](https://github.com/user-attachments/assets/60491c83-7c93-4320-a9c5-730ffddf4c7c)
y  /monitor
 ![image](https://github.com/user-attachments/assets/6b680f56-6e31-4523-a64f-64854b3fabef)

