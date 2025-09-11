from ailogx.trace.trace_summarizer import summarize_by_trace

def test_summarize_by_trace_basic(monkeypatch):

    # Mock analyzer
    class DummyAnalyzer:
        def summarize_logs(self, text):
            return f"Summary for: {text[:30]}..."

    logs = [
        {"trace_id": "abc", "message": "User login", "function": "auth", "file": "auth.py"},
        {"trace_id": "abc", "message": "2FA failed", "function": "auth", "file": "auth.py"},
        {"trace_id": "xyz", "message": "Checkout started", "function": "cart", "file": "checkout.py"}
    ]

    result = summarize_by_trace(logs, DummyAnalyzer())
    assert "abc" in result and "xyz" in result
    assert "User login" in result["abc"]
