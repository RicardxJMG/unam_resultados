from components import ui_page, server
from shiny import App

app: App = App(ui_page, server)

if __name__ == "__main__":
    app.run()
