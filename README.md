# PiSlideshow

>A Raspberry Pi powered smart photo frame / slide show. Anyone can upload photos using Balloon.io, which are added to the display and cycled using FBI

<p align="center">
  <img width="450" height=auto src="./README/cover.jpg" alt="Frame loading">
</p>
<p align="center">
  <img width="450" height=auto src="./README/cover_alt.jpg" alt="Frame with penguin image">
</p>

## How it works

Balloon.io allows you to setup a website where anyone can upload images that are placed into the Apps folder of the linked Dropbox account, which works on mobile and desktop. The app pulls all images from the set Dropbox folder and loads them locally. Once completely downloaded, the FBI task is started to update the image at short time intervals. There is additional logic to handle stopping and starting the FBI task to keep the display always up to date as new photos are downloaded and added to the cycle.

The photo frame can additionally be turned on and off. I wired a GPIO pin to the display controller that toggles the display state from on in the afternoon and off at night.

## The hardware

I modified an IKEA frame to hold a small TFT display with space for airflow and mounting point for the Raspberry Pi and driver board. I stacked a piece of thick white paper for a crisp edge around the display then three pieces of laser cut acrylic. The first piece holds the display, the second provides space for the ribbon cable, and the third has air holes for circulation and is the surface that the boards are mounted to with standoffs

<p align="center">
  <img width="450" height=auto src="./README/lc_base_layer.jpg" alt="LC base layer">
</p>
<p align="center">Laser Cut Base Layer / Display Support</p>

<p align="center">
  <img width="450" height=auto src="./README/stacked_lc_acrylic.jpg" alt="Stacked laser cut acrylic">
</p>
<p align="center">Additional laser cut stacked layers</p>

Three 3D printed feet hold everything sandwiched in place along with the original stand for support. Just on the inside surface of the stand is a small perf board with an indicator LED and pushbutton. The pushbutton allows for manual updates of the display

<p align="center">
  <img width="450" height=auto src="./README/3D_printed_feet.jpg" alt="3D Printed Feet">
</p>
<p align="center">3D Printed Feet</p>

<p align="center">
  <img width="450" height=auto src="./README/the_guts.jpg" alt="The guts">
</p>
<p align="center">Full assembly</p>

## How to run your own version

<!-- FIXME -->

*(TODO) I'm currently migrating to Dropbox v2 authentication, which is a major change, so open up an issue and I'll make sure to let you know my current progress*

<!-- [![Balloon.io](README/balloon.png)](https://balloon.io/) -->

## Acknowledgments

[This guide](http://www.ofbrooklyn.com/2014/01/2/building-photo-frame-raspberry-pi-motion-detector/) inspired this project
