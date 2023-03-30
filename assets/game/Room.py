import assets.game.Sprite

class Room:
    startRoom = 0
    mainRoom = 0
    corridor = 0
    villainRoom = 0
    potentialVillainRoom = 0
    itemVisible = 1
    sprite = assets.game.Sprite.Sprite()
    location = [0, 0]

    east = None
    west = None
    north = None
    south = None

    def __init__(self):
        for x in range(40):
            self.sprite.graphic[0][x] = 'O'
            self.sprite.graphic[19][x] = 'O'
        for y in range(20):
            self.sprite.graphic[y][0] = 'O'
            self.sprite.graphic[y][39] = 'O'

    def addRoom(self, wall):
        if wall == 'north':
            self.north = Room()
        elif wall == 'south':
            self.south = Room()
        elif wall == 'east':
            self.east = Room()
        elif wall == 'west':
            self.west = Room()

    def setFlags(self, s=0, m=0, c=0, v=0, pv=0):
        self.startRoom = s
        self.mainRoom = m
        self.corridor = c
        self.villainRoom = v
        self.potentialVillainRoom = pv

    def setLocation(self, x=0, y=0):
        self.location = [x, y]

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
