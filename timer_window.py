from kivy.uix.modalview import ModalView
from kivy.app import App

class TimerWindow(ModalView):
    def start_timer(self, duration):
        main_screen = App.get_running_app().root
        main_screen.start_timer(duration)
        main_screen.set_timer_active(True)
