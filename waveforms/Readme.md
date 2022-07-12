# Reading and modifying Pinenote waveform files

** WORK IN PROGRESS **

Parsing of waveform files is based on smaeuls (Samuel Holland
<samuel@sholland.org>) work:

https://github.com/smaeul/linux/blob/rk35/ebc-drm-v5/drivers/gpu/drm/drm_epd_helper.c

## Usage

copy your waveform image to 02_waveform.img and run ./waveform.py
A new waveform file "test.bin" is then produced with modified A2 waveform.

## Analysis of factory-provided waveforms

[default_waveform_lengths.jpg](default_waveform_lengths.jpg)
