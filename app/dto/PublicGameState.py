import json
import numpy as np
from app.dto.PublicPlayer import PublicPlayer


class PublicGameState:
    def __init__(self, ext_dict=None):
        self.gameField = [[]]
        self.publicPlayers = []
        if ext_dict is not None:
            self.__dict__ = ext_dict
        self.gameField = np.asarray(self.gameField)

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
