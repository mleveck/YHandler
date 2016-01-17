from abc import ABCMeta, abstractmethod


class BaseSelector:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.root = None

	@abstractmethod
	def parse(self, content):
		pass

	@abstractmethod
	def xpath(self, query):
		pass
