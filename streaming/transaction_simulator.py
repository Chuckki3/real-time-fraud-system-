import pandas as pd
import random
import time
import os
from datetime import datetime

file_path = "/content/data/raw_stream/transactions_stream.csv"

users = [f"user_{i}" for i in range(1, 101)]
transaction_types = ["PAYMENT", "TRANSFER", "CASH_OUT"]

def generate_transaction():
    return {
        "timestamp": datetime.now(),
        "customer_id": random.choice(users),
        "amount": round(random.uniform(100, 500000), 2),
        "transaction_type": random.choice(transaction_types),
        "is_fraud": random.choice([0, 0, 0, 1])
    }

def stream_transactions(n=20):
    print("Streaming transactions...\n")

    for i in range(n):
        txn = generate_transaction()
        df = pd.DataFrame([txn])

        df.to_csv(
            file_path,
            mode='a',
            header=not os.path.exists(file_path),
            index=False
        )

        print(f"{i+1}: {txn}")

        time.sleep(0.5)

    print("\n✅ Done streaming!")

# Run it
stream_transactions(20)

# Run the stream
stream_transactions(n=20, delay=1)
