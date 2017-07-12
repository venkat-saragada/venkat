from odoo import tools, exceptions, api

def validate_from_date_to_date(from_date, to_date):
		result = False
		if from_date <= to_date:
			result = True
		return result

def validation_alphanumeric_characters_only(received_string):
    result = False
    if re.match("^[A-Za-z0-9]*$", received_string):
        result = True
    return result