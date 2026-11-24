from pathlib import Path
import csv, hashlib, json, shutil, sqlite3, tempfile
from contextlib import closing

# ID, age (minutes), fixture, delivery state, mock BIA drill duration (minutes)
cases = [
    ("B01", 45, "ok", "success", 9),
    ("B02", 300, "ok", "success", 9),
    ("B03", 60, "corrupt", "success", 9),
    ("B04", 60, "partial", "success", 10),
    ("B05", 60, "missing", "success", 9),
    ("B06", None, "ok", "success", 11),
    ("B07", 240, "ok", "success", 30),
    ("B08", 240, "ok", "success", 31),
    ("B09", 241, "ok", "success", 30),
    ("B10", 120, "ok", "warning", 13),
    ("B11", 60, "semantic", "success", 14),
    ("B12", 300, "partial", "success", 31),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def examine(root, case):
    key, age, fixture, status, duration = case
    source, backup, restored = [root / f"{key}-{x}.db" for x in ("source", "backup", "restore")]
    with closing(sqlite3.connect(source)) as db:
        db.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, amount INTEGER)")
        amounts = [(i, 10 * i) for i in range(1, 101)]
        if fixture == "semantic":
            amounts[-1] = (100, 999)
        db.executemany("INSERT INTO orders VALUES (?, ?)", amounts[:90] if fixture == "partial" else amounts)
        db.commit()
        if fixture != "missing":
            with closing(sqlite3.connect(backup)) as dst:
                db.backup(dst)

    hash_ok = integrity = count = total = None
    if backup.exists():
        expected = sha(backup)
        if fixture == "corrupt":
            backup.write_bytes(b"invalid test fixture")
        shutil.copyfile(backup, restored)
        hash_ok = sha(restored) == expected
        try:
            with closing(sqlite3.connect(restored.as_uri() + "?mode=ro", uri=True)) as db:
                integrity = db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                count, total = db.execute("SELECT COUNT(*), SUM(amount) FROM orders").fetchone()
        except sqlite3.DatabaseError:
            integrity = False

    issues = []
    for condition, code in (
        (not backup.exists(), "MISSING"),
        (hash_ok is False, "HASH"),
        (integrity is False, "SQL"),
        (count is not None and count != 100, "COUNT"),
        (total is not None and total != 50500, "SUM"),
        (age is None, "TIME_UNKNOWN"),
        (age is not None and age > 240, "RPO"),
        (duration > 30, "RTO"),
        (status != "success", "JOB_WARN"),
    ):
        if condition:
            issues.append(code)
    critical = {"MISSING", "HASH", "SQL", "COUNT", "SUM", "RPO", "RTO"}
    decision = "FAIL" if critical.intersection(issues) else "REVIEW" if issues else "PASS"
    return dict(id=key, job=status, age=age, duration=duration, exists=backup.exists(),
                hash=hash_ok, integrity=integrity, count=count, total=total,
                issues=issues, decision=decision)

def main():
    with tempfile.TemporaryDirectory() as tmp:
        evidence = [examine(Path(tmp), case) for case in cases]
    expected = ["PASS", "FAIL", "FAIL", "FAIL", "FAIL", "REVIEW",
                "PASS", "FAIL", "FAIL", "REVIEW", "FAIL", "FAIL"]
    assert [r["decision"] for r in evidence] == expected
    Path("evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    with open("evidence.csv", "w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=list(evidence[0]))
        writer.writeheader()
        writer.writerows(evidence)
    for row in evidence:
        print(row["id"], row["job"], row["decision"], ",".join(row["issues"]) or "-")

if __name__ == "__main__":
    main()
