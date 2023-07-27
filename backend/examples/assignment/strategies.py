import abc
import dataclasses
import random
from typing import List

import numpy as np


@dataclasses.dataclass
class Assignment:
    user: int
    example: int


class BaseStrategy(abc.ABC):
    @abc.abstractmethod
    def assign(self) -> List[Assignment]:
        ...


class WeightedSequentialStrategy(BaseStrategy):
    def __init__(self, dataset_size: int, weights: List[int]):
        assert sum(weights) == 100
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        assignments = []
        proba = np.array(self.weights) / 100
        counts = np.round(proba * self.dataset_size).astype(int)
        reminder = self.dataset_size - sum(counts)
        for i in np.random.choice(range(len(self.weights)), size=reminder, p=proba):
            counts[i] += 1

        start = 0
        for user, count in enumerate(counts):
            assignments.extend([Assignment(user=user, example=example) for example in range(start, start + count)])
            start += count
        return assignments


class WeightedRandomStrategy(BaseStrategy):
    def __init__(self, dataset_size: int, weights: List[int]):
        assert sum(weights) == 100
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        proba = np.array(self.weights) / 100
        assignees = np.random.choice(range(len(self.weights)), size=self.dataset_size, p=proba)
        return [Assignment(user=user, example=example) for example, user in enumerate(assignees)]


class SamplingWithoutReplacementStrategy(BaseStrategy):
    def __init__(self, dataset_size: int, weights: List[int]):
        assert 0 <= sum(weights) <= 100 * len(weights)
        self.dataset_size = dataset_size
        self.weights = weights

    def assign(self) -> List[Assignment]:
        assignments = []
        proba = np.array(self.weights) / 100
        for user, p in enumerate(proba):
            count = int(self.dataset_size * p)
            examples = random.sample(range(self.dataset_size), count)
            assignments.extend([Assignment(user=user, example=example) for example in examples])
        return assignments
