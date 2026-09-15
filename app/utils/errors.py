class NotFoundError(ValueError):
    pass


class ForbiddenError(PermissionError):
    pass


class InsufficientInventoryError(ValueError):
    pass
