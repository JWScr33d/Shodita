# Shodita-Scadita
Shodita es un sistema de bot independientes que permite obtener información para posteriormente almacenarlo en una base de datos. En este proyecto se orienta a la identificación de PLCs S7 (200, 300, 1500, 2000) con snap7 y PLCs que usen modbus.

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
