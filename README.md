# OptiNotes

## Overview

Welcome to OptiNotes, a powerful command line tool designed to enhance your online learning experience by simplifying the process of taking screenshots during online lectures. Say goodbye to the hassle of manually capturing important lecture moments – let this tool do the work for you!

## Features

- **Automated Screenshot Capture**: Easily capture screenshots at specified intervals during your online lectures without manual intervention.

- **Configurable Settings**: Customize the tool to suit your needs. Adjust capture intervals, output directory, and filename conventions.

- **Silent Mode**: Enable silent mode to run the tool discreetly in the background, ensuring it doesn't interfere with your learning experience.

- **Cross-Platform Compatibility**: Works seamlessly on Windows and Linux, providing a consistent experience across different operating systems.

## Installation

1. **Windows**:

   ```bash
   git clone https://github.com/Espacio-root/optinotes.git
   cd optinotes
   python3 -m venv venv
   pip install -r requirements.txt
   setx PATH "%PATH%;%CD%\scripts" /M
   ```

2. **Linux - Hyprland**:

   ```bash
   git clone https://github.com/Espacio-root/optinotes.git
   cd optinotes/scripts
   sudo chmod +x hyprland.sh
   ./hyprland.sh
   source ~/.bashrc
   ```

## Usage

**Note**: f2 is the default capture key and f4 is the default delete key. These can be changed by passing the -kc and -kd flags respectively.

To begin capturing screenshots, simply run the following command:
```bash
optinotes [-h] [-kc CAPTURE_KEY] [-kd DELETE_KEY] output_dir
```

**Arguments**:
1. **-h, --help**: Show help message and exit.
2. **-kc CAPTURE_KEY `f2`**: Specify the key to be used for capturing screenshots.
3. **-kd DELETE_KEY `f4`**: Specify the key to be used for deleting screenshots.
4. **output_dir**: Specify the output directory for storing screenshots.
