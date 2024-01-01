from kivy.uix.modalview import ModalView
from model import create_connection, update_preset, retrieve_preset, retrieve_user_id, generate_user_id
import os
from img_combine import combine_images, body_parts, images_count
from kivy.app import App

class CharacterWindow(ModalView):
    DB_CONNECTION = create_connection()
    user_id = retrieve_user_id(DB_CONNECTION) or generate_user_id()
    current_images = retrieve_preset(DB_CONNECTION, user_id) or \
                                    {'clothe': 1, 'hair': 1, 'expression': 1}

    def load_image(self):
        previous_image_path = 'images/character/character.png'
        if os.path.exists(previous_image_path):
            os.remove(previous_image_path)
        
        update_preset(self.DB_CONNECTION, self.user_id,
                                self.current_images['clothe'],
                                self.current_images['hair'],
                                self.current_images['expression'])
        
        image_path = combine_images(body_parts(self.current_images['clothe'],
                                               self.current_images['hair'],
                                               self.current_images['expression']),
                                               'images/character/character.png')

        print('load_image called')
        return image_path
    

    def load_friend_image(self):
        previous_image_path = 'images/character/friend_character.png'
        if os.path.exists(previous_image_path):
            os.remove(previous_image_path)
        
        pass


    def load_next_image(self, body_part):
        image_count = images_count(body_part)
        if ((self.current_images[body_part] % image_count) + 1) != 1:
            self.current_images[body_part] = (self.current_images[body_part] % image_count) + 1
        else:
            self.current_images[body_part] = (self.current_images[body_part] % image_count) + 2
            
        self.ids.character_image.source = self.load_image()
        self.ids.character_image.reload()

        image_path = self.load_image()
        main_screen = App.get_running_app().root
        main_screen.character_window.ids.character_image.source = image_path
        main_screen.character_window.ids.character_image.reload()

        app = App.get_running_app()
        app.root.update_character_image(image_path)
