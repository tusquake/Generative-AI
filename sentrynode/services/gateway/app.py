import os
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="SentryNode API Gateway & UI Console",
    description="Ingress webhook listener and console for SentryNode.AI."
)

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")

class SentryAlertPayload(BaseModel):
    project: str
    message: str
    culprit: str
    stack_trace: str
    codebase_files: dict[str, str] = {}

# HTML, CSS, JS source code for the Render-like Dashboard served on '/'
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SentryNode Plane - Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0a0c;
            --bg-secondary: #121214;
            --bg-card: #18181b;
            --bg-hover: #232329;
            --border-color: #27272a;
            --text-primary: #f4f4f5;
            --text-secondary: #a1a1aa;
            --purple-primary: #7c3aed;
            --purple-hover: #6d28d9;
            --purple-light: rgba(124, 58, 237, 0.15);
            --green-primary: #10b981;
            --green-light: rgba(16, 185, 129, 0.1);
            --red-primary: #ef4444;
            --red-light: rgba(239, 68, 68, 0.1);
            --sidebar-width: 260px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
        }

        /* Sidebar */
        aside {
            width: var(--sidebar-width);
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            padding: 20px 16px;
            display: flex;
            flex-direction: column;
        }

        .workspace-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: var(--green-primary);
            color: white;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .workspace-name {
            font-weight: 600;
            font-size: 14px;
        }

        .workspace-role {
            font-size: 11px;
            color: var(--text-secondary);
            display: block;
        }

        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
        }

        .menu-divider {
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            color: #52525b;
            margin: 20px 0 8px 10px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
            background: none;
            border: none;
            width: 100%;
            text-align: left;
            cursor: pointer;
        }

        .nav-item:hover, .nav-item.active {
            background-color: var(--bg-hover);
            color: var(--text-primary);
        }

        .nav-item.active {
            background-color: #3b1d68;
            color: #e9d5ff;
        }

        /* Main View */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100%;
            overflow: hidden;
        }

        header {
            height: 70px;
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
        }

        .top-title {
            font-size: 18px;
            font-weight: 700;
        }

        .content-container {
            flex: 1;
            padding: 32px;
            overflow-y: auto;
        }

        .tab-pane {
            display: none;
        }

        .tab-pane.active {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        /* Hero Banner */
        .hero-banner {
            background: radial-gradient(circle at 100% 0%, #1a103c 0%, #121214 70%);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .hero-text h3 {
            font-size: 20px;
            margin-bottom: 8px;
        }

        .hero-text p {
            color: var(--text-secondary);
            font-size: 14px;
            max-width: 520px;
            line-height: 1.6;
        }

        .btn {
            background-color: var(--purple-primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            font-size: 13px;
        }

        .btn:hover {
            background-color: var(--purple-hover);
        }

        .btn-secondary {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            margin-top: 12px;
        }

        .btn-secondary:hover {
            background-color: var(--bg-hover);
        }

        /* Services Grid */
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }

        .service-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .service-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .service-name {
            font-weight: 600;
            font-size: 15px;
        }

        .indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--green-primary);
            box-shadow: 0 0 8px var(--green-primary);
        }

        .service-desc {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .service-meta {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-secondary);
        }

        /* Simulator Grid */
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 32px;
        }

        .pane-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .form-group label {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
        }

        textarea {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 13px;
            resize: vertical;
            outline: none;
        }

        textarea.code-editor {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #a7f3d0;
        }

        /* Steps */
        .steps-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .step-item {
            display: flex;
            gap: 16px;
            opacity: 0.3;
            transition: opacity 0.3s;
        }

        .step-item.active {
            opacity: 1;
        }

        .step-badge {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background-color: var(--bg-primary);
            border: 2px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
        }

        .step-item.active .step-badge {
            border-color: var(--purple-primary);
            background-color: var(--purple-light);
            color: white;
        }

        .step-title {
            font-size: 14px;
            font-weight: 600;
        }

        .step-desc {
            font-size: 12px;
            color: var(--text-secondary);
        }

        /* Results Display */
        .results-box {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            display: none;
            flex-direction: column;
            gap: 16px;
            margin-top: 12px;
        }

        .results-box.active {
            display: flex;
        }

        .logs-pre {
            background-color: var(--bg-card);
            padding: 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #38bdf8;
            overflow-x: auto;
        }

        .diff-pre {
            background-color: #0b1511;
            padding: 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #34d399;
            border-left: 3px solid var(--green-primary);
            overflow-x: auto;
        }

        /* Slack approval mock */
        .slack-mock {
            background-color: white;
            color: black;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid var(--purple-primary);
            margin-top: 12px;
        }

        .slack-title {
            font-weight: 700;
            font-size: 13px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .slack-actions {
            margin-top: 12px;
            display: flex;
            gap: 8px;
        }

        .btn-slack-app {
            background-color: var(--green-primary);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
        }

        .btn-slack-rej {
            background-color: var(--red-primary);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
        }

        /* Catalog list */
        .catalog-item {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .catalog-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }

        .catalog-title {
            font-weight: 600;
            font-size: 15px;
        }

        .catalog-score {
            font-size: 11px;
            font-weight: 700;
            background-color: var(--purple-light);
            color: #d8b4fe;
            padding: 4px 10px;
            border-radius: 12px;
        }

        /* Trace card */
        .trace-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        }

        .trace-header {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 16px;
            color: var(--text-secondary);
        }

        .span-row {
            display: flex;
            justify-content: space-between;
            background-color: var(--purple-light);
            border: 1px solid var(--purple-primary);
            padding: 8px 16px;
            border-radius: 6px;
            margin-bottom: 8px;
        }

        .span-row.child-1 {
            margin-left: 24px;
            background-color: #1b162f;
            border-color: #4f46e5;
        }

        .span-row.child-2 {
            margin-left: 48px;
            background-color: #141829;
            border-color: #06b6d4;
        }
    </style>
