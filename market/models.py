from dataclasses import dataclass


@dataclass
class Security:
    exchange: str
    security_id: int