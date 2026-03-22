
class ImagesAnimationLoader:

    frames = []
    animation_frame = 0
    counter = 0
    animation_speed = 10

    def __init__(self, animation_speed = 10):
        self.animation_speed = animation_speed
    
    def set_animation_speed(self, speed): 
        self.animation_speed = speed

    def set_frames_assets(self, frames):
        self.frames = frames

    def update_frame(self):
        if not self.frames:
            return
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % len(self.frames)
            self.counter = 0

    def get_frame(self):
        if not self.frames:
            return None
        return self.frames[self.animation_frame]