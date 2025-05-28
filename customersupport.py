import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from wordcloud import WordCloud

# Load Excel file (your uploaded file is .xlsx)
df = pd.read_excel('compressed_data.csv.xlsx')

# Print all column names to check available ones
print("Available columns:", df.columns)

# Find the most likely text column (you can manually set this if needed)
possible_text_cols = [col for col in df.columns if df[col].dtype == 'object']
text_column = possible_text_cols[0]  # or change to the correct one if known

# Clean and preprocess text data
text_data = df[text_column].dropna().astype(str)
all_text = ' '.join(text_data)
cleaned_text = re.sub(r'[^a-zA-Z\s]', '', all_text).lower()
words = cleaned_text.split()

# Remove common stopwords
stopwords = set([
    'the', 'is', 'in', 'and', 'to', 'of', 'a', 'for', 'on', 'with',
    'that', 'this', 'as', 'it', 'at', 'by', 'an', 'be', 'from', 'are', 'was'
])
filtered_words = [word for word in words if word not in stopwords]

# Word frequency
word_counts = Counter(filtered_words)
most_common_words = word_counts.most_common(10)
labels, counts = zip(*most_common_words)

# --- Graph 1: Bar Chart ---
plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color='skyblue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 10 Most Common Words')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Graph 2: Word Cloud ---
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Descriptions')
plt.tight_layout()
plt.show()

# --- Graph 3: Pie Chart ---
top5_words = word_counts.most_common(5)
labels_pie, sizes_pie = zip(*top5_words)
plt.figure(figsize=(8, 6))
plt.pie(sizes_pie, labels=labels_pie, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Top 5 Words Distribution')
plt.tight_layout()
plt.show()



