class RequestParser:
	handlers_ = []
	def __init__(self):
		pass

	# request is a JSon object
	def parse(request):
		# extract apiName and determine which request handler to invoke
		# right now we will have only one request handler
		# apiName = extract api name from request
		for i, handler in enumerate(handlers_):
			if (handler.apiName_ == apiName):
				# encode a response
				handler.process()
				handler.encode()
				break

	# register different handlers
	def registerHandler(handler):
		handlers_.append(obj);
		pass


