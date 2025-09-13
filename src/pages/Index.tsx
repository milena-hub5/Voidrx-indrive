import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MapIcon, TrendingUpIcon, AlertTriangleIcon, BarChartIcon, GithubIcon, FileTextIcon } from "lucide-react";
import { HeatmapVisualization } from "@/components/HeatmapVisualization";
import { PopularRoutes } from "@/components/PopularRoutes";
import { AnomalyDetection } from "@/components/AnomalyDetection";
import { ProjectMetrics } from "@/components/ProjectMetrics";

const Index = () => {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-primary">
                <MapIcon className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">inDrive Geo Analytics</h1>
                <p className="text-sm text-muted-foreground">
                  Privacy-Preserved Trip Pattern Analysis
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary">
                <GithubIcon className="mr-1 h-3 w-3" />
                Hackathon Project
              </Badge>
              <Badge variant="outline">Case 2</Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview" className="flex items-center space-x-2">
              <BarChartIcon className="h-4 w-4" />
              <span>Overview</span>
            </TabsTrigger>
            <TabsTrigger value="heatmap" className="flex items-center space-x-2">
              <MapIcon className="h-4 w-4" />
              <span>Heatmap</span>
            </TabsTrigger>
            <TabsTrigger value="routes" className="flex items-center space-x-2">
              <TrendingUpIcon className="h-4 w-4" />
              <span>Popular Routes</span>
            </TabsTrigger>
            <TabsTrigger value="anomalies" className="flex items-center space-x-2">
              <AlertTriangleIcon className="h-4 w-4" />
              <span>Anomalies</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {/* Project Overview Card */}
              <Card className="md:col-span-2 lg:col-span-2">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <FileTextIcon className="h-5 w-5 text-primary" />
                    <span>Project Overview</span>
                  </CardTitle>
                  <CardDescription>
                    Comprehensive analysis of anonymized trip geotrack data
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="space-y-2">
                      <h4 className="font-semibold text-sm">Key Features</h4>
                      <ul className="space-y-1 text-sm text-muted-foreground">
                        <li>• H3 Geospatial Aggregation</li>
                        <li>• DBSCAN/HDBSCAN Clustering</li>
                        <li>• Isolation Forest Anomaly Detection</li>
                        <li>• Privacy-Preserved Analytics</li>
                      </ul>
                    </div>
                    <div className="space-y-2">
                      <h4 className="font-semibold text-sm">Business Value</h4>
                      <ul className="space-y-1 text-sm text-muted-foreground">
                        <li>• Demand Pattern Identification</li>
                        <li>• Driver Allocation Optimization</li>
                        <li>• Safety & Security Enhancement</li>
                        <li>• Route Efficiency Insights</li>
                      </ul>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 pt-2">
                    <Badge variant="secondary">Python</Badge>
                    <Badge variant="secondary">Streamlit</Badge>
                    <Badge variant="secondary">Folium</Badge>
                    <Badge variant="secondary">Scikit-learn</Badge>
                    <Badge variant="secondary">H3</Badge>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Stats */}
              <ProjectMetrics />
            </div>

            {/* Quick Access Cards */}
            <div className="grid gap-4 md:grid-cols-3">
              <Card className="group cursor-pointer transition-all hover:shadow-lg" onClick={() => setActiveTab("heatmap")}>
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center justify-between text-base">
                    <span>Demand Heatmap</span>
                    <MapIcon className="h-4 w-4 text-chart-1 transition-transform group-hover:scale-110" />
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Visualize trip density and demand patterns across the city
                  </p>
                  <Button variant="outline" size="sm" className="mt-3">
                    View Heatmap →
                  </Button>
                </CardContent>
              </Card>

              <Card className="group cursor-pointer transition-all hover:shadow-lg" onClick={() => setActiveTab("routes")}>
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center justify-between text-base">
                    <span>Popular Routes</span>
                    <TrendingUpIcon className="h-4 w-4 text-chart-2 transition-transform group-hover:scale-110" />
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Discover frequently used routes and passenger corridors
                  </p>
                  <Button variant="outline" size="sm" className="mt-3">
                    Explore Routes →
                  </Button>
                </CardContent>
              </Card>

              <Card className="group cursor-pointer transition-all hover:shadow-lg" onClick={() => setActiveTab("anomalies")}>
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center justify-between text-base">
                    <span>Anomaly Detection</span>
                    <AlertTriangleIcon className="h-4 w-4 text-chart-3 transition-transform group-hover:scale-110" />
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Identify unusual patterns for safety and operational insights
                  </p>
                  <Button variant="outline" size="sm" className="mt-3">
                    View Anomalies →
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="heatmap">
            <HeatmapVisualization />
          </TabsContent>

          <TabsContent value="routes">
            <PopularRoutes />
          </TabsContent>

          <TabsContent value="anomalies">
            <AnomalyDetection />
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t bg-muted/30 mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <p>inDrive Hackathon 2024 • Case 2: Geotracks Analysis</p>
            <p>Privacy-First • ML-Powered • Real-Time Insights</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;