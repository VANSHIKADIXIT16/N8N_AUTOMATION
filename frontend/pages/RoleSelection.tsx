import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Zap,
  Users,
  Briefcase,
  ArrowRight,
  MessageSquare,
  FileText,
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function RoleSelection() {
  const navigate = useNavigate();
  const [selectedRole, setSelectedRole] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    if (!selectedRole) return;

    setIsLoading(true);
    try {
      // Navigate based on selected role
      switch (selectedRole) {
        case "customer-service":
          navigate("/cs-dashboard");
          break;
        case "employee":
          navigate("/employee-dashboard");
          break;
        case "hr":
          navigate("/ats-dashboard");
          break;
        case "complaints":
          navigate("/complaints-dashboard");
          break;
      }
    } finally {
      setIsLoading(false);
    }
  };

  const roles = [
    {
      id: "hr",
      title: "HR / ATS Manager",
      icon: Briefcase,
      description: "Manage job roles, resume parsing, and candidate pipelines",
      features: [
        "Create & Manage Job Roles",
        "Resume Parsing & Scoring",
        "Candidate Shortlisting",
        "Automated Email Responses",
        "ATS Analytics Dashboard",
        "Recruitment Workflow Monitoring",
      ],
      color: "from-green-50 to-green-100",
      borderColor: "border-green-200",
      accentColor: "bg-green-100",
    },
    {
      id: "customer-service",
      title: "Customer & Complaints Support",
      icon: MessageSquare,
      description:
        "Manage support tickets, customer complaints, and AI-assisted responses",
      features: [
        "Ticket & Complaint queue management",
        "AI-suggested response review",
        "Customer satisfaction tracking",
        "SLA monitoring & alerts",
        "Knowledge base management",
        "Real-time performance metrics",
      ],
      color: "from-blue-50 to-blue-100",
      borderColor: "border-blue-200",
      accentColor: "bg-blue-100",
    },
    {
      id: "employee",
      title: "Employee",
      icon: Users,
      description: "View your personal profile, tasks, and company resources",
      features: [
        "Personal profile management",
        "Task list & deadline tracking",
        "Company announcement feed",
        "Internal resource library",
        "Peer communication tools",
        "Performance self-tracking",
      ],
      color: "from-purple-50 to-purple-100",
      borderColor: "border-purple-200",
      accentColor: "bg-purple-100",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6">
      <div className="max-w-5xl w-full space-y-8">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center p-2 bg-blue-100 text-blue-700 rounded-full mb-4">
            <Zap className="w-5 h-5 mr-2 fill-current" />
            <span className="text-sm font-bold tracking-wider uppercase">AI Automation</span>
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">
            Choose Your Workspace
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Select the interface tailored to your specific role and responsibilities.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          {roles.map((role) => {
            const Icon = role.icon;
            const isSelected = selectedRole === role.id;

            return (
              <Card
                key={role.id}
                className={`cursor-pointer transition-all duration-300 border-2 relative overflow-hidden ${
                  isSelected
                    ? `${role.borderColor} shadow-lg scale-105 z-10`
                    : "border-transparent hover:border-slate-200 hover:shadow-md"
                }`}
                onClick={() => setSelectedRole(role.id)}
              >
                <div className={`absolute top-0 right-0 p-3 ${isSelected ? "opacity-100" : "opacity-0"} transition-opacity`}>
                  <div className={`w-6 h-6 rounded-full ${role.accentColor} flex items-center justify-center`}>
                    <Zap className="w-3 h-3 text-blue-600" />
                  </div>
                </div>

                <CardHeader className={`bg-gradient-to-br ${role.color} border-b`}>
                  <div className={`w-12 h-12 rounded-xl ${role.accentColor} flex items-center justify-center mb-2`}>
                    <Icon className="w-6 h-6 text-slate-700" />
                  </div>
                  <CardTitle className="text-xl font-bold">{role.title}</CardTitle>
                  <CardDescription className="text-slate-600 font-medium">
                    {role.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-6">
                  <ul className="space-y-2 mb-6">
                    {role.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start text-sm text-slate-600">
                        <ArrowRight className="w-4 h-4 mr-2 text-slate-400 flex-shrink-0 mt-0.5" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="flex flex-col items-center mt-12 space-y-4">
          <Button
            size="lg"
            className="px-12 py-6 text-lg font-bold rounded-xl shadow-xl hover:shadow-2xl transition-all duration-300"
            disabled={!selectedRole || isLoading}
            onClick={handleContinue}
          >
            {isLoading ? "Loading..." : "Enter Workspace"}
          </Button>
          <p className="text-sm text-slate-400">
            You can switch between workspaces later from your dashboard.
          </p>
        </div>
      </div>
    </div>
  );
}