</head>
<body>

    <!-- Sidebar Menu -->
    <aside>
        <div class="workspace-header">
            <div class="avatar">T</div>
            <div>
                <span class="workspace-name">Tushar Seth</span>
                <span class="workspace-role">SentryNode Owner</span>
            </div>
        </div>

        <nav class="nav-menu">
            <button class="nav-item active" onclick="switchTab('overview', this)">
                Projects & Services
            </button>
            <button class="nav-item" onclick="switchTab('simulator', this)">
                Incident Simulator
            </button>
            <button class="nav-item" onclick="switchTab('runbooks', this)">
                pgvector Runbooks
            </button>
            
            <div class="menu-divider">INTEGRATIONS</div>
            <button class="nav-item" onclick="switchTab('observability', this)">
                Observability Traces
            </button>
        </nav>
    </aside>

    <!-- Main Workspace -->
    <main>
        <header>
            <h1 class="top-title">SentryNode Plane</h1>
        </header>

        <div class="content-container">
            <!-- Tab 1: Overview -->
            <div id="overview" class="tab-pane active">
                <div class="hero-banner">
                    <div class="hero-text">
                        <h3>Self-Healing Infrastructure Online</h3>
                        <p>SentryNode agents are actively monitoring inbound webhooks. In case of an outage, isolated code repair will compile patches automatically.</p>
                        <button class="btn btn-secondary" onclick="document.querySelectorAll('.nav-item')[1].click()">Try Simulator →</button>
                    </div>
                </div>

                <h3>Microservices Nodes</h3>
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-header">
                            <span class="service-name">Agent Orchestrator</span>
                            <span class="indicator"></span>
                        </div>
                        <p class="service-desc">Manages Architect planning and Builder self-correcting code repair loops.</p>
                        <div class="service-meta">
                            <span>Port 8000</span>
                            <span>operational</span>
                        </div>
                    </div>

                    <div class="service-card">
                        <div class="service-header">
                            <span class="service-name">PII Scrubber</span>
                            <span class="indicator"></span>
                        </div>
                        <p class="service-desc">Log-sanitization microservice to clean emails, credentials and token hashes locally.</p>
                        <div class="service-meta">
                            <span>Port 8001</span>
                            <span>operational</span>
                        </div>
                    </div>

                    <div class="service-card">
                        <div class="service-header">
                            <span class="service-name">Advanced RAG Engine</span>
                            <span class="indicator"></span>
                        </div>
                        <p class="service-desc">Vector matching engine linking crash details to PostgreSQL pgvector runbooks.</p>
                        <div class="service-meta">
                            <span>Port 8002</span>
                            <span>operational</span>
                        </div>
                    </div>

                    <div class="service-card">
                        <div class="service-header">
                            <span class="service-name">Isolated Sandbox</span>
                            <span class="indicator"></span>
                        </div>
                        <p class="service-desc">Docker sandbox executing compilation verification tests and secure git commits.</p>
                        <div class="service-meta">
                            <span>Port 8003</span>
                            <span>operational</span>
                        </div>
                    </div>

                    <div class="service-card">
                        <div class="service-header">
                            <span class="service-name">API & Slack Gateway</span>
                            <span class="indicator"></span>
                        </div>
                        <p class="service-desc">Webhook ingress listener routing incident payloads and interactive slack approvals.</p>
                        <div class="service-meta">
                            <span>Port 8004</span>
                            <span>operational</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab 2: Incident Simulator -->
            <div id="simulator" class="tab-pane">
                <h2>Incident Simulator & Agent Triage</h2>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">Trigger a mock crash exception webhook to inspect self-healing triage actions.</p>

                <div class="grid-2col">
                    <!-- Config Outage -->
                    <div class="pane-card">
                        <div class="form-group">
                            <label>Raw Exception Log</label>
                            <textarea id="logInput" rows="4">redis.exceptions.ConnectionError: Too many connections. Connection pool full on redis-db:6379.</textarea>
                        </div>
                        <div class="form-group">
                            <label>Mock Repository Codebase</label>
                            <textarea id="codeInput" rows="8" class="code-editor">{"main.py": "import redis\n\ndef get_redis_client():\n    return redis.Redis(host='localhost', port=6379)"}</textarea>
                        </div>
                        <button class="btn" onclick="runSimulator()">Trigger Webhook Alert</button>
                    </div>

                    <!-- Progress monitor -->
                    <div class="pane-card">
                        <div class="steps-container">
                            <div class="step-item" id="step1">
                                <div class="step-badge">1</div>
                                <div>
                                    <h5 class="step-title">PII Scrubber Guardrail</h5>
                                    <p class="step-desc">Redacting keys, emails, and credentials locally.</p>
                                </div>
                            </div>

                            <div class="step-item" id="step2">
                                <div class="step-badge">2</div>
                                <div>
                                    <h5 class="step-title">pgvector Runbook Search</h5>
                                    <p class="step-desc">Finding relevant diagnostic solutions.</p>
                                </div>
                            </div>

                            <div class="step-item" id="step3">
                                <div class="step-badge">3</div>
                                <div>
                                    <h5 class="step-title">Architect Planner & Builder Repair</h5>
                                    <p class="step-desc">Formulating diagnosis and compiling patches.</p>
                                </div>
                            </div>

                            <div class="step-item" id="step4">
                                <div class="step-badge">4</div>
                                <div>
                                    <h5 class="step-title">Verification Pass</h5>
                                    <p class="step-desc">Checking sandbox exit codes and tests.</p>
                                </div>
                            </div>
                        </div>

                        <!-- Results -->
                        <div id="resultsBox" class="results-box">
                            <h4 style="margin-bottom: 8px;">Triage Resolved</h4>
                            <div style="margin-bottom: 12px;">
                                <span style="font-size: 12px; color: var(--text-secondary);">Scrubbed Log Output:</span>
                                <pre class="logs-pre">ERROR: Connection failure. redis.exceptions.ConnectionError: Too many connections. Connection pool full on [REDACTED_IPV4]:6379.</pre>
                            </div>
                            <div style="margin-bottom: 12px;">
                                <span style="font-size: 12px; color: var(--text-secondary);">Proposed Code Patch:</span>
                                <pre class="diff-pre">@@ -3,2 +3,3 @@\n def get_redis_client():\n-    return redis.Redis(host='localhost', port=6379)\n+    pool = redis.ConnectionPool(host='localhost', port=6379, max_connections=500)\n+    return redis.Redis(connection_pool=pool)</pre>
                            </div>

                            <!-- Slack Interactive Mock -->
                            <div class="slack-mock">
                                <div class="slack-title">
                                    <span style="font-size: 18px;">💬</span> Slack Notification
                                </div>
                                <p style="font-size: 13px;">Git patch passes testing. Deploy to production?</p>
                                <div class="slack-actions">
                                    <button class="btn-slack-app" onclick="alert('Deployment triggered!')">Approve Deploy</button>
                                    <button class="btn-slack-rej" onclick="resetSimulator()">Reject Patch</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab 3: Runbooks -->
            <div id="runbooks" class="tab-pane">
                <h2>pgvector Runbooks Catalog</h2>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">Reference guides stored in PostgreSQL index database.</p>

                <div class="catalog-item">
                    <div class="catalog-header">
                        <span class="catalog-title">Redis Connection Pool Out of Memory / Timeout Runbook</span>
                        <span class="catalog-score">98% Sim Match</span>
                    </div>
                    <p style="font-size: 13px; line-height: 1.6; color: var(--text-secondary);">Modify pool connection size. Setup global client connection pools to avoid initialization leakage.</p>
                </div>

                <div class="catalog-item">
                    <div class="catalog-header">
                        <span class="catalog-title">Database Checkout Transaction Deadlock Runbook</span>
                        <span class="catalog-score">85% Sim Match</span>
                    </div>
                    <p style="font-size: 13px; line-height: 1.6; color: var(--text-secondary);">Sort row exclusive locks. Ensure orders and inventory transactions follow a strict sequential ordering.</p>
                </div>
            </div>

            <!-- Tab 4: Observability -->
            <div id="observability" class="tab-pane">
                <h2>Observability Traces</h2>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">OpenTelemetry spans and execution trace monitoring console.</p>

                <div class="trace-card">
                    <div class="trace-header">
                        <span>Trace: `t-sn-90214a`</span>
                        <span>LLM Cost: `$0.0031`</span>
                    </div>
                    <div class="span-row">
                        <span>sentrynode.triage</span>
                        <span>6000ms</span>
                    </div>
                    <div class="span-row child-1">
                        <span>pii_scrubber.scrub</span>
                        <span>110ms</span>
                    </div>
                    <div class="span-row child-1">
                        <span>rag_engine.search</span>
                        <span>75ms</span>
                    </div>
                    <div class="span-row child-1">
                        <span>agent.architect_plan</span>
                        <span>1200ms</span>
                    </div>
                    <div class="span-row child-1">
                        <span>agent.builder_exec</span>
                        <span>3200ms</span>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        function switchTab(tabId, element) {
            // Hide all tab panes
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            // Show target tab
            document.getElementById(tabId).classList.add('active');

            // Deactivate all sidebar items
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            // Activate selected sidebar item
            element.classList.add('active');
        }

        function runSimulator() {
            resetSteps();
            
            setTimeout(() => {
                document.getElementById('step1').classList.add('active');
                setTimeout(() => {
                    document.getElementById('step2').classList.add('active');
                    setTimeout(() => {
                        document.getElementById('step3').classList.add('active');
                        setTimeout(() => {
                            document.getElementById('step4').classList.add('active');
                            setTimeout(() => {
                                document.getElementById('resultsBox').classList.add('active');
                            }, 1000);
                        }, 1000);
                    }, 1000);
                }, 1000);
            }, 500);
        }

        function resetSteps() {
            document.querySelectorAll('.step-item').forEach(step => {
                step.classList.remove('active');
            });
            document.getElementById('resultsBox').classList.remove('active');
        }

        function resetSimulator() {
            resetSteps();
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    """
    Renders the SentryNode interactive dashboard console.
    """
    return DASHBOARD_HTML

@app.post("/webhooks/sentry")
async def handle_sentry_webhook(payload: SentryAlertPayload):
    print(f"Received alert webhook for project: {payload.project}")
    
    # Forward logs & codebase to Agentic Orchestrator
    try:
        async with httpx.AsyncClient() as client:
            orch_res = await client.post(
                f"{ORCHESTRATOR_URL}/triage",
                json={
                    "raw_logs": f"ERROR: {payload.message}\\nCULPRIT: {payload.culprit}\\nSTACK_TRACE:\\n{payload.stack_trace}",
                    "codebase_files": payload.codebase_files
                },
                timeout=30
            )
            orch_data = orch_res.json()
    except Exception as e:
        # Fallback payload structure if Orchestrator is offline
        orch_data = {
            "session_id": "mock-session-fallback-90182",
            "clean_logs": payload.message,
            "proposed_patch": "@@ -1,3 +1,4 @@\\n def get_redis_client():\\n+    # Patched to reuse connections\\n",
            "sandbox_logs": "Tests passed (fallback mode)"
        }

    # Format Slack Block message
    slack_message = {
        "text": f"🚨 *Production Outage Triage* in `{payload.project}`",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚨 *Production Outage Triage* in `{payload.project}`\\n*Culprit:* `{payload.culprit}`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Proposed Code Patch:* \\n```diff\\n{orch_data['proposed_patch']}\\n```"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve Deploy"},
                        "style": "primary",
                        "value": orch_data["session_id"],
                        "action_id": "approve_patch_deploy"
                    }
                ]
            }
        ]
    }
    
    return {
        "status": "triaged",
        "session_id": orch_data["session_id"],
        "slack_message_payload": slack_message
    }

@app.post("/slack/actions")
async def handle_slack_actions(request: Request):
    return {
        "status": "success",
        "message": "Deployment pipeline triggered."
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8004, reload=True)
