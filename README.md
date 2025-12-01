# merge_cli_tool

A macOS-compatible CLI tool to merge RGB videos with `.zlib` depth maps and metadata files, built entirely in the cloud using GitHub Actions.

## 📄 Description

This tool was created to simplify merging RGB video frames with depth maps for Flutter teammates, without requiring them to install Python or dependencies.  

Key features:  
- Merge RGB video, depth maps (`.zlib`), and metadata into a single video output  
- Single executable that runs on macOS (`./merge_cli input_folder`)  
- No Python installation required on client machines  
- Built and packaged in the cloud using GitHub Actions  

## ⚙️ Features

- Automated macOS binary builds using GitHub Actions  
- Cross-platform source code (Python) for easy development  
- Lightweight and fast merging using OpenCV and NumPy  
- Uses ZLIB compression for depth data  

## 🧩 Project Structure

```
merge_tool/
│── merger/
│ └── merge_logic.py # Core merging logic
│── merge_cli.py # CLI entry point
│── requirements.txt # Python dependencies
│── merge_cli.spec # Optional PyInstaller spec file
│── build.sh # Optional build script
```


### File Descriptions

- **merger/merge_logic.py** – Contains all functions for loading videos, decompressing `.zlib` depth maps, aligning frames, and merging RGB + depth frames.  
- **merge_cli.py** – Command-line interface for the tool; parses arguments and calls functions from `merge_logic.py`.  
- **requirements.txt** – Lists all Python dependencies.  
- **merge_cli.spec / build.sh** – Optional files for packaging the CLI into a macOS binary.  

### 🚀 Installation (Developers)

If you want to build or test the Python version locally:

```git clone https://github.com/sanatankafle12/merge_cli_tool.git
cd merge_cli_tool
pip install -r requirements.txt
python merge_cli.py --folder input_folder
```

### 🖥️ Running the macOS Executable (Teammates / End Users)

Once the GitHub Action finishes:

Go to GitHub → Actions

Open the latest workflow run

Download the artifact:
merge-cli-macos.zip

Unzip it

Make it executable:

```chmod +x merge_cli```


Run it:

```./merge_cli --folder input_folder```


- No Python.
- No pip install.
- No dependencies.
Just run and get the merged video.


### 🧪 Example Folder Structure for Input
```input_folder/
│── rgb.mp4
│── depth.zlib
│── metadata.json
```


