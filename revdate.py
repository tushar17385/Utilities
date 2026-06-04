import pandas as pd
from datetime import timedelta
 
# Load CSV
df = pd.read_csv("C:\\Users\\tpp930693\\Downloads\\revisions_with_latest_flag_revision_order_mismatches_items_with_multiple_revisions_Item_vln.txt", sep="|")
 
# Convert date column to datetime
df["Revision_Creation_Date"] = pd.to_datetime(df["Revision_Creation_Date"], errors="coerce")
 
def assign_dates(group):
    # Sort revisions alphabetically
    group = group.sort_values("Revision").copy()
    
    # Get migration revisions and their dates
    migration_revs = group[group["Revision_Owner"] != "migration"].copy()
 
    for idx, row in group.iterrows():
        if row["Revision_Owner"] == "migration":
            # Find the *next higher* revision that belongs to migration
            higher_migration = migration_revs[migration_revs["Revision"] > row["Revision"]]
            if not higher_migration.empty:
                # Take the first higher migration revision date - 1 day
                assign_date = higher_migration["Revision_Creation_Date"].min() - timedelta(days=1)
                group.at[idx, "OrderedDate"] = assign_date
            else:
                # If no higher migration exists, keep its own date
                group.at[idx, "OrderedDate"] = row["Revision_Creation_Date"]
        else:
            # Migration revisions keep their own date
            group.at[idx, "OrderedDate"] = row["Revision_Creation_Date"]
    
    return group
 
# Apply per Item_ID + Item_Type
df = (
    df.groupby(["Item_ID", "Item_Type"], group_keys=False, sort=False)
    .apply(assign_dates)
    .reset_index(drop=True)
)
 
# Save output
df.to_csv("output.csv", sep="|", index=False)
 
print("✅ File saved as output.csv")