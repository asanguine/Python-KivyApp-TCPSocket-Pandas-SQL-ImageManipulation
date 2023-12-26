class StateManager:
    def __init__(self):
        self.connected_users = []
        self.character_pos = {'x': 0, 'y': 0}
        self.friend_image_pos = {'x': 0, 'y': 0}

    def set_connected_users(self, users):
        self.connected_users = users

    def get_connected_users(self):
        return self.connected_users

    def set_character_pos(self, x, y):
        self.character_pos = {'x': x, 'y': y}

    def get_character_pos(self):
        return self.character_pos
    
    def set_friend_picture_pos(self, x, y):
        self.friend_image_pos = {'x': x, 'y': y}
    
    def get_friend_picture_pos(self):
        return self.friend_image_pos
