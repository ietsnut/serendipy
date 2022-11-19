import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QWidget, QDesktopWidget
import sys, random

isq2 = 1.0/(2.0**0.5)
qubits = 3
gates = [{0: 'h', 1: 'cnot', 2:'h'}, {0: 's', 1: 'h'}, {0: 't', 1: 't'}, {1: 'h', 2: 'h'}]

class Qstate:
  def __init__(self, n):
    self.n = n
    self.state = np.zeros(2**self.n, dtype=np.complex)
    self.state[0] = 1

  def op(self, t, i):
    eyeL = np.eye(2**i, dtype=np.complex)
    eyeR = np.eye(2**(self.n - i - int(t.shape[0]**0.5)), 
        dtype = np.complex)
    t_all = np.kron(np.kron(eyeL, t), eyeR)
    self.state = np.matmul(t_all, self.state)

  def h(self, i):
    h_matrix = isq2 * np.array([
        [1,1],
        [1,-1]
    ])
    self.op(h_matrix, i)

  def t(self, i):
    t_matrix = np.array([
        [1,0],
        [0,isq2 + isq2 * 1j]
    ])
    self.op(t_matrix, i)

  def s(self, i):
    s_matrix = np.array([
        [1,0],
        [0,0+1j]
    ])
    self.op(s_matrix,i)

  def cnot(self, i):
    cnot_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    self.op(cnot_matrix, i)

  def swap(self, i):
    swap_matrix = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    self.op(swap_matrix, i)

class Gate(QWidget):

    def __init__(self, i, width, height):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(str(i))
        self.setWindowTitle(str(i))
        self.setGeometry(random.randint(0, width - 500), random.randint(0, height - 500), 500, 500)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def evaluate(self, next_state):
        self.label.setText(str(next_state))
      
class Serendipity(QMainWindow):

    def __init__(self, n, size):
        super().__init__()
        self.setGeometry(500, 500, 300, 300)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle(str(n) + " Qubit Circuit")
        self.s = Qstate(n)
        self.step = 0
        self.w = {}
        self.button = QPushButton(str(gates[self.step]))
        self.button.clicked.connect(self.evaluate)
        self.setCentralWidget(self.button)
        i = 0
        for state in self.s.state:
          self.w[i] = Gate(i, size.width(), size.height())
          i+=1

    def evaluate(self, checked):
      if (self.step < len(gates)):
        if (self.step < len(gates) - 1):
          self.button.setText(str(gates[self.step+1]))
        else:
          self.button.setText("close")
        for gate in gates[self.step]:
          getattr(self.s, gates[self.step][gate])(gate)
        i = 0
        for state in self.s.state:
          if state != 0j:
            self.w[i].evaluate(state)
            self.w[i].show()
          else:
            self.w[i].hide()
          i+=1
        self.step+=1
      else:
        for window in self.w:
          self.w[window].close() 
          self.w[window] = None
        self.close()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  screen = app.primaryScreen()
  size = screen.size()
  w = Serendipity(qubits, size)
  w.show()
  app.exec()