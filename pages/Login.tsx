import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Zap, ArrowRight } from "lucide-react";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      // Simulate login - in real app would call API
      if (!email || !password) {
        setError("Please fill in all fields");
        return;
      }

      // Demo: route based on email domain
      if (email.includes("cs") || email.includes("customer")) {
        navigate("/cs-dashboard");
      } else if (email.includes("employee")) {
        navigate("/employee-dashboard");
      } else {
        navigate("/employee-dashboard"); // Default to employee
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-white flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary to-accent p-12 flex-col justify-between">
        <Link to="/" className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-primary" />
          </div>
          <span className="text-2xl font-bold text-white">WorkflowAI</span>
        </Link>

        <div>
          <h1 className="text-4xl font-bold text-white mb-6">
            Automate Your Business Workflows
          </h1>
          <p className="text-lg text-white/80">
            Let AI make decisions, n8n execute workflows, and APIs connect
            everything together. Start automating today.
          </p>
        </div>

        <div className="text-white/60 text-sm">
          &copy; 2024 WorkflowAI. All rights reserved.
        </div>
      </div>

      {/* Right side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex lg:hidden items-center gap-2 mb-6">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-secondary">WorkflowAI</span>
            </Link>
            <h2 className="text-3xl font-bold text-secondary mb-2">
              Welcome Back
            </h2>
            <p className="text-slate-600">
              Sign in to access your dashboard and workflows
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-11"
              />
              <p className="text-xs text-slate-500">
                Demo: Use "cs@" or "employee@" for different roles
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-sm font-medium">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-11"
              />
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 rounded" />
                <span className="text-slate-600">Remember me</span>
              </label>
              <a href="#" className="text-primary hover:text-primary/80">
                Forgot password?
              </a>
            </div>

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full h-11 gap-2"
            >
              {isLoading ? "Signing in..." : "Sign In"}
              {!isLoading && <ArrowRight className="w-4 h-4" />}
            </Button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-200" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-slate-600">
                  Or continue with
                </span>
              </div>
            </div>

            <Button variant="outline" className="w-full h-11">
              Continue with Google
            </Button>
          </form>

          <p className="text-center text-slate-600 text-sm mt-8">
            Don't have an account?{" "}
            <Link to="/signup" className="text-primary font-semibold hover:text-primary/80">
              Sign up
            </Link>
          </p>

          <p className="text-center text-slate-500 text-xs mt-6">
            This is a demo application. No real credentials required.
          </p>
        </div>
      </div>
    </div>
  );
}
