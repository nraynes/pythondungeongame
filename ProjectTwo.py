import threading
import platform
import subprocess
import keyboard
import time
import random

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


# Room class holds room information and acts as a node in a graph.
class Room:
    # Flags used for map generation.
    startRoom = 0
    mainRoom = 0
    corridor = 0
    villainRoom = 0
    potentialVillainRoom = 0
    itemVisible = 1

    # Location variable to hold the location of the room on the map.
    location = [0, 0]

    # Variables to hold references to attached rooms. (These are rooms the player can access from this room.)
    east = None
    west = None
    north = None
    south = None

    # Setter function to add a new instance of a Room on one of the four walls based on the input.
    def addRoom(self, wall):
        if wall == 'north':
            self.north = Room()
        elif wall == 'south':
            self.south = Room()
        elif wall == 'east':
            self.east = Room()
        elif wall == 'west':
            self.west = Room()

    # Setter function to set all the flags.
    def setFlags(self, s=0, m=0, c=0, v=0, pv=0):
        self.startRoom = s
        self.mainRoom = m
        self.corridor = c
        self.villainRoom = v
        self.potentialVillainRoom = pv

    # Setter function to set the location.
    def setLocation(self, x=0, y=0):
        self.location = [x, y]

    # getOpenSides takes in width and height of the map and returns a list of the walls with rooms attached.
    # Output example: [0, 1, 0, 1]; (This means that the south and west walls
    # have rooms or a border on the other side of them.)
    def getOpenSides(self, width=0, height=0):
        def collidesWithBorder(x=self.location[0], y=self.location[1], w=width, h=height):
            if width and height:
                if x < 0 or x > w - 1 or y < 0 or y > h - 1:
                    return 1
            return 0

        return [
            0 if self.north or collidesWithBorder(self.location[0], self.location[1] - 1) else 1,
            0 if self.south or collidesWithBorder(self.location[0], self.location[1] + 1) else 1,
            0 if self.east or collidesWithBorder(self.location[0] + 1, self.location[1]) else 1,
            0 if self.west or collidesWithBorder(self.location[0] - 1, self.location[1]) else 1
        ]

