from kivy.uix.floatlayout import FloatLayout
from model import create_connection, retrieve_user_id, retrieve_preset, generate_user_id, add_study_session
from kivy.properties import ObjectProperty
from character_window import CharacterWindow
from timer_window import TimerWindow
from img_combine import combine_images, body_parts
from kivy.clock import Clock
import friend
from congrats_window import CongratsWindow
from stats_window import StatsWindow

DB_CONNECTION = create_connection()
user_id = retrieve_user_id(DB_CONNECTION) or generate_user_id()


class MainScreen(FloatLayout):
    
    character_window = ObjectProperty(None)
    current_images = retrieve_preset(DB_CONNECTION, user_id) or \
                                    {'clothe': 1, 'hair': 1, 'expression': 1}
    timer_active = False
    #timer_paused = False
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.character_window = CharacterWindow()
        Clock.schedule_interval(self.update_friend_image, 1)
        Clock.schedule_interval(self.update_character_pos, 1)
        Clock.schedule_interval(self.return_friend_coordinates, 1)
        Clock.schedule_interval(self.return_friend_size, 1)
        #self.timer_active = False
        self.timer_paused = False

    def show_timer_window(self):
        timer_window = TimerWindow()
        timer_window.open()

    def show_character_window(self):
        character_window = CharacterWindow()
        character_window.open()

    def show_stats_window(self):
        stats_window = StatsWindow()
        stats_window.create_barplot()
        stats_window.update_stats_image()
        stats_window.open()

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
        #print("getting friend image source...")
        friend_preset = friend.get_friend_preset()
        
        #print(f"Friend's preset data: {friend_preset}")
        source = combine_images(body_parts(friend.get_friend_preset()['clothe'],
                                        friend.get_friend_preset()['hair'],
                                        friend.get_friend_preset()['expression']),
                                        'images/character/friend_character.png')
        return source

    def update_friend_image(self, *args):
        #print("Updating friend's image...")
        friend_image_source = self.get_friend_image_source()
        #print(f"Friend's image source: {friend_image_source}")
        friend_character_image_main = self.ids.friend_character_image_main
        friend_character_image_main.source = friend_image_source
        friend_character_image_main.pos = self.return_friend_coordinates()
        friend_character_image_main.reload()


    def update_character_pos(self, *args):
        x, y = self.ids.character_image_main.pos
        size = self.ids.character_image_main.size_hint
        #print(f"pos: {x}, {y}")
        friend.set_character_pos(x, y, size[1])
    
    def return_friend_coordinates(self, *args):
        coords = friend.get_friend_picture_pos()
        #print(f'\n\n()()coords\n {coords}\n\n=============\n===============')
        x = coords['x']
        y = coords['y']
        return x, y

    def return_friend_size(self, *args):
        size = friend.get_friend_picture_pos()
        #print(f'\n\n()()coords\n {size}\n\n=============\n===============')
        s = size['size']
        return s


################ timer ###

    def set_timer_active(self, bool):
        self.timer_active = bool

    def get_timer_active(self):
        print(f"get called: {self.timer_active}")
        if self.timer_active == True:
            self.ids.pause_buttons.opacity = 1
            return 1
        else:
            self.ids.pause_buttons.opacity = 0
            return 0

    def on_timer_dismiss(self, instance, duration):
        self.timer_active = False
        congrats_window = CongratsWindow()
        congrats_window.open()
        self.add_study_session_to_db(duration)

    def add_study_session_to_db(self, dur):
        duration = dur
        add_study_session(DB_CONNECTION, user_id, duration)

    def update_timer(self, instance, value):
        hours, remainder = divmod(value * 60, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        timer_label = self.ids.timer_label
        timer_label.text = time_str

    def start_timer(self, duration):
        self.timer_active = True
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
                Clock.unschedule(update_callback) #also call this when cancelling :todo
                self.ids.timer_label.text = ''
                self.on_timer_dismiss(None, duration)
                print(f"Timer: ")
                print(self.get_timer_active())       
        #Clock.schedule_interval(update_callback, 1)   ###########  TODO: pause feature
        if not self.timer_paused:
            Clock.schedule_interval(update_callback, 1)
        else:
            Clock.unschedule(update_callback)
        print(f"Timer: ")
        print(self.get_timer_active())


    def pause_continue_timer(self):
        self.timer_paused = not self.timer_paused
        print(f"Pause/Continue button pressed:{self.timer_paused}")

    def cancel_timer(self):
        if self.timer_active:
            self.timer_active = False
            print("Cancel button pressed")
