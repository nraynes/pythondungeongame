# Player class holds player information and methods.
class Player:
    playerSprite = '8'    # The character that represents the player.
    position = [0, 0]    # The current position of the player on the field.

    # getCollision function takes in the display object and optionally coordinates and returns whether
    # the player is colliding with a wall (Returns 1), an item (Returns 2), or nothing (Returns 0).
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

    # Next four functions are for moving the player. Takes in the display object and will check
    # whether the player is going to collide with something, then either update the players position
    # if applicable, and return whatever the player may have been colliding with. (Returns either 0; 1; or 2)
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

    # Next four functions will place the player at a predetermined position on the field.
    # This is used to place the player in the right position when moving between rooms.
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
