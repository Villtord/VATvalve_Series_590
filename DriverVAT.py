"""
Last update: 21 August 2020
Created: 21 August 2020

Driver for motorised VAT valve series 590 with serial RS232 interface.
The latter must be connected through a certain COM port (virtual or real).

@author: Victor Rogalev
"""

import serial.tools.list_ports
import logging
import io
import time


class DriverVAT:
    def __init__(self, com_name):
        self.com_name = com_name

        """Opens serial connection and request/read the values"""
        self.ser = serial.Serial(self.com_name,
                            baudrate=9600,
                            bytesize=serial.SEVENBITS,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=0.05)
        self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1),
                                  newline='\n',
                                  line_buffering=True)
        
    def get_parameter(self, *args: "required command(s)"):
        self.answer = ""
        """Write a command(s) to the controller and read the reply """
        if args:
            for command in args:
                try:
                    command_full = str(command)+ "\n"
                    self.ser_io.write(command_full)
                    self.read_str_raw = self.ser_io.read()
                except Exception as e:
                    logging.exception(e)
                    print (e)
                    pass
                self.answer += self.read_str_raw
        else:
            pass
        try:
            return self.answer
        except Exception as e:
            logging.exception(e)
            pass
    
    def close(self):
        self.ser.close()

# my_driver = DriverVAT("COM25")
# # # # reply = my_driver.get_parameter("R:000100")
# reply = my_driver.get_parameter("i:38")
# # # # reply = my_driver.get_parameter("C:")
# reply = my_driver.get_parameter("P:")
# # # # reply = my_driver.get_parameter("i:21")
# print (reply)
# # my_driver.close()
