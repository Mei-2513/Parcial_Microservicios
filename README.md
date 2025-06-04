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




