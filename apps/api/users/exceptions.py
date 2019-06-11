from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
	# Call REST framework's default exception handler first,
	# to get the standard error response.
	response = exception_handler(exc, context)

	# Now add the HTTP status code to the response.

	try:
		if response.data['non_field_errors']:
			response.data['msg'] = "Login failed invalid credentials"
			response.data['status'] = 0
			del response.data['non_field_errors']
	except Exception as e:
		pass

	return response