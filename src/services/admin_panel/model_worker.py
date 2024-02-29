from typing import Callable


class ModelCollector:
    def __init__(self):
        self.admin_models = []

    def target_model(self, model: Callable):
        self.admin_models.append(model)

        return model

    @property
    def models(self):
        return self.admin_models
