"""
Last update: 21 August 2020
Created: 21 August 2020

main UI to control motorised VAT valve series 590

@author: Victor Rogalev
"""
from __future__ import unicode_literals

import logging
import math

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMessageBox

from MonitorClass import MonitorStatus
from SetupUI import Ui_MainWindow

global COM_port

COM_port = "COM25"


def are_you_sure_decorator(func):
    """Are you sure confirmation window is not shown only if god_mode_flag is True"""

    def wrapper(self, *args):
        button_reply = QMessageBox.question(self, 'PyQt5 message', "ARE YOU SURE???",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
        if button_reply == QMessageBox.Yes:
            func(self, *args)

    return wrapper


class ValveControlApp(Ui_MainWindow):
    global COM_port

    def __init__(self, *args):
        super(self.__class__, self).__init__(self, *args)
        self.objects_dict["Pressure [mbar]"][2].setText("0.000075")
        self.objects_dict["Position [0-1000]"][2].setText("0")
        self.threadpool = QThreadPool()

        "Thread to monitor valve position and pressure in He lamp as the valve see it"
        self.status_monitor = MonitorStatus(COM_port, "P:", "A:")
        self.status_monitor.signals.value.connect(self.update_monitor)
        self.threadpool.start(self.status_monitor)

        "Connect other slots to set up pressure or position"
        self.objects_dict["Pressure [mbar]"][2].returnPressed.connect(self.set_pressure)
        self.objects_dict["Position [0-1000]"][2].returnPressed.connect(self.set_position)

    def update_monitor(self, value):
        self.values = value.split("\n")[:-1]
        for x in self.values:
            if "P:" in x:
                value_pressure = 10**((int(x[3:])/100-12.66)/1.33)
                try:
                    self.objects_dict["Pressure [mbar]"][1].setText("{:1.9f}".format(value_pressure))
                except:
                    print("error updating pressure")

            elif "A:" in x:
                value_position = int(x[2:])
                try:
                    self.objects_dict["Position [0-1000]"][1].setText(str(value_position))
                except:
                    print("error updating position")
            else:
                self.statusbar.showMessage(x)

    @are_you_sure_decorator
    def set_pressure(self):
        print ("setting pressure")
        "replace comma with dot"
        if "," in self.objects_dict["Pressure [mbar]"][2].text():
            self.objects_dict["Pressure [mbar]"][2].setText(
                self.objects_dict["Pressure [mbar]"][2].text().replace(",", "."))

        new_pressure = float(self.objects_dict["Pressure [mbar]"][2].text())

        "set pressure"
        try:
            if 0.01 > new_pressure > 0.0:
                new_pressure_to_send = int((math.log10(new_pressure)*1.33+12.6945)*100)
                self.status_monitor.request("S:"+f'{new_pressure_to_send:08}')
        except Exception as e:
            logging.exception(e)
            print('error reading new pressure value from LineEdit')
            pass
    
    def set_position(self):
        print ("setting position")
        new_position = int(self.objects_dict["Position [0-1000]"][2].text())
        "set position"
        try:
            if 1000 >= new_position >= 0:
                self.status_monitor.request("R:"+f'{new_position:06}')
        except Exception as e:
            logging.exception(e)
            print('error setting new position value from LineEdit')
            pass
        
    def __close__(self):
        self.status_monitor.kill()
