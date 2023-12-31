from kivy.app import App
from kivy.core.window import Window
from model import initialize_database, create_connection
from main_screen import MainScreen
from client import MyClient
from state_manager import StateManager
import logging, os
from kivy.clock import Clock

#  ______                        __    __                         __     
# /\__  _\                      /\ \__/\ \                       /\ \    
# \/_/\ \/   ___      __      __\ \ ,_\ \ \___      __   _ __    \ \ \   
#    \ \ \  / __`\  /'_ `\  /'__`\ \ \/\ \  _ `\  /'__`\/\`'__\   \ \ \  
#     \ \ \/\ \L\ \/\ \L\ \/\  __/\ \ \_\ \ \ \ \/\  __/\ \ \/     \ \_\ 
#      \ \_\ \____/\ \____ \ \____\\ \__\\ \_\ \_\ \____\\ \_\      \/\_\
#       \/_/\/___/  \/___L\ \/____/ \/__/ \/_/\/_/\/____/ \/_/       \/_/
#                     /\____/                                            
#                     \_/__/                                                                                                                
# ┓     ┓ •  ┓      
# ┣┓┓┏  ┣┓┓┏┓┃┏┏┓┏┓ 
# ┗┛┗┫  ┗┛┗┛ ┛┗┗┻┛┗•
#    ┛              
logging.getLogger('kivy').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
DB_CONNECTION = create_connection()


class TogetherApp(App):
    def show_character_window(self):
        main_screen = self.root
        main_screen.show_character_window()

    def on_window_resize(self, instance, width, height):
        pass

    def update_aspect_ratio(self, dt):
        aspect_ratio = 512 / 768
        new_width = min(Window.width, Window.height * aspect_ratio)
        new_height = min(Window.height, Window.width / aspect_ratio)
        Window.size = (new_width, new_height)

    def __init__(self, **kwargs):
        super(TogetherApp, self).__init__(**kwargs)
        self.client = None

    def build(self):
        state_manager = StateManager()
        client = MyClient(state_manager=state_manager)
        client.start()
        initialize_database()
        Window.size = (512, 768)
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_interval(self.update_aspect_ratio, 1 / 60.0)
        return MainScreen()
    
    def on_stop(self):
        if self.client:
            self.client.stop()
        os._exit(0)

if __name__ == '__main__':
    TogetherApp().run()
