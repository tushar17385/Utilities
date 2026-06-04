import pandas as pd
from datetime import timedelta
# === File Path ===
file_path = "C:\\Users\\tpp930693\\Downloads\\creation_date_lower_revision.xlsx"
# === Read Sheets ===
db = pd.read_excel(file_path, sheet_name="DB")
inp = pd.read_excel(file_path, sheet_name="input")
# === Clean and Normalize Column Names ===
db.columns = db.columns.str.strip()
inp.columns = inp.columns.str.strip()
# === Convert types ===
db['Item_ID'] = db['Item_ID'].astype(str).str.strip()
inp['Item:item_id'] = inp['Item:item_id'].astype(str).str.strip()
db['Revision'] = db['Revision'].astype(str).str.strip()
inp['ItemRevision:item_revision_id'] = inp['ItemRevision:item_revision_id'].astype(str).str.strip()
# === Parse Dates (ensure correct space in format) ===
db['Revision_Creation_Date'] = pd.to_datetime(
   db['Revision_Creation_Date'], errors='coerce', format='%Y-%m-%d %H:%M:%S.%f'
)
inp['creation_date'] = pd.to_datetime(
   inp['creation_date'], errors='coerce', format='%Y-%m-%d %H:%M:%S.%f'
)
# === Sort DB for predictable lookup ===
db = db.sort_values(by=['Item_ID', 'Revision']).reset_index(drop=True)
# === Function: find next higher revision ===
def get_next_rev_date(row):
   item_id = row['Item:item_id']
   rev = row['ItemRevision:item_revision_id']
   # find higher revisions for same item (alphabetical comparison)
   higher_revs = db[(db['Item_ID'] == item_id) & (db['Revision'] > rev)]
   if not higher_revs.empty:
       # get the first (next) higher revision alphabetically
       next_rev_date = higher_revs.iloc[0]['Revision_Creation_Date']
       if pd.notnull(next_rev_date):
           return next_rev_date - timedelta(days=1)
   # no higher revision found → keep original date
   return row['creation_date']
# === Apply logic ===
inp['creation_date'] = inp.apply(get_next_rev_date, axis=1)
# === Format back to yyyy-mm-dd hh:mm:ss.000 ===
inp['creation_date'] = inp['creation_date'].dt.strftime('%Y-%m-%d %H:%M:%S.000')
# === Write updated sheet back using openpyxl (supports append/replace) ===
with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
   inp.to_excel(writer, sheet_name='input', index=False)
print("✅ Input sheet updated successfully with adjusted creation dates (openpyxl engine used).")