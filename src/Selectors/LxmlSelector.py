import lxml.etree as ET
from BaseSelector import BaseSelector

class DefaultSelector(BaseSelector):

	def __init__(self):
		super(DefaultSelector, self).__init__()

	def parse(self, content):
		self.root = ET.fromstring(content)
		