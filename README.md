# Straight Line Deviation Analysis

This Python script analyzes GPX tracks to calculate the straight line with the least average deviation from the given points. It provides both a visual representation of the GPX points and the best-fit line using matplotlib and an interactive map visualization using Folium.

## Features
- **GPX File Parsing**: Load and parse GPX files to extract track points.
- **Linear Regression**: Calculate the best-fit line using linear regression.
- **Deviation Analysis**: Compute the maximum and average deviation of points from the line.
- **Visualization**:
  - Static visualization using `matplotlib`.
  - Interactive map visualization using `Folium` with OpenStreetMap.

## Requirements
The script requires the following Python libraries:
- `gpxpy`
- `numpy`
- `shapely`
- `geopy`
- `matplotlib`
- `folium`
- `tkinter` (built-in for file dialogs)

You can install the required libraries using pip:
```bash
pip install gpxpy numpy shapely geopy matplotlib folium
