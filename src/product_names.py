### Get Product Name, Review Text from cell phones file
# import pandas as pd
# import gzip
# import json
# from tqdm import tqdm
# import time
#
# start_total = time.time()
#
# # Step 1: Load and clean reviews
# df_reviews = pd.read_csv(r"C:\Users\Rinchal shete\Downloads\cell_phone_reviews.csv")
# df_reviews = df_reviews[df_reviews['parent_asin'].notna()]
#
# # Drop full row duplicates
# df_reviews = df_reviews.drop_duplicates()
#
# # Drop duplicate reviewText values (optional but cleaner for downstream use)
# if 'text' in df_reviews.columns:
#     df_reviews = df_reviews.drop_duplicates(subset=['text'])
#
# print(f"✅ Cleaned reviews: {len(df_reviews)} rows")
#
# # Step 2: Prepare parent_asins for filtering
# parent_asins = set(df_reviews['parent_asin'])
#
# # Step 3: Load and filter meta data
# meta = []
# with gzip.open(r"C:\Users\Rinchal shete\Downloads\meta_Cell_Phones_and_Accessories.jsonl.gz", 'rt') as f:
#     for line in tqdm(f, desc="📦 Reading filtered meta file"):
#         item = json.loads(line.strip())
#         if item.get("parent_asin") in parent_asins:
#             meta.append(item)
#
# df_meta = pd.DataFrame(meta)
# df_meta = df_meta[df_meta['parent_asin'].notna()]
#
# # Step 4: Merge
# df_merged = pd.merge(df_reviews, df_meta, on='parent_asin', how='inner')
# print(f"✅ Merged: {len(df_merged)} rows")
#
# # Step 5: Save merged output
# df_merged.to_csv("merged_reviews_with_meta.csv", index=False)
# print(f"✅ Saved merged data to 'merged_reviews_with_meta.csv'")
#
# # Total time
# print(f"⏱️ Total time: {time.time() - start_total:.2f} seconds.")









# import pandas as pd
# reviews_file = "merged_reviews_with_meta.csv"
# mappings_file = "product_mappings.csv"
# output_file = "KeybertFile1.csv"
#
# # Step 1: Load the merged reviews file
# df_reviews = pd.read_csv(reviews_file)
#
# # Step 2: Load the product mappings file
# df_mappings = pd.read_csv(mappings_file)
#
# # Step 3: Merge based on matching 'title' with 'Original Product Name'
# df_final = pd.merge(
#     df_reviews,
#     df_mappings,
#     how='left',
#     left_on='title',
#     right_on='Original Product Name'
# )
#
# # Step 4: Rename columns
# df_final = df_final.rename(columns={
#     "text": "Review Text",
#     "Base Product Name": "Product Name"
# })
#
# # Step 5: Keep only required columns
# columns_to_keep = ["Review Text", "Product Name"]
# df_result = df_final[columns_to_keep]
#
# # Step 6: Ensure review count consistency
# print(f"✅ Reviews in original file: {len(df_reviews)}")
# print(f"✅ Reviews in merged result: {len(df_result)}")
#
# # Step 7: Save to new CSV
# df_result.to_csv(output_file, index=False)
# print(f"📁 Saved to: {output_file}")










### Get Product Name, Review Text from flipkart file
# import pandas as pd
# import re
# import csv
# Step 1: Load the Flipkart dataset
# flipkart_file = r"C:\Users\Rinchal shete\OneDrive\Desktop\flipkart_dataset.csv"
# df = pd.read_csv(flipkart_file)
#
# # Step 2: Clean 'Product Name' by removing text in parentheses
# df['Product Name'] = df['Product Name'].apply(lambda x: re.sub(r'\s*\(.*?\)\s*', '', str(x)).strip())
#
# # Step 3: Select columns in the desired order
# df_output = df[['Review Text', 'Product Name']]
#
# # Step 4: Save to CSV
# output_path = "KeybertFile2.csv"
#
# # Save manually row-by-row to quote only Review Text
# with open(output_path, mode='w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(['Review Text', 'Product Name'])  # Header
#     for _, row in df_output.iterrows():
#         writer.writerow([row['Review Text'], row['Product Name']])
#
# print(f"✅ Cleaned and saved to: {output_path} with only 'Product Name' unquoted.")









### Get Product Name, Review Text from amazon file
# import pandas as pd
#
# # File path
# input_file = r"C:\Users\Rinchal shete\OneDrive\Desktop\AmazonReviewsFinal.csv"
# output_file = "KeybertFile3.csv"
#
# # Load the file
# df = pd.read_csv(input_file)
#
# # Reorder and select only the needed columns
# df_output = df[["Review Text", "Product Name"]]
#
# # Save to CSV
# df_output.to_csv(output_file, index=False)
#
# print(f"✅ Saved to: {output_file} with columns in order: [Review Text, Product Name]")









### Get number of unique products from all datasets
# import pandas as pd
#
# # Load the review dataset
# df = pd.read_csv("KeybertFile1.csv")
# df1 = pd.read_csv("KeybertFile2.csv")
# df2 = pd.read_csv("KeybertFile3.csv")
# # Get unique product names
# up = df["Product Name"].unique()
# up1 = df1["Product Name"].unique()
# up2 = df2["Product Name"].unique()
#
# # Print the number of unique products
# print(f"🛍️ Total Unique Products: {len(up)+len(up1)+len(up2)}")



















