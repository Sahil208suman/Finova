
from dataclasses import dataclass

@dataclass
class Transaction:
    description: str
    amount: float
    transaction_type: str
    category: str