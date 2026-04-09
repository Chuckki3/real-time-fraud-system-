import pandas as pd
import time
import os

file_path = "data/raw_stream/transactions_stream.csv"
processed_path = "data/processed/processed_transactions.csv"

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

# Store user behavior in memory
user_state = {}

def process_stream():
    print("Starting stream processing...\n")

    last_processed_row = 0

    while True:
        if not os.path.exists(file_path):
            time.sleep(1)
            continue

        df = pd.read_csv(file_path)

        # Only process new rows
        new_data = df.iloc[last_processed_row:]

        if new_data.empty:
            time.sleep(1)
            continue

        for _, row in new_data.iterrows():
            user = row["customer_id"]
            amount = row["amount"]

            # Initialize user state
            if user not in user_state:
                user_state[user] = {
                    "transaction_count": 0,
                    "total_amount": 0
                }

            # Update state
            user_state[user]["transaction_count"] += 1
            user_state[user]["total_amount"] += amount

            # Compute features
            txn_count = user_state[user]["transaction_count"]
            total_amt = user_state[user]["total_amount"]
            avg_amt = total_amt / txn_count

            processed_row = row.to_dict()
            processed_row.update({
                "transaction_count": txn_count,
                "total_amount": total_amt,
                "avg_transaction_amount": avg_amt
            })

            # Save processed row
            pd.DataFrame([processed_row]).to_csv(
                processed_path,
                mode='a',
                header=not os.path.exists(processed_path),
                index=False
            )

            print(f"Processed → {user} | Count: {txn_count} | Avg: {avg_amt:.2f}")

        last_processed_row = len(df)

        time.sleep(1)

if __name__ == "__main__":
    process_stream()
