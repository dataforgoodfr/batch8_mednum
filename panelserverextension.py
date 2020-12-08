from subprocess import Popen
import os
def load_jupyter_server_extension(nbapp):
    """serve the gapminder.ipynb directory with bokeh server"""
    os.chdir("dockerize-apps/panel")
    Popen(["panel", "serve", "mednumapp.py", "--allow-websocket-origin=*"])
