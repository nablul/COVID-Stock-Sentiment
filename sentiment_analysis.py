#Import modules
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import string

#COVID-19 indicator, trigger and modifier/booster words
covid_indicator_words = ['COVID', 'covid', 'COVID-19', 'covid-19', 'corona', 'coronavirus', 'virus', 'pandemic', 'quarantine']
negative_trigger_words = {'death':-1.0, 'ICU':-0.9, 'hospital':-0.85, 'hospitalization':-0.85, 'fear':-0.85, 'fearful':-0.85, 'pandemic':-0.75, 'outbreak':-0.75, 'pessimistic':-0.75, 'pessimism':-0.75, 'COVID':-0.75, 'covid':-0.75, 'COVID-19':-0.75, 'covid-19':-0.75, 'corona':-0.75, 'coronavirus':-0.75, 'virus':-0.75, 'quarantine':-0.5, 'lockdown':-0.5, 'shelter':-0.5, 'restriction':-0.5}
positive_trigger_words = {'optimism':0.85, 'optimistic':0.85, 'hope':0.85, 'hopeful':0.85, 'vaccine': 0.75, 'test': 0.5, 'trial': 0.5}
negative_modifier_words = {'worsen':2.0, 'worse':2.0, 'surge':2.0, 'spike':1.85, 'increase':1.75, 'again':1.75, 'rapid':1.5, 'decrease':-1.75, 'improve':-2.0, 'improvement':-2.0}
positive_modifier_words = {'improve':2.0, 'improvement':2.0, 'progress':2.0, 'increase':1.75, 'decrease':-1.75}

#Function to return NLTK word tag for corresponding POS tag
def nltk_tag_to_wordnet_tag(tag_text):
    if tag_text.startswith('J'):
        return wordnet.ADJ
    elif tag_text.startswith('V'):
        return wordnet.VERB
    elif tag_text.startswith('N'):
        return wordnet.NOUN
    elif tag_text.startswith('R'):
        return wordnet.ADV
    else:
        return None

#Function to perform sentiment analysis using NLTK's VADER module
def news_sentiment(list_of_headlines):
    if not list_of_headlines:
        return 0
    else:
        sentiment_scores = []
        sid = SentimentIntensityAnalyzer()
        for headline in list_of_headlines:
            ss = sid.polarity_scores(headline)['pos'] - sid.polarity_scores(headline)['neg']
            sentiment_scores.append(ss)
        return sum(sentiment_scores)/len(sentiment_scores)

#Function to perform lexical sentiment analysis for COVID-19 news
def COVID_sentiment(list_of_headlines):
    #Empty list. Return 0 sentiment score
    if not list_of_headlines:
        return 0
    #List not empty -> Calculate sentiment score for each headline and return avg sentiment
    else:
        sentiment_scores = []
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
    
        for headline in list_of_headlines:
        
            #Sentence tokenize
            sentence_tokenized = sent_tokenize(headline)

            #Word tokenize
            word_tokenized = []
            for s in sentence_tokenized:
                word_tokenized.append(word_tokenize(s))

            #Filter out punctuations and stop words
            sentence_filtered = []
            for s in word_tokenized:
                word_filtered = []
                for w in s:
                    if w not in stop_words and w not in string.punctuation:
                        word_filtered.append(w)
                sentence_filtered.append(word_filtered)

            #Assign Part Of Speech (POS) tag
            sentence_pos_tagged = []
            for s in sentence_filtered:
                sentence_pos_tagged.append(pos_tag(s))

            #Lemmatize words
            sentence_lemmatized = []
            for s in sentence_pos_tagged:
                word_lemmatized = []
                for w, tag in s:
                    wordnet_tag = nltk_tag_to_wordnet_tag(tag)
                    if  wordnet_tag is None:
                        word_lemmatized.append(w)
                    else:
                        word_lemmatized.append(lemmatizer.lemmatize(w, wordnet_tag))
                sentence_lemmatized.append(word_lemmatized)

            #Determine if headline contains COVID-19 indicator words
            COVID_news = False
            for s in sentence_lemmatized:
                for w in s:
                    if w in covid_indicator_words:
                        COVID_news = True

            #If headline contains COVID-19 indicator words, increment sentiment score per trigger & booster words
            for s in sentence_lemmatized:
                trigger_word_sentiment = 0
                sentiment_modifier = 1
                if COVID_news == True:
                    for w in s:
                        if w in negative_trigger_words:
                            trigger_word_sentiment += negative_trigger_words[w]
                        if w in positive_trigger_words:
                            trigger_word_sentiment += positive_trigger_words[w]
                        if w in negative_modifier_words:
                            sentiment_modifier += negative_modifier_words[w]
                        if w in positive_modifier_words:
                            sentiment_modifier += positive_modifier_words[w]
                sentiment_scores.append(trigger_word_sentiment*sentiment_modifier)
      
        #Return average sentiment score for list of headlines
        return sum(sentiment_scores)/len(sentiment_scores)
