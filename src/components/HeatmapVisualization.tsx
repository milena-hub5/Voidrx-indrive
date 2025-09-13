import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapIcon, FilterIcon, DownloadIcon, RefreshCwIcon } from "lucide-react";

const HeatmapVisualization = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState("24h");
  const [selectedRegion, setSelectedRegion] = useState("all");
  const [isLoading, setIsLoading] = useState(false);

  const handleRefresh = () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => setIsLoading(false), 1500);
  };

  // Sample heatmap data points
  const heatmapStats = [
    { label: "Total Trips", value: "12,847", change: "+5.2%" },
    { label: "Peak Hours", value: "7-9 AM, 5-7 PM", change: "Consistent" },
    { label: "Hot Zones", value: "5 Districts", change: "+1 zone" },
    { label: "Coverage", value: "89.3%", change: "+2.1%" }
  ];

  return (
    <div className="space-y-6">
      {/* Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <MapIcon className="h-5 w-5 text-primary" />
                <span>Trip Density Heatmap</span>
              </CardTitle>
              <CardDescription>
                Visualize trip patterns and demand hotspots across the city
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline">
                <FilterIcon className="mr-1 h-3 w-3" />
                H3 Aggregated
              </Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium">Time Range:</label>
              <Select value={selectedTimeRange} onValueChange={setSelectedTimeRange}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1h">Last Hour</SelectItem>
                  <SelectItem value="6h">Last 6 Hours</SelectItem>
                  <SelectItem value="24h">Last 24 Hours</SelectItem>
                  <SelectItem value="7d">Last Week</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium">Region:</label>
              <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                <SelectTrigger className="w-40">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Regions</SelectItem>
                  <SelectItem value="central">Central District</SelectItem>
                  <SelectItem value="north">Northern Zone</SelectItem>
                  <SelectItem value="south">Southern Zone</SelectItem>
                  <SelectItem value="airport">Airport Area</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center space-x-2 ml-auto">
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={isLoading}
              >
                {isLoading ? (
                  <RefreshCwIcon className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <RefreshCwIcon className="mr-2 h-4 w-4" />
                )}
                Refresh
              </Button>
              <Button variant="outline" size="sm">
                <DownloadIcon className="mr-2 h-4 w-4" />
                Export
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Heatmap Visualization */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">Interactive Heatmap</CardTitle>
            <CardDescription>
              Trip density visualization with H3 hexagonal binning
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative aspect-[4/3] rounded-lg border bg-gradient-data p-8">
              {/* Simulated heatmap visualization */}
              <div className="absolute inset-4 flex items-center justify-center rounded-lg border-2 border-dashed border-white/30">
                <div className="text-center text-white/80">
                  <MapIcon className="mx-auto mb-4 h-12 w-12" />
                  <h3 className="mb-2 font-semibold">Interactive Folium Map</h3>
                  <p className="text-sm">
                    Real heatmap would render here using Folium/Leaflet
                  </p>
                  <div className="mt-4 flex justify-center space-x-2">
                    <div className="h-2 w-2 rounded-full bg-chart-2"></div>
                    <div className="h-2 w-2 rounded-full bg-chart-4"></div>
                    <div className="h-2 w-2 rounded-full bg-chart-1"></div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Heatmap Legend */}
            <div className="mt-4 flex items-center justify-between rounded-lg border bg-muted/50 p-3">
              <span className="text-sm font-medium">Trip Density:</span>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1">
                  <div className="h-3 w-3 rounded-full bg-chart-1"></div>
                  <span className="text-xs">High</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="h-3 w-3 rounded-full bg-chart-4"></div>
                  <span className="text-xs">Medium</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="h-3 w-3 rounded-full bg-chart-2"></div>
                  <span className="text-xs">Low</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Heatmap Statistics */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Heatmap Insights</CardTitle>
            <CardDescription>
              Key metrics and trends from the current view
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {heatmapStats.map((stat, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg border bg-card/50">
                <div>
                  <p className="text-sm font-medium">{stat.label}</p>
                  <p className="text-lg font-bold text-primary">{stat.value}</p>
                </div>
                <Badge variant={stat.change.includes("+") ? "default" : "secondary"}>
                  {stat.change}
                </Badge>
              </div>
            ))}

            <div className="mt-6 space-y-3">
              <h4 className="font-semibold text-sm">Top Hotspots</h4>
              <div className="space-y-2">
                {[
                  { name: "City Center", trips: 2847, density: "High" },
                  { name: "Airport Terminal", trips: 1923, density: "High" },
                  { name: "Business District", trips: 1654, density: "Medium" },
                  { name: "Shopping Mall", trips: 987, density: "Medium" }
                ].map((hotspot, index) => (
                  <div key={index} className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">{hotspot.name}</span>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="text-xs">
                        {hotspot.trips}
                      </Badge>
                      <Badge 
                        variant={hotspot.density === "High" ? "default" : "secondary"}
                        className="text-xs"
                      >
                        {hotspot.density}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export { HeatmapVisualization };