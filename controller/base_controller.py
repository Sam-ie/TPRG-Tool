from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.main_controller import MainController


class BaseController(ABC):
    """控制器基类"""

    def __init__(self, main_controller: "MainController"):
        self.main_controller = main_controller

    @property
    def root(self):
        return self.main_controller.root

    @property
    def model(self):
        return self.main_controller.model

    @property
    def view(self):
        return self.main_controller.view

    @property
    def language_manager(self):
        return self.main_controller.language_manager

    @property
    def command_manager(self):
        return self.main_controller.command_manager