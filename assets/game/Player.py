class Player:
    playerSprite = '8'
    position = [0, 0]

    def getCollision(self, display, x=-1, y=-1):
        if x == -1:
            x = self.position[0]
        if y == -1:
            y = self.position[1]
        if x <= 0 or x >= display.width-1 or y <= 0 or y >= display.height-1:
            return 1
        elif display.playingField[y][x] == 'I':
            return 2
        return 0

    def moveUp(self, display):
        willCollide = self.getCollision(display, self.position[0], self.position[1]-1)
        if willCollide != 1:
            display.playingField[self.position[1]][self.position[0]] = ' '
            self.position[1] -= 1
            display.playingField[self.position[1]][self.position[0]] = self.playerSprite
        return willCollide

    def moveDown(self, display):
        willCollide = self.getCollision(display, self.position[0], self.position[1]+1)
        if willCollide != 1:
            display.playingField[self.position[1]][self.position[0]] = ' '
            self.position[1] += 1
            display.playingField[self.position[1]][self.position[0]] = self.playerSprite
        return willCollide

    def moveRight(self, display):
        willCollide = self.getCollision(display, self.position[0]+1, self.position[1])
        if willCollide != 1:
            display.playingField[self.position[1]][self.position[0]] = ' '
            self.position[0] += 1
            display.playingField[self.position[1]][self.position[0]] = self.playerSprite
        return willCollide

    def moveLeft(self, display):
        willCollide = self.getCollision(display, self.position[0]-1, self.position[1])
        if willCollide != 1:
            display.playingField[self.position[1]][self.position[0]] = ' '
            self.position[0] -= 1
            display.playingField[self.position[1]][self.position[0]] = self.playerSprite
        return willCollide

    def setUp(self, display):
        display.playingField[self.position[1]][self.position[0]] = ' '
        self.position[1] = 1
        display.playingField[self.position[1]][self.position[0]] = self.playerSprite

    def setDown(self, display):
        display.playingField[self.position[1]][self.position[0]] = ' '
        self.position[1] = 18
        display.playingField[self.position[1]][self.position[0]] = self.playerSprite

    def setLeft(self, display):
        display.playingField[self.position[1]][self.position[0]] = ' '
        self.position[0] = 1
        display.playingField[self.position[1]][self.position[0]] = self.playerSprite

    def setRight(self, display):
        display.playingField[self.position[1]][self.position[0]] = ' '
        self.position[0] = 38
        display.playingField[self.position[1]][self.position[0]] = self.playerSprite
