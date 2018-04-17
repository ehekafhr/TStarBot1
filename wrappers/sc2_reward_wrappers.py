import gym
from gym import spaces
from enum import Enum, unique

from pysc2.lib.typeenums import UNIT_TYPEID

from envs.space import PySC2RawObservation
from envs.space import PySC2RawAction


@unique
class AllianceType(Enum):
    SELF = 1
    ALLY = 2
    NEUTRAL = 3
    ENEMY = 4


class RewardClipWrapper(gym.RewardWrapper):

    def __init__(self, env):
        super(RewardClipWrapper, self).__init__(env)

    def _reward(self, reward):
        if reward > 1.0:
            return 1.0
        elif reward < -1.0:
            return -1.0
        else:
            return reward


class RewardShapingWrapperV1(gym.Wrapper):

    def __init__(self, env):
        super(RewardShapingWrapperV1, self).__init__(env)
        assert isinstance(env.observation_space, PySC2RawObservation)
        self._combat_unit_types = set([
                       UNIT_TYPEID.ZERG_ZERGLING.value,
                       UNIT_TYPEID.ZERG_ROACH.value,
                       UNIT_TYPEID.ZERG_HYDRALISK.value])

    def step(self, action):
        observation, outcome, done, info = self.env.step(action)
        n_enemies, n_self_combats = self._get_unit_counts(observation)
        if n_self_combats - n_enemies > self._n_self_combats - self._n_enemies:
            reward = 1
        elif n_self_combats - n_enemies < self._n_self_combats - self._n_enemies:
            reward = -1
        else:
            reward = 0
        reward += outcome * 10
        self._n_enemies = n_enemies
        self._n_self_combats = n_self_combats
        return observation, reward, done, info

    def _get_unit_counts(self, observation):
        num_enemy_units = 0
        num_self_combat_units = 0
        for u in observation['units']:
            if u.int_attr.alliance == AllianceType.ENEMY.value:
                num_enemy_units += 1
            elif u.int_attr.alliance == AllianceType.SELF.value:
                if u.unit_type in self._combat_unit_types:
                    num_self_combat_units += 1
        return num_enemy_units, num_self_combat_units

    def reset(self):
        observation = self.env.reset()
        self._n_enemies, self._n_self_combats = self._get_unit_counts(
            observation)
        return observation
