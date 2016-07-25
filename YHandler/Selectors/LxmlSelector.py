import lxml.etree as ET
from BaseSelector import BaseSelector

class LxmlSelector(BaseSelector):

	def __init__(self, root=None):
		super(LxmlSelector, self).__init__()
		self.root = root
		self.text = root.text if root else ''

	def parse(self, content):
		self.root = ET.fromstring(content)
		return LxmlSelector(self.root)
		
	def select(self, query, ns=None):
		els = []
		for el in self.root.findall(query, ns):
			selector = LxmlSelector(el)
			els.append(selector)
		return els

	def select_one(self, query, ns=None):
		el = self.root.findall(query, ns)
		if not el:
			return LxmlSelector()
		else:
			return LxmlSelector(el[0])		

	def iter_select(self, query, ns=None):

		for el in self.root.iterfind(query, ns):
			selector = LxmlSelector(el)
			yield selector