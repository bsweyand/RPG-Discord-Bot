# '@author Brad Weyand
# This class defines the base stats/abilities of a character
from exceptions import AlreadyInBattleException
import random


class Character:
    DEFAULT_HEALTH = 100.0
    DEFAULT_DEFENSE = 0
    DEFAULT_ATTACK = 10
    DEFAULT_ACCURACY = 0.5
    DEFAULT_MAGIC = 0

    def __init__(self, name):
        """Initializes the base stats for the character"""
        self._name = name
        self._health = self.DEFAULT_HEALTH
        self._defense = self.DEFAULT_DEFENSE
        self._attack = self.DEFAULT_ATTACK
        self._accuracy = self.DEFAULT_ACCURACY
        self._magic = self.DEFAULT_MAGIC
        self._is_dead = False
        self._battle = None

    def get_name(self):
        """
        getter for a character's name attribute
        :return: the name of the character
        """
        return self._name

    def get_health(self):
        """
        getter for a character's health attribute
        :return: the health of the character
        """
        return self._health

    async def attack(self, character, ability):
        """
        attacks a character using given ability
        :param character: the character to attack
        :param ability: the ability to use (must return an amount of damage)
        :return a result string representing the attack
        """
        dmg = ability()
        result = await character.receive_damage(dmg)
        result_string = "{} attacked {} for a total of {} dmg".format(self._name, character.get_name(), result[0])
        if result[1]:
            result_string += "\n{} is dead".format(character.get_name())
        return result_string

    async def receive_damage(self, dmg):
        """
        Subtracts health using defense and current
        :param dmg: the damage done from an ability or effect
        :return a tuple representing the dmg taken and whether or not the character is dead
        """
        total_dmg = (dmg * (1 - self._defense))
        self._health -= total_dmg
        is_dead = await self.check_death()
        return total_dmg, is_dead

    async def check_death(self):
        """
        Checks to see if character is dead and sets flag appropriately
        :return True if player is dead, otherwise False
        """
        if self._health <= 0:
            self._is_dead = True
            await self.leave_battle(self._battle)
            return True

    async def join_battle(self, battle):
        """
        Joins the specified battle
        :param battle: The battle to join
        """
        if self._battle is not None:
            raise AlreadyInBattleException("character is already in a battle")
        await battle.add(self)
        self._battle = battle

    def get_battle(self):
        """
        getter for a character's battle
        :return: the battle the character is in, or None if the character is not in battle
        """
        return self._battle

    def is_in_battle(self):
        """
        assesses whether the character is in battle or not
        :return: true if the character is in battle otherwise false
        """
        return self._battle is not None

    def hit(self):
        """ returns attack dmg if attack lands, otherwise return 0 """
        if random.random() < self._accuracy:
            return self._attack
        return 0

    def set_default_stats(self):
        """Sets character stats back to their defaults"""
        self._health = self.DEFAULT_HEALTH
        self._defense = self.DEFAULT_DEFENSE
        self._attack = self.DEFAULT_ATTACK
        self._accuracy = self.DEFAULT_ACCURACY
        self._magic = self.DEFAULT_MAGIC

    async def leave_battle(self, battle):
        """
        Removes player from the battle if it
        :param battle: the battle to leave
        """
        await battle.remove(self)
        self._battle = None
        self.set_default_stats()








