import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate();

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await login(username, password);
      localStorage.setItem("token", res.data.access_token);
      nav("/dashboard");
    } catch (err) {
      alert("Login failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="container">
      <h2>ورود</h2>
      <form onSubmit={onSubmit}>
        <div><label>نام کاربری</label><br/>
          <input placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div><label>رمز</label><br/>
          <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button type="submit">ورود</button>
      </form>
    </div>
  );
}
