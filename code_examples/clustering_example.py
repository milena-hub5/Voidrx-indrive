"""
Route Clustering Example
inDrive Hackathon 2024 - Case 2

This module demonstrates DBSCAN and HDBSCAN clustering algorithms
for identifying popular route patterns in trip data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import hdbscan
from typing import Tuple, List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

def prepare_route_features(df: pd.DataFrame) -> np.ndarray:
    """
    Prepare features for route clustering
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with trip data including start/end coordinates
        
    Returns:
    --------
    np.ndarray
        Feature matrix for clustering
    """
    
    # Calculate route features
    features_df = df.copy()
    
    # Basic route vectors
    features_df['lat_delta'] = features_df['end_lat'] - features_df['start_lat']
    features_df['lon_delta'] = features_df['end_lon'] - features_df['start_lon']
    
    # Distance and bearing
    features_df['distance'] = np.sqrt(
        features_df['lat_delta']**2 + features_df['lon_delta']**2
    )
    features_df['bearing'] = np.arctan2(
        features_df['lon_delta'], features_df['lat_delta']
    )
    
    # Midpoint coordinates
    features_df['mid_lat'] = (features_df['start_lat'] + features_df['end_lat']) / 2
    features_df['mid_lon'] = (features_df['start_lon'] + features_df['end_lon']) / 2
    
    # Select features for clustering
    feature_columns = [
        'start_lat', 'start_lon', 'end_lat', 'end_lon',
        'lat_delta', 'lon_delta', 'distance', 'bearing',
        'mid_lat', 'mid_lon'
    ]
    
    return features_df[feature_columns].values

def dbscan_clustering(
    features: np.ndarray,
    eps: float = 0.01,
    min_samples: int = 10,
    standardize: bool = True
) -> Tuple[np.ndarray, Dict]:
    """
    Perform DBSCAN clustering on route features
    
    Parameters:
    -----------
    features : np.ndarray
        Feature matrix
    eps : float
        Maximum distance between points in a cluster
    min_samples : int
        Minimum points required to form a cluster
    standardize : bool
        Whether to standardize features before clustering
        
    Returns:
    --------
    tuple
        (cluster_labels, clustering_metrics)
    """
    
    print(f"Running DBSCAN clustering (eps={eps}, min_samples={min_samples})")
    
    # Standardize features if requested
    if standardize:
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
    else:
        features_scaled = features
    
    # Perform clustering
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(features_scaled)
    
    # Calculate metrics
    n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    n_noise = list(cluster_labels).count(-1)
    
    metrics = {
        'n_clusters': n_clusters,
        'n_noise_points': n_noise,
        'noise_ratio': n_noise / len(cluster_labels) if len(cluster_labels) > 0 else 0
    }
    
    # Calculate silhouette score if there are clusters
    if n_clusters > 1:
        # Remove noise points for silhouette calculation
        non_noise_mask = cluster_labels != -1
        if non_noise_mask.sum() > 1:
            silhouette_avg = silhouette_score(
                features_scaled[non_noise_mask], 
                cluster_labels[non_noise_mask]
            )
            metrics['silhouette_score'] = silhouette_avg
        else:
            metrics['silhouette_score'] = None
    else:
        metrics['silhouette_score'] = None
    
    print(f"Found {n_clusters} clusters with {n_noise} noise points")
    if metrics['silhouette_score']:
        print(f"Silhouette score: {metrics['silhouette_score']:.3f}")
    
    return cluster_labels, metrics

def hdbscan_clustering(
    features: np.ndarray,
    min_cluster_size: int = 10,
    min_samples: Optional[int] = None,
    standardize: bool = True
) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """
    Perform HDBSCAN clustering on route features
    
    Parameters:
    -----------
    features : np.ndarray
        Feature matrix
    min_cluster_size : int
        Minimum size of clusters
    min_samples : int, optional
        Minimum samples in a neighborhood
    standardize : bool
        Whether to standardize features
        
    Returns:
    --------
    tuple
        (cluster_labels, cluster_probabilities, metrics)
    """
    
    print(f"Running HDBSCAN clustering (min_cluster_size={min_cluster_size})")
    
    # Standardize features if requested
    if standardize:
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
    else:
        features_scaled = features
    
    # Set default min_samples
    if min_samples is None:
        min_samples = min_cluster_size
    
    # Perform clustering
    hdb = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples
    )
    
    cluster_labels = hdb.fit_predict(features_scaled)
    cluster_probs = hdb.probabilities_
    
    # Calculate metrics
    n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    n_noise = list(cluster_labels).count(-1)
    
    metrics = {
        'n_clusters': n_clusters,
        'n_noise_points': n_noise,
        'noise_ratio': n_noise / len(cluster_labels) if len(cluster_labels) > 0 else 0,
        'cluster_persistence': hdb.cluster_persistence_ if hasattr(hdb, 'cluster_persistence_') else None
    }
    
    # Calculate silhouette score
    if n_clusters > 1:
        non_noise_mask = cluster_labels != -1
        if non_noise_mask.sum() > 1:
            silhouette_avg = silhouette_score(
                features_scaled[non_noise_mask], 
                cluster_labels[non_noise_mask]
            )
            metrics['silhouette_score'] = silhouette_avg
    else:
        metrics['silhouette_score'] = None
    
    print(f"Found {n_clusters} clusters with {n_noise} noise points")
    if metrics['silhouette_score']:
        print(f"Silhouette score: {metrics['silhouette_score']:.3f}")
    
    return cluster_labels, cluster_probs, metrics

def analyze_route_clusters(
    df: pd.DataFrame, 
    cluster_labels: np.ndarray,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Analyze and summarize route clusters
    
    Parameters:
    -----------
    df : pd.DataFrame
        Original trip data
    cluster_labels : np.ndarray
        Cluster assignments for each trip
    top_n : int
        Number of top clusters to return
        
    Returns:
    --------
    pd.DataFrame
        Cluster analysis summary
    """
    
    # Add cluster labels to dataframe
    df_clustered = df.copy()
    df_clustered['cluster'] = cluster_labels
    
    # Remove noise points for analysis
    df_clean = df_clustered[df_clustered['cluster'] != -1]
    
    if len(df_clean) == 0:
        print("No valid clusters found")
        return pd.DataFrame()
    
    # Calculate cluster statistics\n    cluster_stats = df_clean.groupby('cluster').agg({\n        'trip_id': 'count',\n        'start_lat': ['mean', 'std'],\n        'start_lon': ['mean', 'std'],\n        'end_lat': ['mean', 'std'],\n        'end_lon': ['mean', 'std']\n    }).round(4)\n    \n    # Flatten column names\n    cluster_stats.columns = ['trip_count', 'start_lat_mean', 'start_lat_std',\n                           'start_lon_mean', 'start_lon_std', 'end_lat_mean', \n                           'end_lat_std', 'end_lon_mean', 'end_lon_std']\n    \n    # Calculate additional metrics\n    cluster_stats['frequency_rank'] = cluster_stats['trip_count'].rank(ascending=False)\n    cluster_stats['trip_percentage'] = (cluster_stats['trip_count'] / len(df_clean)) * 100\n    \n    # Calculate average route characteristics for each cluster\n    for cluster_id in cluster_stats.index:\n        cluster_trips = df_clean[df_clean['cluster'] == cluster_id]\n        \n        # Calculate average distance and bearing\n        if len(cluster_trips) > 0:\n            distances = np.sqrt(\n                (cluster_trips['end_lat'] - cluster_trips['start_lat'])**2 + \n                (cluster_trips['end_lon'] - cluster_trips['start_lon'])**2\n            )\n            cluster_stats.loc[cluster_id, 'avg_distance'] = distances.mean()\n            cluster_stats.loc[cluster_id, 'distance_std'] = distances.std()\n    \n    # Sort by trip count and return top N\n    cluster_summary = cluster_stats.sort_values('trip_count', ascending=False).head(top_n)\n    \n    return cluster_summary\n\ndef visualize_clusters(\n    df: pd.DataFrame, \n    cluster_labels: np.ndarray,\n    max_clusters_to_show: int = 10,\n    figsize: Tuple[int, int] = (15, 10)\n) -> None:\n    \"\"\"\n    Visualize route clusters\n    \n    Parameters:\n    -----------\n    df : pd.DataFrame\n        Trip data with coordinates\n    cluster_labels : np.ndarray\n        Cluster assignments\n    max_clusters_to_show : int\n        Maximum number of clusters to visualize\n    figsize : tuple\n        Figure size for plots\n    \"\"\"\n    \n    # Add cluster labels to dataframe\n    df_viz = df.copy()\n    df_viz['cluster'] = cluster_labels\n    \n    # Create subplots\n    fig, axes = plt.subplots(2, 2, figsize=figsize)\n    \n    # 1. Geographic distribution of clusters\n    unique_clusters = sorted([c for c in df_viz['cluster'].unique() if c != -1])[:max_clusters_to_show]\n    colors = plt.cm.Set3(np.linspace(0, 1, len(unique_clusters)))\n    \n    for i, cluster_id in enumerate(unique_clusters):\n        cluster_data = df_viz[df_viz['cluster'] == cluster_id]\n        axes[0, 0].scatter(\n            cluster_data['start_lon'], cluster_data['start_lat'], \n            c=[colors[i]], label=f'Cluster {cluster_id}', alpha=0.6, s=10\n        )\n    \n    # Plot noise points\n    noise_data = df_viz[df_viz['cluster'] == -1]\n    if len(noise_data) > 0:\n        axes[0, 0].scatter(\n            noise_data['start_lon'], noise_data['start_lat'],\n            c='black', label='Noise', alpha=0.3, s=5\n        )\n    \n    axes[0, 0].set_xlabel('Start Longitude')\n    axes[0, 0].set_ylabel('Start Latitude')\n    axes[0, 0].set_title('Route Clusters - Start Points')\n    axes[0, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n    axes[0, 0].grid(True, alpha=0.3)\n    \n    # 2. Cluster size distribution\n    cluster_counts = df_viz[df_viz['cluster'] != -1]['cluster'].value_counts().sort_index()\n    axes[0, 1].bar(range(len(cluster_counts)), cluster_counts.values)\n    axes[0, 1].set_xlabel('Cluster ID')\n    axes[0, 1].set_ylabel('Number of Trips')\n    axes[0, 1].set_title('Cluster Size Distribution')\n    axes[0, 1].grid(True, alpha=0.3)\n    \n    # 3. Route vectors for top clusters\n    top_clusters = cluster_counts.head(5).index\n    \n    for i, cluster_id in enumerate(top_clusters):\n        cluster_data = df_viz[df_viz['cluster'] == cluster_id].sample(min(50, len(df_viz[df_viz['cluster'] == cluster_id])))\n        \n        for _, row in cluster_data.iterrows():\n            axes[1, 0].arrow(\n                row['start_lon'], row['start_lat'],\n                row['end_lon'] - row['start_lon'], row['end_lat'] - row['start_lat'],\n                head_width=0.001, head_length=0.001, fc=colors[i % len(colors)], \n                ec=colors[i % len(colors)], alpha=0.5, length_includes_head=True\n            )\n    \n    axes[1, 0].set_xlabel('Longitude')\n    axes[1, 0].set_ylabel('Latitude')\n    axes[1, 0].set_title('Route Vectors - Top 5 Clusters')\n    axes[1, 0].grid(True, alpha=0.3)\n    \n    # 4. Cluster quality metrics\n    if len(unique_clusters) > 0:\n        cluster_sizes = [len(df_viz[df_viz['cluster'] == c]) for c in unique_clusters]\n        noise_size = len(df_viz[df_viz['cluster'] == -1])\n        \n        # Pie chart of cluster vs noise\n        sizes = cluster_sizes + ([noise_size] if noise_size > 0 else [])\n        labels = [f'Cluster {c}' for c in unique_clusters] + (['Noise'] if noise_size > 0 else [])\n        \n        axes[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)\n        axes[1, 1].set_title('Clustering Results Distribution')\n    \n    plt.tight_layout()\n    plt.show()\n\n# Example usage\nif __name__ == \"__main__\":\n    # Generate sample route data\n    np.random.seed(42)\n    \n    # Moscow coordinates\n    center_lat, center_lon = 55.7558, 37.6176\n    \n    # Generate sample trips with route patterns\n    n_trips = 500\n    sample_data = []\n    \n    for i in range(n_trips):\n        trip_id = f\"T-{i:04d}\"\n        \n        # Create different route patterns\n        pattern = i % 4\n        \n        if pattern == 0:  # Airport to city center\n            start_lat = center_lat + np.random.normal(0.15, 0.01)  # Airport area\n            start_lon = center_lon + np.random.normal(0.20, 0.01)\n            end_lat = center_lat + np.random.normal(0, 0.005)      # City center\n            end_lon = center_lon + np.random.normal(0, 0.005)\n        elif pattern == 1:  # Business district to residential\n            start_lat = center_lat + np.random.normal(-0.05, 0.01)  # Business\n            start_lon = center_lon + np.random.normal(-0.10, 0.01)\n            end_lat = center_lat + np.random.normal(0.08, 0.02)     # Residential\n            end_lon = center_lon + np.random.normal(-0.05, 0.02)\n        elif pattern == 2:  # Shopping to university\n            start_lat = center_lat + np.random.normal(-0.02, 0.01)  # Shopping\n            start_lon = center_lon + np.random.normal(0.08, 0.01)\n            end_lat = center_lat + np.random.normal(0.05, 0.01)     # University\n            end_lon = center_lon + np.random.normal(-0.12, 0.01)\n        else:  # Random routes (noise)\n            start_lat = center_lat + np.random.normal(0, 0.05)\n            start_lon = center_lon + np.random.normal(0, 0.05)\n            end_lat = center_lat + np.random.normal(0, 0.05)\n            end_lon = center_lon + np.random.normal(0, 0.05)\n        \n        sample_data.append({\n            'trip_id': trip_id,\n            'start_lat': start_lat,\n            'start_lon': start_lon,\n            'end_lat': end_lat,\n            'end_lon': end_lon\n        })\n    \n    df_sample = pd.DataFrame(sample_data)\n    \n    # Prepare features\n    print(\"Preparing route features...\")\n    features = prepare_route_features(df_sample)\n    \n    # Test DBSCAN clustering\n    print(\"\\n=== DBSCAN Clustering ===\")\n    dbscan_labels, dbscan_metrics = dbscan_clustering(features, eps=0.01, min_samples=5)\n    dbscan_summary = analyze_route_clusters(df_sample, dbscan_labels)\n    \n    print(\"\\nDBSCAN Results:\")\n    print(dbscan_summary)\n    \n    # Test HDBSCAN clustering\n    print(\"\\n=== HDBSCAN Clustering ===\")\n    hdbscan_labels, hdbscan_probs, hdbscan_metrics = hdbscan_clustering(features, min_cluster_size=10)\n    hdbscan_summary = analyze_route_clusters(df_sample, hdbscan_labels)\n    \n    print(\"\\nHDBSCAN Results:\")\n    print(hdbscan_summary)\n    \n    # Visualize results\n    print(\"\\nGenerating visualizations...\")\n    print(\"DBSCAN Clustering:\")\n    visualize_clusters(df_sample, dbscan_labels, figsize=(16, 12))\n    \n    print(\"HDBSCAN Clustering:\")\n    visualize_clusters(df_sample, hdbscan_labels, figsize=(16, 12))\n    \n    print(\"\\nClustering analysis complete!\")