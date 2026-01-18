from fastapi import Header
import uuid

def get_identifier(x_client_id: str | None = Header(None)):
    return x_client_id or str(uuid.uuid4())
