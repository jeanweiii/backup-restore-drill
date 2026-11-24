import json
from pathlib import Path

actions = {
    "RPO": "FIND_NEWER", "RTO": "RETIME", "HASH": "RECOPY",
    "SQL": "RECHECK_DB", "COUNT": "RECONCILE", "SUM": "RECONCILE",
    "MISSING": "LOCATE_COPY", "TIME_UNKNOWN": "GET_TIMESTAMP",
    "JOB_WARN": "REVIEW_WARNING",
}
evidence = json.loads(Path("evidence.json").read_text(encoding="utf8"))
tickets = {}
for line in Path("tickets.tsv").read_text(encoding="utf8").splitlines():
    key, state, codes, todo, note = line.split("\t")
    assert key not in tickets and note.strip()
    tickets[key] = (state, [] if codes == "-" else codes.split(","), todo.split(","))
assert set(tickets) == {e["id"] for e in evidence}
n = 0
for e in evidence:
    state, codes, todo = tickets[e["id"]]
    assert state == e["decision"]
    assert sorted(codes) == sorted(e["issues"])
    assert set(todo) == ({actions[c] for c in codes} if codes else {"ARCHIVE"})
    n += len(codes)
print(f"{len(tickets)} tickets accepted, {n} evidence codes matched")
print("Unsafe passes (job success but restore FAIL or REVIEW):",
      sum(e["job"] == "success" and e["decision"] != "PASS" for e in evidence))
