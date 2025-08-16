# Rembg-Fuse

## 🎬 **Automatic Background Remover for DaVinci Resolve Fusion**  
Free and open-source plugin that integrates the power of [rembg](https://github.com/danielgatis/rembg) into Fusion workflows for seamless background removal.

## ✨ Features

- 🔍 AI-powered background removal using U-2-Net
- 🎞️ Designed for DaVinci Resolve Fusion workflows
- 🛠️ Lightweight, script-based implementation (Python + Fuse)
- 🧩 Easy to integrate
- 🆓 100% Free and Open Source

## ⬇️ Download

### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/Rembg-Fuse?&color=white&label=Download%20Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="400">](https://github.com/Akascape/Rembg-Fuse/archive/refs/heads/main.zip)
<br> _Don't forget to leave a_ ⭐

## ⚙️ How to Install

1. First install the latest python3 from [www.python.org](www.python.org) 
2. Download/Clone the Rembg-Fuse Repo
3. Paste the folder in the fuse plugin directory of Resolve. [Know How](https://youtube.com/shorts/OFHyc48WOqc?feature=shared)
4. Follow the Rembg setup, either using rembg_manager.py or manually.
5. Open the Fusion page in DaVinci Resolve
6. Search for the Rembg plugin in the node menu (_Shift+Spacebar_)
7. Add the node with any footage
8. Select the model and let the plugin do its work
9. The removed background will be displayed through the media out (if connected)
    
### ⮞ Automatic Setup for beginners [Rembg_Manager]
An easy-to-use Python script has been developed to simplify the Rembg setup. Just open the setup.py file—either directly in Python or via the Fuse interface — and follow the installation steps.

<br> ![demo_rembg_manager](https://github.com/user-attachments/assets/a5de323e-6bf9-4823-ba59-fb7e29ddad65)

<details> 
<summary><span style="font-size:1.25em"><strong>Or Setup Manually</strong></span></summary>
   
<br> If you encounter any error or prefer to manually install Rembg and its models, follow the steps below:

* * Install rembg using pip/pip3 command

```
pip install rembg
```
<br> For CUDA support, use `rembg[gpu]`
<br> For AMD/ROCM support, use `rembg[rocm]`

* * Download the models using this script commands:
```python
import rembg

rembg.new_session("model_name") # replace model name with the actual model name
```
* *  Also write the _model_name_ in the models.txt file (newline)
</details> 

## 📦 Available Models
| Model Name             | Description                                                         | Estimated Download Size      |
|------------------------|---------------------------------------------------------------------|------------------------------|
| u2net                  | Standard U2-Net model for high-quality general segmentation         | 168 MB                       |
| u2netp                 | Lightweight U2-Net for faster, lower-resource inference             | 4 MB                         |
| u2net_human_seg        | U2-Net model specialized for human segmentation                     | 168 MB                       |
| u2net_cloth_seg        | U2-Net model specialized for clothing segmentation                  | 168 MB                       |
| isnet-general-use      | ISNet model for general-purpose image segmentation                  | 170 MB                       |
| isnet-anime            | ISNet model optimized for anime-style image segmentation            | 168 MB                       |
| silueta                | Silueta model for silhouette and background removal                 | 43 MB                        |
| sam                    | Segment Anything Model (SAM) ViT decoder for versatile segmentation | 400 MB                       |
| birefnet-general       | BiRefNet model for high-quality general segmentation                | 928 MB                       |
| birefnet-general-lite  | Lightweight BiRefNet for general segmentation                       | 214 MB                       |
| birefnet-portrait      | BiRefNet model tailored for portrait segmentation                   | 928 MB                       |
| ben2-base              | BEN2 base model for efficient background removal                    | 213 MB                       |

For more details, visit this repo: https://github.com/danielgatis/rembg

## 🪄 Demo

## 🌱 Overview

| Fuse Version                   | 0.1                           |
|:-------------------------------|:------------------------------|
| Fuse Version                   | 0.1                           |
| Setup Version                  | 1.0                           |
| DaVinci Resolve Requirement    | Free or Studio : 18+          |
| License                        | MIT                           |
| Copyright                      | 2025                          |
| Author                         | Akash Bora                    |

## 🚧 Planned Improvements
- Streamline Python Script Execution on Windows Eliminate the disruptive console popup by implementing a cleaner method to trigger the processing script. Maybe consider using `comp:DoAction()` for a more integrated Fusion workflow.

- Optimize Model Reloading and improve overall performance during repeated operations.

- Refactor Image I/O Handling, replace the use of the `Clip()` method with direct image data passing. Maybe consider the `GetPixel()` method.
  
Whether you're fixing bugs, suggesting enhancements, or adding new features—your input is valued. Feel free to fork, improve, and submit pull requests to help evolve this tool.

**Get more Resolve plugins at [www.akascape.com](www.akascape.com) 👈**
## Thank You




