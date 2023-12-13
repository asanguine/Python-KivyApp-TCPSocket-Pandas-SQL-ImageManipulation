from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import DragBehavior


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
