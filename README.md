# 📂 File Organizer

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

### 🎥 Video Demo: https://www.youtube.com/watch?v=xyUQ1zj_sfM

## 📝 Description

**File Organizer** is a Python-based tool that automatically organizes your files into clean, structured folders based on the type of operation you choose to perform on the folder.
It comes with both a **Command Line Interface (CLI)** and a **Graphical User Interface (GUI)** using **PySide6**, so it can be used comfortably by both technical and non-technical users.
The project was developed as part of my **CS50 Final Project**.
The main goal of this project is to combine **simplicity, automation, and flexibility**. Instead of manually dragging files into folders, you can run this organizer and instantly achieve a clean workspace.

Over time, folders like _Downloads_ or _Desktop_ often become cluttered with hundreds of random files. This project saves you time by sorting those files into categories like **Images, Documents, Audio, Video, Code, Archives, and Others** — all in just a few seconds. This is one of the use case of the project, others are described below.

## ✨ Features

- 🔍 **File Categorization**  
  Automatically detects the type of each file using its extension and moves it to the appropriate folder.
  The folder name for the corresponding extension is added in the file_categories.json
  - `.txt` → **Text files**
  - `.md` → **Markdown**
  - `.rtf` → **Rich Text Format**
  - `.log` → **Log Files**
  - `.json`, `.xml`, `.yaml` → **Data Files**
  - `.pdf` → **PDF Documents**
  - `.doc`, `.docx` → **Word Documents**
  - `.odt` → **OpenDocument Text**
  - `.ppt`, `.pptx` → **PowerPoint Presentations**
  - `.odp` → **OpenDocument Presentations**
  - `.xls`, `.xlsx` → **Spreadsheets**
  - `.ods` → **OpenDocument Spreadsheets**
  - `.csv` → **CSV Files**
  - `.jpeg`, `.jpg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.heic` → **Raster Images**
  - `.svg` → **Vector Images**
  - `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` → **Videos**
  - `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, `.wma` → **Audio Files**
  - `.c`, `.cpp`, `.h` → **C/C++ Source & Headers**
  - `.java` → **Java Source Code**
  - `.py` → **Python Files**
  - `.ipynb` → **Jupyter Notebooks**
  - `.js` → **JavaScript**
  - `.ts` → **TypeScript**
  - `.jsx`, `.tsx` → **React (JSX/TSX)**
  - `.html`, `.css`, `.php` → **Web Development**
  - `.rb` → **Ruby**
  - `.go` → **Go**
  - `.rs` → **Rust**
  - `.swift` → **Swift**
  - `.kt` → **Kotlin**
  - `.sh` → **Shell Scripts**
  - `.bat` → **Batch Files**
  - `.sql` → **Database SQL Scripts**
  - `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` → **Compressed Archives**
  - `.exe` → **Executable Files**
  - `.msi` → **Windows Installers**
  - `.apk` → **Android Apps**
  - `.dmg` → **macOS Disk Images**
  - `.iso` → **Disk Images**
  - `.bin` → **Binary Files**
  - `.dll` → **Dynamic Link Libraries**
  - `.sys` → **System Files**
  - `.ttf`, `.otf`, `.woff`, `.woff2` → **Font Files**
- Any unrecognized extension is placed into the **Others** category.

- 📅 **Organize by Creation Date**  
  Files can also be grouped into folders by the year of creation (e.g., `2023`, `2024`), making it very easy to access files based on their year of creation

- 📦 **Subfolder Extraction**  
  If you have nested folders (top level), the program can extract files from sub folders and bring them into a single organized parent folder.

- 📊 **Progress Bar & Status Updates**  
  For the CLI, progress is shown using **Rich** (colored progress bars). In the GUI, the **status bar** updates dynamically to reflect the current task (e.g., _“Processing...”_).

- 🖥️ **Dual Interface**
  - **CLI Mode:** Lightweight, perfect for terminal users with progress bar and status.
  - **GUI Mode (PySide6):** User-friendly interface with buttons, radio options, a live folder tree view, status bar and a summary after the operation is completed.

## 🎯 Motive & Problem Solved

I came across the idea of building this project while sorting my backup files on an external storage device.  
The process was extremely **hectic and time-consuming**, especially when it came to **removing duplicate files**.  
I had to carefully ensure that the **original file remained untouched** while only its duplicate copies were deleted.

This frustration made me realize the need for an **automated file organizer** that could:

- Detect and separate duplicates
- Organize files by extension or creation date
- Flatten deeply nested folders
- Remove empty directories safely

The goal of this project is to **save time, reduce manual effort, and make file management stress-free**

## 🏗️ Project Structure

- `file_organizer.py`: Contains all the functions to organize files by type, creation year, uniqueness, or flatten nested folders. Includes progress bars and error handling. This is the program that is used as **CLI Tool**
- `gui_tool.py`: Graphical interface for the File Organizer allowing users to select folders, choose modes, and view a summary of operations. This program enables **GUI**
- `file_categories.json`: JSON file containing mappings from file extensions to user-friendly categories (e.g., `.jpg` → `Images`).
- `README.md`: Documentation of the project including features, usage, and file categorization.
- `requirements.txt`: Python dependencies including `PySide6` and `rich`.
- `examples/`: Optional folder to test and demonstrate the tool.

This structure ensures a **clean separation between code, configuration, and examples**, making it easier for contributors to understand and extend the project.

## ⚡ Installation

Ensure you have **Python 3.8+** installed.

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd File-Organizer

# Install dependencies
pip install -r requirements.txt
```

