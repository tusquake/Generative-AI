import httpx

RUNBOOKS = [
    {
        "title": "Redis Connection Pool Out of Memory / Timeout Runbook",
        "content": """Symptoms: logs display 'redis.exceptions.ConnectionError: Too many connections' or Redis command timeouts.

Diagnosis: Check total connection count using 'redis-cli info clients'. If clients count is > 10000, clients are not closing connections properly.

Resolution: Adjust the application pool settings. Modify the redis pool configuration class to set `max_connections=500`. Ensure that connection pools are reused globally rather than initialized on every request.

Verification: Run `redis-cli info clients` and assert total clients is below 100."""
    },
    {
        "title": "Database Checkout Transaction Deadlock Runbook",
        "content": """Symptoms: API calls to `/checkout` fail with 'psycopg2.errors.DeadlockDetected' under high concurrency checkout load.

Diagnosis: Check Postgres locks using query `SELECT * FROM pg_locks`. Look for overlapping row-exclusive locks.

Resolution: Ensure that row-locking happens in a sorted order. Modify update operations so that the `inventory` table update always executes before the `orders` table insertion inside the SQL transaction block.

Verification: Run checkout concurrency load test and assert 0 deadlock exceptions are raised."""
    },
    {
        "title": "NodeJS OOM Memory Leak Diagnostic Runbook",
        "content": """Symptoms: Container crashes repeatedly with code 'Exit Code 137' (OOM-killed).

Diagnosis: Inspect memory profiles using heap snapshot tools. Look for accumulating event listeners or closure leaks.

Resolution: Clear intervals and remove event listeners during shutdown hooks. Increase container memory limit in deployment configuration from 512Mi to 1Gi.

Verification: Run application under simulated load and track heap size stability using PM2 or metrics dashboards."""
    }
]

def seed():
    print("Starting database runbook seeding...")
    url = "http://localhost:8002/index"
    for r in RUNBOOKS:
        try:
            response = httpx.post(url, json=r, timeout=10)
            if response.status_code == 200:
                print(f"Successfully seeded: {r['title']}")
            else:
                print(f"Failed to seed '{r['title']}': {response.text}")
        except Exception as e:
            print(f"Failed to connect to RAG service at {url}: {e}. Ensure the service is running.")

if __name__ == "__main__":
    seed()
