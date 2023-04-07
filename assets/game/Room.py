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
