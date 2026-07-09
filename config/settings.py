from pathlib import Path
import yaml


class AIWeights:

    def __init__(self):

        config = Path("config/weights.yaml")

        with open(config, "r") as f:
            self.weights = yaml.safe_load(f)

    def get(self, key):

        return self.weights.get(key, 0)


weights = AIWeights()