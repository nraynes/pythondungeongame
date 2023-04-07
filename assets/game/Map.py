import random
import assets.game.Room

# Map class is a graph data structure that stores all the rooms.
class Map:
    startRoom = assets.game.Room.Room()
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
        self.startRoom = assets.game.Room.Room()
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
