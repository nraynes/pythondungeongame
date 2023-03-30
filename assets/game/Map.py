import random
import assets.game.Room
import time


class Map:
    startRoom = assets.game.Room.Room()
    itemCount = 0
    height = 40
    width = 40
    seed = 0
    coords = []

    def __init__(self):
        self.seed = random.randint(10000, 99999)

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

    def getItemCount(self):
        return self.itemCount

    def reset(self):
        self.itemCount = 0
        self.seed = random.randint(10000, 99999)
        self.startRoom = assets.game.Room.Room()
        self.coords = []

    # Debug function for setting a seed.
    def setSeed(self):
        newSeed = int(input('What is the new seed: '))
        self.seed = newSeed

    def build(self):
        self.startRoom.setFlags(1)
        self.startRoom.setLocation(19, 39)
        self.coords.append(self.startRoom.location)
        maxMainRooms = self.seed % 40
        if maxMainRooms < 9:
            maxMainRooms = 9
        currentBuildRoom = self.startRoom

        # Build the main hallway.
        currentSeed = self.seed
        for i in range(maxMainRooms - 1):
            availableWalls = self.getOpenSides(currentBuildRoom, self.width, self.height)
            mod = 0
            for x in range(len(availableWalls)):
                if availableWalls[x]:
                    mod += 1
            if not mod:
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
            currentSeed = self.morphSeed(currentSeed)

        # Build the corridors
        currentBuildRoom = self.startRoom
        previousBuildRoom = None
        currentCorridor = None
        currentSeed = self.morphSeed(currentSeed)
        guarantee = round((self.itemCount + 1) / 2)
        setBit = 0
        while 1:
            # find next main room
            if currentBuildRoom.north and currentBuildRoom.north.mainRoom \
                    and (not previousBuildRoom or (previousBuildRoom and currentBuildRoom.north.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.north
            elif currentBuildRoom.south and currentBuildRoom.south.mainRoom \
                    and (not previousBuildRoom or
                         (previousBuildRoom and currentBuildRoom.south.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.south
            elif currentBuildRoom.east and currentBuildRoom.east.mainRoom \
                    and (not previousBuildRoom or
                         (previousBuildRoom and currentBuildRoom.east.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.east
            elif currentBuildRoom.west and currentBuildRoom.west.mainRoom \
                    and (not previousBuildRoom or
                         (previousBuildRoom and currentBuildRoom.west.location != previousBuildRoom.location)):
                previousBuildRoom = currentBuildRoom
                currentBuildRoom = currentBuildRoom.west
            else:
                break
            factor = currentSeed % 2
            currentSeed = self.morphSeed(currentSeed)
            secondFactor = (currentSeed % guarantee) + setBit
            if factor or (not factor and not secondFactor):
                setBit == 1
                # Start making a new corridor here
                currentCorridor = currentBuildRoom
                while 1:
                    availableWalls = self.getOpenSides(currentCorridor, self.width, self.height)
                    mod = 0
                    for x in range(len(availableWalls)):
                        if availableWalls[x]:
                            mod += 1
                    if not mod:
                        if not currentCorridor.mainRoom:
                            currentCorridor.setFlags(0, 0, 1, 0, 1)
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
                    elif pickedSide == 1:
                        currentCorridor.addRoom('south')
                        self.itemCount += 1
                        currentCorridor.south.setFlags(0, 0, 1)
                        currentCorridor.south.setLocation(currentCorridor.location[0],
                                                          currentCorridor.location[1] + 1)
                        self.coords.append([currentCorridor.location[0], currentCorridor.location[1] + 1])
                        currentCorridor.south.north = currentCorridor
                        currentCorridor = currentCorridor.south
                    elif pickedSide == 2:
                        currentCorridor.addRoom('east')
                        self.itemCount += 1
                        currentCorridor.east.setFlags(0, 0, 1)
                        currentCorridor.east.setLocation(currentCorridor.location[0] + 1,
                                                         currentCorridor.location[1])
                        self.coords.append([currentCorridor.location[0] + 1, currentCorridor.location[1]])
                        currentCorridor.east.west = currentCorridor
                        currentCorridor = currentCorridor.east
                    elif pickedSide == 3:
                        currentCorridor.addRoom('west')
                        self.itemCount += 1
                        currentCorridor.west.setFlags(0, 0, 1)
                        currentCorridor.west.setLocation(currentCorridor.location[0] - 1,
                                                         currentCorridor.location[1])
                        self.coords.append([currentCorridor.location[0] - 1, currentCorridor.location[1]])
                        currentCorridor.west.east = currentCorridor
                        currentCorridor = currentCorridor.west
                    else:
                        if not currentCorridor.mainRoom:
                            currentCorridor.setFlags(0, 0, 1, 0, 1)
                        break
                    currentSeed = self.morphSeed(currentSeed)

            currentSeed = self.morphSeed(currentSeed)
            if guarantee > 1:
                guarantee -= 1

        # Place the villain in one of the rooms.
        PVRooms = []

        def recurse(room, cancelCheck=-1):
            if room.potentialVillainRoom:
                PVRooms.append(room)
            if room.north and cancelCheck != 0:
                recurse(room.north, 1)
            if room.south and cancelCheck != 1:
                recurse(room.south, 0)
            if room.east and cancelCheck != 2:
                recurse(room.east, 3)
            if room.west and cancelCheck != 3:
                recurse(room.west, 2)
        recurse(self.startRoom)
        randIndex = random.randint(0, len(PVRooms)-1)
        PVRooms[randIndex].potentialVillainRoom = 0
        PVRooms[randIndex].villainRoom = 1

        return self.itemCount

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

    def getNumberOfRooms(self):
        def recurse(room, cancelCheck=-1):
            countRooms = 1
            if room.north and cancelCheck != 0:
                countRooms += recurse(room.north, 1)
            if room.south and cancelCheck != 1:
                countRooms += recurse(room.south, 0)
            if room.east and cancelCheck != 2:
                countRooms += recurse(room.east, 3)
            if room.west and cancelCheck != 3:
                countRooms += recurse(room.west, 2)
            return countRooms

        return recurse(self.startRoom)
