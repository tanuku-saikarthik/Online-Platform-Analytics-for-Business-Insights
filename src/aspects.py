import pandas as pd
from collections import Counter
import ast

# Read CSV file
df = pd.read_csv(r'C:\PycharmProjects\Practice\Mini-Project ( new )\KeywordsExtracted.csv')
# Convert 'keywords' column from string to list if needed
df['Keywords'] = df['Keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Flatten all keywords from all reviews into a single list
all_keywords = [kw.lower() for sublist in df['Keywords'] for kw in sublist]

# Count most common keywords
keyword_counts = Counter(all_keywords)

# Show top 20 keywords (manually scan for aspects)
print(keyword_counts.most_common(300))
