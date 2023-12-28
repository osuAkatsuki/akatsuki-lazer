import hashlib

def calculate_md5(input: str) -> str:
    return hashlib.md5(input.encode()).hexdigest()