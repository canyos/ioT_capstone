import tfluna
import timeout_decorator

with tfluna.TfLuna(baud_speed=115200, serial_name="/dev/serial0") as tfluna:
    tfluna.get_version()
    tfluna.set_samp_rate(10)
    #tfluna.set_baudrate(57600) # can be used to change the baud_speed
    distance,strength,temperature = tfluna.read_tfluna_data() 