# from core.config import *
from core.ui import ui_page
from core.server import server
from shiny import App

app: App = App(ui_page, server)

if __name__ == "__main__":
    app.run()
