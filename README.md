# Rembg-Fuse

## 🎬 **Automatic Background Remover for DaVinci Resolve Fusion**  
Free and open-source plugin that integrates the power of [Rembg](https://github.com/danielgatis/rembg) into Fusion workflows for seamless background removal.

## ✨ Features

- 🔍 AI-powered background removal using U-2-Net via Rembg
- 🎞️ Designed for DaVinci Resolve Fusion workflows
- 🛠️ Lightweight, script-based implementation (Python + Fuse)
- 🧩 Easy to integrate 
- 🆓 100% Free and Open Source

## ⬇️ Download

### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/Rembg-Fuse?&color=white&label=Download%20Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="400">](https://github.com/Akascape/Rembg-Fuse/archive/refs/heads/main.zip)

## ⚙️ How to Install

1. First install the latest python3 from [www.python.org](www.python.org) 
2. Download/Clone the Rembg-Fuse Repo in the fuse folder of DaVinci Resolve. [Know How](https://youtube.com/shorts/OFHyc48WOqc?feature=shared)
3. Follow the Rembg setup:
   
### Automatic Setup for beginners
An easy-to-use python application is developed for setuping rembg. Open the setup.py file in python or (through the fuse) and follow the installation. 

### Or Manual Setup
Incase you ran into some erro, or want to manually install rembg and its models, follow this setup:
- Install rembg using pip/pip3 command

```
pip install rembg
```
<br> For CUDA support, use `rembg[gpu]`
<br> For AMD/ROCM support, use `rembg[rocm]`

- Download the models using this script commands:
```python
import rembg

rembg.new_session("model_name") # replace model name with the actual model name
```

4. Open Fusion page in DaVinci Resolve
5. Search for the Rembg plugin in the node menu (_Shift+Spacebar_)
6. Add the node with some footage
7. Select the model and let the plugin do its work
8. The removed background will be displayed through the media out if connected
   
## Demo

## Overview





