import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import IsolationForest
import numpy as np
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

wnl = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Expanded training dataset with more ham examples including greetings
sample_messages = [
    "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005.",
    "U dun say so early hor... U c already then say...",
    "Nah I don't think he goes to usf, he lives around here though",
    "WINNER!! As a valued network customer you have been selected to receivea £900 prize reward!",
    "Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free!",
    "I'm gonna be home soon and i don't want to talk about this stuff anymore tonight",
    "SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575.",
    "Hey there! Are you free to meet up later?",
    "URGENT! You have won a 1 week FREE membership in our £100,000 Prize Jackpot!",
    "I'll call you later when I get home.",
    "Alert..!! your acount has been hacked",
    "Alert..!! your a/c has been hacked.. Click on this link for more details...",
    # Added ham greetings
    "hi",
    "hai",
    "hy",
    "hello",
    "good morning",
    "good evening",
    "how are you",
    "what's up",
    "hey",
    "greetings",
    "Congratulations! You won a prize",
    "Win a free ticket now",
    "Claim your free prize",
    "You have been selected for a reward"
]

sample_labels = [
    1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1
]  # 1 for spam, 0 for ham

def preprocess_message(message):
    message = re.sub(pattern='[^A-Za-z]', repl=' ', string=message)
    message = message.lower()
    words = message.split()
    filtered_words = [word for word in words if word not in stop_words]
    lemmatized_words = [wnl.lemmatize(word) for word in filtered_words]
    return ' '.join(lemmatized_words)

processed_samples = [preprocess_message(msg) for msg in sample_messages]

tfidf = TfidfVectorizer()
X_train = tfidf.fit_transform(processed_samples)

model = MultinomialNB()
model.fit(X_train, sample_labels)

# Anomaly detection model for adversarial or novel spam detection
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(X_train.toarray())

def predict_message(message):
    processed = preprocess_message(message)
    features = tfidf.transform([processed]).toarray()
    prediction = model.predict(features)[0]
    anomaly_score = iso_forest.decision_function(features)[0]
    is_anomaly = iso_forest.predict(features)[0] == -1
    # If anomaly detected, treat as spam (1)
    if is_anomaly:
        return 1
    return prediction

# Test the greetings and anomaly detection
test_messages = ["hi", "hai", "hy", "hello", "good morning", "free money", "win prize now", "unknown spammy text"]

for test_msg in test_messages:
    pred = predict_message(test_msg)
    print(f"Message: '{test_msg}' classified as: {'spam' if pred == 1 else 'ham'}")
