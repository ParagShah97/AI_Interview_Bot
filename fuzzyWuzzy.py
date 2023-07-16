from fuzzywuzzy import fuzz 
from fuzzywuzzy import process

def fuzzSimilarity(s1,s2):
	fuzzyRatio=fuzz.ratio(s1, s2)
	fuzzyPartialRatio=fuzz.partial_ratio(s1, s2)
	fuzzyTokenSortRatio=fuzz.token_sort_ratio(s1, s2)
	fuzzyWRatio=fuzz.WRatio(s1, s2)
	dic={"fuzzyRatio":fuzzyRatio,"fuzzyPartialRatio":fuzzyPartialRatio,"fuzzyTokenSortRatio":fuzzyTokenSortRatio,"fuzzyWRatio":fuzzyWRatio}
	return dic


"""

print ("FuzzyWuzzy Ratio: ", fuzz.ratio(s1, s2))
print ("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(s1, s2))
print ("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(s1, s2)) 
print ("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(s1, s2)) 
print ("FuzzyWuzzy WRatio: ", fuzz.WRatio(s1, s2),'\n\n')

print ("FuzzyWuzzy Ratio: ", fuzz.ratio(t1, t2))
print ("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(t1, t2))
print ("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(t1, t2)) 
print ("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(t1, t2)) 
print ("FuzzyWuzzy WRatio: ", fuzz.WRatio(t1, t2),'\n\n')
"""