class DatabaseError(Exception):
    """
    Generic exception for all database errors.
    """

    pass


class DbnotFoundException(DatabaseError):
    pass


class SectionInUseError(DatabaseError):
    pass
