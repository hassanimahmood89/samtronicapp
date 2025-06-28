import { useState, useEffect } from 'react';

function App() {
  const [customers, setCustomers] = useState([]);
  const [form, setForm] = useState({ first_name: '', last_name: '', phone: '' });

  // دریافت لیست مشتری‌ها
  useEffect(() => {
    fetch('http://localhost:3000/customers')
      .then(res => res.json())
      .then(data => setCustomers(data))
      .catch(err => console.error('خطا در دریافت مشتری‌ها:', err));
  }, []);

  // تغییر مقادیر فرم
  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ارسال فرم
  const handleSubmit = async e => {
    e.preventDefault();
    const res = await fetch('http://localhost:3000/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    const newCustomer = await res.json();
    setCustomers([...customers, newCustomer]);
    setForm({ first_name: '', last_name: '', phone: '' });
  };

  return (
    <div style={{ maxWidth: '600px', margin: '30px auto', fontFamily: 'Tahoma' }}>
      <h2 style={{ textAlign: 'center' }}>👨‍🔧 مشتری‌های سامترونیک</h2>

      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          name="first_name"
          placeholder="نام"
          value={form.first_name}
          onChange={handleChange}
          required
          style={{ margin: '5px', padding: '8px', width: '30%' }}
        />
        <input
          name="last_name"
          placeholder="نام خانوادگی"
          value={form.last_name}
          onChange={handleChange}
          required
          style={{ margin: '5px', padding: '8px', width: '30%' }}
        />
        <input
          name="phone"
          placeholder="شماره تلفن"
          value={form.phone}
          onChange={handleChange}
          required
          style={{ margin: '5px', padding: '8px', width: '30%' }}
        />
        <button type="submit" style={{ margin: '5px', padding: '8px 20px' }}>
          افزودن
        </button>
      </form>

      {customers.length === 0 ? (
        <p style={{ textAlign: 'center' }}>هیچ مشتری‌ای ثبت نشده.</p>
      ) : (
        <ul>
          {customers.map(c => (
            <li key={c.id}>
              {c.first_name} {c.last_name} — 📞 {c.phone}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;