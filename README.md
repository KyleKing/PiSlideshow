# PiSlideshow

>A Raspberry Pi powered smart photo frame / slide show. Anyone can upload photos using Balloon.io, which are added to the display and cycled using FBI

![Frame in use](README/cover.jpg)
![Actual Photo](README/cover_alt.jpg)

## How it works

Balloon.io allows you to setup a website where anyone can upload images that are placed into the Apps folder of the linked Dropbox account, which works on mobile and desktop. The app pulls all images from the set Dropbox folder and loads them locally. Once completely downloaded, the FBI task is started to update the image at short time intervals. There is additional logic to handle stopping and starting the FBI task to keep the display always up to date as new photos are downloaded and added to the cycle.

The photo frame can additionally be turned on and off. I wired a GPIO pin to the display controller that toggles the display state from on in the afternoon and off at night.

## The hardware

I modified an IKEA frame to hold a small TFT display with space for airflow and mounting point for the Raspberry Pi and driver board. I stacked a piece of thick white paper for a crisp edge around the display then three pieces of laser cut acrylic. The first piece holds the display, the second provides space for the ribbon cable, and the third has air holes for circulation and is the surface that the boards are mounted to with standoffs

![First base layer](README/lc_base_layer.jpg)
![Stacked laser cut acrylic](README/stacked_lc_acrylic.jpg)

Three 3D printed feet hold everything sandwiched in place along with the original stand for support. Just on the inside surface of the stand is a small perf board with an indicator LED and pushbutton. The pushbutton allows for manual updates of the display

![3D Printed Feet](README/3D_printed_feet.jpg)
![The guts](README/the_guts.jpg)

## How to run your own version

<!-- FIXME -->

*(TODO) I'm currently migrating to Dropbox v2 authentication, which is a major change, so open up an issue and I'll make sure to let you know my current progress*

[![Balloon.io](README/balloon.png)](https://balloon.io/)

## Acknowledgments

[This guide](http://www.ofbrooklyn.com/2014/01/2/building-photo-frame-raspberry-pi-motion-detector/) inspired this project
