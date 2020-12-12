# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
import subprocess
from copy import copy
from astro import start_astro_scanner
from threading import Thread

from typing import List  # noqa: F401

COLORS = {
    "Polar Night": ["#2e3440", "#3b4252", "#434c5e", "#4c566a"],
    "Snow Storm": ["#d8dee9", "#e5e9f0", "#eceff4"],
    "Frost": ["#8fbcbb", "#88c0d0", "#81a1c1", "#5e81ac"],
    "Aurora": ["bf616a", "d08770", "ebcb8b", "a3be8c", "b48ead"],
}


HOME = os.path.expanduser('~')

def_colors = {
    "background": COLORS["Polar Night"][0],
    "window active": COLORS["Frost"][1],
    "window inactive": COLORS["Frost"][3],
}

##### KEYBINDINGS ######
SUPER = "mod4"
ALT = "mod1"

mod = SUPER

##### CUSTOM GROUPS ######
groups = [
    ScratchPad("scpd", [
        # Dropdown alacritty terminal
        DropDown("term", "alacritty", opacity=0.8),
        # Dropdown spotify using spotify-tui
        DropDown("music", "alacritty -e spt --tick-rate=17", opacity=0.99, x=0.05, width=0.9, height=0.6),
        # Dropdown calendar using calcurse
        DropDown("calendar", "alacritty -e calcurse", opacity=0.99, x=0.05, width=0.9, height=0.6)
    ]),
    Group("a", layout="monadtall"),
    Group("s", spawn="firefox", layout="max"),
    Group("d", spawn="alacritty", layout="monadtall"), #, matches=[Match(wm_class=["alacritty", "Alacritty"])],
    Group("f", layout="monadwide"),
    Group("u"),
    Group("i", matches=[Match(wm_class=["lutris"])], spawn="lutris"),
    Group("o", matches=[Match(wm_class=["thunderbird", "Mozilla Thunderbird"])], spawn="thunderbird", layout="max"),
    Group("p", matches=[Match(wm_class=["discord"])], spawn="discord", layout="max"),
]

##### LAYOUTS #####
layout_config = dict(
    margin = 6, # Gap between windows
    border_focus = def_colors["window active"], # Focused window border color
    border_normal = def_colors["window inactive"], # Inactive window border color
    border_width = 3, # Width of focused and inactive borders
)


layouts = [
    layout.Max(
        margin=layout_config["margin"]),

    layout.MonadTall(
        **layout_config,
        ),

    layout.MonadWide(
        **layout_config,
        ),

    layout.floating.Floating(
        auto_float_types="toolbar",
        border_normal = COLORS["Frost"][0],
        border_focus = COLORS["Aurora"][3],
        **({key:val for key, val in layout_config.items() if key != 'border_normal' and key != 'border_focus'}),
        ),
]


##### KEYS #####
keys = [
    # Switch between windows in current stack pane
    Key([mod, "shift"], "k", lazy.layout.down()),
    Key([mod, "shift"], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod], "k", lazy.layout.shuffle_down()),
    Key([mod], "j", lazy.layout.shuffle_up()),
    Key([mod], "h", lazy.layout.grow()),
    Key([mod], "l", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.reset()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key(["control", ALT], "t", lazy.group['scpd'].dropdown_toggle('term')),
    Key([mod], "period", lazy.group['scpd'].dropdown_toggle('music')),
    Key([mod], "comma", lazy.group['scpd'].dropdown_toggle('calendar')),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "c", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu --no-symbols")),
    Key([mod], "r", lazy.spawn('rofi -show drun')),
    Key([mod, "shift"], "r", lazy.spawn('rofi -show run')),
    # Sow Greenclip clipboard manager
    Key([mod], "c", lazy.spawn('rofi -modi "clipboard:greenclip print" -show clipboard -run-command \'{cmd}\'')),
    # Switch to last used group with Alt+Tab
    #Key([ALT], "Tab", lazy.screen.toggle_group()),
    Key([ALT], "Tab", lazy.spawn('rofi -show window')),

    # Lock screen
    #Key([mod, "shift"], "l", lazy.spawn("dm-tool lock")),
    # Toggle if a window is floating
    Key([mod, "shift"], "Tab", lazy.window.toggle_floating()),
    # Spawn "explorer", file manager
    #Key([mod], "e", subprocess.call([start_sh])),

    ### Special keys ###
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),

    Key([], "Print", lazy.spawn("flameshot gui")),
    Key(["shift"], "Print", lazy.spawn("flameshot screen")),
    Key(["control"], "Print", lazy.spawn("flameshot full")),

]

