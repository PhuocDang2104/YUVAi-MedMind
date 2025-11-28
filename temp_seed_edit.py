from pathlib import Path

text = Path('backend/app/db/seed.py').read_text()
start = """        session.add(
            SymptomLog(
                id=_uuid(),
                patient_id=patient.id,
                interaction_id=inter.id,
                llm_request_id=llm_req.id,
                location=\"head\""""
end = "        alert = AlertLog"
start_idx = text.find(start)
end_idx = text.find(end)
if start_idx == -1 or end_idx == -1:
    raise SystemExit("markers not found")
new_block = """        symptom_logs_asha = [
            {\"raw\": \"Headache dizziness after a short walk\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=1, hours=1), \"symptoms\": [\"headache dizziness\"]},
            {\"raw\": \"Headache dizziness mild, improved after rest\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=2), \"symptoms\": [\"headache dizziness\"]},
            {\"raw\": \"Headache dizziness worse at night\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=3, hours=2), \"symptoms\": [\"headache dizziness\"]},
            {\"raw\": \"Headache dizziness returned after lunch\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=4, hours=3), \"symptoms\": [\"headache dizziness\"]},
            {\"raw\": \"Shortness of breath climbing stairs\", \"severity\": \"severe\", \"created_at\": now - timedelta(hours=5), \"symptoms\": [\"shortness of breath\"]},
            {\"raw\": \"Shortness of breath when walking uphill\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=1, hours=4), \"symptoms\": [\"shortness of breath\"]},
            {\"raw\": \"Shortness of breath mild in the afternoon\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=2, hours=3), \"symptoms\": [\"shortness of breath\"]},
            {\"raw\": \"Shortness of breath eased after rest\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=3, hours=6), \"symptoms\": [\"shortness of breath\"]},
            {\"raw\": \"Chest pain with tightness while cooking\", \"severity\": \"severe\", \"created_at\": now - timedelta(hours=7), \"symptoms\": [\"chest pain\"]},
            {\"raw\": \"Chest pain light pressure in evening\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=1, hours=6), \"symptoms\": [\"chest pain\"]},
            {\"raw\": \"Chest pain fleeting, resolved after sitting\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=2, hours=5), \"symptoms\": [\"chest pain\"]},
            {\"raw\": \"Chest pain when walking fast\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=4), \"symptoms\": [\"chest pain\"]},
            {\"raw\": \"Palpitations at night for a few minutes\", \"severity\": \"moderate\", \"created_at\": now - timedelta(days=1, hours=1), \"symptoms\": [\"palpitations\"]},
            {\"raw\": \"Blurred vision brief episode\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=2, hours=2), \"symptoms\": [\"blurred vision\"]},
            {\"raw\": \"Nausea after breakfast\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=1, hours=20), \"symptoms\": [\"nausea\"]},
            {\"raw\": \"Fatigue mid-afternoon, needed to sit\", \"severity\": \"mild\", \"created_at\": now - timedelta(days=3, hours=4), \"symptoms\": [\"fatigue\"]},
            {\"raw\": \"Lightheadedness on standing quickly\", \"severity\": \"mild\", \"created_at\": now - timedelta(hours=12), \"symptoms\": [\"lightheadedness\"]},
        ]
        for sym in symptom_logs_asha:
            session.add(
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient.id,
                    severity=sym[\"severity\"],
                    symptoms_raw=sym[\"raw\"],
                    structured_json={\"symptoms\": sym[\"symptoms\"], \"severity\": sym[\"severity\"]},
                    created_at=sym[\"created_at\"],
                )
            )

        session.add_all(
            [
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient2.id,
                    severity=\"mild\",
                    symptoms_raw=\"Mild headache after evening walk\",
                    structured_json={\"symptoms\": [\"headache\"], \"severity\": \"mild\"},
                    created_at=now - timedelta(days=3),
                ),
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient2.id,
                    severity=\"mild\",
                    symptoms_raw=\"Brief lightheadedness after standing\",
                    structured_json={\"symptoms\": [\"lightheadedness\"], \"severity\": \"mild\"},
                    created_at=now - timedelta(days=1, hours=3),
                ),
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient3.id,
                    severity=\"moderate\",
                    symptoms_raw=\"Shortness of breath while gardening\",
                    structured_json={\"symptoms\": [\"shortness of breath\"], \"severity\": \"moderate\"},
                    created_at=now - timedelta(days=2),
                ),
                SymptomLog(
                    id=_uuid(),
                    patient_id=patient3.id,
                    severity=\"mild\",
                    symptoms_raw=\"Mild chest discomfort after dinner\",
                    structured_json={\"symptoms\": [\"chest discomfort\"], \"severity\": \"mild\"},
                    created_at=now - timedelta(days=1, hours=5),
                ),
            ]
        )
"""

text = text[:start_idx] + new_block + text[end_idx:]
Path('backend/app/db/seed.py').write_text(text)
print('patched symptom block')
