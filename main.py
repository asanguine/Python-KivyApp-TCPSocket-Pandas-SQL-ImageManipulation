# main.py
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.clock import Clock
from datetime import timedelta
from kivy.uix.image import Image, AsyncImage
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
import os
from img_combine import combine_images, body_parts, images_count
from model import create_connection, update_preset, retrieve_preset

user_id = 1234

########################  TimerWindow  ##########################

class TimerWindow(ModalView):
    def start_timer(self, duration):
        main_screen = App.get_running_app().root
        main_screen.start_timer(duration)


########################  CharacterWindow  ##########################

class CharacterWindow(ModalView):
    DB_CONNECTION = create_connection()
    current_images = retrieve_preset(DB_CONNECTION, user_id) or \
                                    {'clothe': 1, 'hair': 1, 'expression': 1}

    def load_image(self):
        previous_image_path = 'images/character/character.png'
        if os.path.exists(previous_image_path):
            os.remove(previous_image_path)
        
        update_preset(self.DB_CONNECTION, user_id,
                                self.current_images['clothe'],
                                self.current_images['hair'],
                                self.current_images['expression'])
        
        image_path = combine_images(body_parts(self.current_images['clothe'],
                                               self.current_images['hair'],
                                               self.current_images['expression']))

        print('load_image called')
        return image_path
    
    
    def load_next_image(self, body_part):
        image_count = images_count(body_part)
        self.current_images[body_part] = (self.current_images[body_part] % image_count) + 1
        self.ids.character_image.source = self.load_image()
        self.ids.character_image.reload()

        image_path = self.load_image()
        main_screen = App.get_running_app().root
        main_screen.character_window.ids.character_image.source = image_path
        main_screen.character_window.ids.character_image.reload()

        app = App.get_running_app()
        app.root.update_character_image(image_path)

class ImageButton(RecycleDataViewBehavior, Button):
    source = StringProperty('')
    pass


class DragImage(DragBehavior, AsyncImage):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super(DragImage, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.x += touch.dx
            self.y += touch.dy
            return True
        return super(DragImage, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(DragImage, self).on_touch_up(touch)


########################  MainScreen  ############################

class MainScreen(FloatLayout):
    DB_CONNECTION = create_connection()
    character_window = ObjectProperty(None)
    current_images = retrieve_preset(DB_CONNECTION, user_id) or \
                                    {'clothe': 1, 'hair': 1, 'expression': 1}

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.character_window = CharacterWindow()

    def show_timer_window(self):
        timer_window = TimerWindow()
        timer_window.open()

    def show_character_window(self):
        character_window = CharacterWindow()
        character_window.open()

    def update_character_image(self, image_path):
        character_image_main = self.ids.character_image_main
        character_image_main.source = image_path
        character_image_main.reload()

    def get_character_image(self):
        return combine_images(body_parts(self.current_images['clothe'],
                                         self.current_images['hair'],
                                         self.current_images['expression']))


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
    
    def show_character_window(self):
        main_screen = self.root
        main_screen.show_character_window()

if __name__ == '__main__':
    TogetherApp().run()
