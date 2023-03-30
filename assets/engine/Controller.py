import keyboard
import time

class Controller:
    currentInput = [
        0,  # Up command, index 0
        0,  # Down command, index 1
        0,  # Right command, index 2
        0   # Left command, index 3
    ]
    forceEnd = 0

    def start(self):
        while not self.forceEnd:
            if keyboard.is_pressed('w'):
                if self.currentInput[0] != 1:
                    self.currentInput[0] = 1
            else:
                if self.currentInput[0] != 0:
                    self.currentInput[0] = 0
            if keyboard.is_pressed('s'):
                if self.currentInput[1] != 1:
                    self.currentInput[1] = 1
            else:
                if self.currentInput[1] != 0:
                    self.currentInput[1] = 0
            if keyboard.is_pressed('d'):
                if self.currentInput[2] != 1:
                    self.currentInput[2] = 1
            else:
                if self.currentInput[2] != 0:
                    self.currentInput[2] = 0
            if keyboard.is_pressed('a'):
                if self.currentInput[3] != 1:
                    self.currentInput[3] = 1
            else:
                if self.currentInput[3] != 0:
                    self.currentInput[3] = 0
            if keyboard.is_pressed('p'):
                self.forceEnd = 1
            time.sleep(0.001)

    def end(self):
        self.forceEnd = 1

    def getInput(self, command):
        if command == 'up':
            return self.currentInput[0]
        elif command == 'down':
            return self.currentInput[1]
        elif command == 'right':
            return self.currentInput[2]
        elif command == 'left':
            return self.currentInput[3]
        else:
            return 0

