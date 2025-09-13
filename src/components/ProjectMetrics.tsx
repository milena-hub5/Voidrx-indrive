import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { DatabaseIcon, ShieldCheckIcon, BrainCircuitIcon, MapIcon } from "lucide-react";

const ProjectMetrics = () => {
  const metrics = [
    {
      title: "Data Coverage",
      value: "89.3%",
      description: "City area coverage",
      icon: DatabaseIcon,
      color: "text-chart-1",
      progress: 89
    },
    {
      title: "Privacy Score",
      value: "A+",
      description: "K-anonymity compliance",
      icon: ShieldCheckIcon,
      color: "text-success",
      progress: 98
    },
    {
      title: "ML Accuracy",
      value: "94.7%",
      description: "Anomaly detection",
      icon: BrainCircuitIcon,
      color: "text-chart-3",
      progress: 95
    },
    {
      title: "H3 Resolution",
      value: "Level 9",
      description: "Spatial aggregation",
      icon: MapIcon,
      color: "text-chart-4",
      progress: 100
    }
  ];

  const techStack = [
    { name: "Python 3.9+", category: "Runtime" },
    { name: "Pandas", category: "Data Processing" },
    { name: "Scikit-learn", category: "Machine Learning" },
    { name: "H3", category: "Geospatial" },
    { name: "Folium", category: "Visualization" },
    { name: "Streamlit", category: "Dashboard" }
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Project Metrics</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Key Metrics */}
        <div className="space-y-4">
          {metrics.map((metric, index) => {
            const Icon = metric.icon;
            return (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Icon className={`h-4 w-4 ${metric.color}`} />
                    <span className="text-sm font-medium">{metric.title}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-primary">{metric.value}</div>
                    <div className="text-xs text-muted-foreground">{metric.description}</div>
                  </div>
                </div>
                <Progress value={metric.progress} className="h-1" />
              </div>
            );
          })}
        </div>

        {/* Tech Stack */}
        <div className="space-y-3">
          <h4 className="font-semibold text-sm">Technology Stack</h4>
          <div className="grid grid-cols-2 gap-2">
            {techStack.map((tech, index) => (
              <div key={index} className="flex flex-col space-y-1">
                <Badge variant="outline" className="text-xs justify-start">
                  {tech.name}
                </Badge>
                <span className="text-xs text-muted-foreground px-2">{tech.category}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-4 text-center pt-2 border-t">
          <div>
            <div className="text-lg font-bold text-primary">12.8K</div>
            <div className="text-xs text-muted-foreground">Trips Analyzed</div>
          </div>
          <div>
            <div className="text-lg font-bold text-primary">127</div>
            <div className="text-xs text-muted-foreground">Anomalies Found</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export { ProjectMetrics };