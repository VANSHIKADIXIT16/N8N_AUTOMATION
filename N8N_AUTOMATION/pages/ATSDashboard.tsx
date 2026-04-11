import { useState, useEffect } from "react";
import { 
  uploadResume, 
  getCandidates, 
  submitComplaint, 
  getRoles, 
  createRole, 
  addSkillsToRole 
} from "../shared/api";
import { parseResumeFromPdf } from "../lib/parse-resume";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@/components/ui/select";
import { toast } from "sonner";
import { Plus, Trash2, UserPlus, LogOut } from "lucide-react";
import { auth } from "@/lib/auth";

export default function ATSDashboard() {
  const [candidates, setCandidates] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedRoleId, setSelectedRoleId] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  // Role Management State
  const [newRoleName, setNewRoleName] = useState("");
  const [roleSkills, setRoleSkills] = useState([{ name: "", type: "required" }]);

  // Complaint state
  const [userName, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [description, setDescription] = useState("");

  const fetchData = async () => {
    try {
      const rolesData = await getRoles();
      setRoles(rolesData);
      
      // If we have roles but none selected, select the first one
      if (rolesData.length > 0 && !selectedRoleId) {
        setSelectedRoleId(rolesData[0].id.toString());
      }
    } catch (error) {
      console.error("Error fetching roles:", error);
      toast.error("Failed to load job roles");
    }

    try {
      const candidatesData = await getCandidates();
      setCandidates(candidatesData);
    } catch (error) {
      console.error("Error fetching candidates:", error);
      toast.error("Failed to load candidates");
    }
  };
  
  useEffect(() => {
  fetchData(); // initial load

  const interval = setInterval(() => {
    fetchData(); // auto refresh
  }, 8000); // every 8 sec

  return () => clearInterval(interval);
}, []);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file || !selectedRoleId) {
      toast.error("Please select a role and a file");
      return;
    }

    setLoading(true);
    try {
      // Step 1: Parse the resume locally
      const parsedData = await parseResumeFromPdf(file);

      // Step 2: Upload with role_id
      const result = await uploadResume(file, parseInt(selectedRoleId), parsedData);

      if (result.error) throw new Error(result.error);

      toast.success(`Resume processed! Status: ${result.status}`);
      fetchData();
      setFile(null);
    } catch (error) {
      console.error("Error processing resume:", error);
      toast.error(error instanceof Error ? error.message : "Error processing resume");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRole = async (e) => {
    e.preventDefault();
    if (!newRoleName) return;

    try {
      const role = await createRole(newRoleName);
      if (roleSkills.some(s => s.name)) {
        await addSkillsToRole(role.id, roleSkills.filter(s => s.name));
      }
      toast.success("Role and skills created successfully");
      setNewRoleName("");
      setRoleSkills([{ name: "", type: "required" }]);
      
      // Auto-select the newly created role
      setSelectedRoleId(role.id.toString());
      
      fetchData();
    } catch (error) {
      console.error("Error creating role:", error);
      toast.error(error instanceof Error ? error.message : "Error creating role");
    }
  };

  const addSkillRow = () => {
    setRoleSkills([...roleSkills, { name: "", type: "required" }]);
  };

  const removeSkillRow = (index) => {
    setRoleSkills(roleSkills.filter((_, i) => i !== index));
  };

  const updateSkill = (index, field, value) => {
    const newSkills = [...roleSkills];
    newSkills[index][field] = value;
    setRoleSkills(newSkills);
  };

  const handleComplaintSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await submitComplaint(userName, email, description);
      toast.success(`Complaint routed to ${result.department} department`);
      setUserName("");
      setEmail("");
      setDescription("");
    } catch (error) {
      toast.error("Error submitting complaint");
    }
  };

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">Mini ATS & Complaint System</h1>
        <Button variant="ghost" onClick={() => auth.logout()} className="gap-2">
          <LogOut className="w-4 h-4" /> Logout
        </Button>
      </div>

      <Tabs defaultValue="upload">
        <TabsList className="mb-4">
          <TabsTrigger value="upload">Upload Resume</TabsTrigger>
          <TabsTrigger value="roles">Job Roles</TabsTrigger>
          <TabsTrigger value="hr-dashboard">HR Dashboard</TabsTrigger>
          <TabsTrigger value="complaints">Submit Complaint</TabsTrigger>
        </TabsList>

        <TabsContent value="upload">
          <Card>
            <CardHeader>
              <CardTitle>Resume Upload (PDF Only)</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleFileUpload} className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Select Job Role</label>
                  <Select
                    value={selectedRoleId}
                    onValueChange={setSelectedRoleId}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Choose a role..." />
                    </SelectTrigger>
                    <SelectContent>
                      {roles.map((role) => (
                        <SelectItem key={role.id} value={role.id.toString()}>
                          {role.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Resume File</label>
                  <Input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                  />
                </div>
                <Button type="submit" disabled={loading || !file || !selectedRoleId}>
                  {loading ? "Processing..." : "Upload & Parse"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="roles">
          <Card>
            <CardHeader>
              <CardTitle>Manage Job Roles & Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateRole} className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Role Name</label>
                  <Input
                    placeholder="e.g. Senior Backend Developer"
                    value={newRoleName}
                    onChange={(e) => setNewRoleName(e.target.value)}
                    required
                  />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium">Skills Requirements</label>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={addSkillRow}
                    >
                      <Plus className="h-4 w-4 mr-2" /> Add Skill
                    </Button>
                  </div>

                  {roleSkills.map((skill, index) => (
                    <div key={index} className="flex gap-4 items-end">
                      <div className="flex-1 space-y-1">
                        <Input
                          placeholder="Skill name"
                          value={skill.name}
                          onChange={(e) => updateSkill(index, "name", e.target.value)}
                        />
                      </div>
                      <div className="w-32 space-y-1">
                        <Select
                          value={skill.type}
                          onValueChange={(val) => updateSkill(index, "type", val)}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="required">Required</SelectItem>
                            <SelectItem value="optional">Optional</SelectItem>
                            <SelectItem value="bonus">Bonus</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        onClick={() => removeSkillRow(index)}
                        disabled={roleSkills.length === 1}
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  ))}
                </div>

                <Button type="submit" className="w-full">
                  Create Role & Skills
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="hr-dashboard">
          <Card>
            <CardHeader>
              <CardTitle>All Candidates</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Skills</TableHead>
                    <TableHead>Exp (Yrs)</TableHead>
                    <TableHead>Score</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Shortlisted?</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {candidates.map((c) => (
                    <TableRow key={c.id}>
                      <TableCell>{c.name}</TableCell>
                      <TableCell>{c.email}</TableCell>
                      <TableCell>{c.skills}</TableCell>
                      <TableCell>{c.experience}</TableCell>
                      <TableCell>{c.score}</TableCell>
                      <TableCell>
                        <span
                          className={`px-2 py-1 rounded-full text-xs ${
                            c.status === "Shortlisted"
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          {c.status}
                        </span>
                      </TableCell>
                      <TableCell>
                        {c.status === "Shortlisted" ? (
                          <span className="text-green-600 font-bold">✓ Yes</span>
                        ) : (
                          <span className="text-red-600">✗ No</span>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="complaints">
          <Card>
            <CardHeader>
              <CardTitle>Submit a Complaint</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleComplaintSubmit} className="space-y-4">
                <Input
                  placeholder="Your Name"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  required
                />
                <Input
                  type="email"
                  placeholder="Your Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <Textarea
                  placeholder="Describe your complaint..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                />
                <Button type="submit">Submit & Route</Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
