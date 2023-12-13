from kivy.uix.modalview import ModalView
from model import create_connection, update_preset, retrieve_preset, retrieve_user_id, generate_user_id, create_presets_table
import os
from img_combine import combine_images, body_parts, images_count
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import DragBehavior

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
