from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import gensim
from gensim import corpora, models

sampletext = "We went for our first time to Arrivederchi Ahwautukee recently on a weeknight, thinking it would not be crowded, but we were dead wrong! Parking was easy, but when we walked in the door, the place was hopping. Every table was taken, and all the staff were working fast like a well-oiled, but super-friendly, machine. (Surely, you have met at least one other friendly machine in your life.) We actually had a short wait for a table. Water and wine service were prompt and jovial. Their menu is loaded with nice touches on classic Italian dishes. It has been a while since we were there, so my wife and I both are a bit hazy on what we ordered. But we remember clearly that we were highly impressed by their kitchen, their staff, their location, and their charming Italian decor. Now we need to go back and refresh our memories. We highly recommend it."
sample = "the stemming is a  stemmer and stemmed"

p_stemmer = PorterStemmer()

rawdata = sampletext.lower()
tokens = tokenizer.tokenize(rawdata)
en_stop = get_stop_words('en')
stopped_tokens = [i for i in tokens if not i in en_stop]
#print stopped_tokens

#To remove all the tensed words into normal form
stemmed_token = [p_stemmer.stem(i) for i in stopped_tokens]
#print stemmed_token

texts = []
texts.append(stemmed_token)
#print texts

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

#print dictionary.token2id
#print corpus[0]

#Applying LDA model

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary,passes = 50)

#passes - no of iteration

print ldamodel.print_topics(num_topics=3, num_words = 8)