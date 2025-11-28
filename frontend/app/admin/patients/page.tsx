const patients = [
  { name: "Minh An Bui", caregiver: "Thao Nguyen", doctor: "Dr. Le Hai" }
];

export default function AdminPatients() {
  return (
    <main className="admin-page">
      <section className="card">
        <div className="pill">Patients</div>
        <div className="grid" style={{ gap: 8 }}>
          {patients.map((p) => (
            <div key={p.name} className="card" style={{ display: "grid", gridTemplateColumns: "repeat(3,minmax(0,1fr))", gap: 6 }}>
              <span>{p.name}</span>
              <span>{p.caregiver}</span>
              <span>{p.doctor}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
