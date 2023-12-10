# main.py
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.clock import Clock
from datetime import timedelta

########################  TimerWindow  ##########################

class TimerWindow(ModalView):
    def start_timer(self, duration):
        main_screen = App.get_running_app().root
        main_screen.start_timer(duration)

########################  MainScreen  ############################

class MainScreen(FloatLayout):

    def show_timer_window(self):
        timer_window = TimerWindow()
        timer_window.open()


    def on_timer_dismiss(self, instance):
        pass


    def update_timer(self, instance, value):
        hours, remainder = divmod(value * 60, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        timer_label = self.ids.timer_label
        timer_label.text = time_str


    def start_timer(self, duration):
        total_seconds = duration * 60

        def update_callback(dt):
            nonlocal total_seconds
            if total_seconds > 0:
                total_seconds -= 1
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                if (hours == 0):
                    time_str = f"{int(minutes):02d}:{int(seconds):02d}"
                else:             
                    time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

                timer_label = self.ids.timer_label
                timer_label.text = time_str
            else:
                #when the timer reaches 0
                Clock.unschedule(update_callback)
        Clock.schedule_interval(update_callback, 1)




######################################################
######################################################

class TogetherApp(App):
    def build(self):
        Window.size = (350, 600)
        return MainScreen()

if __name__ == '__main__':
    TogetherApp().run()
