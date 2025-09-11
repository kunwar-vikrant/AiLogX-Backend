from auth import authenticate
from utils import greet
from ailogx.core import LLMLogger

log = LLMLogger("sample-app")

def main():
    try:
        log.llm_info("Starting authentication", inputs={"user": "admin"})
        result = authenticate("admin", "wrong-password")
        greet("admin")
    except Exception as e:
        log.llm_error("Authentication failed", reason=str(e), exception=e)

if __name__ == "__main__":
    main()
