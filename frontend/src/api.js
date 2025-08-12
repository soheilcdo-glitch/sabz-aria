import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const login = (username, password) =>
  API.post("/token", new URLSearchParams({ username, password }));

export const fetchRecentLogins = (token) =>
  API.get("/login-history/recent", { headers: { Authorization: `Bearer ${token}` } });

export const createUser = (token, payload) =>
  API.post("/users/", payload, { headers: { Authorization: `Bearer ${token}` } });

export default API;
