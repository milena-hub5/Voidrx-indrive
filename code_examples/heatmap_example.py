"""
Heatmap Generation Example
inDrive Hackathon 2024 - Case 2

This module demonstrates how to create interactive heatmaps using Folium
with H3-aggregated trip data for privacy-preserved visualization.
"""

import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, HeatMapWithTime
import h3
from typing import List, Tuple, Optional
from datetime import datetime, timedelta

def create_trip_heatmap(
    df: pd.DataFrame,
    center_coords: Tuple[float, float] = (55.7558, 37.6176),
    zoom_start: int = 11,
    radius: int = 15,
    max_zoom: int = 18,
    gradient: Optional[dict] = None
) -> folium.Map:
    """
    Create an interactive heatmap from trip data
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'lat' and 'lon' columns
    center_coords : tuple
        (latitude, longitude) for map center
    zoom_start : int
        Initial zoom level
    radius : int
        Heatmap point radius
    max_zoom : int
        Maximum zoom level
    gradient : dict
        Custom color gradient for heatmap
        
    Returns:
    --------
    folium.Map
        Interactive map with heatmap layer
    """
    
    # Create base map
    m = folium.Map(
        location=center_coords,
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    
    # Prepare heatmap data
    heat_data = [[row['lat'], row['lon']] for idx, row in df.iterrows()]
    
    # Default gradient (green theme for inDrive)
    if gradient is None:
        gradient = {
            0.0: '#22c55e',  # Green
            0.3: '#16a34a',  # Dark green
            0.6: '#facc15',  # Yellow
            1.0: '#ef4444'   # Red
        }
    
    # Add heatmap layer
    HeatMap(
        heat_data,
        radius=radius,
        max_zoom=max_zoom,
        gradient=gradient
    ).add_to(m)
    
    # Add map controls
    folium.LayerControl().add_to(m)
    
    return m

def create_temporal_heatmap(
    df: pd.DataFrame,
    time_column: str = 'timestamp',
    time_format: str = '%Y-%m-%d %H:00:00',
    center_coords: Tuple[float, float] = (55.7558, 37.6176)
) -> folium.Map:
    """
    Create a time-animated heatmap
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with coordinates and timestamp
    time_column : str
        Name of timestamp column
    time_format : str
        Time aggregation format
    center_coords : tuple
        Map center coordinates
        
    Returns:
    --------
    folium.Map
        Map with time-animated heatmap
    """
    
    # Prepare temporal data
    df_temp = df.copy()
    df_temp['time_bin'] = pd.to_datetime(df_temp[time_column]).dt.strftime(time_format)
    
    # Group by time bins
    time_bins = sorted(df_temp['time_bin'].unique())
    heat_data = []
    
    for time_bin in time_bins:
        bin_data = df_temp[df_temp['time_bin'] == time_bin]
        heat_points = [[row['lat'], row['lon']] for idx, row in bin_data.iterrows()]
        heat_data.append(heat_points)
    
    # Create base map
    m = folium.Map(location=center_coords, zoom_start=11)
    
    # Add temporal heatmap
    HeatMapWithTime(
        heat_data,
        index=time_bins,
        auto_play=True,
        radius=20,
        max_opacity=0.8
    ).add_to(m)
    
    return m

def create_h3_aggregated_heatmap(
    df: pd.DataFrame,
    h3_resolution: int = 9,
    min_trips: int = 5,
    center_coords: Tuple[float, float] = (55.7558, 37.6176)
) -> folium.Map:
    """
    Create heatmap with H3 hexagonal aggregation for privacy
    
    Parameters:
    -----------
    df : pd.DataFrame
        Trip data with lat/lon coordinates
    h3_resolution : int
        H3 hexagon resolution level
    min_trips : int
        Minimum trips per hexagon (k-anonymity)
    center_coords : tuple
        Map center coordinates
        
    Returns:
    --------
    folium.Map
        Map with H3-aggregated heatmap
    """
    
    # Convert to H3 hexagons
    df_h3 = df.copy()
    df_h3['h3_hex'] = df_h3.apply(
        lambda row: h3.geo_to_h3(row['lat'], row['lon'], h3_resolution),
        axis=1
    )
    
    # Aggregate trips by hexagon
    hex_counts = df_h3['h3_hex'].value_counts()
    
    # Apply k-anonymity filter
    valid_hexes = hex_counts[hex_counts >= min_trips].index
    
    # Create base map
    m = folium.Map(location=center_coords, zoom_start=11)
    
    # Add hexagon markers with trip density
    for hex_id in valid_hexes:
        # Get hexagon center
        hex_center = h3.h3_to_geo(hex_id)
        trip_count = hex_counts[hex_id]
        
        # Color intensity based on trip count
        max_trips = hex_counts.max()
        intensity = trip_count / max_trips
        
        # Color gradient from green to red
        if intensity < 0.3:
            color = '#22c55e'  # Green
        elif intensity < 0.6:
            color = '#facc15'  # Yellow
        else:
            color = '#ef4444'  # Red
        
        # Add circle marker
        folium.CircleMarker(
            location=hex_center,
            radius=5 + (intensity * 15),  # Size based on intensity
            popup=f'H3: {hex_id}<br>Trips: {trip_count}',
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6
        ).add_to(m)
    
    # Add hexagon boundaries (optional)
    for hex_id in list(valid_hexes)[:20]:  # Show first 20 hexagons to avoid clutter
        hex_boundary = h3.h3_to_geo_boundary(hex_id, geo_json=False)
        
        folium.Polygon(
            locations=hex_boundary,
            color='#16a34a',
            weight=2,
            fillOpacity=0.1
        ).add_to(m)
    
    return m

def add_heatmap_controls(folium_map: folium.Map) -> folium.Map:
    """
    Add interactive controls to heatmap
    
    Parameters:
    -----------
    folium_map : folium.Map
        Map object to add controls to
        
    Returns:
    --------
    folium.Map
        Map with added controls
    """
    
    # Add fullscreen plugin
    from folium.plugins import Fullscreen
    Fullscreen().add_to(folium_map)
    
    # Add measure tool
    from folium.plugins import MeasureControl
    MeasureControl().add_to(folium_map)
    
    # Add minimap
    from folium.plugins import MiniMap
    minimap = MiniMap(toggle_display=True)
    folium_map.add_child(minimap)
    
    # Add layer control
    folium.LayerControl().add_to(folium_map)
    
    return folium_map

# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    
    # Moscow center coordinates
    center_lat, center_lon = 55.7558, 37.6176
    
    # Generate sample trips
    n_trips = 1000
    sample_data = []
    
    for i in range(n_trips):
        # Create clusters around different areas
        if i % 4 == 0:  # Airport
            lat = center_lat + np.random.normal(0.1, 0.02)
            lon = center_lon + np.random.normal(0.2, 0.02)
        elif i % 4 == 1:  # City center
            lat = center_lat + np.random.normal(0, 0.01)
            lon = center_lon + np.random.normal(0, 0.01)
        elif i % 4 == 2:  # Business district
            lat = center_lat + np.random.normal(-0.05, 0.02)
            lon = center_lon + np.random.normal(-0.1, 0.02)
        else:  # Residential
            lat = center_lat + np.random.normal(0.08, 0.03)
            lon = center_lon + np.random.normal(-0.05, 0.03)
        
        sample_data.append({
            'lat': lat,
            'lon': lon,
            'timestamp': datetime.now() - timedelta(hours=np.random.randint(0, 168))
        })
    
    df_sample = pd.DataFrame(sample_data)
    
    # Create different types of heatmaps
    print("Creating basic heatmap...")
    basic_map = create_trip_heatmap(df_sample)
    basic_map.save("basic_heatmap.html")
    
    print("Creating H3-aggregated heatmap...")
    h3_map = create_h3_aggregated_heatmap(df_sample, h3_resolution=9, min_trips=5)
    h3_map = add_heatmap_controls(h3_map)
    h3_map.save("h3_heatmap.html")
    
    print("Creating temporal heatmap...")
    temporal_map = create_temporal_heatmap(df_sample)
    temporal_map.save("temporal_heatmap.html")
    
    print("Heatmap examples created successfully!")
    print("Files saved: basic_heatmap.html, h3_heatmap.html, temporal_heatmap.html")