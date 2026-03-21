
class Timer:

    duration = 0
    duration_increment = 0
    start_time = False
    trigger_action_at_the_end = False

    def __init__(self, duration):
        self.duration = duration
        self.duration_increment = duration

    def check_cronometer(self):
        self.trigger_action_at_the_end = False
        if self.start_time is False and self.duration_increment == self.duration:
            return False
        self.duration_increment -= 1
        if self.duration_increment == 0:
            self.duration_increment = self.duration
            self.start_time = False
            self.trigger_action_at_the_end = True
            return False
        return True