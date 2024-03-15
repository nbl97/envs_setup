import platform

import os,subprocess,shlex
from pathlib import Path
import urllib

from io import BytesIO
import shutil
import tarfile,zipfile,requests

def verbose_run(cmd:str,debug:bool=False,*args,**kwargs):
    print(f"running cmd:\n{cmd}")
    cmdl = shlex.split(cmd) 
    if not debug:
        subprocess.run(cmdl,*args,**kwargs)
        print(f"Finish running!")

def fish_setup():
    cmds = ["sudo apt-add-repository ppa:fish-shell/release-3", 
            "sudo apt update","sudo apt install fish -y"
        ]
    for cmd in cmds:
        verbose_run(cmd)

def tmux_setup():
    cmds = ["git clone https://github.com/nbl97/.tmux.git",
            "ln -s -f .tmux/.tmux.conf",
            "cp .tmux/.tmux.conf.local .",
        ]
    cwd = os.path.expanduser("~") # which is the ~
    for cmd in cmds:
        verbose_run(cmd,cwd=cwd)
    with open(f"{cwd}/.tmux.conf.local","a") as fout:
        # set up fish and vim mode
        print("setting up fish and vi mode for tmux...")
        fout.writelines(["setw -g mode-keys vi\n" ])
        fout.writelines([
                            "set-option -g default-shell /usr/bin/fish\n",
                        ])

def nvim_setup():
    cwd = os.path.expanduser("~") # which is the ~
    cmds = [
        "curl -LO https://github.com/neovim/neovim/releases/download/v0.7.2/nvim.appimage", 
        "chmod u+x ./nvim.appimage",
        'git config --global core.editor "~/nvim.appimage"',
        'git clone -b reign https://github.com/REIGN12/ReignNVim.git ./.config/nvim', # cloning my nvim config
    ]
    for cmd in cmds:
        verbose_run(cmd,cwd=cwd)

    with open(f"{cwd}/.bash_aliases","a") as fout:
        fout.write('alias nvim="~/nvim.appimage"\n') # .bash_profile is not sourced in fish
    os.makedirs(f"{cwd}/.config/fish",exist_ok=True) # in case no fish config file
    with open(f"{cwd}/.config/fish/config.fish","a") as fout:
        fout.write('source ~/.bash_aliases\n') # source all fish compatible in config.fish; the path should be correct! 

    print("Finish nvim setup!")
