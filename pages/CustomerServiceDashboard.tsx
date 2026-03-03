import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Zap,
  MessageSquare,
  Clock,
  CheckCircle,
  AlertCircle,
  LogOut,
  Settings,
  Bell,
  Menu,
  User,
  Search,
  Filter,
  ArrowUpRight,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";

export default function CustomerServiceDashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("Dashboard");
  const [selectedTicket, setSelectedTicket] = useState<any>(null);

  const stats = [
    { label: "Active Tickets", value: "42", icon: MessageSquare, color: "text-blue-600", bg: "bg-blue-100" },
    { label: "Avg Response Time", value: "12m", icon: Clock, color: "text-purple-600", bg: "bg-purple-100" },
    { label: "Resolved Today", value: "128", icon: CheckCircle, color: "text-green-600", bg: "bg-green-100" },
    { label: "Urgent Issues", value: "5", icon: AlertCircle, color: "text-red-600", bg: "bg-red-100" },
  ];

  const tickets = [
    {
      id: "TKT-482",
      customer: "Sarah Johnson",
      subject: "Login issue with mobile app",
      priority: "High",
      status: "Assigned",
      aiSuggested: true,
      time: "15m ago",
      details: {
        customerInfo: {
          id: "CUST-9921",
          name: "Sarah Johnson",
          email: "sarah.j@example.com",
          phone: "+1 (555) 123-4567",
          accountNumber: "AC-778899",
          type: "VIP",
        },
        ticketInfo: {
          id: "TKT-482",
          title: "Login issue with mobile app",
          description: "Customer reports being unable to login after the latest update. Error code 503 is displayed on the screen.",
          category: "Technical",
          priority: "High",
          status: "Assigned",
          createdDate: "Oct 24, 2023, 10:15 AM",
          lastUpdated: "Oct 24, 2023, 10:30 AM",
        },
        aiAttributes: {
          intent: "Login/Access Issue",
          sentiment: "Negative",
          prioritySuggestion: "High",
          confidenceScore: "98%",
          autoResponse: "Yes (Drafted)",
        },
        workflowTracking: {
          status: "Active",
          escalationStatus: "None",
          assignedAgent: "CS Support (Tier 2)",
          slaTimer: "45m remaining",
          escalationLevel: "L2",
          autoNotification: "Yes",
        }
      }
    },
    {
      id: "TKT-481",
      customer: "Michael Chen",
      subject: "Subscription billing inquiry",
      priority: "Medium",
      status: "In Progress",
      aiSuggested: false,
      time: "45m ago",
    },
    {
      id: "TKT-480",
      customer: "Elena Rodriguez",
      subject: "Data export request",
      priority: "Low",
      status: "Open",
      aiSuggested: true,
      time: "1h ago",
    },
    {
      id: "TKT-479",
      customer: "David Kim",
      subject: "API integration error",
      priority: "Critical",
      status: "Assigned",
      aiSuggested: true,
      time: "2h ago",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="md:hidden p-2"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-secondary">WorkflowAI</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center relative">
              <Search className="w-4 h-4 absolute left-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search tickets..."
                className="pl-10 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 w-64"
              />
            </div>
            <button className="p-2 hover:bg-slate-100 rounded-lg relative">
              <Bell className="w-5 h-5 text-slate-600" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white" />
            </button>
            <button className="p-2 hover:bg-slate-100 rounded-lg">
              <Settings className="w-5 h-5 text-slate-600" />
            </button>
            <Link to="/login">
              <button className="p-2 hover:bg-slate-100 rounded-lg">
                <LogOut className="w-5 h-5 text-slate-600" />
              </button>
            </Link>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`${
            sidebarOpen ? "block" : "hidden"
          } md:block w-64 bg-white border-r border-slate-200 p-6 min-h-screen`}
        >
          <div className="mb-8">
            <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl border border-slate-100 mb-6">
              <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                <User className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm font-bold text-secondary">CS Support</p>
                <p className="text-xs text-slate-500">Tier 2 Specialist</p>
              </div>
            </div>
          </div>

          <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">
            Queue Management
          </h2>
          <nav className="space-y-1 mb-8">
            {[
              { label: "Dashboard", icon: TrendingUp },
              { label: "My Tickets", icon: MessageSquare },
              { label: "Open Queue", icon: Clock },
              { label: "Resolved", icon: CheckCircle },
            ].map((item) => (
              <button
                key={item.label}
                onClick={() => {
                  setActiveTab(item.label);
                  setSelectedTicket(null);
                }}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg transition ${
                  activeTab === item.label
                    ? "bg-primary/10 text-primary font-medium"
                    : "text-slate-600 hover:bg-slate-50"
                }`}
              >
                <item.icon className="w-5 h-5" />
                {item.label}
              </button>
            ))}
          </nav>

          <div className="mt-auto pt-6">
            <div className="p-4 bg-gradient-to-br from-primary/10 to-accent/10 rounded-xl border border-primary/20">
              <div className="flex items-center gap-2 mb-2">
                <Zap className="w-4 h-4 text-primary" />
                <span className="text-sm font-bold text-secondary">AI Assistant</span>
              </div>
              <p className="text-xs text-slate-600 mb-4">
                AI is monitoring 12 new tickets. Suggested responses are ready.
              </p>
              <Button size="sm" className="w-full text-xs">Review Suggestions</Button>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-4 sm:p-8">
          {selectedTicket ? (
            <div className="max-w-5xl mx-auto">
              <div className="flex items-center gap-4 mb-8">
                <Button variant="ghost" size="sm" onClick={() => setSelectedTicket(null)}>
                  &larr; Back to Queue
                </Button>
                <h1 className="text-2xl font-bold text-secondary">Ticket Detail: {selectedTicket.id}</h1>
              </div>

              <div className="grid lg:grid-cols-2 gap-8">
                {/* 📌 1️⃣ Customer Basic Information */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                  <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center gap-2">
                    <span className="text-xl">📌</span>
                    <h2 className="font-bold text-secondary text-lg">1️⃣ Customer Basic Information</h2>
                  </div>
                  <div className="p-6 grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Customer ID</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.customerInfo.id || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Full Name</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.customerInfo.name || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Email Address</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.customerInfo.email || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Phone Number</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.customerInfo.phone || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Account Number</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.customerInfo.accountNumber || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Customer Type</p>
                      <span className="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 text-blue-700 uppercase">
                        {selectedTicket.details?.customerInfo.type || "New"}
                      </span>
                    </div>
                  </div>
                  <div className="px-6 pb-4">
                    <p className="text-[10px] text-slate-400 italic">These attributes help personalize and categorize support workflows.</p>
                  </div>
                </div>

                {/* 🎫 2️⃣ Ticket Information */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                  <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center gap-2">
                    <span className="text-xl">🎫</span>
                    <h2 className="font-bold text-secondary text-lg">2️⃣ Ticket Information (Core)</h2>
                  </div>
                  <div className="p-6 space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase">Ticket ID</p>
                        <p className="text-sm font-medium text-slate-900">{selectedTicket.id}</p>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase">Status</p>
                        <p className="text-sm font-medium text-slate-900">{selectedTicket.status}</p>
                      </div>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Issue Title</p>
                      <p className="text-sm font-medium text-secondary">{selectedTicket.subject}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Issue Description</p>
                      <p className="text-sm text-slate-600 mt-1">{selectedTicket.details?.ticketInfo.description || "No detailed description available."}</p>
                    </div>
                    <div className="grid grid-cols-3 gap-2 pt-2">
                      <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                        <p className="text-[10px] text-slate-400 uppercase">Category</p>
                        <p className="text-xs font-bold text-secondary">{selectedTicket.details?.ticketInfo.category || "General"}</p>
                      </div>
                      <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                        <p className="text-[10px] text-slate-400 uppercase">Priority</p>
                        <p className="text-xs font-bold text-secondary">{selectedTicket.priority}</p>
                      </div>
                      <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                        <p className="text-[10px] text-slate-400 uppercase">Created</p>
                        <p className="text-[10px] font-bold text-secondary">{selectedTicket.details?.ticketInfo.createdDate || "N/A"}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* 🤖 3️⃣ AI-Based Attributes */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden border-l-4 border-l-primary">
                  <div className="bg-primary/5 px-6 py-4 border-b border-slate-200 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-primary" />
                    <h2 className="font-bold text-secondary text-lg">3️⃣ AI-Based Attributes (Smart Layer)</h2>
                  </div>
                  <div className="p-6 grid grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">AI Intent Classification</p>
                        <p className="text-sm font-bold text-primary">{selectedTicket.details?.aiAttributes.intent || "Unknown"}</p>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">AI Priority Suggestion</p>
                        <p className="text-sm font-bold text-slate-900">{selectedTicket.details?.aiAttributes.prioritySuggestion || "N/A"}</p>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Sentiment Score</p>
                        <span className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          selectedTicket.details?.aiAttributes.sentiment === "Negative" ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
                        }`}>
                          {selectedTicket.details?.aiAttributes.sentiment || "Neutral"}
                        </span>
                      </div>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">AI Confidence Score</p>
                        <div className="flex items-center gap-2">
                          <div className="flex-1 h-1.5 bg-slate-100 rounded-full">
                            <div className="h-full bg-primary rounded-full" style={{ width: selectedTicket.details?.aiAttributes.confidenceScore || "0%" }} />
                          </div>
                          <span className="text-xs font-bold text-slate-700">{selectedTicket.details?.aiAttributes.confidenceScore || "N/A"}</span>
                        </div>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Auto-Response Generated</p>
                        <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.aiAttributes.autoResponse || "No"}</p>
                      </div>
                    </div>
                  </div>
                  <div className="bg-slate-50 px-6 py-3 border-t border-slate-100">
                    <p className="text-[10px] text-slate-500 italic">
                      AI analyzes customer queries and classifies the issue type and sentiment. Based on this, n8n routes the ticket to the appropriate department.
                    </p>
                  </div>
                </div>

                {/* 🔄 4️⃣ Workflow Automation Tracking */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden border-l-4 border-l-accent">
                  <div className="bg-accent/5 px-6 py-4 border-b border-slate-200 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-accent" />
                    <h2 className="font-bold text-secondary text-lg">4️⃣ Workflow Automation Tracking (n8n)</h2>
                  </div>
                  <div className="p-6 grid grid-cols-2 gap-x-8 gap-y-4">
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Workflow Status</p>
                      <p className="text-sm font-bold text-accent">{selectedTicket.details?.workflowTracking.status || "Pending"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">SLA Timer</p>
                      <p className="text-sm font-medium text-red-600">{selectedTicket.details?.workflowTracking.slaTimer || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Escalation Level</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.workflowTracking.escalationLevel || "None"}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase">Assigned Agent</p>
                      <p className="text-sm font-medium text-slate-900">{selectedTicket.details?.workflowTracking.assignedAgent || "Unassigned"}</p>
                    </div>
                    <div className="col-span-2 flex items-center justify-between p-3 bg-slate-50 rounded-lg mt-2">
                      <span className="text-xs text-slate-600">Auto-Notification Sent:</span>
                      <span className="text-xs font-bold text-green-600">{selectedTicket.details?.workflowTracking.autoNotification || "No"}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-8 flex justify-end gap-3">
                <Button variant="outline">Escalate to Tier 3</Button>
                <Button className="gap-2">
                  <MessageSquare className="w-4 h-4" /> Send Reply
                </Button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
                <div>
                  <h1 className="text-3xl font-bold text-secondary mb-2">
                    Customer Service {activeTab}
                  </h1>
                  <p className="text-slate-600">
                    Manage your support queue and AI-automated responses
                  </p>
                </div>
                <div className="flex gap-3">
                  <Button variant="outline" className="gap-2">
                    <Filter className="w-4 h-4" /> Filter
                  </Button>
                  <Button className="gap-2">
                    <MessageSquare className="w-4 h-4" /> New Ticket
                  </Button>
                </div>
              </div>

              {activeTab === "Dashboard" && (
                <>
                  {/* Stats Grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {stats.map((stat, idx) => (
                      <div
                        key={idx}
                        className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm"
                      >
                        <div className="flex items-center justify-between mb-4">
                          <div className={`p-2 rounded-lg ${stat.bg}`}>
                            <stat.icon className={`w-6 h-6 ${stat.color}`} />
                          </div>
                          <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full flex items-center gap-1">
                            <ArrowUpRight className="w-3 h-3" /> 12%
                          </span>
                        </div>
                        <p className="text-slate-600 text-sm font-medium">{stat.label}</p>
                        <h3 className="text-2xl font-bold text-secondary mt-1">
                          {stat.value}
                        </h3>
                      </div>
                    ))}
                  </div>

                  <div className="grid lg:grid-cols-3 gap-8">
                    {/* Tickets Table */}
                    <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                      <div className="p-6 border-b border-slate-200 flex items-center justify-between">
                        <h2 className="text-lg font-bold text-secondary">Active Tickets</h2>
                        <Button variant="ghost" size="sm" className="text-primary" onClick={() => setActiveTab("My Tickets")}>View All</Button>
                      </div>
                      <div className="overflow-x-auto">
                        <table className="w-full text-left">
                          <thead>
                            <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                              <th className="px-6 py-4 font-semibold">Ticket & Customer</th>
                              <th className="px-6 py-4 font-semibold">Priority</th>
                              <th className="px-6 py-4 font-semibold">Status</th>
                              <th className="px-6 py-4 font-semibold">AI Tool</th>
                              <th className="px-6 py-4 font-semibold text-right">Action</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100">
                            {tickets.map((ticket) => (
                              <tr key={ticket.id} className="hover:bg-slate-50 transition">
                                <td className="px-6 py-4">
                                  <div className="flex flex-col">
                                    <span className="text-sm font-bold text-secondary">{ticket.id}</span>
                                    <span className="text-xs text-slate-500">{ticket.customer}</span>
                                    <span className="text-xs text-slate-400 mt-1 line-clamp-1">{ticket.subject}</span>
                                  </div>
                                </td>
                                <td className="px-6 py-4">
                                  <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                                    ticket.priority === "Critical" ? "bg-red-100 text-red-700" :
                                    ticket.priority === "High" ? "bg-orange-100 text-orange-700" :
                                    "bg-blue-100 text-blue-700"
                                  }`}>
                                    {ticket.priority}
                                  </span>
                                </td>
                                <td className="px-6 py-4 text-xs font-medium text-slate-700">
                                  {ticket.status}
                                </td>
                                <td className="px-6 py-4">
                                  {ticket.aiSuggested ? (
                                    <span className="flex items-center gap-1.5 text-xs text-primary font-medium">
                                      <Zap className="w-3 h-3" /> Ready
                                    </span>
                                  ) : (
                                    <span className="text-xs text-slate-400">-</span>
                                  )}
                                </td>
                                <td className="px-6 py-4 text-right">
                                  <Button size="sm" variant="ghost" onClick={() => setSelectedTicket(ticket)}>Detail</Button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    {/* AI Insights & Performance */}
                    <div className="space-y-8">
                      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
                        <h2 className="text-lg font-bold text-secondary mb-6 flex items-center gap-2">
                          <Zap className="w-5 h-5 text-primary" /> AI Insights
                        </h2>
                        <div className="space-y-4">
                          <div className="p-4 bg-blue-50 border border-blue-100 rounded-lg">
                            <p className="text-xs font-bold text-blue-900 uppercase mb-2">Trend Alert</p>
                            <p className="text-sm text-blue-800">
                              Increased queries regarding "v2 API changes". Suggested KB article update.
                            </p>
                          </div>
                          <div className="p-4 bg-purple-50 border border-purple-100 rounded-lg">
                            <p className="text-xs font-bold text-purple-900 uppercase mb-2">Automation Opportunity</p>
                            <p className="text-sm text-purple-800">
                              85% of "billing" tickets can be resolved with the new Refund Workflow.
                            </p>
                          </div>
                        </div>
                      </div>

                      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
                        <h2 className="text-lg font-bold text-secondary mb-6">Performance</h2>
                        <div className="space-y-4">
                          <div>
                            <div className="flex justify-between text-xs mb-1.5">
                              <span className="text-slate-600">SLA Compliance</span>
                              <span className="font-bold text-secondary">98.2%</span>
                            </div>
                            <div className="w-full bg-slate-100 rounded-full h-1.5">
                              <div className="bg-green-500 h-1.5 rounded-full" style={{ width: "98.2%" }} />
                            </div>
                          </div>
                          <div>
                            <div className="flex justify-between text-xs mb-1.5">
                              <span className="text-slate-600">Customer Satisfaction</span>
                              <span className="font-bold text-secondary">4.8/5</span>
                            </div>
                            <div className="w-full bg-slate-100 rounded-full h-1.5">
                              <div className="bg-primary h-1.5 rounded-full" style={{ width: "96%" }} />
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {activeTab !== "Dashboard" && (
                <div className="bg-white rounded-xl border border-slate-200 p-8 text-center">
                   <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Clock className="w-8 h-8 text-slate-400" />
                   </div>
                   <h2 className="text-xl font-bold text-secondary mb-2">{activeTab} View</h2>
                   <p className="text-slate-600 italic">This view is currently being optimized for AI integration. Please use the Dashboard to view active tickets.</p>
                </div>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}
