# Pixora

> A natural pixel art converter that actually looks like pixel art.

Pixora converts any image into authentic pixel art using a real conversion pipeline — perceptual color quantization, Floyd-Steinberg dithering, edge enhancement, and smart pixel size detection. The result looks like something you would draw by hand in Aseprite, not like a blurry Instagram filter. Drop your image, hit Convert, done.

## What makes it different

Most pixel art converters just resize the image down and call it a day. Pixora does not do that. It analyzes the image dimensions and content density to automatically pick the right pixel size, then builds a color palette using median cut quantization, applies dithering to smooth color transitions, and reinforces edges to give the output that handcrafted pixel art depth. The whole process is automatic. You do not have to touch a single setting if you do not want to.

## Features

**Smart auto pixel size** — Pixora reads your image dimensions and picks a pixel block size that makes sense. A wide landscape will get larger blocks. A detailed weapon render will get smaller ones. You get pixel art that respects the original subject, not a 32x32 blob of nothing.

**Perceptual color quantization** — Colors are reduced using median cut, which splits the color space based on actual visual variety rather than arbitrary buckets. The palette feels natural because it is built from what is actually in your image.

**Floyd-Steinberg dithering** — The classic dithering algorithm used in real pixel art and old-school game graphics. Color transitions blend smoothly without harsh banding. You can adjust the strength or turn it off entirely.

**Edge enhancement** — Pixel boundaries at high-contrast edges are darkened slightly to simulate the outline depth you would add manually in a pixel art editor. It adds weight and clarity to the result.

**4K export** — The output PNG is rendered at 4096 pixels on the longest side, always at an integer multiple of the pixel block size. That means every pixel block is perfectly crisp, never blurry, never anti-aliased. You get a file that scales down cleanly for game sprites or prints large without artifacts.

**Multiple import methods** — Drag and drop, browse, or paste directly from clipboard with Ctrl+V. Whatever is fastest for your workflow.

**Original vs result view** — Switch between the source image and the converted result inside the app. The canvas fits automatically to your window and supports mouse wheel zoom.

## Requirements

Python 3.9 or higher. Works on Windows, macOS, and Linux.

```
pywebview>=4.4.1
Pillow>=10.0.0
```

## Installation

Clone the repository:

```bash
git clone https://github.com/strykey/pixora.git
cd pixora
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python pixora.py
```

## How to use it

Launch the app and you will land on the main interface after a short loading screen. The sidebar on the left handles everything. The large area on the right is where your image lives.

**Importing your image**

Drop your image directly onto the interface, click Browse to pick a file, or paste an image from your clipboard with Ctrl+V. Pixora accepts PNG, JPG, WEBP, BMP, and GIF. As soon as the image loads it appears in the canvas at a zoom level that fits your window. You can see the source dimensions in the info bar at the bottom.

**Converting**

Click Convert. That is it. Pixora will automatically determine the right pixel size for your image, build the color palette, apply dithering and edge enhancement, and render the result. The whole process takes a few seconds depending on your image size. When it is done the result appears in the canvas and the info bar updates with the output dimensions, block size, and color count.

If you want to tweak the output before converting, you have four sliders available. Pixel Size lets you override the auto detection and force a specific block size between 1 and 32 pixels. Color Depth controls how many colors the palette will contain. Dither adjusts the strength of the Floyd-Steinberg algorithm. Edge Enhance is a toggle that turns the boundary darkening on or off. For most images the default settings produce excellent results without any adjustments.

**Comparing**

Use the Result and Original tabs in the toolbar to switch between the converted output and your source image. Both are displayed at the same zoom level so you can visually compare them.

**Zooming**

Use the plus and minus buttons in the toolbar or scroll with your mouse wheel directly on the canvas. The reset button fits the image back to the window.

**Exporting**

Click Export 4K. Pixora saves a PNG file to your Pictures folder on Windows and macOS, or your home directory on Linux. The file is named pixora_export.png and increments automatically if a file with that name already exists. The exported file is the full 4K resolution render, not what you see in the canvas preview.

## Project structure

```
pixora/
├── pixora.py          # Entire application, single file
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── LICENSE            # License
```

## And later?

Pixora is a first release and there is more planned.

The next big addition will be an export to the native Aseprite format. That means you will be able to take your converted pixel art directly into Aseprite and start editing it as a proper layered pixel art file, with the palette already organized and each pixel block preserved exactly as Pixora rendered it. No import tricks, no workarounds, just open the file and keep working.

After that, export profiles for game engines are on the roadmap. That means presets that optimize the output for specific use cases like Unity sprites, Godot tilesets, or GameMaker sprite sheets. Things like power-of-two dimensions, specific color depth targets, transparent background handling, and sprite sheet packing. The idea is that you drop your concept art in and get a game-ready asset out without touching any other tool in between.

Other ideas in the backlog include batch conversion for processing entire folders of images at once, a palette lock feature to force the output to match a specific game palette like NES or Game Boy, and animation support for GIF inputs that preserves frame timing in the output.

## License

This project is licensed under the Pixora Source License. See the LICENSE file for the full terms.

**Key points:**

Attribution is required. If you use any portion of this code, modified or not, in any project, you must visibly credit Strykey as the original author. This includes private tools, public repositories, forks, and any derivative works.

You may not use this code or any derivative for commercial purposes without explicit written permission from the author.

You may not redistribute this software under a different license or remove the original attribution.

## Author

**Strykey**

*"Pixel art without the 40 hours."*