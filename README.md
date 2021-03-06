# Hydrogen Download Drumkits
Python script to download Hydrogen drumkits from all configured servers.

## Motivation
The [Hydrogen drum machine](https://github.com/hydrogen-music/hydrogen) has to ability to subscribe to drumkit servers, but does not seem to have the ability to batch download all drumkits. This script does that.

## What does this do?
The script loads at the drumkit server list configured in your Hydrogen config `~/.hydrogen/hydrogen.conf`, and download all drumkits to `~/.hydrogen/data/drumkits/`

## Usage
Run `python download.py`

## Limitation
This script avoids re-downloading drumkits by checking if the drumkit already exists in `~/.hydrogen/data/drumkits/{DRUMKIT_DIR_NAME}`. It checks the drumkit directory name against the name of the drumkit file (`{DRUMKIT_NAME}.h2drumkit`).

This only works as long as `{DRUMKIT_DIR_NAME}`, which is the top-level directory name inside the `.h2drumkit` zip file once extracted, is the same as `{DRUMKIT_NAME}`. For most drumkits this is true, but not all.

## Example usage
```
$ python download.py
http://www.hydrogen-music.org/feeds/drumkit_list.php

    - Audiophob | soundcloud.com/audiophobdubstep
      http://hydro.smoors.de/Audiophob.h2drumkit
      Drumkit already exists. Skipping.

    - belofilms.com - AC-Guitar-Strums (flac) | Gabriel Verdugo Soto (belo@belofilms.com)
      http://hydro.smoors.de/belofilms_GuitarStrums.h2drumkit
      Drumkit already exists. Skipping.

    - BJA_Pacific | Luc Tunguay
      http://sourceforge.net/projects/hydrogen/files/Sound%20Libraries/Main%20sound%20libraries/BJA_Pacific.h2drumkit
      [====================] 16.42 MB / 16.42 MB, 6.93s, 2.37 Mbps

    - JazzFunkKit | Orange Tree Samples / Oddtime
      https://www.orangetreesamples.com/download/JazzFunkKit.h2drumkit
      [====================] 39.39 MB / 39.39 MB, 14.22s, 2.77 Mbps

    - Boss DR-110 (sf) | Artemiy Pavlov
      http://prdownloads.sf.net/hydrogen/Boss_DR-110.h2drumkit
      [====================] 0.21 MB / 0.21 MB, 5.26s, 0.04 Mbps

    - Classic 3355606 (sf) | Artemiy Pavlov
      http://prdownloads.sf.net/hydrogen/3355606kit.h2drumkit
      [====================] 0.40 MB / 0.40 MB, 5.49s, 0.07 Mbps

    - Classic 626 (sf) | Artemiy Pavlov
      http://prdownloads.sf.net/hydrogen/Classic-626.h2drumkit
      [==================  ] 0.53 MB / 0.59 MB, 5.66s, 0.10 Mbps

...
```

