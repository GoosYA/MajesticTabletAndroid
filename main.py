
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.core.window import Window

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
    "Благодарность": 1
}


class ActionCard(BoxLayout):
    def __init__(self, action_name, **kwargs):
        super().__init__(**kwargs)

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
            height=dp(35)
        )

        self.count_input = TextInput(
            hint_text="Количество",
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )

        self.link_input = TextInput(
            hint_text="Ссылка",
            multiline=False,
            size_hint_y=None,
            height=dp(45)
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
            height=dp(50)
        )

        self.add_widget(header)

        scroll = ScrollView()

        self.grid = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None
        )

        self.grid.bind(minimum_height=self.grid.setter("height"))

        self.cards = []

        for action in SCORES_PM:
            card = ActionCard(action)
            self.cards.append(card)
            self.grid.add_widget(card)

        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        button_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        generate_btn = Button(
            text="СГЕНЕРИРОВАТЬ"
        )

        clear_btn = Button(
            text="ОЧИСТИТЬ"
        )

        button_layout.add_widget(generate_btn)
        button_layout.add_widget(clear_btn)

        self.add_widget(button_layout)


class EMSApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    EMSApp().run()
