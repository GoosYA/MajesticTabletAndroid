# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

Window.clearcolor = (0.04, 0.06, 0.12, 1)

SCORES_PM = {
    "-- ПМП --": "header",
    "ПМП (город | День)": 3,
    "ПМП (город | Ночь)": 5,
    "ПМП (пригород | День)": 4,
    "ПМП (пригород | Ночь)": 6,
    "-- ТАБЛЕТКИ --": "header",
    "Таблетка (город)": 1,
    "Таблетка (пригород)": 2,
    "-- ВАКЦИНЫ --": "header",
    "Вакцина (город)": 3,
    "Вакцина (пригород)": 5,
    "-- ДЕЖУРСТВА --": "header",
    "Дневное дежурство ELSH": 10,
    "Ночное дежурство ELSH": 25,
    "-- СПРАВКИ --": "header",
    "Справка: Днём в ELSH": 3,
    "Справка: Ночью в ELSH": 6,
    "Справка: Днём в Sandy / Paleto": 5,
    "Справка: Ночью в Sandy / Paleto": 9,
    "-- ПРОЧЕЕ --": "header",
    "Благодарность": 1,
}


class SectionLabel(Label):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.text = title.replace("-", "").strip().upper()
        self.font_size = "18sp"
        self.bold = True
        self.color = (0.23, 0.51, 0.96, 1)
        self.size_hint_y = None
        self.height = dp(42)


class ActionCard(BoxLayout):
    def __init__(self, action_name, score, **kwargs):
        super().__init__(**kwargs)

        self.action_name = action_name
        self.score = score
        self.orientation = "vertical"
        self.spacing = dp(8)
        self.padding = dp(10)
        self.size_hint_y = None
        self.height = dp(160)

        title = Label(
            text=action_name,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(35),
        )

        self.count_input = TextInput(
            text="0",
            hint_text="Количество",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
        )

        self.link_input = TextInput(
            hint_text="Ссылка",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
        )

        self.add_widget(title)
        self.add_widget(self.count_input)
        self.add_widget(self.link_input)


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.last_report = ""
        self.entries = {}
        self.orientation = "vertical"
        self.padding = dp(15)
        self.spacing = dp(10)

        header = Label(
            text="Majestic RP | EMS Tablet",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=dp(50),
        )
        self.add_widget(header)

        scroll = ScrollView()
        self.grid = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None,
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))

        for action, value in SCORES_PM.items():
            if value == "header":
                self.grid.add_widget(SectionLabel(action))
                continue

            card = ActionCard(action, value)
            self.entries[action] = card
            self.grid.add_widget(card)

        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        button_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(8),
        )

        generate_btn = Button(text="СГЕНЕРИРОВАТЬ")
        generate_btn.bind(on_press=self.generate_report)

        copy_btn = Button(text="КОПИРОВАТЬ")
        copy_btn.bind(on_press=self.copy_report)

        clear_btn = Button(text="ОЧИСТИТЬ")
        clear_btn.bind(on_press=self.clear_fields)

        button_layout.add_widget(generate_btn)
        button_layout.add_widget(copy_btn)
        button_layout.add_widget(clear_btn)
        self.add_widget(button_layout)

        self.status_label = Label(
            text="Заполните данные и нажмите СГЕНЕРИРОВАТЬ.",
            size_hint_y=None,
            height=dp(32),
        )
        self.add_widget(self.status_label)

        self.result_output = TextInput(
            text="",
            hint_text="Здесь появится готовый отчет",
            readonly=True,
            multiline=True,
            size_hint_y=None,
            height=dp(190),
        )
        self.add_widget(self.result_output)

    def generate_report(self, *_args):
        try:
            report = self.build_report()
        except Exception as exc:
            self.last_report = ""
            self.result_output.text = ""
            self.status_label.text = f"Ошибка генерации: {exc}"
            return

        self.last_report = report
        self.result_output.text = report
        self.status_label.text = "Отчет сгенерирован. Нажмите КОПИРОВАТЬ."

    def build_report(self):
        report = "ВАШ ОТЧЕТ\n"
        total = 0
        total_pm = 0

        items = list(SCORES_PM.items())
        for index, (action, value) in enumerate(items):
            if value != "header":
                continue

            section_lines = []
            section_title = action.replace("-", "").strip()

            for sub_action, sub_value in items[index + 1:]:
                if sub_value == "header":
                    break

                card = self.entries[sub_action]
                count_text = card.count_input.text.strip()
                count = int(count_text) if count_text.isdigit() else 0
                if count <= 0:
                    continue

                link = card.link_input.text.strip() or "нет ссылки"
                score = count * sub_value
                total += score

                if "ПМП" in section_title.upper():
                    total_pm += score

                section_lines.append(f"• {sub_action}:\n   {count} | {link} | {score}")

            if section_lines:
                report += f"\n[{section_title}]\n" + "\n".join(section_lines) + "\n"

        report += f"\n------------------\nИТОГО: {total}"
        if total > 0:
            report += f"\nПМП составляет: {(total_pm / total * 100):.1f}% от общих баллов"

        return report

    def copy_report(self, *_args):
        if not self.last_report:
            self.status_label.text = "Сначала нажмите СГЕНЕРИРОВАТЬ."
            return

        try:
            Clipboard.copy(self.last_report)
        except Exception as exc:
            self.status_label.text = f"Не удалось скопировать: {exc}"
            return

        self.status_label.text = "Отчет скопирован в буфер обмена."

    def clear_fields(self, *_args):
        for card in self.entries.values():
            card.count_input.text = "0"
            card.link_input.text = ""

        self.last_report = ""
        self.result_output.text = ""
        self.status_label.text = "Поля очищены."


class EMSApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    EMSApp().run()
