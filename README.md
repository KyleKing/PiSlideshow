# PiSlideshow

A Raspberry Pi photo frame using DropBox, Balloon.io, FIM, and Python.

<p align="center">
  <img width="450" height=auto src="./README/cover.jpg" alt="Frame loading">
</p>
<p align="center">
  <img width="450" height=auto src="./README/cover_alt.jpg" alt="Frame with penguin image">
</p>

## How it works

Images are uploaded to Dropbox either through the Dropbox app if the user has permission or uploaded through Balloon.io with given credentials. A Python script on the Raspberry Pi syncs with Dropbox using the V2 API to keep the local directory up to date. [FIM (FBI IMproved)](http://www.nongnu.org/fbi-improved/#docs) is used to cycle the images. A GPIO pin from the Pi is connected to the TFT control board to automatically turn the display off at night.

## Hardware

The Raspberry Pi and TFT display are mounted in a modified IKEA frame. Laser cut pieces hold the electronics in place while allowing plenty of airflow.

<p align="center">
  <img width="450" height=auto src="./README/lc_base_layer.jpg" alt="LC base layer">
</p>
<p align="center">Laser Cut Base Layer / Display Support</p>

<p align="center">
  <img width="450" height=auto src="./README/stacked_lc_acrylic.jpg" alt="Stacked laser cut acrylic">
</p>
<p align="center">Additional laser cut stacked layers</p>

<p align="center">
  <img width="450" height=auto src="./README/the_guts.jpg" alt="The guts">
</p>
<p align="center">Full assembly</p>

## Software/Getting Started Guide

1. Boot a fresh Raspberry Pi with Raspbian Jessie ([KyleKing/Another\_Raspberry\_Pi\_Guide](https://github.com/KyleKing/Another_Raspberry_Pi_Guide#starting-fresh))
2. Download the PiSlideshow code onto the Raspberry Pi (`git clone https://github.com/KyleKing/PiSlideshow.git`)
3. Build FIM (at the time, FIM was not available via `apt-get`)

    ```bash
    wget http://download.savannah.nongnu.org/releases/fbi-improved/fim-0.6-trunk.tar.gz

    # Install these additional packages for good measure
    # Source: https://raspberrypi.stackexchange.com/a/53675
    sudo apt-get install -y flex bison libreadline-dev libexif-dev libpng-dev libjpeg-dev libgif-dev libtiff-dev libpoppler-dev checkinstall

    tar xzf fim-0.6-trunk.tar.gz
    cd fim-0.6-trunk
    ./configure --help=short  # read to see if any options are necessary
    ./configure
    make
    sudo su -c "make install"

    # Point to some directory with images
    fim -R ~/dir\_with\_images/
    ```

4. Install RPi.GPIO `sudo apt-get -y install python-rpi.gpio` *(Optional: you can comment out the related code in `display.py` if you don't want this functionality)*
5. Install other necessary python packages by navigating into the downloaded directory and running `pip install -r requirements.txt`
6. Make the following modifications to Raspberry Pi:

    - Prevent the display from sleeping ([Source - IBEX](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/gui/disable-screen-sleep)). Run `sudo nano /etc/lightdm/lightdm.conf` then add the below lines to [SeatDefaults]:

    ```bash
    # Prevent Display Sleep:
    xserver-command=X -s 0 dpms
    ```

    - Keep the HDMI output always active. Open the Raspberry Pi configuration file for editing with `sudo nano /boot/config.txt` and append below lines ([Source - RPI forum blog post](https://www.raspberrypi.org/forums/viewtopic.php?p=960208&sid=4f3c69da2d903451a832d908ad557917#p960208)):

    ```bash
    # Always force HDMI output and enable HDMI sound
    hdmi_force_hotplug=1
    hdmi_drive=2
    # Power down monitor when lockscreen enabled
    hdmi_blanking=1
    ```

    - Then modify: `sudo nano ~/.config/lxsession/LXDE-pi/autostart` and append the below lines

    ```bash
    # Prevent Screen Blanking
    @xset s 0 0
    @xset s noblank
    @xset s noexpose
    @xset dpms 0 0 0
    ```

7. Hide the LXDE panel (a.k.a. taskbar/doc) because the Bluetooth and WiFi indicators will be redrawn at regular intervals and will appear above the images in the slide show. The easiest solution is to decrease the panel height. Edit the configuration file: `nano ~/.config/lxpanel/LXDE-pi/panels/panel` and change the parameter height from `52` to `1`

    ```bash
    Global {
      ...
      height=1
      autohide=1
      ...
    }
    ```

8. Reboot the pi to allow all changes to take effect (`sudo reboot`). When rebooted, try running the application over SSH to make sure everything is properly installed. Please open a [new issue](https://github.com/KyleKing/PiSlideshow/issues/new) if anything goes awry.
9. Configure rc.local to run the slide show on system startup: [KyleKing/Another\_Raspberry\_Pi\_Guide/.../BashTools.md](https://github.com/KyleKing/Another_Raspberry_Pi_Guide/blob/master/BashTools.md#boot-on-startup)
10. Other:

    - On this particular Raspberry Pi, I ran into issues with http requests for `apt-get` and needed to manually add the nameserver 8.8.8.8 and 4.4.4.4. If necessary, see this guides: https://www.raspberrypi.org/forums/viewtopic.php?p=171733#p171733 (`sudo nano resolvconf.conf`)


## Acknowledgments

This project was inspired by [this guide](http://www.ofbrooklyn.com/2014/01/2/building-photo-frame-raspberry-pi-motion-detector/)

## Made by

[Kyle King](http://kyleking.me)
