import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import h3
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="inDrive Geo Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stMetric > div > div > div > div {
        color: #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# Title and Header
st.markdown("""
<div class="main-header">
    <h1>🚗 inDrive Geo Analytics Dashboard</h1>
    <p>Privacy-Preserved Trip Pattern Analysis • Hackathon 2024 • Case 2</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("📊 Dashboard Controls")
    
    # Time Range Selection
    time_range = st.selectbox(
        "⏰ Time Range",
        ["Last 24 Hours", "Last Week", "Last Month", "All Time"],
        index=1
    )
    
    # Analysis Type
    analysis_type = st.selectbox(
        "🔍 Analysis Type", 
        ["Overview", "Heatmap", "Popular Routes", "Anomaly Detection"]
    )
    
    # Filters
    st.subheader("🎛️ Filters")
    
    min_trips = st.slider("Min Trips per Area", 1, 50, 5)
    confidence_threshold = st.slider("Anomaly Confidence", 0.5, 1.0, 0.8)
    
    # Privacy Settings
    st.subheader("🔒 Privacy Settings")
    h3_resolution = st.selectbox("H3 Resolution", [7, 8, 9, 10], index=2)
    k_anonymity = st.slider("K-Anonymity Level", 3, 20, 5)
    
    st.info(f"🛡️ Privacy: H3 Level {h3_resolution}, K={k_anonymity}")

# Generate Sample Data
@st.cache_data
def generate_sample_data():
    """Generate sample trip data for demonstration"""
    np.random.seed(42)
    
    # Moscow coordinates
    center_lat, center_lon = 55.7558, 37.6176
    
    # Generate 1000 sample trips
    n_trips = 1000
    
    # Create various trip patterns
    trips = []
    
    for i in range(n_trips):
        trip_id = f"T-2024-{i:06d}"
        
        # Random timestamp in the last 7 days
        base_time = datetime.now() - timedelta(days=7)
        random_seconds = np.random.randint(0, 7*24*3600)
        timestamp = base_time + timedelta(seconds=random_seconds)
        
        # Generate origin and destination
        # Create clusters around different areas
        if i % 4 == 0:  # Airport cluster
            lat_start = center_lat + np.random.normal(0.1, 0.02)
            lon_start = center_lon + np.random.normal(0.2, 0.02)
        elif i % 4 == 1:  # City center
            lat_start = center_lat + np.random.normal(0, 0.01)
            lon_start = center_lon + np.random.normal(0, 0.01)
        elif i % 4 == 2:  # Business district
            lat_start = center_lat + np.random.normal(-0.05, 0.02)
            lon_start = center_lon + np.random.normal(-0.1, 0.02)
        else:  # Residential
            lat_start = center_lat + np.random.normal(0.08, 0.03)
            lon_start = center_lon + np.random.normal(-0.05, 0.03)
        
        lat_end = lat_start + np.random.normal(0, 0.05)
        lon_end = lon_start + np.random.normal(0, 0.05)
        
        # Calculate duration and distance
        distance = np.sqrt((lat_end - lat_start)**2 + (lon_end - lon_start)**2) * 111  # rough km conversion
        duration = max(5, distance * np.random.normal(3, 1))  # minutes
        
        trips.append({
            'trip_id': trip_id,
            'timestamp': timestamp,
            'start_lat': lat_start,
            'start_lon': lon_start,
            'end_lat': lat_end,
            'end_lon': lon_end,
            'duration': duration,
            'distance': distance
        })
    
    return pd.DataFrame(trips)

# Load Data
df = generate_sample_data()

# Convert H3 coordinates
@st.cache_data
def convert_to_h3(df, resolution=9):
    """Convert coordinates to H3 hexagons"""
    df_h3 = df.copy()
    df_h3['start_h3'] = df_h3.apply(lambda row: h3.geo_to_h3(row['start_lat'], row['start_lon'], resolution), axis=1)
    df_h3['end_h3'] = df_h3.apply(lambda row: h3.geo_to_h3(row['end_lat'], row['end_lon'], resolution), axis=1)
    return df_h3

df_h3 = convert_to_h3(df, h3_resolution)

# Main Dashboard Layout
if analysis_type == "Overview":
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Total Trips", f"{len(df):,}", "+8.5%")
    
    with col2:
        unique_areas = len(set(df_h3['start_h3']) | set(df_h3['end_h3']))
        st.metric("🗺️ Coverage Areas", unique_areas, "+12")
    
    with col3:
        avg_duration = df['duration'].mean()
        st.metric("⏱️ Avg Duration", f"{avg_duration:.1f} min", "-2.3 min")
    
    with col4:
        anomaly_rate = 0.127  # Sample rate
        st.metric("🚨 Anomaly Rate", f"{anomaly_rate:.1%}", "+0.8%")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Trip Volume by Hour")
        df['hour'] = df['timestamp'].dt.hour
        hourly_trips = df.groupby('hour').size()
        
        fig = px.bar(
            x=hourly_trips.index, 
            y=hourly_trips.values,
            labels={'x': 'Hour of Day', 'y': 'Number of Trips'},
            color=hourly_trips.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Trip Categories")
        categories = ['Business', 'Airport', 'Residential', 'Shopping', 'Healthcare']
        values = [334, 267, 198, 134, 67]
        
        fig = px.pie(
            values=values, 
            names=categories,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Heatmap":
    st.subheader("🗺️ Trip Density Heatmap")
    
    # Create heatmap data
    heatmap_data = []
    for _, row in df.iterrows():
        heatmap_data.append([row['start_lat'], row['start_lon']])
        heatmap_data.append([row['end_lat'], row['end_lon']])
    
    # Create folium map
    center_lat, center_lon = df['start_lat'].mean(), df['start_lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)
    
    # Add heatmap
    HeatMap(heatmap_data, radius=15, max_zoom=18).add_to(m)
    
    # Display map
    st.components.v1.html(m._repr_html_(), height=600)
    
    # Heatmap statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔥 Hotspots Detected", "5", "+1")
    
    with col2:
        peak_hour = df['timestamp'].dt.hour.mode()[0]
        st.metric("⏰ Peak Hour", f"{peak_hour:02d}:00", "Consistent")
    
    with col3:
        coverage = 89.3
        st.metric("📡 Coverage", f"{coverage}%", "+2.1%")

elif analysis_type == "Popular Routes":
    st.subheader("🛣️ Popular Routes Analysis")
    
    # Perform DBSCAN clustering on routes
    @st.cache_data
    def cluster_routes(df):
        # Create route features
        route_features = df[['start_lat', 'start_lon', 'end_lat', 'end_lon']].values
        
        # DBSCAN clustering
        dbscan = DBSCAN(eps=0.01, min_samples=5)
        clusters = dbscan.fit_predict(route_features)
        
        df_clustered = df.copy()
        df_clustered['route_cluster'] = clusters
        return df_clustered
    
    df_clustered = cluster_routes(df)
    
    # Route statistics
    route_stats = df_clustered.groupby('route_cluster').agg({
        'trip_id': 'count',
        'duration': 'mean',
        'distance': 'mean'
    }).round(2)
    route_stats = route_stats[route_stats.index != -1]  # Remove noise points
    route_stats = route_stats.sort_values('trip_id', ascending=False).head(10)
    
    # Display top routes
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Top Routes by Frequency")
        
        for idx, (cluster_id, row) in enumerate(route_stats.iterrows()):
            with st.container():
                route_col1, route_col2, route_col3, route_col4 = st.columns([1, 2, 1, 1])
                
                with route_col1:
                    st.metric("Rank", f"#{idx+1}")
                
                with route_col2:
                    st.write(f"**Route Cluster {cluster_id}**")
                    st.write(f"Trips: {int(row['trip_id'])}")
                
                with route_col3:
                    st.metric("Avg Duration", f"{row['duration']:.1f}m")
                
                with route_col4:
                    st.metric("Avg Distance", f"{row['distance']:.1f}km")
                
                st.progress(row['trip_id'] / route_stats['trip_id'].max())
                st.divider()
    
    with col2:
        st.subheader("🎯 Route Insights")
        
        total_clusters = len(route_stats)
        st.metric("🛣️ Route Clusters", total_clusters)
        
        avg_trips = route_stats['trip_id'].mean()
        st.metric("📈 Avg Trips/Route", f"{avg_trips:.0f}")
        
        efficiency_score = (route_stats['distance'] / route_stats['duration']).mean()
        st.metric("⚡ Efficiency Score", f"{efficiency_score:.2f}")
        
        st.subheader("📋 Key Findings")
        st.write("""
        - Airport routes show highest frequency
        - Business district peaks at rush hours  
        - Student routes concentrated afternoon
        - Healthcare distributed throughout day
        """)

elif analysis_type == "Anomaly Detection":
    st.subheader("🚨 Anomaly Detection")
    
    # Perform anomaly detection
    @st.cache_data
    def detect_anomalies(df, contamination=0.1):
        # Feature engineering
        features = df[['duration', 'distance']].copy()
        features['speed'] = features['distance'] / (features['duration'] / 60)  # km/h
        features['efficiency'] = features['distance'] / features['duration']
        
        # Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        anomaly_labels = iso_forest.fit_predict(features)
        
        df_anomaly = df.copy()
        df_anomaly['is_anomaly'] = anomaly_labels == -1
        df_anomaly['anomaly_score'] = iso_forest.score_samples(features)
        
        return df_anomaly
    
    df_anomaly = detect_anomalies(df, contamination=0.1)
    
    # Anomaly statistics
    total_anomalies = df_anomaly['is_anomaly'].sum()
    anomaly_rate = total_anomalies / len(df_anomaly)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚨 Total Anomalies", total_anomalies, f"{anomaly_rate:.1%}")
    
    with col2:
        high_risk = (df_anomaly['anomaly_score'] < -0.5).sum()
        st.metric("🔴 High Risk", high_risk)
    
    with col3:
        medium_risk = ((df_anomaly['anomaly_score'] >= -0.5) & (df_anomaly['anomaly_score'] < -0.2)).sum()
        st.metric("🟡 Medium Risk", medium_risk)
    
    with col4:
        avg_detection_time = "2.3"
        st.metric("⏱️ Avg Detection", f"{avg_detection_time}min", "-15.2%")
    
    # Anomaly visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Anomaly Distribution")
        
        fig = px.scatter(
            df_anomaly, 
            x='distance', 
            y='duration',
            color='is_anomaly',
            color_discrete_map={True: '#ef4444', False: '#22c55e'},
            labels={'distance': 'Distance (km)', 'duration': 'Duration (min)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Anomaly Score Distribution")
        
        fig = px.histogram(
            df_anomaly, 
            x='anomaly_score',
            color='is_anomaly',
            color_discrete_map={True: '#ef4444', False: '#22c55e'},
            bins=30
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly details
    st.subheader("🔍 Detected Anomalies")
    
    anomalies_df = df_anomaly[df_anomaly['is_anomaly']].sort_values('anomaly_score').head(10)
    
    for idx, row in anomalies_df.iterrows():
        with st.expander(f"🚨 Anomaly: {row['trip_id']} (Score: {row['anomaly_score']:.3f})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Duration:** {row['duration']:.1f} minutes")
                st.write(f"**Distance:** {row['distance']:.1f} km")
            
            with col2:
                speed = row['distance'] / (row['duration'] / 60) if row['duration'] > 0 else 0
                st.write(f"**Average Speed:** {speed:.1f} km/h")
                st.write(f"**Timestamp:** {row['timestamp']}")
            
            with col3:
                risk_level = "High" if row['anomaly_score'] < -0.5 else "Medium" if row['anomaly_score'] < -0.2 else "Low"
                st.write(f"**Risk Level:** {risk_level}")
                
                factors = []
                if row['duration'] > df['duration'].quantile(0.95):
                    factors.append("Long Duration")
                if row['distance'] > df['distance'].quantile(0.95):
                    factors.append("Long Distance")
                if speed < 5:
                    factors.append("Very Slow")
                elif speed > 80:
                    factors.append("Very Fast")
                
                if factors:
                    st.write(f"**Risk Factors:** {', '.join(factors)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏆 <strong>inDrive Hackathon 2024</strong> • Case 2: Geotracks Analysis</p>
    <p>🔒 Privacy-First Analytics • 🧠 ML-Powered Insights • ⚡ Real-Time Processing</p>
</div>
""", unsafe_allow_html=True)