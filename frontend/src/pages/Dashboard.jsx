import { useEffect, useState } from "react";
import API from "../api";
import jalaali from "jalaali-js";

function toPersianDate(isoString){
  if(!isoString) return '-';
  const d = new Date(isoString);
  const j = jalaali.toJalaali(d.getFullYear(), d.getMonth()+1, d.getDate());
  const time = d.toLocaleTimeString('fa-IR');
  return `${j.jy}/${String(j.jm).padStart(2,'0')}/${String(j.jd).padStart(2,'0')} - ${time}`;
}

export default function Dashboard(){
  const [recentLogins, setRecentLogins] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(()=> {
    API.get("/login-history/recent", { headers:{ Authorization:`Bearer ${token}` } })
       .then(r=> setRecentLogins(r.data))
       .catch(e=> console.log(e));
  }, []);

  return (
    <div className="container">
      <h2>داشبورد</h2>
      <div style={{display:'flex', gap:20}}>
        <div style={{flex:1}}>
          <h3>۱۰ کاربر آخر واردشده</h3>
          <ul>
            {recentLogins.map(r => (
              <li key={r.id}>
                {r.username} — {toPersianDate(r.timestamp)}
              </li>
            ))}
          </ul>
        </div>
        <div style={{flex:2}}>
          <h3>عملیات سریع</h3>
          <p>این بخش می‌تواند نمودارها و امکانات اضافی را نمایش دهد.</p>
        </div>
      </div>
    </div>
  );
}
