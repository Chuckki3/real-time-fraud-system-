import pandas as pd
import random
import time
import os
from datetime import datetime

# ✅ Create folder if it doesn't exist
os.makedirs("data/raw_stream", exist_ok=True)

file_path = "data/raw_stream/transactions_stream.csv"

# Sample users and transaction types
users = [f"user_{i}" for i in range(1, 101)]
transaction_types = ["PAYMENT", "TRANSFER", "CASH_OUT"]

# Generate one transaction
def generate_transaction():
    return {
        "timestamp": datetime.now(),
        "customer_id": random.choice(users),
        "amount": round(random.uniform(100, 500000), 2),
        "transaction_type": random.choice(transaction_types),
        "is_fraud": random.choice([0, 0, 0, 1])  # imbalanced fraud simulation
    }

# Stream transactions (LIMITED for testing)
def stream_transactions(n=20, delay=1):
    print(f"Starting stream for {n} transactions...\n")
    
    for i in range(n):
        txn = generate_transaction()
        df = pd.DataFrame([txn])

        # Write to CSV (append mode)
        df.to_csv(
            file_path,
            mode='a',
            header=not os.path.exists(file_path),
            index=False
        )

        print(f"{i+1}: New Transaction → {txn}")
        
        time.sleep(delay)

    print("\n✅ Streaming complete!")

# Run the stream
stream_transactions(n=20, delay=1)
