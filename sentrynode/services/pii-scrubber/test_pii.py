from app import scrub_text

def test_email_redaction():
    raw = "Contact support at user.name@domain.com for billing issues."
    clean, count = scrub_text(raw)
    assert "[REDACTED_EMAIL]" in clean
    assert "user.name@domain.com" not in clean
    assert count == 1

def test_api_key_redaction():
    raw = "Setting api_key = 'sk-proj1234567890abcdef' inside environment."
    clean, count = scrub_text(raw)
    assert "[REDACTED_API_KEY]" in clean
    assert "sk-proj1234567890abcdef" not in clean
    assert count == 1

def test_ip_address_redaction():
    raw = "Connection failed from source server at 192.168.1.45 to backend."
    clean, count = scrub_text(raw)
    assert "[REDACTED_IPV4]" in clean
    assert "192.168.1.45" not in clean
    assert count == 1

def test_multiple_redactions():
    raw = "Send email to customer@gmail.com. API key: token='ab12cd34ef56gh78'. DB IP is 10.0.0.1."
    clean, count = scrub_text(raw)
    assert "[REDACTED_EMAIL]" in clean
    assert "[REDACTED_API_KEY]" in clean
    assert "[REDACTED_IPV4]" in clean
    assert count == 3
