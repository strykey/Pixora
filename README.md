# Pixora

> A pixel art converter that actually looks like pixel art.

Pixora converts any image into authentic pixel art using a real conversion pipeline: perceptual color quantization, Floyd-Steinberg dithering, edge enhancement, and smart automatic pixel size detection. The result looks like something you drew by hand in Aseprite, not like a blurry resize filter. Drop your image, hit Convert, done.

<img width="1366" height="768" alt="Pixora1" src="https://github.com/user-attachments/assets/d407fb5f-7bb4-4bbe-8bea-6bc8b3c56828" />

## What makes it different

Most pixel art converters just resize the image down and call it a day. Pixora does not do that. It analyzes your image dimensions and content to automatically pick a pixel block size that makes sense for the subject, builds a color palette using median cut quantization based on what is actually in your image, applies dithering to smooth out color transitions, and darkens edges to give the output that handcrafted depth you would normally add manually. The whole process is automatic. You do not have to touch a single setting if you do not want to.

## What it does

Smart auto pixel size : Pixora reads your image and picks a block size that fits the subject. A detailed render gets small precise blocks. A wide landscape gets larger ones. The pixel art respects what the image actually is, not a one-size-fits-all grid.

Perceptual color quantization : Colors are reduced using median cut, which splits the color space based on actual visual variety in your image. The palette feels natural because it comes from the image itself, not from arbitrary rounding.

Floyd-Steinberg dithering : The classic dithering algorithm used in real pixel art and old-school game graphics. Color transitions blend smoothly without banding. You can adjust the strength with a slider or turn it off entirely.

Edge enhancement : High-contrast pixel boundaries get a slight darkening that simulates the outlines you would draw manually in a pixel art editor. It adds weight and readability to the result.

4K export : The output PNG is rendered at 4096 pixels on the longest side, always at an exact integer multiple of the pixel block size. Every block is perfectly crisp. The file scales down cleanly for game sprites or prints large without any artifacts.

Multiple import methods : Drag and drop onto the window, click Browse to pick a file, or paste directly from your clipboard with Ctrl+V.

Original vs result view : Switch between the source image and the converted output inside the app. The canvas fits to your window automatically and supports mouse wheel zoom.

## Requirements

Python 3.9 or higher. Works on Windows, macOS, and Linux.

```
pywebview>=4.4.1
Pillow>=10.0.0
```

## Installation

```bash
git clone https://github.com/strykey/pixora.git
cd pixora
pip install -r requirements.txt
python pixora.py
```

## How to use it

Launch the app and you land on the main interface after a short loading screen. The sidebar on the left handles everything. The large area on the right is your canvas.

Importing : Drop your image onto the window, click Browse, or paste from clipboard with Ctrl+V. Pixora accepts PNG, JPG, WEBP, BMP, and GIF. The image appears immediately at a zoom level that fits your window, and the source dimensions show up in the info bar at the bottom.

Converting : Click Convert. Pixora automatically picks the pixel size, builds the palette, applies dithering and edge enhancement, and renders the result. Takes a few seconds depending on image size. When it is done the output appears in the canvas and the info bar updates with the output dimensions, block size, and color count.

Tweaking : If you want to adjust things before converting, four controls are available in the sidebar. Pixel Size lets you override the auto detection and force a specific block size from 1 to 32 pixels. Color Depth sets the maximum number of colors in the palette. Dither adjusts the Floyd-Steinberg strength. Edge Enhance is a toggle for the boundary darkening. For most images the defaults give excellent results with no adjustments needed.

Comparing : The Result and Original tabs in the toolbar let you switch between the converted output and your source image at the same zoom level.

Zooming : Use the toolbar buttons or scroll with your mouse wheel on the canvas. The reset button fits the image back to the window.

Exporting : Click Export 4K. Pixora saves a PNG to your Pictures folder on Windows and macOS, or your home directory on Linux. The file is named pixora_export.png and increments automatically if one already exists. The exported file is the full 4K render, not the preview you see in the canvas.

## Project structure

```
pixora/
    pixora.py          entire application, single file
    requirements.txt   Python dependencies
    README.md          this file
    LICENSE            license
```

## And later?

Pixora is a first release and a lot more is coming, and most of it is coming very soon.

The biggest upcoming feature is a native Aseprite export. You will be able to export your converted pixel art directly as an Aseprite file and open it straight in the software to keep editing. The palette will already be organized, every pixel block will be preserved exactly as Pixora rendered it, and you will be able to start refining your art immediately without any import workaround or manual setup. This is the top priority right now and should land very soon.

After that, export profiles for game engines are planned. Presets that optimize the output for Unity sprites, Godot tilesets, GameMaker sprite sheets and more, with things like power-of-two dimensions, specific color depth targets, transparent background handling, and sprite sheet packing. The idea is to drop your concept art in and get a game-ready asset out without touching anything else in between.

Other things in the backlog include batch conversion for entire folders at once, a palette lock to force the output to match a specific game palette like NES or Game Boy, and animation support for GIF inputs that preserves frame timing through the conversion.

## License

This project is under the Pixora Source License. See the LICENSE file for the full terms.

Attribution is required. Any use of this code, modified or not, in any project, requires you to visibly credit Strykey as the original author. This applies to private tools, public repos, forks, and any derivative works.

Commercial use is not allowed without explicit written permission from the author.

You cannot redistribute this software under a different license or remove the original attribution.

## Author

**Strykey**

*"Pixel art without the 40 hours."*

