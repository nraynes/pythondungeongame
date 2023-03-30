import platform
import subprocess

class Display:
    width = 40
    height = 20
    playingField = [[' ' for x in range(40)] for y in range(20)]
    message = ""

    def update(self, newField):
        for y in range(self.height):
            for x in range(self.width):
                self.playingField[y][x] = newField[y][x]

    def clearScreen(self):
        if platform.system() == "Windows":
            if platform.release() in {"10", "11"}:
                subprocess.run("", shell=True)
                print("\033c", end="")
            else:
                subprocess.run(["cls"])
        else:
            print("\033c", end="")

    def render(self):
        strOutput = ''
        for h in range(self.height):
            for w in range(self.width):
                strOutput += self.playingField[h][w]
            strOutput += '\n'
        self.clearScreen()
        print(strOutput + '\n' + self.message + '\n')

    def setMiddle(self, c):
        self.playingField[9][19] = c

    def checkMiddle(self, c):
        return 1 if self.playingField[9][19] == c else 0

    def setRight(self, c):
        self.playingField[9][39] = c

    def setLeft(self, c):
        self.playingField[9][0] = c

    def setUp(self, c):
        self.playingField[0][19] = c

    def setDown(self, c):
        self.playingField[19][19] = c

    def clearMessage(self):
        self.message = ''
