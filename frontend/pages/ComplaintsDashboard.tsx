import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { auth } from "@/lib/auth";
import { triggerComplaintWorkflow } from "../shared/api";
import { Button } from "@/components/ui/button";

interface Complaint {
  id: number;
  user_name: string;
  email: string;
  description: string;
  department: string;
}

export default function ComplaintsDashboard() {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [triggerLoading, setTriggerLoading] = useState(false);

  const fetchComplaints = async () => {
    setLoading(true);
    try {
      const response = await auth.fetchWithAuth("/complaints/");
      const data = await response.json();
      setComplaints(data);
    } catch (error) {
      console.error("Error fetching complaints:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerWorkflow = async () => {
    setTriggerLoading(true);
    try {
      await triggerComplaintWorkflow({
        issue: "Manual trigger from dashboard",
      });
      alert("Workflow triggered successfully via n8n!");
    } catch (err) {
      console.error(err);
      alert("Error triggering workflow");
    } finally {
      setTriggerLoading(false);
    }
  };

  useEffect(() => {
    fetchComplaints();
  }, []);

  return (
    <div className="container mx-auto p-4 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Complaints Management</h1>
        <Button 
          onClick={handleTriggerWorkflow} 
          disabled={triggerLoading}
          variant="outline"
        >
          {triggerLoading ? "Triggering..." : "Trigger Manual Workflow"}
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Customer Complaints</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-center py-4">Loading complaints...</p>
          ) : complaints.length === 0 ? (
            <p className="text-center py-4 text-slate-500">No complaints found.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>User Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead>Department</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {complaints.map((c) => (
                  <TableRow key={c.id}>
                    <TableCell className="font-medium">{c.id}</TableCell>
                    <TableCell>{c.user_name}</TableCell>
                    <TableCell>{c.email}</TableCell>
                    <TableCell className="max-w-xs truncate">{c.description}</TableCell>
                    <TableCell>
                      <span className="px-2 py-1 bg-slate-100 rounded text-xs font-semibold">
                        {c.department}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
