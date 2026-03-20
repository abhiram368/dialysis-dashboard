import { useState } from "react";
import { createSession } from "../api/client";

export default function CreateSession() {
  const [form, setForm] = useState({
    patient_id: "",
    pre_weight: "",
    post_weight: "",
  });

  const handleSubmit = async () => {
    await createSession({
      ...form,
      pre_weight: Number(form.pre_weight),
      post_weight: Number(form.post_weight),
    });
    alert("Created");
  };

  return (
    <div>
      <input
        placeholder="Patient ID"
        onChange={(e) => setForm({ ...form, patient_id: e.target.value })}
      />
      <input
        placeholder="Pre weight"
        onChange={(e) => setForm({ ...form, pre_weight: e.target.value })}
      />
      <input
        placeholder="Post weight"
        onChange={(e) => setForm({ ...form, post_weight: e.target.value })}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}