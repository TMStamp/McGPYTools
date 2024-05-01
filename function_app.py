import azure.functions as func
import logging
import io
import os
import json
import logging
import re
import base64
import markdown

ACCEPTED_ENCODINGS = ['utf-8-sig', 'utf-8', 'windows-1252', 'iso-8859-1']
PARAMS_SOURCE = "source"
PARAMS_SEARCH_EXPR = "search_expr"
PARAMS_REPLACE_EXPR = "replace_expr"
PARAMS_IGNORE_CASE = "ignore_case"
PARAMS_USE_REGEX = "use_regex"
PARAMS_MULTILINE_REGEX = 'multiline_regex'

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# ------------------------------------------------------------------------------------------
#  Decode string
# ------------------------------------------------------------------------------------------
def decode(input_string):
    encodings = ['utf-8-sig', 'utf-8', 'windows-1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            result = input_string.encode().decode(encoding)
            return result
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError


# ------------------------------------------------------------------------------------------
#  Landing page
# ------------------------------------------------------------------------------------------
@app.route(route="tools")
def tools(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the path to the README.md file
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")

    try:
        # Read the contents of the README.md file
        readme_file = open(readme_path, "r")
        readme_content = markdown.markdown(readme_file.read())

        # Return the contents as an HttpResponse
        return func.HttpResponse(readme_file.read(), status_code=200, mimetype="text/plain")
    except Exception as e:
        return func.HttpResponse('Unable to return API information', status_code=400, mimetype="text/plain")

# ------------------------------------------------------------------------------------------
#  findText request
# ------------------------------------------------------------------------------------------
def search(source: str, search_expr: str, ignore_case=False,use_regex=False) -> str:
    # Create an empty list to store the matches
    matches = []
    
    # Iterate over the lines and check for matches with the regular expression
    for i, line in enumerate(source):
        if use_regex:
            for match in re.finditer(search_expr, line, flags=(re.I if ignore_case else 0)):
                # Add the matching text and line number to the list
                matches.append({
                    'text': match.group(),
                    'line_number': i+1,
                    'index': match.start()+1
                })

        else:
            index = line.lower().find(search_expr.lower()) if ignore_case else line.find(search_expr)
            while index >= 0:
                matches.append({
                    'text':search_expr,
                    'line_number':i+1,
                    'index':index+1
                })
                index = line.lower().find(search_expr.lower(), index+1) if ignore_case else line.find(search_expr, index+1)

    return json.dumps({"values":matches})

@app.route(route="tools/findText")
def findText(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Initiating [{req.method}] request with {str(req.route_params)}.')

    if req.method == 'GET':
        source = req.params.get(PARAMS_SOURCE)
        search_expr = req.params.get(PARAMS_SEARCH_EXPR)
        ignore_case = True if str.upper(req.params.get(PARAMS_IGNORE_CASE)) == 'Y' else False
        use_regex = True if str.upper(req.params.get(PARAMS_USE_REGEX)) == 'Y' else False
    elif req.metho == 'POST':
        try:
            req_body = req.get_json()
            source = req_body.get(PARAMS_SOURCE)
            search_expr = req_body.get(PARAMS_SEARCH_EXPR)
            ignore_case = True if str.upper(req_body.get(PARAMS_IGNORE_CASE)) == 'Y' else False
            use_regex = True if str.upper(req_body.get(PARAMS_USE_REGEX)) == 'Y' else False
        except ValueError:
            return func.HttpResponse(f'When using a POST method, please provide a JSON request object in the body with the required and available parameters.')

    else:
        return func.HttpResponse(f'This resource only supports GET or POST methods.', status_code=405)


    # Base 64 decode if required
    try:
        source = base64.b64decode(source)
    except Exception as e:
        pass

    # Decode strings received
    try:
        source = decode(source)
        search_expr = decode(search_expr)
    except UnicodeDecodeError:
        return func.HttpResponse(f'Only the following character encoding types are supported: {str(ACCEPTED_ENCODINGS)}',status_code=400)

    try:
        return func.httpResponse(search(source.splitlines(), search_expr, ignore_case, use_regex), status_code=200)
    except Exception as e:
        return func.HttpResponse(f'Unable to process request: {str(e)}',status_code=400)
