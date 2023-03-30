import assets.game.Map
import assets.game.Player
import time

class Game:
    currentRoom = None
    score = 0
    itemTotal = 0
    retry = 1

    def displayStory(self, display, controller):
        for x in reversed(range(60)):
            if controller.getInput('down'):
                break
            display.clearScreen()
            print(
                'It is the year 1235 and alien lifeforms have visited earth to study them.\n'
                + 'Some of the humans have been rounded up and placed into labyrinths to study how they learn \n'
                + 'and remember. Your goal is to get all the items in every room of the labyrinth in order to escape \n'
                + 'the labyrinth and stop the alien lifeforms from taking any more humans.\n'
                + 'Be careful, however, because one of the aliens who is overseeing the experiment \n'
                + 'is hiding in a room waiting to strike. Be sure not to enter the wrong room or your journey may \n'
                + 'end before it even begins!\n\n'
                + 'Instructions: Make your way through each room in the labyrinth. \n'
                + 'To enter a new room, just walk into a wall that has a marking on it \n'
                + 'indicating that there is a room behind that wall. \n'
                + 'Walk over the items in the center of each room to pick them up. \n'
                + 'You win if you collect all the items. \n'
                + 'You lose if you encounter the villain before collecting all the items.\n\n'
                + 'Hold "S" to skip.\n\n'
                + 'Game starts in ' + str(x) + ' seconds...'
            )
            time.sleep(1)

    def reset(self):
        self.score = 0
        self.itemTotal = 0

    def main(self, display, controller):
        self.reset()
        self.displayStory(display, controller)
        gameMap = assets.game.Map.Map()
        gameMap.reset()
        gameMap.setSeed()
        self.itemTotal = gameMap.build()
        numOfRooms = gameMap.getNumberOfRooms()
        player = assets.game.Player.Player()
        self.currentRoom = gameMap.startRoom
        display.update(self.currentRoom.sprite.graphic)
        player.position = [19, 18]
        display.playingField[player.position[1]][player.position[0]] = player.playerSprite
        display.render()

        while 1:
            if not self.currentRoom.startRoom:
                if self.currentRoom.villainRoom:
                    display.setMiddle('V')
                    gameScorePercent = round((100 / self.itemTotal) * self.score)
                    display.message = "Oh no! You've encountered the alien!"
                    display.render()
                    time.sleep(3)
                    display.message = 'You lost! Your score was ' + str(gameScorePercent) + '%'
                    display.render()
                    time.sleep(3)
                    display.clearScreen()
                    break
                elif self.currentRoom.itemVisible:
                    display.setMiddle('I')
                elif not display.checkMiddle(player.playerSprite):
                    display.setMiddle(' ')
            elif not display.checkMiddle(player.playerSprite):
                display.setMiddle(' ')
            if self.currentRoom.north:
                display.setUp('^')
            else:
                display.setUp('O')
            if self.currentRoom.south:
                display.setDown('-')
            else:
                display.setDown('O')
            if self.currentRoom.east:
                display.setRight('>')
            else:
                display.setRight('O')
            if self.currentRoom.west:
                display.setLeft('<')
            else:
                display.setLeft('O')
            collision = 0
            if controller.getInput('up'):
                collision = player.moveUp(display)
                if collision == 1 and self.currentRoom.north:
                    self.currentRoom = self.currentRoom.north
                    player.setDown(display)
            if controller.getInput('down'):
                collision = player.moveDown(display)
                if collision == 1 and self.currentRoom.south:
                    self.currentRoom = self.currentRoom.south
                    player.setUp(display)
            if controller.getInput('right'):
                collision = player.moveRight(display)
                if collision == 1 and self.currentRoom.east:
                    self.currentRoom = self.currentRoom.east
                    player.setLeft(display)
            if controller.getInput('left'):
                collision = player.moveLeft(display)
                if collision == 1 and self.currentRoom.west:
                    self.currentRoom = self.currentRoom.west
                    player.setRight(display)

            if collision == 2:
                self.score += 1
                self.currentRoom.itemVisible = 0
                if self.score >= self.itemTotal:
                    display.message = 'You won!'
                    display.render()
                    time.sleep(3)
                    display.clearScreen()
                    break

            # Debug block
            display.message = 's = ' + str(self.currentRoom.startRoom) + '\nm = ' \
                              + str(self.currentRoom.mainRoom) + '\nc = ' \
                              + str(self.currentRoom.corridor) + '\nv = ' \
                              + str(self.currentRoom.villainRoom) + '\npv = ' \
                              + str(self.currentRoom.potentialVillainRoom) + '\nseed = ' \
                              + str(gameMap.seed) + '\nrooms = ' \
                              + str(numOfRooms)

            display.render()
            time.sleep(0.005)

        while 1:
            playAgain = input('\n\nType "retry" if you would like to play again.'
                              + ' Otherwise, type "exit" to stop playing:\n')
            if playAgain == 'exit':
                self.retry = 0
                break
            elif playAgain == 'retry':
                print('retrying')
                break

    def start(self, display, controller):
        while self.retry:
            self.main(display, controller)

        print('Game over!')

