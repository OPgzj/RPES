class CameraNotFoundError(Exception):
    def __init__(self, message="Camera not found"):
        self.message = message
        super().__init__(self.message)

class FrameLostError(Exception):
    def __init__(self, message="Lost Frame"):
        self.message = message
        super().__init__(self.message)