from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

Window.clearcolor = (0.04, 0.06, 0.12, 1)

SCORES_PM = {
    "ПМП (город | День)": 3,
    "ПМП (город | Ночь)": 5,
    "ПМП (пригород | День)": 4,
    "ПМП (пригород | Ночь)": 6,
    "Таблетка (город)": 1,
    "Таблетка (пригород)": 2,
    "Вакцина (город)": 3,
    "Вакцина (пригород)": 5,
    "Благодарность": 1,
}


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
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(35),
        )

        self.count_input = TextInput(
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

        self.cards = []

        for action, score in SCORES_PM.items():
            card = ActionCard(action, score)
            self.cards.append(card)
            self.grid.add_widget(card)

        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        button_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
        )

        generate_btn = Button(text="СГЕНЕРИРОВАТЬ")
        generate_btn.bind(on_release=self.generate_report)

        clear_btn = Button(text="ОЧИСТИТЬ")
        clear_btn.bind(on_release=self.clear_fields)

        button_layout.add_widget(generate_btn)
        button_layout.add_widget(clear_btn)

        self.add_widget(button_layout)

    def generate_report(self, *_args):
        lines = []
        total_score = 0

        for card in self.cards:
            count_text = card.count_input.text.strip()
            link = card.link_input.text.strip()

            if not count_text:
                continue

            count = int(count_text)
            if count <= 0:
                continue

            score = count * card.score
            total_score += score

            line = f"{card.action_name}: {count} x {card.score} = {score} балл."
            if link:
                line += f" Ссылка: {link}"
            lines.append(line)

        if not lines:
            self.show_message("Отчет", "Введите количество хотя бы в одном пункте.")
            return

        report = "\n".join(lines)
        report += f"\n\nИтого: {total_score} балл."
        Clipboard.copy(report)
        self.show_message("Отчет скопирован", report)

    def clear_fields(self, *_args):
        for card in self.cards:
            card.count_input.text = ""
            card.link_input.text = ""

    def show_message(self, title, message):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10),
        )
        text = TextInput(
            text=message,
            readonly=True,
            multiline=True,
            size_hint_y=True,
        )
        close_btn = Button(
            text="ЗАКРЫТЬ",
            size_hint_y=None,
            height=dp(48),
        )
        content.add_widget(text)
        content.add_widget(close_btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.75),
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


class EMSApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    EMSApp().run()
