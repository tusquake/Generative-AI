import re

def content_safety_guardrail(text: str):
    """
    Simulates a rule-based guardrail to detect PII.
    """
    # Simple regex for a Credit Card number
    cc_pattern = r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
    
    if re.search(cc_pattern, text):
        print("[GUARDRAIL ALERT] Sensitive information detected!")
        return "[REDACTED]"
    
    return text

def run_guardrail_demo():
    raw_ai_output = "I have successfully processed the payment for card 4111 2222 3333 4444."
    
    print(f"RAW OUTPUT: {raw_ai_output}")
    
    safe_output = content_safety_guardrail(raw_ai_output)
    
    print("-" * 50)
    print(f"SAFE OUTPUT: {safe_output}")
    print("-" * 50)
    print("[Senior Note] Modern frameworks like NeMo Guardrails use "
          "mini-LLMs to check for 'Tone' and 'Intent' rather than just Regex.")

if __name__ == "__main__":
    run_guardrail_demo()
