# Shodita-Scadita
Shodita es un sistema de bots en Python que permite obtener información para  almacenarlo en una base de datos mongoDB. En este proyecto se analiza la información con el objetivo de identificar PLCs S7 (200, 300, 1500, 2000) con snap7 y PLCs que usen modbus para posteriormente auditar esas IPs públicas para encontrar fallos de configuración, posibles denegación de servicios, vulnerabilidades públicas, etc
# ¿Qué necesitas?
- Python 2.7
  - Librerías:
- mongoDB 2.6.10
  - apt-get install mongoDB

# Bots:
  - Nobita-bot.py: 
    1. Identificar si el target es un PLC
    2. Extraer información de geolocalización del target
    3. Insertar datos en mongoDB
  - Shizuka-bot.py:
    1. Obtener dominios de los targets
    2. Insertar datos en mongoDB
  - Suneo-heartbleed.py:
    1. Comprobar si el target es vulnerable a Heartbleed
    2. Insertar datos en mongoDB
