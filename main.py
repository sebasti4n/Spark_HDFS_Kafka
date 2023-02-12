from pymodbus.client.sync import ModbusSerialClient

client =  ModbusSerialClient(method='rtu', port="", baudrate, bytesize=8, stopbits=1, parity='N')
connection = client.connect()
print(connection)

res = client.read_input_registers(address=0, count=10, unit=1)
print(res.registers)