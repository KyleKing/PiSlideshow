# Notes on FBI
# fbi -a -t 5 *.jpg

# Main Site: http://www.nongnu.org/fbi-improved/#bugs

# Docs: http://www.nongnu.org/fbi-improved/fim.man.html
# -T {terminal}, --vt {terminal}
# 	The terminal will be used as virtual terminal device file (as in fbi). See (chvt (1)), (openvt (1)) for more info about this. Use (con2fb (1)) to map a terminal to a framebuffer device.
# -u, --random
# Randomly shuffle the files list before browsing (seed depending on time() function).
# --random-no-seed
# Randomly shuffle the files list before browsing (no seeding).
# -q, --quiet
# Quiet mode. Sets _display_status=0;_display_busy=0;.
# -a, --autozoom
# Enable autozoom. fim will automagically pick a reasonable zoom factor when loading a new image (as in fbi).

# https://www.raspberrypi.org/forums/viewtopic.php?t=196043
fim --random --quiet -R ~/PiSlideShow/test/ -c 'while(1){display;sleep "2";next;}'

# kilall fim

# cd ~/.config/lxpanel/LXDE-pi/panels
# nano panel
# # (Change auto-hide to 1? > set height from 52 > 1)

# See: https://raspberrypi.stackexchange.com/a/28707
# 	cp /usr/share/lxpanel/panel ~/.config/lxpanel/LXDE-pi/panels/

# And: https://unix.stackexchange.com/a/177839
# # lxpanel processes must be killed before it can reload an lxpanel profile.
# killall lxpanel
# # Finds and deletes cached menu items to ensure updates will appear.
# find ~/.cache/menus -name '*' -type f -print0 | xargs -0 rm
# # Starts lxpanel with the `--profile` option and runs as a background process.
# # In this example the profile is LXDE. Profiles are the directories located
# # in $HOME/.config/lxpanel/. In this case, $HOME/.config/lxpanel/LXDE.
# lxpanel -p LXDE &