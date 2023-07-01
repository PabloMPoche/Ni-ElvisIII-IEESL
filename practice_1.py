# -*- coding: utf-8 -*-
import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

# En esta estapa especificamos el banco de entradas
ai_bankA = Bank.A
ai_bankB = Bank.B

# Indicamos los canal a habilitar para las lecturas
ai_channel0 = AIChannel.AI0
ai_channel1 = AIChannel.AI1
ai_channel2 = AIChannel.AI2

# Establecemos el rango del toma de muestras para las entradas
ai_range = AIRange.PLUS_OR_MINUS_5V

# Elegimos el modo de lectura
ai_mode = AIMode.SINGLE_ENDED

# Acá guardaremos las lecturas para luego ser pasadas a un TXT
measures = []

# Número de lecturas a realizar
n_of_measures_ps = 50000

# Tiempo entre lecturas
time_between_measures = 0.0001

print('Aplificador Operacional en desgloce')

# Configuramos los canales de entrada de acuerdo a los parametros
with AnalogInput({
        'bank': ai_bankA,
        'channel': ai_channel0,
        'range': ai_range,
        'mode': ai_mode
    }, {'bank': ai_bankA,
        'channel': ai_channel1,
        'range': ai_range,
        'mode': ai_mode
    }, {'bank': ai_bankB,
        'channel': ai_channel2,
        'range': ai_range,
        'mode': ai_mode
    }) as AI_multiple_channels:

    # configure the sample rate and start the acquisition
    AI_multiple_channels.start_continuous_mode(n_of_measures_ps)

    init_time = time.time()

    # leemos durante un periodo especificado
    for i in range(0, n_of_measures_ps):
        # Leemos los datos de entrada
        value_array = AI_multiple_channels.read()

        # Imprimimos los valores
        # (T, PR1, PR2, PR3)
        measure = tuple((time.time() - init_time)) + str(value_array)
        measures.append(measure)

        # Agregamos un pequeño delay para la toma de las muestras de un tiempo especificado
        time.sleep(time_between_measures)

    # stop signal acquisition
    AI_multiple_channels.stop_continuous_mode()
    
    # Escribimos en un txt
    with open('output.txt', 'a') as f:
        f.write('\n'.join(measures))
