from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Static


class ButtonsApp(App[str]):
    CSS_PATH = "button.tcss"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            VerticalScroll(
                Static("Standard Buttons", classes="header"),
                Button("Default",id="button2"),
                Button("Primary!", variant="primary",id="button1"),
                Button.success("Success!"),
                Button.warning("Warning!"),
                Button.error("Error!"),
            ),
            VerticalScroll(
                Static("Disabled Buttons", classes="header"),
                Button("Default", disabled=True),
                Button("Primary!", variant="primary", disabled=True),
                Button.success("Success!", disabled=True),
                Button.warning("Warning!", disabled=True),
                Button.error("Error!", disabled=True),
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "button1":
            print("button1")
        if event.button.id == "button2":
            print("button2")
        self.exit(str(event.button))


if __name__ == "__main__":
    app = ButtonsApp()
    print(app.run())