for i in groups:
    if i.name == "scpd":
        continue

    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, 'shift'], i.name, lazy.window.togroup(i.name)),
    ])

##### SCREENS #####

widget_defaults = dict(
    font='FiraMono',
    fontsize=12,
    padding=3,
    background=def_colors["background"],
    foreground=COLORS["Snow Storm"][2],
)
extension_defaults = widget_defaults.copy()

separator = copy(widget.Sep(linewidth=2))
arrow_left = dict(
    text='',
    fontsize = 43,
    padding = 0
)


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.GroupBox(invert_mouse_wheel=True),
                separator,
                widget.TaskList(
                    font = "FiraMono Bold",
                    markup_focused = "<b>{}</b>",
                    txt_floating =  "🗗 ",
                    txt_maximized = "🗖 ",
                    txt_minimized = "🗕 ",
                    border = COLORS["Polar Night"][3],
                    ),
                widget.TextBox(
                       foreground = COLORS["Frost"][3],
                       **arrow_left
                       ),
                widget.Systray(background = COLORS["Frost"][3]),
                widget.TextBox(
                       foreground = COLORS["Aurora"][1],
                       background = COLORS["Frost"][3],
                       **arrow_left
                       ),
                widget.Volume(
                    volume_down_command = "amixer -D pulse sset Master 5%-", 
                    volume_up_command = "amixer -D pulse sset Master 1%+", 
                    volume_app = "pavucontrol",
                    background = COLORS["Aurora"][1],
                    ),
                widget.TextBox(
                       foreground = COLORS["Aurora"][0],
                       background = COLORS["Aurora"][1],
                       **arrow_left
                       ),
                widget.Clock(
                    format='%I:%M %p %m/%d',
                    timezone=None,
                    background = COLORS["Aurora"][0],
                    )
            ],
            24,
            opacity=0.9,
            background=def_colors["background"]
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.GroupBox(invert_mouse_wheel=True),
                separator,
                widget.TaskList(
                    font = "FiraMono Bold",
                    markup_focused = "<b>{}</b>",
                    txt_floating =  "🗗 ",
                    txt_maximized = "🗖 ",
                    txt_minimized = "🗕 ",
                    border = COLORS["Polar Night"][3],
                    ),
                widget.TextBox(
                       foreground = COLORS["Aurora"][1],
                       **arrow_left
                       ),
                widget.Clock(
                    format='%I:%M %p %m/%d',
                    timezone=None,
                    background = COLORS["Aurora"][1]),
                widget.TextBox(
                       foreground = COLORS["Aurora"][0],
                       background = COLORS["Aurora"][1],
                       **arrow_left
                       ),
                widget.LaunchBar(
                    progs=[('Exit', "rofi -show power-menu -modi power-menu:rofi-power-menu --no-symbols", 'Exit menu')], 
                    default_icon=HOME+"/.local/share/icons/logout.png",
                    background = COLORS["Aurora"][0],
                    padding = 0
                    ),
            ],
            24,
            opacity=0.9,
            background=def_colors["background"]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


##### HOOKS & SCRIPTS #####

# Startup programs
@hook.subscribe.startup_once
def autostart():
    start = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.call([start])


astro = Thread(target=start_astro_scanner)
astro.start()

##### SETTINGS #####

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        {'wmclass': 'confirm'},
        {'wmclass': 'dialog'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'confirmreset'},  # gitk
        {'wmclass': 'makebranch'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass
        {'wname': 'Library'},  # Firefox history
        {'wname': 'Kite'},  # Kite AI
        {'wmclass': 'InputOutput'},
    ],
    border_normal = COLORS["Frost"][0],
    border_focus = COLORS["Aurora"][3],
    **({key:val for key, val in layout_config.items() if key != 'border_normal' and key != 'border_focus'}),
    )
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this.
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
# wmname = "Qtile" # Breaks PyCharm :(
wmname = "LG3D"

