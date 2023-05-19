# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

# class Example(QMainWindow):
    
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         btn1 = QPushButton('1', self)
#         btn1.move(30, 50)
#         btn2 = QPushButton('1', self)
#         btn2.move(150, 50)
#         btn1.clicked.connect(self.buttonClicked)
#         btn2.clicked.connect(self.buttonClicked)
#         self.statusBar()
#         self.setGeometry(300, 300, 300, 150)
#         self.setWindowTitle('Window')
#         self.show()

#     def buttonClicked(self):
#         sender = self.sender()
#         sender.setText(str(int(sender.text()) + 1))

# if __name__ == '__main__':
#     app = QApplication([])
#     ex = Example()
#     app.exec()

# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

# class MyEmitter(QObject):
#     my_signal = pyqtSignal(str)

#     def do_something(self):
#         self.my_signal.emit("test")

# class MyReceiver(QObject):

#     def handle_signal(self, text):
#         print("Received signal:", text)

# receiver = MyReceiver() # Creates a MyReceiver object
# emitter = MyEmitter() # Creates a MyEmitter object
# emitter.my_signal.connect(receiver.handle_signal)

# emitter.do_something()  # This will print "Received signal: 42 hello world"

import numpy as np
from scipy.integrate import quad_vec
import matplotlib.pyplot as plt

alpha = np.linspace(0.0, 2.0, num=30)

f = lambda x: x ** alpha * 0
x0, x1 = 0, 2
y = quad_vec(f, x0, x1)[0]

plt.plot(alpha, y)
plt.plot(alpha, f(alpha))
plt.show()
print(alpha)
print(y)