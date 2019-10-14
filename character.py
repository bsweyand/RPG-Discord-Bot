# '@author Brad Weyand
# This class defines the base stats/abilities of a character
from exceptions import AlreadyInBattleException, NotInBattleException
import random


class Character:
    DEFAULT_HEALTH = 100
    DEFAULT_DEFENSE = 0
    DEFAULT_ATTACK = 10
    DEFAULT_ACCURACY = 0.5
    DEFAULT_MAGIC = 0

    def __init__(self, id):
        """Initializes the base stats for the character"""
        self._id = id
        self._health = self.DEFAULT_HEALTH
        self._defense = self.DEFAULT_DEFENSE
        self._attack = self.DEFAULT_ATTACK
        self._accuracy = self.DEFAULT_ACCURACY
        self._magic = self.DEFAULT_MAGIC
        self._is_dead = False
        self._battle = None

    def attack(self, character, ability):
        """
        attacks a character using given ability
        :param character: the character to attack
        :param ability: the ability to use (must return an amount of damage)
        """
        dmg = ability() * self._accuracy
        character.receive_damage(dmg)

    def receive_damage(self, dmg):
        """
        Subtracts health using defense and current
        :param dmg: the damage done from an ability or effect
        """
        self._health -= (dmg * (1 - self._defense))
        self.check_death()

    def check_death(self):
        """
        Checks to see if character is dead and sets flag appropriately
        """
        if self._health <= 0:
            self._is_dead = True
            self.leave_battle(self._battle)

    def join_battle(self, battle):
        """
        Joins the specified battle
        :param battle: The battle to join
        """
        if self._battle is not None:
            raise AlreadyInBattleException("character is already in battle")
        battle.add(self)
        self._battle = battle

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

    def leave_battle(self, battle):
        """
        Removes player from the battle if it
        :param battle: the battle to leave
        """
        if not battle.has_player(self):
            raise NotInBattleException("Player is not in battle")
        battle.remove(self)
        self._battle = None
        self.set_default_stats()








