import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# 🔹 Load datasets
twitter = pd.read_excel("Twitter_Data.csv.xlsx")  # Excel file
reddit = pd.read_csv("Reddit_Data.csv")           # CSV file

# 🔹 Add source column
twitter["source"] = "Twitter"
reddit["source"] = "Reddit"

# 🔹 Rename columns to unify structure
twitter.rename(columns={"clean_text": "text"}, inplace=True)
reddit.rename(columns={"clean_comment": "text"}, inplace=True)

# 🔹 Combine datasets
data = pd.concat([twitter[["text", "category", "source"]],
                  reddit[["text", "category", "source"]]])

# ❗ Drop rows with missing category (target)
data.dropna(subset=["category"], inplace=True)


# 🔹 Clean text
def clean_text(text):
    text = re.sub(r"http\S+", "", str(text))
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^A-Za-z\s]", "", text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

data["cleaned_text"] = data["text"].apply(clean_text)

# 🔹 TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data["cleaned_text"])
y = data["category"]

# 🔹 Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 🔹 Print evaluation
print("📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# 🔹 Visualize sentiment distribution
plt.figure(figsize=(8, 5))
sns.countplot(x="category", data=data, palette="pastel")
plt.title("Overall Sentiment Distribution")
plt.show()

# 🔹 Sentiment by Source
plt.figure(figsize=(8, 5))
sns.countplot(x="category", hue="source", data=data, palette="Set2")
plt.title("Sentiment by Platform (Twitter vs Reddit)")
plt.show()

# 🔹 Word Cloud
all_words = ' '.join(data["cleaned_text"])
wc = WordCloud(width=1000, height=600, background_color='white').generate(all_words)

plt.figure(figsize=(10, 6))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Most Common Words in Social Media Posts")
plt.show()

















