import assets.engine.Display
import assets.engine.Controller
import assets.game.Game
import threading

# An engine class to operate the different threads for input/output along with the game itself.
class Engine:
    def start(self):
        # Create new instances of the classes for input, output, and the game itself.
        display = assets.engine.Display.Display()
        controller = assets.engine.Controller.Controller()
        game = assets.game.Game.Game()

        # Create new threads for the controller and game so that they may run in parallel.
        conTask = threading.Thread(target=controller.start, args=(), kwargs={})
        gameTask = threading.Thread(target=game.start, args=(display, controller), kwargs={})

        # Start the threads for the game and controller.
        # Controller must run in parallel with game in order for input to be measured constantly.
        conTask.start()
        gameTask.start()
