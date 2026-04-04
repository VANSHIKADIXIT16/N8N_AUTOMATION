export interface DemoResponse {
  message: string;
}

export interface Ticket {
  id: number;
  customer_id: number;
  title: string;
  description: string;
  category: string;
  priority: string;
  status: string;
  assigned_to: number | null;
  department: string | null;
  created_at: string;
  updated_at: string;
  customer?: Customer;
}

export interface Customer {
  id: number;
  user_id: number | null;
  name: string;
  email: string;
  phone: string;
  created_at: string;
}

export interface TicketCreate {
  customer_id: number;
  title: string;
  description: string;
  category: string;
}
