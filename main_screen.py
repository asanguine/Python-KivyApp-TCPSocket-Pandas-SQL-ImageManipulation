from kivy.uix.floatlayout import FloatLayout
from model import create_connection, update_preset, retrieve_user_id, retrieve_preset, generate_user_id, create_presets_table
from kivy.properties import ObjectProperty
from character_window import CharacterWindow
from timer_window import TimerWindow
from img_combine import combine_images, body_parts, images_count
from kivy.clock import Clock
import friend

DB_CONNECTION = create_connection()
user_id = retrieve_user_id(DB_CONNECTION) or generate_user_id()


class MainScreen(FloatLayout):
    
    character_window = ObjectProperty(None)
    current_images = retrieve_preset(DB_CONNECTION, user_id) or \
                                    {'clothe': 1, 'hair': 1, 'expression': 1}

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.character_window = CharacterWindow()
        Clock.schedule_interval(self.update_friend_image, 5)
        Clock.schedule_interval(self.update_character_pos, 3)
        Clock.schedule_interval(self.set_friend_image_pos, 3)

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
                                         self.current_images['expression']),
                                         'images/character/character.png')

    def get_friend_image_source(self):
        print("getting friend image source...")
        friend_preset = friend.get_friend_preset()
        
        print(f"Friend's preset data: {friend_preset}")
        source = combine_images(body_parts(friend.get_friend_preset()['clothe'],
                                        friend.get_friend_preset()['hair'],
                                        friend.get_friend_preset()['expression']),
                                        'images/character/friend_character.png')
        return source

    def update_friend_image(self, *args):
        print("Updating friend's image...")
        friend_image_source = self.get_friend_image_source()
        print(f"Friend's image source: {friend_image_source}")
        friend_character_image_main = self.ids.friend_character_image_main
        friend_character_image_main.source = friend_image_source
        friend_character_image_main.reload()


    def update_character_pos(self, *args):
        #try:
        x, y = self.ids.character_image_main.pos
        # except:
        #     x, y = 0
        print(f"pos: {x}, {y}")
        friend.set_character_pos(x, y)
    
    def set_friend_image_pos(self, *args):
        coords = friend.get_friend_picture_pos()
        x = coords['x']
        y = coords['y']
        return x, y



################ timer ###

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
                Clock.unschedule(update_callback) #also call this when cancelling
        Clock.schedule_interval(update_callback, 1)
