import pandas as pd
import os
 
def mark_latest_by_revision(file_path):
    # Read CSV (pipe-delimited)
    df = pd.read_csv(file_path, sep="|", dtype=str)
 
    # Default all to "older"
    df["Latest/Older"] = "older"
 
    # Group by Item_ID (and Item_Type if present)
    group_cols = ["Item_ID"]
    if "Item_Type" in df.columns:
        group_cols.append("Item_Type")
 
    for _, group in df.groupby(group_cols):
        # Find row with max Revision alphabetically
        latest_idx = group["Revision"].idxmax()
        df.loc[latest_idx, "Latest/Older"] = "latest"
 
    # Sort result for readability
    df_sorted = df.sort_values(group_cols + ["Revision"])
 
    # Save output
    folder, filename = os.path.split(file_path)
    output_file = os.path.join(folder, f"revisions_with_latest_flag_creation_date_F3.txt")
    df_sorted.to_csv(output_file, sep="|", index=False)
 
    print(f"✅ File saved with latest/older column: {output_file}")
    return df_sorted
 
# ---- Run Example ----
# Replace with your file path
marked_df = mark_latest_by_revision(r"C:\\Users\\tpp930693\\Downloads\\creation_date_F 3.txt")