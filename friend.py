from model import create_connection, update_preset, retrieve_user_id, retrieve_preset, generate_user_id, create_presets_table
from img_combine import combine_images, body_parts, images_count
from server import get_user_info_list

DB_CONNECTION = create_connection()


#friend_images = retrieve_preset(DB_CONNECTION, user_id)

users_list = get_user_info_list()

for user in users_list:
    print(user)


def get_friend_image(self):
    return combine_images(body_parts(self.friend_images['clothe'],
                                    self.friend_images['hair'],
                                    self.friend_images['expression']))

def generate_friend_character(self, preset_data):
    pass