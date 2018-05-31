class Lift(object):

    def __init__(self):
        pass

    def call_lift(self, level):
        print('Calling lift to level %d' % level)
        return True

    def open_door(self):
        print('Opening lift door')
        return True

    def close_door(self):
        print('Closing lift door')
        return True

    def go_to_level(self, to_level):
        print('Going to level %d' % to_level)
        return True
