class StateManager:
    def __init__(self):
        self.connected_users = []

    def set_connected_users(self, users):
        self.connected_users = users

    def get_connected_users(self):
        return self.connected_users
