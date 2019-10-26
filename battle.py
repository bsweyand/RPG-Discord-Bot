# ' @author Brad Weyand
# Defines the class that handles battle interactions between characters
from exceptions import AlreadyInBattleException
from exceptions import NotInBattleException
from exceptions import BattleAlreadyStartedException
import asyncio


class Battle:

    def __init__(self, name):
        """ initializes a list of players in the battle"""
        self._characters = []
        self._dead = []
        self._turn = 0
        self._is_started = False
        self._name = name

    def get_name(self):
        """
        Getter for the battle's name
        :return: the name attribute of the battle
        """
        return self._name

    async def add(self, character):
        """
        adds character to the battle if it has not started
        :param character: the character to add to the battle
        :return: None
        """
        if self._is_started:
            raise BattleAlreadyStartedException("The battle has already started")
        if await self.has_character(character.get_name()):
            raise AlreadyInBattleException("player is already in this battle")
        self._characters.append(character)

    async def remove(self, character):
        """
        removes character from the battle if battle contains character
        :param character: the character to remove from battle
        :return: None
        """
        if not await self.has_character(character.get_name()):
            raise NotInBattleException("character is not in this battle")
        for player in self._characters:
            if player.get_name() == character.get_name():
                if self._is_started:
                    self._dead.append(player)
                self._characters.remove(player)
            await asyncio.sleep(.1)

    async def has_character(self, character_name):
        """
        assesses whether the given character is in the battle based on its name
        :param character_name: the character to check
        :return: True if character is in the battle, otherwise False
        """
        for character in self._characters:
            if character.get_name() == character_name:
                return True
            await asyncio.sleep(.1)
        return False

    async def get_character(self, character_name):
        """
        return a reference to a character in the battle given a name
        :param character_name: the character name to search for
        :return: the character object if it exists, else None
        """
        for player in self._characters:
            if player.get_name() == character_name:
                return player
            await asyncio.sleep(.1)

    def start(self):
        """
        sets start flag to true
        :return: None
        """
        self._is_started = True

    async def get_stats(self):
        """
        composes a message that represents the stats of each character
        :return: the message composed
        """
        message = "Remaining Characters:\n"
        for player in self._characters:
            message += "{}: {:.2f} hp\n".format(player.get_name(), player.get_health())
            await asyncio.sleep(0.1)

        message += "\nDead Players: "
        for dead_player in self._dead:
            message += "{}\n".format(dead_player.get_name())
            await asyncio.sleep(0.1)

        return message

    def get_turn(self):
        """
        retrieve the character's turn
        :return: the character who has control of the turn
        """
        return self._characters[self._turn]

    def next_turn(self):
        """
        increments turn to be the next player on the list
        :return: None
        """
        if self._turn == len(self._characters) - 1:
            self._turn = 0
        else:
            self._turn += 1