## 🚀 CLI Mode Usage

To use `CLI` mode, run `python file_organizer.py <folder_path> [options]`
If folder path contains white spaces, enclose the folder path in double quote (**" "**) or single quote (**' '**)

| Options                   | Description                                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `-u` or `--unique`        | Move only unique copy of file into separate folder                                                   |
| `-e` or `--extension`     | Organize files based on their type (extension) into corresponding folders                            |
| `-c` or `--creation`      | Organize files based on their year of creation. Folder will be named after the year (e.g 2015, 2016) |
| `-f` or `--flatten`       | Flatten all folders i.e move all the files from sub folders to parent folder                         |
| `-r` or `--remove_folder` | Used with -f, removes the empty folder left behind after flattening the folders                      |

## 🖥️ GUI Mode Usage

- To use GUI Mode, run `python gui_tool.py`
- After the GUI interface starts, select the folder by clicking on `Select folder`
- Choose mode by clicking on the radio buttons. Available modes are:
  - `Separate Unique Copies` same as `-u`
  - `Organize by Type` same as `-e`
  - `Organize by Date` same as `-c`
  - `Flatten Folder` same as `-f`
- If you choose `Flatten Folder`, a checkbox will appear namely `Remove Folder`. Check it to remove the empty folder left after moving all the files to parent folder (same as `-r`).
- Click `Run`
- Wait for some time, until the status bar shows success
- Summary will be displayed in the left panel

## 🧪 Testing the Project

- ./example folder contains few dummy files to test the project
- You can also download additional dummy sample files to test the project from this [Google Drive link](https://drive.google.com/drive/folders/1mUHtVOSLhIhBf4y-l1m4EmE7lPZLMokm?usp=drive_link)
- **CLI**:
  ```bash
  python file_organizer.py ./examples -e
  ```
- **GUI**:

  ```bash
  python gui_tool.py
  ```

## 🛠️ Technologies Used

- 🐍 Python 3.8+
- 🎨 PySide6 (for GUI/User Interface)
- 📊 Rich (CLI progress bars & styling)
- 📂 OS / Shutil / JSON (For core operations)

## 🙌 Acknowledgements

This project was inspired and guided by:

- **CS50’s Introduction to Computer Science** – for encouraging me to build practical, problem-solving projects.
- **Python Community** – for providing excellent libraries and documentation.
- http://examplefiles.com/ - for providing free dummy files for the testing of the project

> A big thanks to everyone who contributed or will contribute, directly or indirectly, to future updates.
