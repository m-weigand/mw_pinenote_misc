#!/usr/bin/env sh

mkdir -p $HOME/.local/share/gnome-shell/extensions
rsync -avh pnhelper@m-weigand.github.com/ $HOME/.local/share/gnome-shell/extensions/pnhelper@m-weigand.github.com/
