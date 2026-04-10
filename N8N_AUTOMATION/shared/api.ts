import { auth } from "../lib/auth";

const API_BASE_URL = "http://localhost:8003";

const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      ...options.headers,
      ...auth.getAuthHeader(),
    },
  });
  if (response.status === 401) {
    auth.logout();
    throw new Error("Session expired. Please login again.");
  }
  return response;
};

export const uploadResume = async (file: File, roleId: number, parsedData?: any) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("role_id", roleId.toString());
  if (parsedData) {
    formData.append("parsed_data", JSON.stringify(parsedData));
  }

  const response = await fetchWithAuth(`/upload_resume/`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to upload resume");
  }
  return response.json();
};

export const getRoles = async () => {
  const response = await fetchWithAuth(`/roles/`); 
  return response.json();
};

export const createRole = async (name: string) => {
  const response = await fetchWithAuth(`/roles/?name=${encodeURIComponent(name)}`, {
    method: "POST",
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to create role");
  }
  return response.json();
};

export const addSkillsToRole = async (roleId: number, skills: { name: string; type: string }[]) => {
  const response = await fetchWithAuth(`/roles/${roleId}/skills/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(skills),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to add skills to role");
  }
  return response.json();
};

export const getRoleSkills = async (roleId: number) => {
  const response = await fetchWithAuth(`/roles/${roleId}/skills/`);
  return response.json();
};

export const submitComplaint = async (
  userName: string,
  email: string,
  description: string,
) => {
  const formData = new FormData();
  formData.append("user_name", userName);
  formData.append("email", email);
  formData.append("description", description);

  const response = await fetchWithAuth(`/submit_complaint/`, {
    method: "POST",
    body: formData,
  });
  return response.json();
};

export const getCandidates = async () => {
  const response = await fetchWithAuth(`/candidates/`);
  return response.json();
};

export const getComplaints = async () => {
  const response = await fetchWithAuth(`/complaints/`);
  return response.json();
};
