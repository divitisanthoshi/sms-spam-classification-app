import re
import os
from flask import Flask, request, jsonify, render_template
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from pymongo import MongoClient

nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/')

# Initialize MongoDB client and database
client = MongoClient(DATABASE_URL)
db = client['sms_spam_db']
collection = db['sms_messages']

# Initialize lemmatizer and stopwords
wnl = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Initialize and train a simple model on a small sample dataset
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
    "greetings"
]
sample_labels = [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 for spam, 0 for ham

def preprocess_message(message):
    message = re.sub(pattern='[^A-Za-z]', repl=' ', string=message)
    message = message.lower()
    words = message.split()
    filtered_words = [word for word in words if word not in stop_words]
    lemmatized_words = [wnl.lemmatize(word) for word in filtered_words]
    return ' '.join(lemmatized_words)

# Preprocess sample messages
processed_samples = [preprocess_message(msg) for msg in sample_messages]

# Train vectorizer and model
tfidf = TfidfVectorizer()
X_train = tfidf.fit_transform(processed_samples)
model = MultinomialNB()
model.fit(X_train, sample_labels)

# Calculate accuracy on training data
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_train)
accuracy = accuracy_score(sample_labels, y_pred)
print(f"Training accuracy: {accuracy:.2f}")

def save_message_to_db(message, prediction):
    doc = {'message': message, 'prediction': int(prediction)}
    collection.insert_one(doc)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    message = data['message']
    from model_improvement import predict_message
    prediction = predict_message(message)
    save_message_to_db(message, prediction)
    return jsonify({'prediction': 'spam' if prediction == 1 else 'ham'})

@app.route('/messages', methods=['GET'])
def get_messages():
    cursor = collection.find().sort('_id', -1).limit(10)
    messages = [{'message': doc['message'], 'prediction': 'spam' if doc['prediction'] == 1 else 'ham'} for doc in cursor]
    return jsonify(messages)

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    collection.delete_many({})
    return jsonify({'message': 'All messages cleared successfully'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)