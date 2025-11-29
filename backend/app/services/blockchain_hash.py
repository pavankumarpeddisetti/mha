import hashlib

def generate_sha256_hash(text: str) -> str:
    """
    Generates SHA-256 hash from certificate text or any string.
    """
    sha = hashlib.sha256()
    sha.update(text.encode("utf-8"))
    return sha.hexdigest()
