# ' @author Brad Weyand
# This file defines the Class player which encapsulates information about the player in a battle
from exceptions import NotInBattleException


class Player:

    def __init__(self, character, name):
        """
        Initializes a player with a character and a name
        :param character: the character to initialize player with
        :param name: the name for the player object
        """
        self._name = name
        self.character = character

    def get_name(self):
        """
        getter for name of player (not to be confused with the name of the character
        :return: the name of the player
        """
        return self._name

    async def join_battle(self, battle):
        """
        Joins the specified battle
        :param battle: the battle to join
        :return: None
        """
        await self.character.join_battle(battle)

    async def leave_battle(self, battle):
        """
        leaves the specified battle
        :param battle: the battle to leave
        :return: None
        """
        await self.character.leave_battle(battle)

    def in_battle(self):
        """
        assesses whether the character is in battle or not
        :return: True if the character is in a battle otherwise False
        """
        return self.character.is_in_battle()

    def has_turn(self):
        """
        assesses whether not it is the player's turn in battle
        :return: True if it is the player's turn otherwise False
        """
        if not self.in_battle():
            raise NotInBattleException("Character is not currently in Battle")
        return self.character.get_battle().get_turn().get_name() == self.character.get_name()
