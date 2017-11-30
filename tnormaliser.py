from abc import ABCMeta, abstractmethod
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string
from collections import defaultdict
import re

class BaseStringNormalizer(metaclass=ABCMeta):

	@abstractmethod
	def _verify_input(self):
		'''
		check that input is a string or perhaps that it's a string with non-zero length
		'''
		pass

class StringNormalizer(BaseStringNormalizer):
	'''
	- words will be separated by a single white space
	'''

	def __init__(self, keep_stopwords=False, keep_punctuation=False, 
					all_lowercase=True, short_state_names=True, 
						full_city_names=True, remove_nonalnum=True):

		assert all([isinstance(_, bool) for _ in [keep_stopwords, keep_punctuation, all_lowercase, 
						short_state_names, full_city_names, remove_nonalnum]]), 'all keyword argument values must be True or False!'

		self.opts = defaultdict()
		self.opts['keep_stopwords'] = keep_stopwords
		self.opts['keep_punctuation'] = keep_punctuation
		self.opts['all_lowercase'] = all_lowercase
		self.opts['short_state_names'] = short_state_names
		self.opts['full_city_names'] = full_city_names
		self.opts['remove_nonalnum'] = remove_nonalnum

		self.state_abbr = {'nsw': 'new south wales', 
							'vic': 'victoria',
							'tas': 'tasmania',
							'sa': 'south australia',
							'wa': 'western australia',
							'act': 'australian capital territory',
							'nt': 'northern territory'}
		
		self.city_variants = {'sydney': ['syd'], 
								'melbourne': ['mel', 'melb'],
								'brisbane': ['bris'],
								'gold coast': ['gc'],
								'adelaide': ['adel'],
								'canberra': ['canb']}

	def _verify_input(self, st):

		assert isinstance(st, str) and len(st) > 0, 'input must be a non-empty string!'

	def _remove_punctuation(self, st):

		for p in string.punctuation:
				st = st.replace(p, ' ')
		return ' '.join(st.split())

	def normalise(self, st):

		self._verify_input(st)

		if self.opts['all_lowercase']:
			st = st.lower()

		if not self.opts['keep_punctuation']:
			st = self._remove_punctuation(st)

		if self.opts['remove_nonalnum']:
			st = ''.join([w for w in st if w.isalnum() or w.isspace()])

		if not self.opts['keep_stopwords']:
			st = ' '.join([w for w in st.split() if self._remove_punctuation(w.lower()) not in ENGLISH_STOP_WORDS])

		if self.opts['short_state_names']:
			for ab, s in self.state_abbr.items():
				st = st.replace(s, ab)

		if self.opts['full_city_names']:
			for cit in self.city_variants:
				for alt in self.city_variants[cit]:
					st = re.sub(r'\b{}\b'.format(alt), cit, st.lower())


		return st

if __name__ == '__main__':

	sn = StringNormalizer()
	print(sn.normalise('this, is an interesting 34- development! %%4#Sydney northern territory and victoria police bris entertainment centre'))


		



