import { Routes, Route } from "react-router-dom";
import CustomerServiceDashboard from "./CustomerServiceDashboard";
import ComplaintsDashboard from "./ComplaintsDashboard";

export default function CustomerDashboard() {
  return (
    <Routes>
      <Route path="/" element={<CustomerServiceDashboard />} />
      <Route path="/tickets" element={<CustomerServiceDashboard />} />
      <Route path="/complaints" element={<ComplaintsDashboard />} />
    </Routes>
  );
}
