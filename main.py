from kivy.app import App
from kivy.core.window import Window
from model import initialize_database
from main_screen import MainScreen

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


class TogetherApp(App):
    def build(self):
        Window.size = (350, 600)
        initialize_database()
        return MainScreen()
    
    def show_character_window(self):
        main_screen = self.root
        main_screen.show_character_window()

if __name__ == '__main__':
    TogetherApp().run()
