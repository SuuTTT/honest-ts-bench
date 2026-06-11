#!/usr/bin/env python3
"""Live fleet/run dashboard for honest-ts-bench.

Stdlib only (the host has ~400MB free RAM). A background thread probes each
fleet box over ssh every PROBE_INTERVAL seconds (nvidia-smi + optional log
tail); the HTTP server serves an auto-refreshing HTML page at / and JSON at
/api/status. Probing is ssh I/O only — no computation runs on this host.

Usage: python3 live_dashboard.py [--port 5180]
"""
import json, subprocess, threading, time, os, html, sys
from http.server import HTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
SSH_KEY = os.path.expanduser("~/.ssh/vastai_id_ed25519")
PROBE_INTERVAL = 120  # seconds

# instance -> (host, port, project, note, logfile-to-tail or None)
BOXES = {
    "40230626": ("ssh5.vast.ai", 30627, "struct-mamba",
                 "PEMS04/07/08 grid", "/root/structmamba.log"),
    "40424707": ("ssh1.vast.ai", 24707, "struct-mamba",
                 "PEMS03 grid DONE 06-11", "/root/sm_pems03.log"),
    "40230497": ("ssh8.vast.ai", 30497, "ts-bench-audit",
                 "from mahjong 06-11", None),
    "40121712": ("ssh2.vast.ai", 11713, "mahjong-eval + ts-bench-audit",
                 "GPU co-tenant; mahjong CPUs until 06-14", None),
    "22734":    ("ssh5.vast.ai", 22734, "ts-bench-audit",
                 "FLAKY - short runs only", None),
}

STATE = {"generated": None, "fleet": [], "runs": [], "queue": []}
LOCK = threading.Lock()


def ssh(host, port, cmd, timeout=25):
    try:
        r = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=8", "-o", "StrictHostKeyChecking=no",
             "-o", "BatchMode=yes", "-i", SSH_KEY, "-p", str(port),
             f"root@{host}", cmd],
            capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return None


def probe_loop():
    while True:
        fleet = []
        for iid, (host, port, project, note, logf) in BOXES.items():
            cmd = ("nvidia-smi --query-gpu=name,utilization.gpu,memory.used,"
                   "memory.total --format=csv,noheader 2>/dev/null")
            if logf:
                cmd += f"; echo __LOG__; tail -c 300 {logf} 2>/dev/null | tail -2"
            out = ssh(host, port, cmd)
            entry = {"instance": iid, "endpoint": f"{host}:{port}",
                     "project": project, "note": note,
                     "gpu": "?", "util": "?", "mem": "?",
                     "logtail": "", "reachable": False}
            if out:
                parts = out.split("__LOG__")
                gpuline = [l for l in parts[0].splitlines() if "," in l]
                if gpuline:
                    name, util, used, total = [x.strip() for x in
                                               gpuline[-1].split(",")]
                    entry.update({"gpu": name, "util": util,
                                  "mem": f"{used} / {total}",
                                  "reachable": True})
                if len(parts) > 1:
                    entry["logtail"] = parts[1].strip()[-200:]
            fleet.append(entry)

        try:
            reg = json.load(open(os.path.join(HERE, "runs.json")))
        except Exception:
            reg = {"runs": [], "queue": []}

        with LOCK:
            STATE["generated"] = time.strftime("%Y-%m-%d %H:%M:%S UTC",
                                               time.gmtime())
            STATE["fleet"] = fleet
            STATE["runs"] = reg.get("runs", [])
            STATE["queue"] = reg.get("queue", [])
        time.sleep(PROBE_INTERVAL)


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>honest-ts-bench dashboard</title>
<style>
 body{font-family:system-ui,sans-serif;margin:2em;max-width:1100px}
 h1{font-size:1.4em} h2{font-size:1.1em;margin-top:1.6em}
 table{border-collapse:collapse;width:100%;font-size:0.85em}
 th,td{border:1px solid #ccc;padding:4px 8px;text-align:left;vertical-align:top}
 th{background:#f0f0f0}
 .dead{opacity:.45} .run{background:#fff8e6} .done{background:#eef7ee}
 .log{font-family:monospace;font-size:0.75em;color:#555;white-space:pre-wrap}
 #ts{color:#666;font-style:italic}
</style></head><body>
<h1>honest-ts-bench — live fleet dashboard</h1>
<p id="ts">loading…</p>
<h2>GPU fleet</h2><table id="fleet"><thead><tr>
<th>Instance</th><th>Endpoint</th><th>GPU</th><th>Util</th><th>Memory</th>
<th>Project</th><th>Note</th><th>Log tail</th></tr></thead><tbody></tbody></table>
<h2>Active runs</h2><table id="runs"><thead><tr>
<th>Project</th><th>Box</th><th>What</th><th>Status</th><th>Progress</th>
</tr></thead><tbody></tbody></table>
<h2>Queue</h2><table id="queue"><thead><tr>
<th>Project</th><th>What</th><th>Target boxes</th><th>Blocked on</th>
</tr></thead><tbody></tbody></table>
<script>
function td(t){var e=document.createElement('td');e.textContent=t==null?'—':t;return e}
function refresh(){fetch('/api/status').then(r=>r.json()).then(d=>{
 document.getElementById('ts').textContent='Last probe: '+d.generated+
   ' (auto-refreshes every 30 s; boxes probed every 2 min)';
 var f=document.querySelector('#fleet tbody');f.innerHTML='';
 d.fleet.forEach(b=>{var tr=document.createElement('tr');
  if(!b.reachable)tr.className='dead';
  ['instance','endpoint','gpu','util','mem','project','note'].forEach(k=>tr.appendChild(td(b[k])));
  var lt=td(b.logtail);lt.className='log';tr.appendChild(lt);f.appendChild(tr)});
 var r=document.querySelector('#runs tbody');r.innerHTML='';
 d.runs.forEach(x=>{var tr=document.createElement('tr');tr.className=x.status;
  ['project','box','what','status','progress'].forEach(k=>tr.appendChild(td(x[k])));
  r.appendChild(tr)});
 var q=document.querySelector('#queue tbody');q.innerHTML='';
 d.queue.forEach(x=>{var tr=document.createElement('tr');
  ['project','what','target_boxes','blocked_on'].forEach(k=>tr.appendChild(td(x[k])));
  q.appendChild(tr)});
})}
refresh();setInterval(refresh,30000);
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/status"):
            with LOCK:
                body = json.dumps(STATE).encode()
            ctype = "application/json"
        elif self.path == "/" or self.path.startswith("/index"):
            body = PAGE.encode()
            ctype = "text/html; charset=utf-8"
        else:
            self.send_response(404); self.end_headers(); return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # quiet
        pass


def main():
    port = 5180
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    t = threading.Thread(target=probe_loop, daemon=True)
    t.start()
    print(f"live dashboard on http://0.0.0.0:{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
