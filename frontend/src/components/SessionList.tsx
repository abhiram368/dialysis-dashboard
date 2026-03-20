import { useEffect, useState } from "react";
import { getTodaySessions } from "../api/client";

export default function SessionList() {
  const [sessions, setSessions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTodaySessions()
      .then(setSessions)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      {sessions.map((s) => (
        <div key={s.id} style={{ border: "1px solid #ccc", margin: 10 }}>
          <p>Patient ID: {s.patient_id}</p>
          <p>Pre Weight: {s.pre_weight}</p>
          <p>Post Weight: {s.post_weight}</p>

          {/* anomalies */}
          {s.anomalies?.length > 0 && (
            <div style={{ color: "red" }}>
              ⚠ Anomalies:
              <ul>
                {s.anomalies.map((a: string, i: number) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}