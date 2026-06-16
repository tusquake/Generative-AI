import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="SentryNode PII Scrubber",
    description="Local log-sanitization service to prevent exfiltration of customer PII."
)

class LogPayload(BaseModel):
    raw_logs: str

class ScrubbedPayload(BaseModel):
    clean_logs: str
    redacted_count: int

# Compiled regex patterns for common PII tokens
PII_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    "ipv4": re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"),
    "jwt": re.compile(r"eyJhbGciOi[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"),
    "api_key": re.compile(r"\b(?:api_key|apikey|secret|password|passwd|token)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})\b", re.IGNORECASE),
    "private_key": re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----[a-zA-Z0-9\/\+\s\=]+-----END [A-Z ]+ PRIVATE KEY-----", re.MULTILINE),
}

def scrub_text(text: str) -> tuple[str, int]:
    clean_text = text
    total_redacted = 0
    
    # 1. Apply regex-based rules
    for pii_type, pattern in PII_PATTERNS.items():
        matches = pattern.findall(clean_text)
        if matches:
            total_redacted += len(matches)
            if pii_type == "api_key":
                # For api keys, only replace the captured key token to avoid breaking the label
                for match in matches:
                    clean_text = clean_text.replace(match, "[REDACTED_API_KEY]")
            else:
                clean_text = pattern.sub(f"[REDACTED_{pii_type.upper()}]", clean_text)
                
    # 2. Simulated Local SLM Named Entity Recognition (NER) pass
    # (Simulating extraction of named entities like names or credit cards)
    credit_card_pattern = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
    cc_matches = credit_card_pattern.findall(clean_text)
    if cc_matches:
        total_redacted += len(cc_matches)
        clean_text = credit_card_pattern.sub("[REDACTED_CREDIT_CARD]", clean_text)
        
    return clean_text, total_redacted

@app.post("/scrub", response_model=ScrubbedPayload)
def scrub_logs(payload: LogPayload):
    try:
        clean_logs, count = scrub_text(payload.raw_logs)
        return ScrubbedPayload(clean_logs=clean_logs, redacted_count=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scrubbing error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
