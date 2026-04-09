import pandas as pd
import time
import os

input_path = "data/processed/processed_transactions.csv"
output_path = "data/processed/scored_transactions.csv"

def calculate_risk(row):
    score = 0

    if row["amount"] > 200000:
        score += 2

    if row["avg_transaction_amount"] > 150000:
        score += 2

    if row["transaction_count"] > 3:
        score += 1

    if row["total_amount"] > 500000:
        score += 2

    return score

def run_scoring():
    print("Starting risk scoring...\n")

    last_processed_row = 0

    while True:
        if not os.path.exists(input_path):
            time.sleep(1)
            continue

        df = pd.read_csv(input_path)

        new_data = df.iloc[last_processed_row:]

        if new_data.empty:
            time.sleep(1)
            continue

        for _, row in new_data.iterrows():
            score = calculate_risk(row)
            risk_flag = 1 if score >= 4 else 0

            scored_row = row.to_dict()
            scored_row.update({
                "risk_score": score,
                "risk_flag": risk_flag
            })

            pd.DataFrame([scored_row]).to_csv(
                output_path,
                mode='a',
                header=not os.path.exists(output_path),
                index=False
            )

            print(f"Scored → User: {row['customer_id']} | Score: {score} | Flag: {risk_flag}")

        last_processed_row = len(df)

        time.sleep(1)

if __name__ == "__main__":
    run_scoring()
