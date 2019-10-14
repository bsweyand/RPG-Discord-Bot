# '@author Brad Weyand
# This file defines exceptions related to RPG


class AlreadyInBattleException(RuntimeError):
    def __init__(self, message):
        super.__init__(message)


class NotInBattleException(RuntimeError):
    def __init__(self, message):
        super.__init__(message)
