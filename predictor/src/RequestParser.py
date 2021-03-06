__author__ = "Sohail Shaikh"
__maintainer__ = "Sohail Shaikh"
__status__ = "Development"

class RequestParser:
	handlers_ = []
	def __init__(self):
		pass

	# request is a JSon object
	def process_request(self, request):
		# extract apiName and determine which request handler to invoke
		# right now we have only one request handler
		apiName = request['apiName']

		for i, handler in enumerate(self.handlers_):
			if (handler.apiName_ == apiName):
				# encode a response
				handler.process(request)
				response = handler.encode(request)
				return response
				break

	# register different handlers
	def registerHandler(self, handler):
		self.handlers_.append(handler);
		pass

