import re

import requests
from bs4 import BeautifulSoup, SoupStrainer


class Category:
	def __init__(self, question=None, label=None, code=None, is_other=False, **kwargs):
		self.question = question
		self.label = label
		self.code = code
		self.is_other = is_other
		for k, v in kwargs.items():
			self.__setattr__(k, v)

	@property
	def count(self):
		if self.question:
			return len(self.question.categories)
		return None

	@classmethod
	def from_soup(cls, soup):
		is_other = 'freebirdFormviewerViewItemsCheckboxOtherCheckbox' in soup.parent.parent.parent.parent['class']
		return cls(label=soup.text, soup=soup, is_other=is_other)


class Question:
	# types: single, multiple, text
	SINGLE = 'SINGLE'
	MULTIPLE = 'MULTIPLE'
	TEXT = 'TEXT'

	def __init__(self, label=None, categories=[], q_type=None, **kwargs):
		self.label = label
		self.categories = categories
		self.q_type = q_type
		if q_type and q_type not in [Question.SINGLE, Question.MULTIPLE, Question.TEXT]:
			raise AttributeError(f'Unknown question type: {q_type}')
		for k, v in kwargs.items():
			self.__setattr__(k, v)

	def add_category(self, category):
		category.question = self
		category.code = category.count + 1
		self.categories.append(category)

	@property
	def has_other(self):
		for i in reversed(self.categories):
			if i.is_other:
				return True
		return False

	@classmethod
	def from_soup(cls, soup):
		label = soup.find('div', {'class': 'exportItemTitle'}).text.strip(' *')
		instance = cls(label, [], None, soup=soup)

		for i in soup.find_all('span', {'class': 'exportLabel'}):
		# r = re.compile('.*OptionContainer')
		# print(soup.find('div', {'class': r}), label)
		# print(soup.find('div', {'class': 'freebirdFormviewerViewItemsRadioOptionContainer'}), label)
		# exit(123)
		# for i in soup.find('div', {'class': r}):
			# print('i', i)
			instance.add_category(Category.from_soup(i))

		try:
			cat_classes = instance.categories[0].soup['class']
			if 'freebirdFormviewerViewItemsRadioLabel' in cat_classes:
				instance.q_type = Question.SINGLE
			elif 'freebirdFormviewerViewItemsCheckboxLabel' in cat_classes:
				instance.q_type = Question.MULTIPLE
		except IndexError:
			instance.q_type = Question.TEXT
		return instance

	def __repr__(self):
		return f'<Question type={self.q_type}; label="{self.label[:31]}..."; cat_count={len(self.categories)};>'


class Questionnaire:
	def __init__(self, questions=[], **kwargs):
		self.questions = questions
		for k, v in kwargs.items():
			self.__setattr__(k, v)

	@classmethod
	def from_url(cls, url):
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer('div', class_='freebirdFormviewerViewNumberedItemContainer'))
		questions = [Question.from_soup(i) for i in soup.find_all('div', {'class': 'freebirdFormviewerViewNumberedItemContainer'})]
		return cls(questions, url=url)


if __name__ == '__main__':
	form_url = 'https://docs.google.com/forms/d/1X8zi7093zRMjV3gGpuew1RKo14pd8Su2qlQsWyOplis/viewform?edit_requested=true'
	quest = Questionnaire.from_url(form_url)
	for q in quest.questions:
		print(q)
		for c in q.categories:
			print(f'\t{c.code}: {c.label}')
