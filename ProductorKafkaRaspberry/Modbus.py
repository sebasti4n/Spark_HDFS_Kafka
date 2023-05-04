from pymodbus.client.sync import ModbusSerialClient
import time
from datetime import datetime

## Cliente Modbus Rtu serial 
client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=9600, bytesize=8, stopbits=1, parity='N')

connection = client.connect()
## Booleano de confirmación de la conección
print("Conección Modbus exitosa", connection)


def datajson():
    ## Lectura de entradas de la conección Modbus
    res = client.read_input_registers(address=0, count=10, unit=1)
    #Getting the current date and time
    dt = datetime.now()
    print("Confirmando Modbus a kafka")
    return {
        "time": dt, 
        "voltage": (res.registers[0])/10,
        "current": (res.registers[1])/1000,
        "Power": (res.registers[3])/10,
        "Energy": res.registers[5],
        "Frecuency": (res.registers[7])/10,
        "PowerFactor": (res.registers[8])/100
        }
    
