import os
from pathlib import Path
from typing import Optional

import typer
from .server_utils import url_azcopy_setup, verbose_run, azcopy_setup,fish_setup,tmux_setup,nvim_setup
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

# improve usability of azcopy

@app.command()
def url_ls(url:str,debug:bool=False):
    url,sas = url_azcopy_setup(url)
    cmd = f'./azcopy ls "{url}"?{sas}'
    verbose_run(cmd,debug)

@app.command()
def url_download(url:str,des:Path=Path("."),
                recursive:bool=False,
                include_pattern:Optional[str]=None,
                is_des_dir:bool=False,
                debug:bool=False):
    url,sas = url_azcopy_setup(url)
    des_str = des.as_posix()
    if is_des_dir:
        des_str = des_str+r"/"
    cmd_l = [
        f'./azcopy cp "{url}"?{sas}', 
        des_str,
    ]
    if recursive:
        cmd_l.append("--recursive")
    if include_pattern is not None:
        cmd_l.append(f"--include-pattern {include_pattern}")
    cmd = " ".join(cmd_l)
    verbose_run(cmd,debug)   

@app.command()
def data_download(data:str,des:Path=Path("."),
                debug:bool=False):
    url = get_dataurl(data)
    url_download(url,des,recursive=True,debug=debug)

@app.command()
def url_upload(url:str,src:Path,
    recursive:bool=False,
    debug:bool=False):
    url,sas = url_azcopy_setup(url)
    src_str = src.as_posix()
    if recursive:
        src_str = src_str+r"/"
    cmd_l = [
        f'./azcopy cp',
        src_str,
        f'"{url}"?{sas}', 
    ]

    if recursive:
        cmd_l.append("--recursive")
    cmd = " ".join(cmd_l)
    verbose_run(cmd,debug)   

