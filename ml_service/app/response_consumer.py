from transformers import AutoTokenizer, AutoModelForSequenceClassification
from classifier import Classifier

def main():
    tokenizer = AutoTokenizer.from_pretrained('VetUps/final_tokenizer')
    model = AutoModelForSequenceClassification.from_pretrained('VetUps/final_model')

    classifier = Classifier(model=model, tokenizer=tokenizer)

    while True:
        text = input('Ввод текста: ')
        predict = classifier.predict(text)

        print(predict)

if __name__ == '__main__':
    main()
