import React, { useState, useEffect } from "react";
import {
  Layers,
  FileCode,
  Globe,
  Settings,
  Shield,
  Activity,
  Terminal,
  Search,
  Plus,
  Play,
  RotateCw,
  CheckCircle,
  AlertTriangle,
  FileText,
  User,
  ExternalLink,
  BookOpen,
  ArrowRight,
  Database,
  Slack,
  Sparkles
} from "lucide-react";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("overview");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedService, setSelectedService] = useState(null);
  const [rawLogs, setRawLogs] = useState(
    "redis.exceptions.ConnectionError: Too many connections. Connection pool full on redis-db:6379."
  );
  const [codebaseFiles, setCodebaseFiles] = useState(
    JSON.stringify(
      {
        "main.py": 'import redis\n\n# Connection pool setup\ndef get_redis_client():\n    # Inefficient connection allocation\n    return redis.Redis(host="localhost", port=6379, db=0)\n',
        "test_main.py": "def test_redis():\n    assert True"
      },
      null,
      2
    )
  );

  const [triageLogs, setTriageLogs] = useState(null);
  const [triageStatus, setTriageStatus] = useState("idle"); // idle | running | success | error
  const [activeStep, setActiveStep] = useState(0);

  // Microservices list mapping SentryNode services
  const services = [
    {
      id: "orchestrator",
      name: "Agent Orchestrator",
      port: 8000,
      status: "healthy",
      description: "Main controller managing planning, repair loops, and verification passes.",
      lastTrigger: "3 mins ago",
      connections: 12
    },
    {
      id: "pii-scrubber",
      name: "PII Scrubber",
      port: 8001,
      status: "healthy",
      description: "Log-sanitization service scrubbing passwords, emails, and API keys locally.",
      lastTrigger: "12 mins ago",
      connections: 8
    },
    {
      id: "rag-service",
      name: "Advanced RAG Engine",
      port: 8002,
      status: "healthy",
      description: "Embeddings vector matching engine connecting incidents to runbooks.",
      lastTrigger: "Just now",
      connections: 4
    },
    {
      id: "sandbox",
      name: "Isolated Sandbox Runner",
      port: 8003,
      status: "healthy",
      description: "Docker sandbox executing command verification and codebase testing.",
      lastTrigger: "1 hour ago",
      connections: 2
    },
    {
      id: "gateway",
      name: "API & Slack Gateway",
      port: 8004,
      status: "healthy",
      description: "Ingestion gateway routing webhook events and Slack integrations.",
      lastTrigger: "4 mins ago",
      connections: 15
    }
  ];

  // Seeded Runbooks in pgvector database
  const seededRunbooks = [
    {
      id: 1,
      title: "Redis Connection Pool Out of Memory / Timeout Runbook",
      desc: "Adjust the application pool settings. Modify the redis pool configuration class to set max_connections=500. Ensure connection pools are reused globally.",
      matchRatio: "98% Sim Score"
    },
    {
      id: 2,
      title: "Database Checkout Transaction Deadlock Runbook",
      desc: "Ensure row-locking happens in a sorted order. Modify update operations so that the inventory table update always executes before orders table insertion.",
      matchRatio: "85% Sim Score"
    },
    {
      id: 3,
      title: "NodeJS OOM Memory Leak Diagnostic Runbook",
      desc: "Clear intervals and remove event listeners during shutdown hooks. Increase container memory limit in deployment configuration from 512Mi to 1Gi.",
      matchRatio: "71% Sim Score"
    }
  ];

  const handleSimulateOutage = () => {
    setTriageStatus("running");
    setActiveStep(1);
    
    // Simulate step execution times
    setTimeout(() => {
      setActiveStep(2);
      setTimeout(() => {
        setActiveStep(3);
        setTimeout(() => {
          setActiveStep(4);
          setTimeout(() => {
            setTriageStatus("success");
            // Set mock response data
            setTriageLogs({
              session_id: "sentrynode-session-5b12a-89f41",
              clean_logs: "ERROR: [REDACTED_EMAIL] reported connection failure. redis.exceptions.ConnectionError: Too many connections. Connection pool full on [REDACTED_IPV4]:6379.",
              diagnosis_plan: "PLAN:\n1. Open main.py and examine get_redis_client.\n2. Configure a single connection pool with max_connections limit.\n3. Run test command: 'python -m pytest'.",
              proposed_patch: '@@ -3,4 +3,5 @@\n def get_redis_client():\n-    return redis.Redis(host="localhost", port=6379, db=0)\n+    pool = redis.ConnectionPool(host="localhost", port=6379, db=0, max_connections=500)\n+    return redis.Redis(connection_pool=pool)',
              sandbox_logs: "pytest -v\n====== 1 passed, 0 failed in 0.45s ======\nExit Code: 0 (Success)"
            });
          }, 1500);
        }, 1500);
      }, 1500);
    }, 1500);
  };

  const handleResetSimulator = () => {
    setTriageStatus("idle");
    setTriageLogs(null);
    setActiveStep(0);
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation (Render.com inspired styling) */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="avatar-circle">T</div>
          <div className="workspace-details">
            <span className="workspace-name">Tushar Seth</span>
            <span className="plan-tag">SentryNode Owner</span>
          </div>
        </div>

        <nav className="nav-menu">
          <button
            className={`nav-item ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            <Layers size={18} />
            <span>Projects & Services</span>
          </button>
          
          <button
            className={`nav-item ${activeTab === "simulator" ? "active" : ""}`}
            onClick={() => setActiveTab("simulator")}
          >
            <Terminal size={18} />
            <span>Incident Simulator</span>
          </button>

          <button
            className={`nav-item ${activeTab === "runbooks" ? "active" : ""}`}
            onClick={() => setActiveTab("runbooks")}
          >
            <BookOpen size={18} />
            <span>pgvector Runbooks</span>
          </button>

          <div className="menu-divider">INTEGRATIONS</div>

          <button
            className={`nav-item ${activeTab === "observability" ? "active" : ""}`}
            onClick={() => setActiveTab("observability")}
          >
            <Activity size={18} />
            <span>Observability Traces</span>
          </button>

          <button className="nav-item">
            <Globe size={18} />
            <span>Webhooks</span>
          </button>

          <button className="nav-item">
            <Shield size={18} />
            <span>Security Policies</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <a href="#" className="footer-link">Changelog</a>
          <a href="#" className="footer-link">SentryNode Status</a>
        </div>
      </aside>

      {/* Main Panel */}
      <main className="main-panel">
        {/* Header Bar */}
        <header className="topbar">
          <div className="topbar-left">
            <h1 className="top-title">SentryNode Plane</h1>
          </div>
          <div className="topbar-right">
            <div className="search-box">
              <Search size={16} />
              <input
                type="text"
                placeholder="Search resources..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <span className="search-shortcut">⌘ K</span>
            </div>
            <button className="btn btn-purple" onClick={() => setActiveTab("simulator")}>
              <Plus size={16} />
              <span>New Simulation</span>
            </button>
            <div className="profile-icon">
              <User size={18} />
            </div>
          </div>
        </header>

        {/* Content Body */}
        <div className="content-body">
          {activeTab === "overview" && (
            <div className="tab-pane">
              <div className="overview-header">
                <h2>Services Overview</h2>
                <div className="flex-row gap-1">
                  <span className="badge badge-success">
                    <CheckCircle size={14} />
                    All nodes operational
                  </span>
                </div>
              </div>

              {/* Get Organized card inspired by Render */}
              <div className="get-organized-card">
                <div className="card-text">
                  <h3><Sparkles size={20} className="purple-icon" /> Self-Healing Infrastructure Enabled</h3>
                  <p>
                    SentryNode agent loops are actively monitoring Sentry & Datadog ingestion lines. 
                    Any exception will trigger isolated docker code repair.
                  </p>
                  <div className="flex-row gap-1 mt-1">
                    <button className="btn btn-white" onClick={() => setActiveTab("simulator")}>
                      Try Simulator <ArrowRight size={14} />
                    </button>
                  </div>
                </div>
                <div className="card-preview">
                  <div className="preview-terminal">
                    <div className="terminal-header">
                      <span className="dot dot-red"></span>
                      <span className="dot dot-yellow"></span>
                      <span className="dot dot-green"></span>
                      <span className="terminal-title">sentrynode-agent</span>
                    </div>
                    <pre className="terminal-content">
                      {`$ sentrynode --monitor
[INFO] LogScrubber service online on port 8001
[INFO] VectorStore loaded with 3 runbooks
[INFO] Agent sandbox pool initialized (3 containers)
[INFO] Awaiting Sentry webhook payload...`}
                    </pre>
                  </div>
                </div>
              </div>

              <h3 className="section-title">Microservices List</h3>
              <div className="services-grid">
                {services.map((svc) => (
                  <div
                    key={svc.id}
                    className={`service-card ${selectedService?.id === svc.id ? "selected" : ""}`}
                    onClick={() => setSelectedService(svc)}
                  >
                    <div className="service-card-header">
                      <div className="flex-row gap-1">
                        <Database size={20} className="gray-icon" />
                        <h4 className="service-name">{svc.name}</h4>
                      </div>
                      <span className="status-indicator healthy"></span>
                    </div>
                    <p className="service-description">{svc.description}</p>
                    <div className="service-card-footer">
                      <span>Port {svc.port}</span>
                      <span>{svc.lastTrigger}</span>
                    </div>
                  </div>
                ))}
              </div>

              {selectedService && (
                <div className="service-details-panel">
                  <div className="details-header">
                    <h4>{selectedService.name} Logs</h4>
                    <button className="btn-close" onClick={() => setSelectedService(null)}>×</button>
                  </div>
                  <pre className="details-logs">
                    {`[INFO] 2026-06-13T13:02:14Z Starting service on 0.0.0.0:${selectedService.port}
[INFO] 2026-06-13T13:02:15Z Database connected pool size: ${selectedService.connections}
[INFO] 2026-06-13T13:05:00Z Health check request received - Status: 200 OK
[INFO] 2026-06-13T13:05:45Z Handling action trigger payload... Done.`}
                  </pre>
                </div>
              )}
            </div>
          )}

          {activeTab === "simulator" && (
            <div className="tab-pane">
              <h2>Incident Simulator & Self-Correction Loop</h2>
              <p className="text-secondary mb-2">
                Simulate a real production crash. This input will trigger the local PII scrubbing, 
                runbook search, Architect planning, and Builder compile loop.
              </p>

              <div className="grid-2col">
                {/* Left Col: Setup Outage */}
                <div className="input-card">
                  <div className="form-group">
                    <label>Raw Exception Log Input</label>
                    <textarea
                      rows={4}
                      value={rawLogs}
                      onChange={(e) => setRawLogs(e.target.value)}
                      disabled={triageStatus === "running"}
                    />
                  </div>

                  <div className="form-group">
                    <label>Mock Codebase Repository Files (JSON)</label>
                    <textarea
                      rows={8}
                      className="code-editor"
                      value={codebaseFiles}
                      onChange={(e) => setCodebaseFiles(e.target.value)}
                      disabled={triageStatus === "running"}
                    />
                  </div>

                  <div className="flex-row gap-1 mt-1">
                    {triageStatus === "idle" && (
                      <button className="btn btn-purple btn-large" onClick={handleSimulateOutage}>
                        <Play size={16} />
                        <span>Trigger Webhook Alert</span>
                      </button>
                    )}
                    {triageStatus === "running" && (
                      <button className="btn btn-purple btn-large disabled" disabled>
                        <RotateCw className="spin" size={16} />
                        <span>Running Agent Triage...</span>
                      </button>
                    )}
                    {triageStatus === "success" && (
                      <button className="btn btn-white btn-large" onClick={handleResetSimulator}>
                        <span>Reset Simulator</span>
                      </button>
                    )}
                  </div>
                </div>

                {/* Right Col: Triage Progress Monitor */}
                <div className="output-card">
                  <div className="triage-steps">
                    <div className={`triage-step ${activeStep >= 1 ? "active" : ""}`}>
                      <div className="step-circle">{activeStep > 1 ? "✓" : "1"}</div>
                      <div className="step-content">
                        <h5>PII Scrubber Guardrail</h5>
                        <p>Removing emails and API tokens locally.</p>
                      </div>
                    </div>

                    <div className={`triage-step ${activeStep >= 2 ? "active" : ""}`}>
                      <div className="step-circle">{activeStep > 2 ? "✓" : "2"}</div>
                      <div className="step-content">
                        <h5>RAG Runbook Matches</h5>
                        <p>Searching pgvector runbook index.</p>
                      </div>
                    </div>

                    <div className={`triage-step ${activeStep >= 3 ? "active" : ""}`}>
                      <div className="step-circle">{activeStep > 3 ? "✓" : "3"}</div>
                      <div className="step-content">
                        <h5>Architect Planner & Code Patcher</h5>
                        <p>Drafting repair diff & executing compile tests.</p>
                      </div>
                    </div>

                    <div className={`triage-step ${activeStep >= 4 ? "active" : ""}`}>
                      <div className="step-circle">{activeStep >= 4 ? "✓" : "4"}</div>
                      <div className="step-content">
                        <h5>Verification Pass</h5>
                        <p>Validating sandbox compliance.</p>
                      </div>
                    </div>
                  </div>

                  {triageLogs && (
                    <div className="agent-results-box">
                      <div className="results-header">
                        <h4>Agent Diagnosis Outputs</h4>
                        <span className="badge badge-success">Triage Resolved</span>
                      </div>
                      
                      <div className="result-section">
                        <h6>Scrubbed Log Output:</h6>
                        <pre className="logs-pre">{triageLogs.clean_logs}</pre>
                      </div>

                      <div className="result-section">
                        <h6>Proposed Code Patch (Diff):</h6>
                        <pre className="diff-pre">{triageLogs.proposed_patch}</pre>
                      </div>

                      <div className="result-section">
                        <h6>Sandbox Verification Output:</h6>
                        <pre className="logs-pre">{triageLogs.sandbox_logs}</pre>
                      </div>

                      {/* Approval Box */}
                      <div className="slack-approval-mimic">
                        <div className="slack-header">
                          <Slack size={18} className="slack-brand-icon" />
                          <span>Interactive Slack Notification Sent</span>
                        </div>
                        <p>A git patch is ready. Deploy automatically?</p>
                        <div className="flex-row gap-1 mt-1">
                          <button className="btn btn-success" onClick={() => alert("Deployment triggered successfully!")}>
                            Approve Deploy
                          </button>
                          <button className="btn btn-danger" onClick={handleResetSimulator}>
                            Reject Patch
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === "runbooks" && (
            <div className="tab-pane">
              <h2>pgvector Advanced Runbook Catalog</h2>
              <p className="text-secondary mb-2">
                Reference guidelines stored in PostgreSQL. Embeddings are created dynamically using text-embedding-004.
              </p>

              <div className="runbooks-list">
                {seededRunbooks.map((rb) => (
                  <div key={rb.id} className="runbook-item">
                    <div className="runbook-header">
                      <div className="flex-row gap-1">
                        <FileText size={20} className="purple-icon" />
                        <h5>{rb.title}</h5>
                      </div>
                      <span className="badge badge-purple">{rb.matchRatio}</span>
                    </div>
                    <p className="runbook-desc">{rb.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "observability" && (
            <div className="tab-pane">
              <h2>Observability & Tracing Console</h2>
              <p className="text-secondary mb-2">
                Simulated OpenTelemetry spans for Agent reasoning paths.
              </p>

              <div className="trace-card">
                <div className="trace-header">
                  <span>Trace ID: `t-sn-90184b2`</span>
                  <span>Cost: `$0.0045`</span>
                </div>
                <div className="trace-spans">
                  <div className="trace-span-row">
                    <span className="span-name">sentrynode.triage</span>
                    <span className="span-duration">6000ms</span>
                  </div>
                  <div className="trace-span-row child-1">
                    <span className="span-name">pii_scrubber.scrub</span>
                    <span className="span-duration">120ms</span>
                  </div>
                  <div className="trace-span-row child-1">
                    <span className="span-name">rag_engine.search</span>
                    <span className="span-duration">85ms</span>
                  </div>
                  <div className="trace-span-row child-1">
                    <span className="span-name">agent.architect_plan</span>
                    <span className="span-duration">1500ms</span>
                  </div>
                  <div className="trace-span-row child-1">
                    <span className="span-name">agent.builder_exec</span>
                    <span className="span-duration">3000ms</span>
                  </div>
                  <div className="trace-span-row child-2">
                    <span className="span-name">sandbox.execute_tests</span>
                    <span className="span-duration">800ms</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
