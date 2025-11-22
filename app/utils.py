def sanitize_text(s: str) -> str:
    if not s:
        return ''
    return ' '.join(s.split())[:5000]
