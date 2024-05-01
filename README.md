---
    title: Information page for the tools API
---

# Welcome to the CSV/Text Tools API

The following API provides a set of practical resources to manipulate text-based content either provided in file or string format. The current version of the API has size-limited text content. In the future, larger sized text content may be supported.

Currently, the resources only support the following file encodings: *UTF-8*, *windows-1252*, *iso-8859-1*.

### *findText*

The *findText* endpoint receives a multi-line text file/string along with a search expression and parameters. The endpoint provides a JSON array response of what was matched and at the line where the match was made.

The endpoint supports both the GET and POST method.

For example:

Suppose a *source* of:
```
The quick brown fox jumped over the fence during lunch downtime.
There were no brownies for the fox to find.
```

And a *search_expr* (no regular expression ignoring case) of:
```
own
```

The JSON response returned would be:
```
{

}
```


### Input Parameters

#### source (any file or block of text)
The file and its contents to search for the matching expression provided in *search_expr*. The file can be provided in the query parameters, the body of the request as a JSON object, or as a form field (if using the POST method), whatever the requestor's preference.

#### search_expr
The expression to match in the text or file contents (if regular expressions are enabled, the expected search expression should be constructed according to the Python regular expression syntax: https://www.w3schools.com/python/python_regex.asp)

#### ignore_case (optional)
Indicate *Y* in order for the service to ignore case when matching against the provided search expression *search_expr*.

#### use_regex (optional)
Indicate *Y* the service will treat the search expression *search_expr* as a regular expression.


## Old API Information Text
```
    return func.HttpResponse(
        f'This API supports the following requests (routes, i.e. /api/tools/<request>): {ACCEPTED_REQUEST_TYPES}\n\n'+
        f'A [{REQUEST_TYPE_CSVTOJSON}] request transforms a source CSV file into a JSON array optionally indexed by a specified column name:\n'+
            f'<{PARAMS_FILE}> Location of the source text file to read (supports {str(ACCEPTED_ENCODINGS)} encodings)\n'+
            f'<{PARAMS_CSVTOJSON_INDEX_COL}> (optional) Index column name.\n\n'+
        f'A [{REQUEST_TYPE_SEARCHTEXT}] request searches text in a string or file and returns a JSON array of matches found indexed by line and position (supports regular expresions):\n'+
            f'<{PARAMS_TEXT}> or <{PARAMS_FILE}> Source text (file) to search (file character encoding supported {str(ACCEPTED_ENCODINGS)} encodings)\n'+
            f'<{PARAMS_SEARCH_EXPR}> The search expression/term to find in the source text (Set <{PARAMS_USE_REGEX}> to Y for regular expression matching)\n'+
            f'<{PARAMS_IGNORE_CASE}> (optional) Set to Y to for case insensitive matching\n\n'+
        f'A [{REQUEST_TYPE_REPLACETEXT}] request finds and replaces text in a string or file according to provided search and replace expressions (supports regular expression matching and replacing):\n'+
            f'<{PARAMS_TEXT}> or <{PARAMS_FILE}> Source text (file) to search (file character encoding supported {str(ACCEPTED_ENCODINGS)} encodings)\n'+
            f'<{PARAMS_SEARCH_EXPR}> The search expression/term to find in the source text (Set <{PARAMS_USE_REGEX}> to Y for regular expression matching)\n'+
            f'<{PARAMS_REPLACE_EXPR}> The expression/term to substitute with the text found (Set <{PARAMS_USE_REGEX}> to Y for regular expression based substitutions)\n'+
            f'<{PARAMS_IGNORE_CASE}> (optional) Set to Y to for case insensitive matching\n'+
            f'<{PARAMS_MULTILINE_REGEX}> (optional) Set to Y for multiline matching (i.e., ^ or $ symbols) when using regular expressions\n'+
        f'A [{REQUEST_TYPE_JSONTRANSPOSE}] request converts a json structure from a recordset to an array of records including an "id" attribute:\n'+
            f'<{PARAMS_TEXT}> or <{PARAMS_FILE}> Source text (file) from which to transpose (file character encoding supported {str(ACCEPTED_ENCODINGS)} encodings)\n'+
            f'<{PARAMS_PARENT_NODE}> (optional) If not the root node/property, specify the parent node/property name containing all of the records to transpose. \n',
        status_code=200
    )

```