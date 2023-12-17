from kivy.uix.floatlayout import FloatLayout
from model import create_connection, update_preset, retrieve_user_id, retrieve_preset, generate_user_id, create_presets_table
from kivy.properties import ObjectProperty
from character_window import CharacterWindow
from timer_window import TimerWindow
from img_combine import combine_images, body_parts, images_count
from kivy.clock import Clock

class MainScreen(FloatLayout):
    DB_CONNECTION = create_connection()
    user_id = retrieve_user_id(DB_CONNECTION) or generate_user_id()

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

    def get_character_pos(self):
        x, y = self.ids.character_image_main.pos
        return x, y


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
