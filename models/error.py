"""
modules for custum error
"""
error = ["NotFoudError"]


class NotFoudError(Exception):
    """
    custum error not found
    """
    def __init__(self, message="No ducument in database", code=None):
        self.message = message
        super().__init__(message)
