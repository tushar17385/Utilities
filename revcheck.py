import pandas as pd
import os
 
def extract_items_with_multiple_revisions_by_type(file_path):
    # Read CSV (pipe-delimited)
    df = pd.read_csv(file_path, sep="|", dtype=str)
 
    # Group by Item_ID and Item_Type, count unique revisions
    revision_counts = df.groupby(["Item_ID", "Item_Type"])["Revision"].nunique()
 
    # Select combinations with more than 1 revision
    items_with_multiple_revs = revision_counts[revision_counts > 2].index
 
    # Filter original dataframe
    filtered_df = df.set_index(["Item_ID", "Item_Type"]).loc[items_with_multiple_revs].reset_index()
 
    # Create output file path in same folder
    folder, filename = os.path.split(file_path)
    output_file = os.path.join(folder, f"3_rev_creation_date_F3.txt")
 
    # Save to CSV
    filtered_df.to_csv(output_file, sep="|", index=False)
 
    print(f"✅ File saved: {output_file}")
    return filtered_df
 
# ---- Run Example ----
# Replace with your file path
extract_items_with_multiple_revisions_by_type(r"C:\\Users\\tpp930693\\Downloads\\creation_date_F 3.txt")