# Map class is a graph data structure that stores all the rooms.
class Map:
    startRoom = Room()
    itemCount = 0    # This holds the amount of items currently available in the map.
    height = 40
    width = 40
    seed = 0
    coords = []    # Holds the locations for every room on the map.
    sprite = [[' ' for x in range(40)] for y in range(20)]    # Holds the border for the room to display.

    # Constructor will build the border and set a random seed.
    def __init__(self):
        self.seed = random.randint(10000, 99999)    # Seed can only be 5 digits long. No less, no more.
        for x in range(40):
            self.sprite[0][x] = 'O'
            self.sprite[19][x] = 'O'
        for y in range(20):
            self.sprite[y][0] = 'O'
            self.sprite[y][39] = 'O'

    # morphSeed takes in a 5-digit number and outputs a different number that is also 5-digits long.
    def morphSeed(self, seed):
        def morphRandomNumber(x):
            return round(((((x + 5) * x) - 7) % (x / 388)) * (x / 10))

        newSeed = morphRandomNumber(seed)
        temp = seed
        while newSeed < 10000:
            temp = temp * 2
            newSeed = morphRandomNumber(temp)
        while newSeed > 99999:
            newSeed = round(newSeed / 2)
        if newSeed == 81458:
            newSeed -= 7
        elif newSeed == 51660:
            newSeed += 12
        if newSeed == 64796:
            newSeed += 2
        return newSeed

    # Simple getter function to return the total amount of items in the map.
    def getItemCount(self):
        return self.itemCount

    # Simple reset function to reset the map to empty.
    def reset(self):
        self.itemCount = 0
        self.seed = random.randint(10000, 99999)
        self.startRoom = Room()
        self.coords = []

    # build function to generate a randomized map based on the seed.
    # (The same seed will always produce the same map.)
    def build(self):
        # Set the start room of the map.
        self.startRoom.setFlags(1)
        self.startRoom.setLocation(19, 39)
        self.coords.append(self.startRoom.location)

        # Determine how many rooms should be the maximum for the length of the main hallway.
        maxMainRooms = self.seed % 40    # 40 rooms is the maximum allowable maximum for the length of the main hallway.
        if maxMainRooms < 8:    # 8 rooms is the minimum length of the main hallway
            maxMainRooms = 8
        currentBuildRoom = self.startRoom    # Room reference to build rooms off of.

        # Build the main hallway.
        currentSeed = self.seed
        for i in range(maxMainRooms):
            # This portion will get the open walls of the current room.
            availableWalls = self.getOpenSides(currentBuildRoom, self.width, self.height)
            mod = 0
            for x in range(len(availableWalls)):
                if availableWalls[x]:
                    mod += 1    # mod will store the amount of available positions to place a room from this room.
            if not mod:
                break    # End the main hallway early if there are no available places to put a room.
            pickedSideNum = currentSeed % mod    # Create a random number between 0 and the amount of available walls.
            sideNum = -1
            pickedSide = -1
            # Gets a random index from the availableWalls where a wall is open.
            for x in range(len(availableWalls)):
                if availableWalls[x]:
                    sideNum += 1
                if sideNum == pickedSideNum:
                    pickedSide = x
                    break
            # Based on pickedSide, a new room is added to the wall of the current room that was picked.
            if pickedSide == 0:
                currentBuildRoom.addRoom('north')
                self.itemCount += 1
                currentBuildRoom.north.setFlags(0, 1)
                currentBuildRoom.north.setLocation(currentBuildRoom.location[0], currentBuildRoom.location[1] - 1)
                self.coords.append([currentBuildRoom.location[0], currentBuildRoom.location[1] - 1])
                currentBuildRoom.north.south = currentBuildRoom
                currentBuildRoom = currentBuildRoom.north
            elif pickedSide == 1:
                currentBuildRoom.addRoom('south')
                self.itemCount += 1
                currentBuildRoom.south.setFlags(0, 1)
                currentBuildRoom.south.setLocation(currentBuildRoom.location[0], currentBuildRoom.location[1] + 1)
                self.coords.append([currentBuildRoom.location[0], currentBuildRoom.location[1] + 1])
                currentBuildRoom.south.north = currentBuildRoom
                currentBuildRoom = currentBuildRoom.south
            elif pickedSide == 2:
                currentBuildRoom.addRoom('east')
                self.itemCount += 1
                currentBuildRoom.east.setFlags(0, 1)
                currentBuildRoom.east.setLocation(currentBuildRoom.location[0] + 1, currentBuildRoom.location[1])
                self.coords.append([currentBuildRoom.location[0] + 1, currentBuildRoom.location[1]])
                currentBuildRoom.east.west = currentBuildRoom
                currentBuildRoom = currentBuildRoom.east
            elif pickedSide == 3:
                currentBuildRoom.addRoom('west')
                self.itemCount += 1
                currentBuildRoom.west.setFlags(0, 1)
                currentBuildRoom.west.setLocation(currentBuildRoom.location[0] - 1, currentBuildRoom.location[1])
                self.coords.append([currentBuildRoom.location[0] - 1, currentBuildRoom.location[1]])
                currentBuildRoom.west.east = currentBuildRoom
                currentBuildRoom = currentBuildRoom.west
            else:
                break
            # morph the seed so that the decision next time is randomized.
            currentSeed = self.morphSeed(currentSeed)

        # Build the corridors
        currentBuildRoom = self.startRoom
        previousBuildRoom = None
        currentCorridor = None
        currentSeed = self.morphSeed(currentSeed)
        # This variable is used to guarantee that at least one corridor will be
        # placed within the first half of the main hallway.
        guarantee = round((self.itemCount + 1) / 2)
        setBit = 0    # A variable that will set to 1 when we have added at least one corridor.
        corridorRooms = []    # List of room references that are part of a corridor
        PVRooms = []    # List of room references that are able to house the villain.

        # addHallways function is used to connect corridors together when possible and by a random factor.
        def addHallways(room):
            roomCoords = [
                [room.location[0], room.location[1] - 1],
                [room.location[0], room.location[1] + 1],
                [room.location[0] + 1, room.location[1]],
                [room.location[0] - 1, room.location[1]]
            ]
            for y in range(len(corridorRooms)):    # For every corridor room created so far.
                for z in range(len(roomCoords)):    # For every possible direction a room can be placed (4)
                    if roomCoords[z][0] == corridorRooms[y].location[0] \
                            and roomCoords[z][1] == corridorRooms[y].location[1] \
                            and currentSeed % 2:    # Random factor.
                        if z == 0:
                            if not room.north:
                                room.north = corridorRooms[y]
                                corridorRooms[y].south = room
                        elif z == 1:
                            if not room.south:
                                room.south = corridorRooms[y]
                                corridorRooms[y].north = room
                        elif z == 2:
                            if not room.east:
                                room.east = corridorRooms[y]
                                corridorRooms[y].west = room
                        elif z == 3:
                            if not room.west:
                                room.west = corridorRooms[y]
                                corridorRooms[y].east = room
        # This first loop goes through the main hallway to find potential rooms to make corridors off of.
        while 1:
            # find next main room
            # If there is a room in the direction, and it is not the previous room.
            if currentBuildRoom.north and currentBuildRoom.north.mainRoom and (not previousBuildRoom or (
                    previousBuildRoom and currentBuildRoom.north.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.north
            elif currentBuildRoom.south and currentBuildRoom.south.mainRoom and (not previousBuildRoom or
                         (previousBuildRoom and currentBuildRoom.south.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.south
            elif currentBuildRoom.east and currentBuildRoom.east.mainRoom and (not previousBuildRoom or
                         (previousBuildRoom and currentBuildRoom.east.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.east
            elif currentBuildRoom.west and currentBuildRoom.west.mainRoom and (not previousBuildRoom or
                         (previousBuildRoom and currentBuildRoom.west.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.west
            else:
                break    # If there is no direction to add a room, stop adding corridors.
            factor = currentSeed % 2
            currentSeed = self.morphSeed(currentSeed)
            # secondFactor is used to make sure that at least one corridor is made.
            # It has a higher percentage of becoming 0 the further we get to the middle of the main hallway.
            # It will always be 0 when at least half of the main hallway has been traversed.
            secondFactor = (currentSeed % guarantee) + setBit
            if factor or (not factor and not secondFactor):
                setBit == 1
                # Start making a new corridor here
                currentCorridor = currentBuildRoom    # Create the corridors just like the main rooms.
                while 1:
                    availableWalls = self.getOpenSides(currentCorridor, self.width, self.height)
                    mod = 0
                    for x in range(len(availableWalls)):
                        if availableWalls[x]:
                            mod += 1
                    if not mod:
                        # End corridor when there are no available sides,
                        # set the last room to potentially house the villain.
                        if not currentCorridor.mainRoom:
                            currentCorridor.setFlags(0, 0, 1, 0, 1)
                            PVRooms.append(currentCorridor)
                        break
                    pickedSideNum = currentSeed % mod
                    sideNum = -1
                    pickedSide = -1
                    for x in range(len(availableWalls)):
                        if availableWalls[x]:
                            sideNum += 1
                        if sideNum == pickedSideNum:
                            pickedSide = x
                            break
                    if pickedSide == 0:
                        currentCorridor.addRoom('north')
                        self.itemCount += 1
                        currentCorridor.north.setFlags(0, 0, 1)
                        currentCorridor.north.setLocation(currentCorridor.location[0],
                                                          currentCorridor.location[1] - 1)
                        self.coords.append([currentCorridor.location[0], currentCorridor.location[1] - 1])
                        currentCorridor.north.south = currentCorridor
                        currentCorridor = currentCorridor.north
                        addHallways(currentCorridor)    # Here we will add connecting hallways to the corridor.
                        corridorRooms.append(currentCorridor)
                    elif pickedSide == 1:
                        currentCorridor.addRoom('south')
                        self.itemCount += 1
                        currentCorridor.south.setFlags(0, 0, 1)
                        currentCorridor.south.setLocation(currentCorridor.location[0],
                                                          currentCorridor.location[1] + 1)
                        self.coords.append([currentCorridor.location[0], currentCorridor.location[1] + 1])
                        currentCorridor.south.north = currentCorridor
                        currentCorridor = currentCorridor.south
                        addHallways(currentCorridor)    # Here we will add connecting hallways to the corridor.
                        corridorRooms.append(currentCorridor)
                    elif pickedSide == 2:
                        currentCorridor.addRoom('east')
                        self.itemCount += 1
                        currentCorridor.east.setFlags(0, 0, 1)
                        currentCorridor.east.setLocation(currentCorridor.location[0] + 1,
                                                         currentCorridor.location[1])
                        self.coords.append([currentCorridor.location[0] + 1, currentCorridor.location[1]])
                        currentCorridor.east.west = currentCorridor
                        currentCorridor = currentCorridor.east
                        addHallways(currentCorridor)    # Here we will add connecting hallways to the corridor.
                        corridorRooms.append(currentCorridor)
                    elif pickedSide == 3:
                        currentCorridor.addRoom('west')
                        self.itemCount += 1
                        currentCorridor.west.setFlags(0, 0, 1)
                        currentCorridor.west.setLocation(currentCorridor.location[0] - 1,
                                                         currentCorridor.location[1])
                        self.coords.append([currentCorridor.location[0] - 1, currentCorridor.location[1]])
                        currentCorridor.west.east = currentCorridor
                        currentCorridor = currentCorridor.west
                        addHallways(currentCorridor)    # Here we will add connecting hallways to the corridor.
                        corridorRooms.append(currentCorridor)
                    else:
                        # End corridor when a side cannot be picked,
                        # set the last room to potentially house the villain.
                        if not currentCorridor.mainRoom:
                            currentCorridor.setFlags(0, 0, 1, 0, 1)
                            PVRooms.append(currentCorridor)
                        break
                    currentSeed = self.morphSeed(currentSeed)    # Morph the seed in the corridor making loop.
            currentSeed = self.morphSeed(currentSeed)    # Morph the seed in the main hallway traversal loop.
            if guarantee > 1:
                guarantee -= 1    # As we get closer to the middle of the main hallway, decrease the modulus.

        # Place the villain in one of the rooms that can house the villain.
        randIndex = random.randint(0, len(PVRooms) - 1)
        PVRooms[randIndex].setFlags(0, 0, 1, 1, 0)
        self.itemCount -= 1

        return self.itemCount    # We return the amount of items available in the map after generation.

    # Function to get the open sides of a room.
    def getOpenSides(self, room, width, height):
        availableWalls = room.getOpenSides(width, height)
        if availableWalls[0]:
            if self.coords.__contains__([room.location[0], room.location[1] - 1]):
                availableWalls[0] = 0
        if availableWalls[1]:
            if self.coords.__contains__([room.location[0], room.location[1] + 1]):
                availableWalls[1] = 0
        if availableWalls[2]:
            if self.coords.__contains__([room.location[0] + 1, room.location[1]]):
                availableWalls[2] = 0
        if availableWalls[3]:
            if self.coords.__contains__([room.location[0] - 1, room.location[1]]):
                availableWalls[3] = 0
        return availableWalls

# This is the game class that houses the game itself, including game state, and the game loop.
class Game:
    # Game state variables.
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

    # This is the main game loop.
    def main(self, display, controller):
        # Build the game first.
        self.reset()    # reset game variables.
        self.displayStory(display, controller)
        gameMap = Map()
        gameMap.reset()    # Map will keep using the same memory space, this is needed to reset the map state.
        self.itemTotal = gameMap.build()    # Build the map and set the itemTotal.
        player = Player()
        self.currentRoom = gameMap.startRoom
        display.update(gameMap.sprite)
        player.position = [19, 18]
        display.playingField[player.position[1]][player.position[0]] = player.playerSprite  # Add the player to screen.
        display.clearMessage()
        display.render()

        # Start the actual loop
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

    # start method and main game loop are separate for improved readability.
    def start(self, display, controller):
        while self.retry:
            self.main(display, controller)

        print('Game over!')

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


# A display class that will handle all the output operations (Stuff to do with the screen).
class Display:
    width = 40
    height = 20
    playingField = [[' ' for x in range(40)] for y in range(20)]
    message = ""    # message is to display a string below the playingField.

    # Update method takes in a whole new field (2d lists) of the same size
    # as the playingField and replaces the playingField with this input.
    def update(self, newField):
        for y in range(self.height):
            for x in range(self.width):
                self.playingField[y][x] = newField[y][x]

    # clearScreen will quickly erase everything on the terminal to get ready for the next frame to be rendered.
    def clearScreen(self):
        if platform.system() == "Windows":
            if platform.release() in {"10", "11"}:
                subprocess.run("", shell=True)
                print("\033c", end="")
            else:
                subprocess.run(["cls"])
        else:
            print("\033c", end="")

    # render function will build the 2d list "playingField" into a string, clear the screen and display the new string.
    def render(self):
        strOutput = ''
        for h in range(self.height):
            for w in range(self.width):
                strOutput += self.playingField[h][w]
            strOutput += '\n'
        self.clearScreen()
        print(strOutput + '\n' + self.message + '\n')

    # All set functions are to set specific points on the playingField to display a specified character.
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

    # Remove any message.
    def clearMessage(self):
        self.message = ''

# An engine class to operate the different threads for input/output along with the game itself.
class Engine:
    def start(self):
        # Create new instances of the classes for input, output, and the game itself.
        display = Display()
        controller = Controller()
        game = Game()

        # Create new threads for the controller and game so that they may run in parallel.
        conTask = threading.Thread(target=controller.start, args=(), kwargs={})
        gameTask = threading.Thread(target=game.start, args=(display, controller), kwargs={})

        # Start the threads for the game and controller.
        # Controller must run in parallel with game in order for input to be measured constantly.
        conTask.start()
        gameTask.start()

def main():
    engine = Engine()    # Create a new game engine.
    engine.start()    # Start your engines!


main()