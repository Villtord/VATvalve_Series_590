"""
Last update: 24 August 2020
Created: 24 August 2020

GUI to control motorised VAT valve series 590

@author: Victor Rogalev
"""

import sys
import PyQt5.QtWidgets
import ValveUI


def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ValveUI.ValveControlApp()  # We set the form
    form.setWindowTitle('Valve Control 2020')  # Change window name
    # form.resize(500, 500)  # Resize the form
    form.show()  # Show the form
    sys.exit(app.exec_())  # Handle exit case


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function