from flask import Flask, render_template, request, jsonify
import csv, io, re
from collections import defaultdict

app = Flask(__name__)

# Demo dataset. Replace/upload your own CSV from the web UI.
DEFAULT_ROWS = [
    {"source":"Arun","target":"Ravi","relation":"phone","amount":"0"},
    {"source":"Ravi","target":"Kumar","relation":"money_transfer","amount":"75000"},
    {"source":"Kumar","target":"Suresh","relation":"money_transfer","amount":"125000"},
    {"source":"Ravi","target":"Chennai","relation":"location","amount":"0"},
    {"source":"Arun","target":"Kumar","relation":"phone","amount":"0"},
    {"source":"Suresh","target":"Ravi","relation":"phone","amount":"0"},
    {"source":"Kumar","target":"Mohan","relation":"money_transfer","amount":"250000"},
]

rows = DEFAULT_ROWS[:]

def analyse(data):
    degree = defaultdict(int)
    money = defaultdict(float)
    relation_count = defaultdict(int)
    nodes = set()

    for r in data:
        s, t = r["source"].strip(), r["target"].strip()
        rel = r["relation"].strip() or "unknown"
        try:
            amount = float(r.get("amount", 0) or 0)
        except ValueError:
            amount = 0

        if not s or not t:
            continue
        nodes.update([s, t])
        degree[s] += 1
        degree[t] += 1
        money[s] += amount
        relation_count[rel] += 1

    # Simple prototype risk score; replace with trained ML model for production.
    max_degree = max(degree.values(), default=1)
    max_money = max(money.values(), default=1)

    people = []
    for n in nodes:
        score = round(
            60 * (degree[n] / max_degree) +
            40 * (money[n] / max_money if max_money else 0), 1
        )
        level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
        people.append({
            "name": n,
            "connections": degree[n],
            "transaction_value": round(money[n], 2),
            "risk_score": score,
            "risk_level": level
        })

    people.sort(key=lambda x: x["risk_score"], reverse=True)

    graph_nodes = [{"data":{"id":n, "label":n}} for n in nodes]
    graph_edges = []
    for i, r in enumerate(data):
        s, t = r["source"].strip(), r["target"].strip()
        if s and t:
            graph_edges.append({
                "data":{
                    "id":f"e{i}",
                    "source":s,
                    "target":t,
                    "label":r["relation"] or "unknown"
                }
            })

    high_risk = [p for p in people if p["risk_level"] == "High"]

    return {
        "nodes": graph_nodes,
        "edges": graph_edges,
        "people": people,
        "stats": {
            "entities": len(nodes),
            "relationships": len(graph_edges),
            "high_risk": len(high_risk),
            "total_value": round(sum(float(r.get("amount", 0) or 0) for r in data
                                     if str(r.get("amount","")).replace(".","",1).isdigit()), 2)
        },
        "relations": dict(relation_count)
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analysis")
def api_analysis():
    return jsonify(analyse(rows))

@app.route("/api/upload", methods=["POST"])
def upload():
    global rows
    file = request.files.get("file")
    if not file:
        return jsonify({"error":"Please select a CSV file."}), 400

    try:
        content = file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))
        required = {"source", "target", "relation", "amount"}
        if not required.issubset(set(reader.fieldnames or [])):
            return jsonify({
                "error":"CSV must contain columns: source,target,relation,amount"
            }), 400

        new_rows = []
        for r in reader:
            new_rows.append({
                "source": r.get("source",""),
                "target": r.get("target",""),
                "relation": r.get("relation",""),
                "amount": r.get("amount","0")
            })
        rows = new_rows
        return jsonify({"message":f"Loaded {len(rows)} relationships.", "analysis":analyse(rows)})
    except Exception as e:
        return jsonify({"error":f"Could not read file: {e}"}), 400

@app.route("/api/reset", methods=["POST"])
def reset():
    global rows
    rows = DEFAULT_ROWS[:]
    return jsonify({"message":"Demo dataset restored.", "analysis":analyse(rows)})

if __name__ == "__main__":
    app.run(debug=True)
