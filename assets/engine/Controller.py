import keyboard
import time

# Controller class that handles all input. This runs asynchronously to prevent input delay/misses.
class Controller:
    currentInput = [
        0,  # Up command, index 0
        0,  # Down command, index 1
        0,  # Right command, index 2
        0   # Left command, index 3
    ]

    # start function will start the loop where input is checked.
    def start(self):
        while 1:
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
            time.sleep(0.001)    # Sleep is to prevent lag.

    # getInput function takes in the name of a command and returns
    # the current status on whether that command is being input
    # by the user.
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

