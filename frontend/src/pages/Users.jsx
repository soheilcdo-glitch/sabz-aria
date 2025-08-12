import React, { useEffect, useState } from "react";
import API from "../api";

function formatCardInput(value){
  const digits = value.replace(/\D/g,'').slice(0,16);
  return digits.replace(/(.{4})/g,'$1-').trim().replace(/-$/,'');
}

export default function Users(){
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({});
  const [editing, setEditing] = useState(null);
  const [usernameExists, setUsernameExists] = useState(false);
  const [nationalExists, setNationalExists] = useState(false);
  const token = localStorage.getItem("token");

  useEffect(()=>{ loadUsers(); }, []);

  async function loadUsers(){
    try {
      const res = await API.get("/users/", { headers:{ Authorization:`Bearer ${token}` } });
      setUsers(res.data);
    } catch(e){
      console.error(e);
    }
  }

  async function checkUsername(u){
    if(!u) { setUsernameExists(false); return; }
    const res = await API.get(`/users/check-username/${encodeURIComponent(u)}`);
    setUsernameExists(res.data.exists);
  }

  async function checkNational(n){
    if(!n || n.length !== 10) { setNationalExists(false); return; }
    const res = await API.get(`/users/check-national/${n}`);
    setNationalExists(res.data.exists);
  }

  function handleChange(e){
    const {name, value} = e.target;
    if(name === "card_number"){
      setForm({...form,[name]: formatCardInput(value)});
      return;
    }
    if(name === "phone"){
      const digits = value.replace(/\D/g,'').slice(0,11);
      setForm({...form,[name]: digits});
      return;
    }
    if(name === "national_id"){
      const digits = value.replace(/\D/g,'').slice(0,10);
      setForm({...form,[name]: digits});
      checkNational(digits);
      return;
    }
    if(name === "username"){
      setForm({...form,[name]: value});
      checkUsername(value);
      return;
    }
    setForm({...form,[name]: value});
  }

  async function submit(e){
    e.preventDefault();
    try {
      if(editing){
        await API.put(`/users/${editing}`, form, { headers:{ Authorization:`Bearer ${token}` } });
      } else {
        await API.post("/users/", form, { headers:{ Authorization:`Bearer ${token}` } });
      }
      setForm({});
      setEditing(null);
      loadUsers();
    } catch(err){
      alert("خطا: " + (err.response?.data?.detail || err.message));
    }
  }

  async function remove(id){
    if(!confirm("مطمئنی حذف کنی؟")) return;
    await API.delete(`/users/${id}`, { headers:{ Authorization:`Bearer ${token}` } });
    loadUsers();
  }

  function edit(u){
    setEditing(u.id);
    setForm({
      first_name: u.first_name || "",
      last_name: u.last_name || "",
      father_name: u.father_name || "",
      national_id: u.national_id || "",
      card_number: u.card_number || "",
      phone: u.phone || "",
      birth_date: u.birth_date ? u.birth_date.split("T")[0] : "",
      role: u.role || "کارمند",
      username: u.username
    });
  }

  return (
    <div className="container" style={{paddingBottom:40}}>
      <h2>مدیریت کاربران</h2>
      <form onSubmit={submit} style={{marginBottom:20}}>
        <div>
          <label>نام کاربری</label><br/>
          <input name="username" value={form.username||""} onChange={handleChange} required />
          {usernameExists && <small style={{color:'red'}}>نام کاربری قبلا موجود است</small>}
        </div>
        <div>
          <label>رمز (برای کاربر جدید یا تغییر)</label><br/>
          <input name="password" type="password" value={form.password||""} onChange={handleChange} required={!editing} />
        </div>
        <div><label>نام</label><br/><input name="first_name" value={form.first_name||""} onChange={handleChange} /></div>
        <div><label>نام خانوادگی</label><br/><input name="last_name" value={form.last_name||""} onChange={handleChange} /></div>
        <div><label>نام پدر</label><br/><input name="father_name" value={form.father_name||""} onChange={handleChange} /></div>
        <div>
          <label>شناسه ملی</label><br/>
          <input name="national_id" value={form.national_id||""} onChange={handleChange} />
          {nationalExists && <small style={{color:'red'}}>شناسه ملی قبلاً استفاده شده</small>}
        </div>
        <div>
          <label>شماره کارت</label><br/>
          <input name="card_number" value={form.card_number||""} onChange={handleChange} placeholder="---- ---- ---- ----" />
        </div>
        <div><label>تلفن</label><br/><input name="phone" value={form.phone||""} onChange={handleChange} /></div>
        <div><label>تاریخ تولد</label><br/><input name="birth_date" type="date" value={form.birth_date||""} onChange={handleChange} /></div>
        <div>
          <label>نقش</label><br/>
          <select name="role" value={form.role||"کارمند"} onChange={handleChange}>
            <option>مدیر مالی</option>
            <option>مدیر سایت</option>
            <option>مدیر ای تی</option>
            <option>مدیر حسابداری</option>
            <option>مدیر انبار</option>
            <option>کارمند</option>
            <option>پرسنل تولید</option>
          </select>
        </div>
        <button type="submit" style={{marginTop:10}}>{editing ? "ویرایش" : "ایجاد"}</button>
      </form>

      <h3>لیست کاربران</h3>
      <table>
        <thead><tr><th>id</th><th>نام کاربری</th><th>نام</th><th>تلفن</th><th>آخرین ورود</th><th>عملیات</th></tr></thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.first_name} {u.last_name}</td>
              <td>{u.phone}</td>
              <td>{u.last_login ? new Date(u.last_login).toLocaleString('fa-IR') : '-'}</td>
              <td>
                <button onClick={()=>edit(u)}>ویرایش</button>
                <button onClick={()=>remove(u.id)}>حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
