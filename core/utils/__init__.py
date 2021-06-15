import uuid


def uid_generator() -> str:
    return uuid.uuid1().hex
