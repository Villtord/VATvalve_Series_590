"""
Last update: 21 August 2020
Created: 21 August 2020

Valve monitor class which runs in a separate thread.

@author: Victor Rogalev
"""
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, QTimer
from DriverVAT import DriverVAT
import time


class WorkerSignals(QObject):
    value = pyqtSignal(str)

class MonitorStatus(QRunnable):
    def __init__(self, COM_port, *args, **kwargs):
        self.comport = COM_port
        self.command = args
        super(self.__class__, self).__init__()
        self.signals = WorkerSignals()
        self.is_paused = False
        self.is_killed = False
        self.request_flag = False
        print("I am a thread monitoring the valve")

    @pyqtSlot()
    def run(self):
        # Start the thread
        print ("starting the thread")
        
        self.my_valve=DriverVAT(self.comport)
        
        while True:
            time.sleep(0.5)  #  update interval
            try:
                received = self.my_valve.get_parameter(*self.command)
            except Exception as e:
                print("An exception occurred during valve monitor process")
                print(e)
                pass
            try:
                if received:
                    self.signals.value.emit(received)
            except:
                print("no received signal")
                pass
            
            while self.is_paused:
                if self.request_flag:
                    response = self.my_valve.get_parameter(self.new_request)
                    if response:
                        self.request_flag = False 
                        self.new_request = ""
                        self.resume()
                time.sleep(0.01)
            
            if self.is_killed:
                return
    
    def request(self, command):
        print ("request received")
        self.is_paused = True
        self.new_request = command
        self.request_flag = True

    
    def resume(self):
        print ("resumed")
        self.is_paused = False
    
    def kill(self):
        self.is_killed = True
        self.timer.stop()
        self.timer.deleteLater()
