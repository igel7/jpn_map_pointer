[日本語はこちら](README_ja.md)

# About This Repository
- An app that displays a map of Japan on offline devices and can show the locations of facilities such as convenience stores.
- While there are many options like Google Maps and GIS applications available online, interactive map apps for offline use are rare, which prompted the creation of this app.
- The main feature is the ability to map custom map layers and address information.

# Technical Innovations
- Utilizes the well-known folium package, which is designed for online environments and therefore typically seeks online files such as JavaScript and CSS files.
- For this reason, the folium package has been directly edited to refer to JavaScript and CSS files downloaded locally.

# Python Code File Structure
- `main.py` is the main controlling code, calling and utilizing `data_loader.py`, `map_creator.py`, and `ui.py`.
- All used data types are stored in the `data` folder. Some information (convenience store addresses) was collected from the internet via web scraping.
- If you want to map other information or add additional layers, you can store them in the `data` folder and adjust the code accordingly.

# Required Packages
- All are listed in `requirements.txt`.

# Supplementary Explanation

## Installing Packages on Offline Devices
- If Python is being used on an offline device within a WinPython environment, launch WinPython Terminal.exe and follow these steps:

### 1. Work on an Online Device
```c
pip download --d ./packages -r requirements.txt
tar cfvz archive.tar.gz ./packages
```
- This downloads all necessary packages into the packages folder, which you can then transfer to an offline device via USB drive, and proceed to the next step.

```c
tar xfvz archive.tar.gz
pip install --no-index --find-links=./packages -r requirements.txt
```
- This completes the installation.
