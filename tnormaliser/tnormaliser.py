from abc import ABCMeta, abstractmethod
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string
from collections import defaultdict, Counter
import re
from num2words import num2words
import arrow
import itertools

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
					lowercase=True, short_state_names=True, 
						full_city_names=True, remove_nonalnum=True, disamb_country_names=True,
							ints_to_words=True, year_to_label=True, remove_dupl_subsrings=True, max_dupl=4,
							remove_dupl_words=False):

		assert all([isinstance(_, bool) for _ in [keep_stopwords, keep_punctuation, lowercase, 
						short_state_names, full_city_names, remove_nonalnum, disamb_country_names, 
							ints_to_words, year_to_label, remove_dupl_subsrings]]), 'all keyword argument values must be True or False!'

		self.opts = defaultdict()
		self.opts['keep_stopwords'] = keep_stopwords
		self.opts['keep_punctuation'] = keep_punctuation
		self.opts['lowercase'] = lowercase
		self.opts['short_state_names'] = short_state_names
		self.opts['full_city_names'] = full_city_names
		self.opts['remove_nonalnum'] = remove_nonalnum
		self.opts['disamb_country_names'] = disamb_country_names
		self.opts['ints_to_words'] = ints_to_words
		self.opts['year_to_label'] = year_to_label
		self.opts['remove_dupl_subsrings'] = remove_dupl_subsrings
		self.opts['max_dupl'] = max_dupl
		self.opts['remove_dupl_words'] = remove_dupl_words

		self.state_abbr = {'nsw': 'new south wales', 
							'vic': 'victoria',
							'tas': 'tasmania',
							'sa': 'south australia',
							'wa': 'western australia',
							'act': 'australian capital territory',
							'nt': 'northern territory'}
		
		self.city_variants = {'sydney': ['syd'], 
								'melbourne': ['mel', 'melb'],
								'brisbane': ['bris', 'brisb'],
								'gold coast': ['gc'],
								'adelaide': ['adel'],
								'canberra': ['canb']}

		self.country_variants = {'usa': ['united states of america', 'united states'],
									'uk': ['united kingdom'],
									'russia': ['russian federation'],
									'taiwan': ['chinese taipei'],
									'korea': ['republic of korea'],
									'netherlands': ['holland'],
									'china': ['prc', 'peoples republic of china'],
									'macedonia': ['fyrom'],
									'new zealand': ['nz']}

	def _verify_input(self, st):

		assert isinstance(st, str) and len(st) > 0, 'input must be a non-empty string!'

	def _remove_punctuation(self, st):

		for p in string.punctuation:
				st = st.replace(p, ' ')
		return ' '.join(st.split())

	def normalise(self, st):

		self._verify_input(st)

		if self.opts['lowercase']:
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

		if self.opts['disamb_country_names']:
			for cn in self.country_variants:
				for alt in self.country_variants[cn]:
					st = re.sub(r'\b{}\b'.format(alt), cn, st.lower())
					# and repeat without stopwords
					st = re.sub(r'\b{}\b'.format(' '.join([w for w in alt.split() if w not in ENGLISH_STOP_WORDS])), cn, st.lower())
		
		if self.opts['ints_to_words']:
			st = ' '.join([num2words(int(w)) if w.isdigit() else w for w in st.split()])

		if self.opts['year_to_label']:
			# attempt to find a year 
			try:
				st = st.replace(str(arrow.get(st, 'YYYY').year), '!YEAR!')
			except:   # if failed to match an exceptinon is thrown
				pass

		def remove_dupl_substrings(d, n):

			if n > 1:
		
				l = []
				its = itertools.tee(iter(d.split()),n)
	
				for i, _ in enumerate(range(n)):
					# i moves ahead by i - 1
					if i > 0:
						for x in range(i):
							next(its[i], None)
			   
				for p in zip(*its):
					l.append(p)
			   
				for k, v in Counter(l).items():
					if v > 1:
						sb = ' '.join(k)
						for _ in range(v - 1):
							d = ' '.join(d.rsplit(sb, maxsplit=1))
			   
				d = remove_dupl_substrings(d, n-1)
		
			return ' '.join(d.split())


		if self.opts['remove_dupl_subsrings']:

			st = remove_dupl_substrings(st, self.opts['max_dupl'])   

		if self.opts['remove_dupl_words']:
			l = []
			[l.append(_) for _ in st.split() if _ not in l]
			st = ' '.join(l)   		

		return st



if __name__ == '__main__':

	sn = StringNormalizer(ints_to_words=False, remove_dupl_words=True)
	print(sn.normalise('this 2016 tour is the united states 34- development! %%4#Sydney the united states northern territory, some Russian Federation efforts and victoria police bris entertainment centre'))


		



