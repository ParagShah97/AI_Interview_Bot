from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import math

def cosineSimilarity(s1,s2):
	documents=[s1,s2]
	count_vectorizer = CountVectorizer(stop_words='english')
	#count_vectorizer = CountVectorizer()
	sparse_matrix = count_vectorizer.fit_transform(documents)
	#print(sparse_matrix)

	doc_term_matrix = sparse_matrix.todense()
	df = pd.DataFrame(doc_term_matrix, 
					  columns=count_vectorizer.get_feature_names(), 
					  index=['s1','s2'])
	#df

	from sklearn.metrics.pairwise import cosine_similarity
	cs=cosine_similarity(df, df)
	aa=math.ceil(cs[0][1]*100)
	return aa
	#print(cosine_similarity(df, df))
	
