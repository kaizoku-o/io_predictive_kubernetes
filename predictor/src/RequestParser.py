class RequestParser:
	handlers_ = []
	def __init__(self):
		pass

	# request is a JSon object
	def parse(self, request):
		# extract apiName and determine which request handler to invoke
		# right now we have only one request handler
		apiName = request['apiName']

		for i, handler in enumerate(self.handlers_):
			if (handler.apiName_ == apiName):
				# encode a response
				handler.process()
				response = handler.encode()
				return response
				break

	# register different handlers
	def registerHandler(self, handler):
		self.handlers_.append(handler);
		pass

