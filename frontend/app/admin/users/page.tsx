const users = [
  { email: "caregiver@example.com", role: "CAREGIVER" },
  { email: "doctor@example.com", role: "DOCTOR" },
  { email: "admin@example.com", role: "ADMIN" }
];

export default function Users() {
  return (
    <main className="admin-page">
      <section className="card">
        <div className="pill">Users</div>
        <div className="grid" style={{ gap: 8 }}>
          {users.map((u) => (
            <div key={u.email} className="card" style={{ display: "flex", justifyContent: "space-between" }}>
              <span>{u.email}</span>
              <span className="pill" style={{ background: "rgba(255,255,255,0.08)" }}>{u.role}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
