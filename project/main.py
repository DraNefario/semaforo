from machine import Pin, time_pulse_us
import time

# Configuração dos pinos dos sensores ultrassônicos
TRIG_PIN_LEFT = 14
ECHO_PIN_LEFT = 12
TRIG_PIN_RIGHT = 21
ECHO_PIN_RIGHT = 19

# Configuração dos pinos do semáforo
SEMAPHORE_PIN = 13

# Configuração dos limiares de distância para detectar carros
DISTANCE_THRESHOLD = 100  # Distância em centímetros

# Inicialização dos pinos
left_trig = Pin(TRIG_PIN_LEFT, Pin.OUT)
left_echo = Pin(ECHO_PIN_LEFT, Pin.IN)
right_trig = Pin(TRIG_PIN_RIGHT, Pin.OUT)
right_echo = Pin(ECHO_PIN_RIGHT, Pin.IN)
semaphore = Pin(SEMAPHORE_PIN, Pin.OUT)

def read_distance(trig_pin, echo_pin):
    trig_pin.value(0)
    time.sleep_us(2)
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)
    duration = time_pulse_us(echo_pin, 1, 20000)  # Timeout de 20ms
    if duration > 0:
        return duration * 0.034 / 2
    else:
        return -1  # Timeout

def detect_car(trig_pin, echo_pin):
    distance = read_distance(trig_pin, echo_pin)
    return distance < DISTANCE_THRESHOLD

while True:
    car_left = detect_car(left_trig, left_echo)
    car_right = detect_car(right_trig, right_echo)

    if car_left and car_right:
        # Se houver carros em ambos os sentidos, feche o semáforo
        semaphore.value(1)
        print("Semáforo fechado")
    else:
        # Caso contrário, mantenha o semáforo aberto
        semaphore.value(0)
        print("Semáforo aberto")

    time.sleep(0.1)  # Aguarda um curto período antes de fazer a próxima verificação

