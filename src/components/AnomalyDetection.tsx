import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AlertTriangleIcon, ShieldIcon, ClockIcon, MapPinIcon, TrendingUpIcon } from "lucide-react";

const AnomalyDetection = () => {
  const [selectedSeverity, setSelectedSeverity] = useState("all");
  const [selectedType, setSelectedType] = useState("all");

  // Sample anomaly data
  const anomalies = [
    {
      id: 1,
      type: "Unusual Route",
      severity: "High",
      description: "Trip took significantly longer detour than optimal route",
      timestamp: "2024-01-15 14:23:45",
      location: "District 5, Zone A",
      tripId: "T-2024-001247",
      duration: "47 min",
      expectedDuration: "18 min",
      distance: "28.5 km",
      expectedDistance: "12.3 km",
      confidence: 0.94,
      riskFactors: ["Unusual Route", "Extended Duration", "Remote Area"]
    },
    {
      id: 2,
      type: "Speed Anomaly",
      severity: "Medium",
      description: "Vehicle speed patterns inconsistent with traffic conditions",
      timestamp: "2024-01-15 12:15:22",
      location: "Highway Section B2",
      tripId: "T-2024-001198",
      duration: "25 min",
      expectedDuration: "22 min",
      distance: "35.2 km",
      expectedDistance: "33.1 km",
      confidence: 0.78,
      riskFactors: ["Speed Variation", "Traffic Inconsistency"]
    },
    {
      id: 3,
      type: "Time Anomaly",
      severity: "Low",
      description: "Trip occurred during unusually low-demand period",
      timestamp: "2024-01-15 03:45:12",
      location: "Business District",
      tripId: "T-2024-001089",
      duration: "12 min",
      expectedDuration: "15 min",
      distance: "8.7 km",
      expectedDistance: "9.2 km",
      confidence: 0.65,
      riskFactors: ["Off-Peak Hours", "Business Area"]
    },
    {
      id: 4,
      type: "Geographic Outlier",
      severity: "High",
      description: "Trip endpoint in isolated area with low historical activity",
      timestamp: "2024-01-15 19:34:56",
      location: "Rural Zone R7",
      tripId: "T-2024-001312",
      duration: "38 min",
      expectedDuration: "25 min",
      distance: "42.1 km",
      expectedDistance: "28.4 km",
      confidence: 0.89,
      riskFactors: ["Isolated Destination", "Low Activity Area", "Late Hours"]
    }
  ];

  const anomalyStats = [
    { 
      label: "Total Anomalies", 
      value: "127", 
      change: "+8.5%", 
      icon: AlertTriangleIcon,
      color: "text-chart-2"
    },
    { 
      label: "High Severity", 
      value: "23", 
      change: "+12.1%", 
      icon: ShieldIcon,
      color: "text-destructive"
    },
    { 
      label: "Avg Detection Time", 
      value: "2.3 min", 
      change: "-15.2%", 
      icon: ClockIcon,
      color: "text-success"
    },
    { 
      label: "False Positive Rate", 
      value: "4.2%", 
      change: "-2.1%", 
      icon: TrendingUpIcon,
      color: "text-chart-4"
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "High": return "bg-destructive text-destructive-foreground";
      case "Medium": return "bg-warning text-warning-foreground";
      case "Low": return "bg-muted text-muted-foreground";
      default: return "bg-secondary text-secondary-foreground";
    }
  };

  const filteredAnomalies = anomalies.filter(anomaly => {
    const matchesSeverity = selectedSeverity === "all" || anomaly.severity.toLowerCase() === selectedSeverity;
    const matchesType = selectedType === "all" || anomaly.type.toLowerCase().includes(selectedType);
    return matchesSeverity && matchesType;
  });

  return (
    <div className="space-y-6">
      {/* Controls and Stats */}
      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangleIcon className="h-5 w-5 text-primary" />
              <span>Anomaly Detection</span>
            </CardTitle>
            <CardDescription>
              ML-powered detection using Isolation Forest algorithm
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium">Severity:</label>
                <Select value={selectedSeverity} onValueChange={setSelectedSeverity}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Levels</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="low">Low</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium">Type:</label>
                <Select value={selectedType} onValueChange={setSelectedType}>
                  <SelectTrigger className="w-40">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="route">Route Anomalies</SelectItem>
                    <SelectItem value="speed">Speed Anomalies</SelectItem>
                    <SelectItem value="time">Time Anomalies</SelectItem>
                    <SelectItem value="geographic">Geographic</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Detection Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3 text-center">
              <div className="space-y-1">
                <div className="text-2xl font-bold text-destructive">23</div>
                <div className="text-xs text-muted-foreground">High Risk</div>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-warning">45</div>
                <div className="text-xs text-muted-foreground">Medium Risk</div>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-muted-foreground">59</div>
                <div className="text-xs text-muted-foreground">Low Risk</div>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-success">95.8%</div>
                <div className="text-xs text-muted-foreground">Accuracy</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {anomalyStats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                  </div>
                  <Icon className={`h-8 w-8 ${stat.color}`} />
                </div>
                <div className="mt-2">
                  <Badge variant={stat.change.includes("+") ? "destructive" : "default"}>
                    {stat.change}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Anomaly List */}
      <Card>
        <CardHeader>
          <CardTitle>Detected Anomalies ({filteredAnomalies.length})</CardTitle>
          <CardDescription>
            Recent anomalous patterns detected in trip data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredAnomalies.map((anomaly) => (
              <div key={anomaly.id} className="rounded-lg border p-4 transition-all hover:shadow-md">
                <div className="grid gap-4 lg:grid-cols-12">
                  {/* Main Info */}
                  <div className="lg:col-span-6 space-y-2">
                    <div className="flex items-center space-x-2">
                      <Badge className={getSeverityColor(anomaly.severity)}>
                        {anomaly.severity}
                      </Badge>
                      <Badge variant="outline">{anomaly.type}</Badge>
                      <Badge variant="outline" className="text-xs">
                        ID: {anomaly.tripId}
                      </Badge>
                    </div>
                    <p className="font-medium text-sm">{anomaly.description}</p>
                    <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <ClockIcon className="h-3 w-3" />
                        <span>{anomaly.timestamp}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPinIcon className="h-3 w-3" />
                        <span>{anomaly.location}</span>
                      </div>
                    </div>
                  </div>

                  {/* Metrics */}
                  <div className="lg:col-span-3 grid grid-cols-2 gap-2 text-sm">
                    <div className="space-y-1">
                      <div className="text-muted-foreground">Duration</div>
                      <div className="font-medium">{anomaly.duration}</div>
                      <div className="text-xs text-muted-foreground">
                        Expected: {anomaly.expectedDuration}
                      </div>
                    </div>
                    <div className="space-y-1">
                      <div className="text-muted-foreground">Distance</div>
                      <div className="font-medium">{anomaly.distance}</div>
                      <div className="text-xs text-muted-foreground">
                        Expected: {anomaly.expectedDistance}
                      </div>
                    </div>
                  </div>

                  {/* Risk Factors & Confidence */}
                  <div className="lg:col-span-3 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Confidence</span>
                      <Badge variant="outline">
                        {(anomaly.confidence * 100).toFixed(1)}%
                      </Badge>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-muted-foreground">Risk Factors:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {anomaly.riskFactors.map((factor, idx) => (
                          <Badge key={idx} variant="secondary" className="text-xs">
                            {factor}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Anomaly Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <ShieldIcon className="h-5 w-5 text-primary" />
            <span>Safety & Security Insights</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <h4 className="font-semibold text-sm">Detection Capabilities</h4>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• Route deviation patterns (unexpected detours)</li>
                <li>• Speed anomalies (too fast/slow for conditions)</li>
                <li>• Temporal outliers (unusual timing patterns)</li>
                <li>• Geographic anomalies (isolated destinations)</li>
                <li>• Duration inconsistencies (trip time variations)</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold text-sm">Business Applications</h4>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• Enhanced passenger safety monitoring</li>
                <li>• Driver behavior analysis and training</li>
                <li>• Fraud detection and prevention</li>
                <li>• Route optimization recommendations</li>
                <li>• Emergency response prioritization</li>
              </ul>
            </div>
          </div>
          <div className="mt-4 p-3 rounded-lg bg-muted/50 border">
            <p className="text-sm text-muted-foreground">
              <strong>Privacy Note:</strong> All anomaly detection is performed on aggregated, anonymized data using H3 spatial indexing. 
              Individual trip details are protected through k-anonymity measures and cannot be traced back to specific users.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export { AnomalyDetection };