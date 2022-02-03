# nested-polygons

Tool for creating cool visualizations of rotating, nested polygons.

## Requirements
* matplotlib
* numpy
* ffmpeg

## Usage
```python
python nested-polygons.py --help
```

Help output
```bash
usage: nested-polygons.py [-h] [--frames FRAMES]
                          [--colors [COLORS [COLORS ...]]]
                          [--max_polygons MAX_POLYGONS] [--delay DELAY]
                          [--frame_rate FRAME_RATE] [--dpi DPI]
                          nsides filename

Animates nested polygons

positional arguments:
  nsides                Number of sides of the polygon
  filename              Output filename.

optional arguments:
  -h, --help            show this help message and exit
  --frames FRAMES, -f FRAMES
                        Number of frames for animation. Defaults to 100.
  --colors [COLORS [COLORS ...]], -c [COLORS [COLORS ...]]
                        Colors for polygon fills. Can be any number of colors.
                        Defaults to matplotlib's C0 and C1
  --max_polygons MAX_POLYGONS, -m MAX_POLYGONS
                        Maximum number of polygons to draw. Defaults to 1000
  --delay DELAY, -d DELAY
                        Delay between frames in ms. Defaults to 20 ms
  --frame_rate FRAME_RATE, --fps FRAME_RATE, -r FRAME_RATE
                        Video playback frame rate. Defaults to 30
  --dpi DPI             Dots per inch. Defaults to 200
```

## Example

```bash
python nested-polygons.py 6 hexagon.mp4 --fps 30 --colors "royalblue" "silver" -f 400
```

https://user-images.githubusercontent.com/76546515/152270266-1c6946ad-dba4-446f-a157-ca474f17b071.mp4
