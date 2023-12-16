from kivy.app import App
from kivy.core.window import Window
from model import initialize_database, retrieve_user_id, generate_user_id, create_connection
from main_screen import MainScreen
import asyncio
import websockets
from kivy.clock import Clock
from threading import Thread

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

DB_CONNECTION = create_connection()


class TogetherApp(App):
    def show_character_window(self):
        main_screen = self.root
        main_screen.show_character_window()
    
    def build(self):
        initialize_database()
        Window.size = (512, 768)

        return MainScreen()


if __name__ == '__main__':
    TogetherApp().run()
