import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { TrendingUpIcon, RouteIcon, BarChartIcon, TimerIcon } from "lucide-react";

const PopularRoutes = () => {
  const [selectedMetric, setSelectedMetric] = useState("frequency");
  const [timeRange, setTimeRange] = useState("7d");

  // Sample route data
  const routes = [
    {
      id: 1,
      from: "City Center",
      to: "Airport Terminal",
      trips: 1247,
      frequency: 95,
      avgDuration: "24 min",
      avgDistance: "18.5 km",
      peakHours: "6-9 AM",
      efficiency: "High",
      category: "Business"
    },
    {
      id: 2,
      from: "Business District",
      to: "Residential Area A",
      trips: 892,
      frequency: 78,
      avgDuration: "16 min",
      avgDistance: "12.3 km",
      peakHours: "5-7 PM",
      efficiency: "Medium",
      category: "Commuter"
    },
    {
      id: 3,
      from: "Shopping Mall",
      to: "University",
      trips: 634,
      frequency: 65,
      avgDuration: "19 min",
      avgDistance: "14.7 km",
      peakHours: "2-4 PM",
      efficiency: "High",
      category: "Student"
    },
    {
      id: 4,
      from: "Train Station",
      to: "Hotel District",
      trips: 543,
      frequency: 52,
      avgDuration: "13 min",
      avgDistance: "8.9 km",
      peakHours: "All Day",
      efficiency: "Very High",
      category: "Tourism"
    },
    {
      id: 5,
      from: "Hospital Complex",
      to: "Pharmacy District",
      trips: 312,
      frequency: 38,
      avgDuration: "11 min",
      avgDistance: "6.2 km",
      peakHours: "9-11 AM",
      efficiency: "Medium",
      category: "Healthcare"
    }
  ];

  const routeCategories = [
    { category: "Business", count: 34, color: "bg-chart-1" },
    { category: "Commuter", count: 28, color: "bg-chart-2" },
    { category: "Tourism", count: 19, color: "bg-chart-3" },
    { category: "Student", count: 12, color: "bg-chart-4" },
    { category: "Healthcare", count: 7, color: "bg-chart-5" }
  ];

  return (
    <div className="space-y-6">
      {/* Controls and Overview */}
      <div className="grid gap-6 lg:grid-cols-4">
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUpIcon className="h-5 w-5 text-primary" />
              <span>Popular Routes Analysis</span>
            </CardTitle>
            <CardDescription>
              Most frequently used routes based on DBSCAN clustering analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium">Metric:</label>
                <Select value={selectedMetric} onValueChange={setSelectedMetric}>
                  <SelectTrigger className="w-36">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="frequency">Frequency</SelectItem>
                    <SelectItem value="trips">Trip Count</SelectItem>
                    <SelectItem value="duration">Avg Duration</SelectItem>
                    <SelectItem value="efficiency">Efficiency</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium">Period:</label>
                <Select value={timeRange} onValueChange={setTimeRange}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="24h">Last 24h</SelectItem>
                    <SelectItem value="7d">Last Week</SelectItem>
                    <SelectItem value="30d">Last Month</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Route Categories</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {routeCategories.map((cat, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className={`h-3 w-3 rounded-full ${cat.color}`}></div>
                <span className="text-sm flex-1">{cat.category}</span>
                <Badge variant="outline" className="text-xs">{cat.count}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Routes List */}
      <div className="grid gap-4">
        {routes.map((route, index) => (
          <Card key={route.id} className="transition-all hover:shadow-md">
            <CardContent className="pt-6">
              <div className="grid gap-4 lg:grid-cols-12 lg:items-center">
                {/* Route Info */}
                <div className="lg:col-span-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <Badge variant="outline" className="text-xs">
                      #{index + 1}
                    </Badge>
                    <Badge variant={route.category === "Business" ? "default" : "secondary"}>
                      {route.category}
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RouteIcon className="h-4 w-4 text-muted-foreground" />
                    <span className="font-medium text-sm">{route.from}</span>
                    <span className="text-muted-foreground">→</span>
                    <span className="font-medium text-sm">{route.to}</span>
                  </div>
                </div>

                {/* Frequency Bar */}
                <div className="lg:col-span-3">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Frequency</span>
                      <span className="text-sm font-medium">{route.frequency}%</span>
                    </div>
                    <Progress value={route.frequency} className="h-2" />
                  </div>
                </div>

                {/* Stats */}
                <div className="lg:col-span-3 grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-lg font-bold text-primary">{route.trips}</div>
                    <div className="text-xs text-muted-foreground">Total Trips</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-primary">{route.avgDuration}</div>
                    <div className="text-xs text-muted-foreground">Avg Duration</div>
                  </div>
                </div>

                {/* Additional Info */}
                <div className="lg:col-span-2 space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Distance:</span>
                    <span className="font-medium">{route.avgDistance}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Peak:</span>
                    <Badge variant="outline" className="text-xs">
                      <TimerIcon className="mr-1 h-3 w-3" />
                      {route.peakHours}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Efficiency:</span>
                    <Badge 
                      variant={route.efficiency === "High" || route.efficiency === "Very High" ? "default" : "secondary"}
                      className="text-xs"
                    >
                      {route.efficiency}
                    </Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Route Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChartIcon className="h-5 w-5 text-primary" />
            <span>Route Insights & Recommendations</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <h4 className="font-semibold text-sm">Key Findings</h4>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• Airport routes show highest consistency (95% frequency)</li>
                <li>• Business district commutes peak during rush hours</li>
                <li>• Student routes concentrated in afternoon hours</li>
                <li>• Healthcare routes distributed throughout the day</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold text-sm">Optimization Opportunities</h4>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• Increase driver allocation on airport route</li>
                <li>• Implement dynamic pricing for peak hours</li>
                <li>• Pre-position drivers near popular origins</li>
                <li>• Consider express routes for high-frequency corridors</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export { PopularRoutes };