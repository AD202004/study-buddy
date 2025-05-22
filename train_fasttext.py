import fasttext

# Train the model (skipgram is good for small data)
model = fasttext.train_unsupervised('fasttext_train.txt', model='skipgram', dim=50)
model.save_model('fasttext.bin')
print("FastText model trained and saved as 'fasttext.bin'")
