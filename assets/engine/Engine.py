import assets.engine.Display
import assets.engine.Controller
import assets.game.Game
import threading

class Engine:
    def start(self):
        display = assets.engine.Display.Display()
        controller = assets.engine.Controller.Controller()
        game = assets.game.Game.Game()
        conTask = threading.Thread(target=controller.start, args=(), kwargs={})
        gameTask = threading.Thread(target=game.start, args=(display, controller), kwargs={})
        conTask.start()
        gameTask.start()
