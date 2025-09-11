from config import *
from ui import ui_page
from server import server
from shiny import App

app: App = App(ui_page, server)

if __name__ == "__main__":
    app.run()
