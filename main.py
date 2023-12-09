# main.py
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.slider import Slider

class TimerWindow(ModalView):
    pass

class MainScreen(FloatLayout):
    def show_timer_window(self):
        timer_window = TimerWindow()
        timer_window.open()


class TogetherApp(App):
    def build(self):
        Window.size = (350, 600)
        return MainScreen()

if __name__ == '__main__':
    TogetherApp().run()
