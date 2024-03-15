import os
from pathlib import Path
from typing import Optional

import typer
from .server_utils import verbose_run, fish_setup,tmux_setup,nvim_setup
from .server_utils import get_dataurl

app = typer.Typer()

@app.command()
def hold(time:str='7d'):
    typer.echo(f"hold the server for {time}")
    cmd = f'sleep {time}'
    verbose_run(cmd)

@app.command()
def dev_setup():
    fish_setup()
    tmux_setup()
    nvim_setup()

@app.command()
def editor_setup():
    nvim_setup()
