import pandas as pd
import os

def find_revision_order_mismatches(file_path):
    df = pd.read_csv(file_path, sep="|", dtype=str)

    # ✅ Safe conversions
    df["Revision"] = pd.to_numeric(df["Revision"], errors="coerce")
    df["Revision_Creation_Date"] = pd.to_datetime(
        df["Revision_Creation_Date"], errors="coerce"
    )

    # ✅ Remove bad rows (like header repeated in data)
    df = df.dropna(subset=["Revision", "Revision_Creation_Date"])
    df["Revision"] = df["Revision"].astype(int)

    bad_groups = []

    for item_id, group in df.groupby("Item_ID"):
        group = group.sort_values("Revision")

        prev_date = None
        for _, row in group.iterrows():
            if prev_date and row["Revision_Creation_Date"] < prev_date:
                bad_groups.append(group)
                break
            prev_date = row["Revision_Creation_Date"]

    bad_df = pd.concat(bad_groups) if bad_groups else pd.DataFrame(columns=df.columns)

    folder, _ = os.path.split(file_path)
    output_file = os.path.join(
        folder, "revision_order_mismatches_creation_date.txt"
    )

    bad_df.to_csv(output_file, sep="|", index=False)
    print(f"✅ Mismatch file saved: {output_file}")

    return bad_df


bad_items_df = find_revision_order_mismatches(
    r"D:\\JE project\\python\\Creation_date.txt"
)