from ConfigController import ConfigController
from Validators import Validator, builtin_validators
from exceptions.ValidatorExceptions import ValidatorAlreadyExists
from exceptions.common import NotValidPythonVariableNameException, PythonKeywordException
from ui.screens.validators import CreateValidatorScreen
from ui.NavigationController import NavigationController
from Colors import Colors

from ui.BaseScreen import BaseScreen
import curses


class CreateValidatorScreen(BaseScreen):
    def __init__(self, stdscr, navigation_controller: NavigationController, config_controller: ConfigController):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.is_typing = False  # Флаг, определяющий активен ли ввод текста
        self.error_messages = []
        self.text_field = ""

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Create custom validator")
        self.stdscr.addstr(1, 0, ("> " if (self.selected_idx == 0 and not self.is_typing) else "  ") + "[Enter validator name]")

        # Визуальное выделение текущей строки
        if self.selected_idx == 0:  # Текстовое поле выбрано
            self.stdscr.addstr(1, 25, f"{self.text_field}")
        else:
            self.stdscr.addstr(1, 25, self.text_field)

        # Отображение остальных пунктов меню
        self.stdscr.addstr(2, 0, ("> " if self.selected_idx == 1 else "  ") + "[Confirm]")
        self.stdscr.addstr(3, 0, ("> " if self.selected_idx == 2 else "  ") + "[Cancel]")

        # Отображение ошибок
        if len(self.error_messages) > 0:
            for idx, message in enumerate(self.error_messages):
                self.stdscr.addstr(5 + idx, 0, message, Colors.RED_BLACK)

        if self.is_typing:
            self.stdscr.move(1, 25 + len(self.text_field))
            curses.curs_set(1)  # Показываем курсор
        else:
            curses.curs_set(0)  # Скрываем курсор

        self.stdscr.refresh()

    def handle_input(self, key):
        # Если активен ввод текста
        if self.is_typing:
            if key in [curses.KEY_ENTER, 10, 13]:  # Завершить ввод
                self.is_typing = False
            elif key in (curses.KEY_BACKSPACE, 127):  # Удалить последний символ
                self.text_field = self.text_field[:-1]
            elif key >= 32 and key <= 126:  # Добавить символ (печатные символы)
                self.text_field += chr(key)
            return  # Останавливаем дальнейшую обработку

        # Навигация между пунктами меню
        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < 2:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:  # Начать ввод текста
                self.is_typing = True
            elif self.selected_idx == 1:  # Подтвердить
                try:
                    self.config_controller.add_validator(self.text_field)
                    self.navigate_back()
                except ValidatorAlreadyExists as e:
                    self.error_messages = [str(e)]
                except NotValidPythonVariableNameException as e:
                    self.error_messages = [str(e)]
                except PythonKeywordException as e:
                    self.error_messages = [str(e)]
            elif self.selected_idx == 2:  # Отмена
                self.navigate_back()
