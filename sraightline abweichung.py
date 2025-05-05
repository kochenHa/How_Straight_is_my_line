import gpxpy
import tkinter as tk
import numpy as np
from tkinter import filedialog
from shapely.geometry import LineString, Point
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import folium

# Visualisierung auf einer OSM-Karte

def visualize_on_osm(points, best_line):
        # Dialog öffnen, um den Speicherpfad auszuwählen
    output_path = filedialog.asksaveasfilename(
        defaultextension=".html",
        filetypes=[("HTML-Dateien", "*.html")],
        title="Speicherort für die Karte auswählen"
    )

    # Abbrechen, falls kein Pfad ausgewählt wurde
    if not output_path:
        print("Speichern abgebrochen.")
        return
    # Mittelpunkt der Karte (erster Punkt)
    center_lat, center_lon = points[0]

    # Erstelle eine Karte mit Folium
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # GPX-Punkte als Marker hinzufügen
    for lat, lon in points:
        folium.CircleMarker(location=[lat, lon], radius=2, color='blue', fill=True).add_to(m)

    # Beste Linie hinzufügen
    line_coords = [(lat, lon) for lon, lat in best_line.coords]  # Shapely nutzt (lon, lat)
    folium.PolyLine(line_coords, color='red', weight=3, opacity=0.8).add_to(m)

    # Karte speichern und anzeigen
    m.save(output_path)
    print(f"Die Karte wurde als '{output_path}' gespeichert.")

# Punkte und Linie visualisieren
def visualize(points, best_line):
    # Punkte extrahieren
    lats, lons = zip(*points)

    # Linie extrahieren
    line_lons, line_lats = zip(*best_line.coords)

    # Plot erstellen
    plt.figure(figsize=(10, 6))
    plt.plot(lons, lats, 'o', label='GPX-Punkte', markersize=3)  # Punkte
    plt.plot(line_lons, line_lats, 'r-', label='Beste Linie', linewidth=2)  # Linie

    # Diagramm beschriften
    plt.title('GPX-Punkte und beste Linie')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_average_deviation(line, points):
    distances = []
    for lat, lon in points:
        p = Point(lon, lat)
        nearest_point = line.interpolate(line.project(p))
        dist = geodesic((lat, lon), (nearest_point.y, nearest_point.x)).meters
        distances.append(dist)
    return sum(distances) / len(distances)

# Lineare Regression zur Bestimmung der besten Linie
def linear_regression(points):
    # Extrahiere die Längen- und Breitengrade
    lons = np.array([lon for lat, lon in points])
    lats = np.array([lat for lat, lon in points])

    # Führe die lineare Regression durch
    A = np.vstack([lons, np.ones(len(lons))]).T  # Design-Matrix
    m, c = np.linalg.lstsq(A, lats, rcond=None)[0]  # Steigung (m) und Achsenabschnitt (c)

    # Erstelle die Linie basierend auf der Regression
    start_lon, end_lon = lons[0], lons[-1]
    start_lat, end_lat = m * start_lon + c, m * end_lon + c
    return LineString([(start_lon, start_lat), (end_lon, end_lat)])

# Eingabedialog für Dateiauswahl
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("GPX-Dateien", "*.gpx")])

if not file_path:
    print("Keine Datei ausgewählt.")
    exit()

# GPX-Datei laden und parsen
with open(file_path, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Alle Punkte sammeln
points = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points.append((point.latitude, point.longitude))

if len(points) < 2:
    print("Zu wenige Punkte im GPX-Track.")
    exit()

# Gerade von Start- zu Endpunkt
start = points[0]
end = points[-1]
line = LineString([start[::-1], end[::-1]])  # Shapely nutzt (lon, lat)

# Abweichungen berechnen
distances = []
for lat, lon in points:
    p = Point(lon, lat)
    nearest_point = line.interpolate(line.project(p))
    dist = geodesic((lat, lon), (nearest_point.y, nearest_point.x)).meters
    distances.append(dist)

# Ergebnisse
max_dist = max(distances)
avg_dist = sum(distances) / len(distances)

# Optimierung: Finde die Linie mit der geringsten durchschnittlichen Abweichung
best_line = None
min_avg_deviation = float('inf')

# Finde die Linie mit der geringsten durchschnittlichen Abweichung
best_line = linear_regression(points)

# Berechne die durchschnittliche Abweichung für die Linie
min_avg_deviation = calculate_average_deviation(best_line, points)




print(f"Anzahl Punkte: {len(points)}")
print(f"Maximale Abweichung: {max_dist:.2f} m")
print(f"Durchschnittliche Abweichung: {avg_dist:.2f} m")
print(f"Beste Linie: Startpunkt {best_line.coords[0]}, Endpunkt {best_line.coords[1]}")
print(f"Minimale durchschnittliche Abweichung: {min_avg_deviation:.2f} m")

visualize(points, best_line)
# Aufruf der Visualisierung
visualize_on_osm(points, best_line)