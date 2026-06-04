import pandas as pd
import os
 
def assign_dates_by_revision_order(file_path):
    df = pd.read_csv(file_path, sep="|", dtype=str)
 
    df["Revision_Creation_Date"] = pd.to_datetime(df["Revision_Creation_Date"], errors="coerce")
 
    df["OrderedDate"] = ""
 
    group_cols = ["Item_ID"]
    if "Item_Type" in df.columns:
        group_cols.append("Item_Type")
 
    for _, group in df.groupby(group_cols):
        group_sorted_revs = group.sort_values("Revision")
 
        sorted_dates = sorted(group["Revision_Creation_Date"].dropna().tolist())
 
        for idx, (rev_idx, _) in enumerate(group_sorted_revs.iterrows()):
            if idx < len(sorted_dates):
                df.loc[rev_idx, "OrderedDate"] = str(sorted_dates[idx])
 
    folder, filename = os.path.split(file_path)
    output_file = os.path.join(folder, f"updated_list.txt")
    df.to_csv(output_file, sep="|", index=False)
    print(f"✅ File saved with OrderedDate column: {output_file}")
    return df
final_df = assign_dates_by_revision_order(r"C:\\Users\\tpp930693\\Downloads\\revisions_with_latest_flag_revision_order_mismatches_items_with_multiple_revisions_Item.txt")