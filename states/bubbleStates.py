from states.state import State

class Idle(State):
    def __init__(self):
        super().__init__("idle")

class Shot(State):
    def __init__(self):
        super().__init__("shoted")

    def update(self, object,dt):
        object.physics.update(dt)
        object.rect.center = (int(object.physics.position.x),int(object.physics.position.y))

class Floating(State):
    def __init__(self, duration,on_finish):
        super().__init__("floating")
        self._time_floating = 0.0
        self.duration = duration
        self.on_finish = on_finish

    def update(self, object, dt):
        object.physics.update(dt)
        object.rect.center = (int(object.physics.position.x),int(object.physics.position.y))

        self._time_floating += dt

        if self._time_floating >= self.duration:
            self.on_finish()

class Pop(State):
    def __init__(self, animation_sprites,total_frames,frames_per_image,scale,on_finish):
        super().__init__("pop")
        self.sprites = animation_sprites
        self._current_frame = 0
        self.frames_per_image = frames_per_image
        self.total_frames = total_frames
        self.scale = scale
        self.on_finish = on_finish

    def update(self, object, dt):
        image = self.sprites[(self._current_frame // self.frames_per_image) % len(self.sprites)]
        object.set_image(image)

        self._current_frame += 1

        if self._current_frame >= self.total_frames:
            self.on_finish()