from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import DragBehavior
from kivy.core.window import Window
from kivy.properties import NumericProperty

class DragImage(DragBehavior, AsyncImage):
    min_size_hint_y = NumericProperty(0.4)
    max_size_hint_y = NumericProperty(0.7)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super(DragImage, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            dy = touch.dy
            screen_height = Window.height
            threshold = screen_height / 2

            if self.top > threshold:
                self.size_hint_y = max(0.4, min(0.7, self.size_hint_y - 0.001 * dy))
            else:
                self.size_hint_y = max(0.4, min(1, self.size_hint_y))

            self.x += touch.dx
            self.y += dy
            return True
        return super(DragImage, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(DragImage, self).on_touch_up(touch)
