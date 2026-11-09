# JSON Generator Pro

A small Windows desktop app for creating one JSON file per device from pasted or loaded account/device pairs. Generated files are also bundled into a timestamped ZIP archive.

## Requirements

- Windows 10 or later
- Python 3 with Tkinter (included with the standard Windows Python installer)
- PyInstaller to build the standalone executable

## Run from VS Code

Open this folder in VS Code, open the integrated PowerShell terminal, and run:

```powershell
python main.py
```

## Input format

Enter one account and device per line, separated by whitespace:

```text
account01 device01
account02 device02
```

Blank lines are ignored. Lines that do not contain exactly two values are reported as invalid, and duplicate device names are skipped.

## Output

By default, the app writes JSON files, a timestamped ZIP archive, and `generator.log` to a `JSON_Output` folder beside the app. When running `main.py`, this folder is beside the script; when running the EXE, it is beside the EXE. Extract the app ZIP to a folder where you have write permission.

Use **Browse Folder** to choose a different output location. Use **Load File** to load a `.txt` or `.csv` text file containing the same two-column format.

## Build the Windows executable

From the project folder in PowerShell, install PyInstaller and package the app:

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The executable will be created at:

```text
dist\main.exe
```

To rename it:

```powershell
Rename-Item .\dist\main.exe JSON_Generator_Pro.exe
```

The renamed executable will be at `dist\JSON_Generator_Pro.exe`. It is a Windows 64-bit app and does not require a separate Python installation on the target machine. On managed company computers, endpoint security policy may require IT approval before an unsigned executable can run.

To create a ZIP to share, put `JSON_Generator_Pro.exe` and this README in the ZIP. Recipients should extract it before running the EXE so the app can create its adjacent `JSON_Output` folder.
