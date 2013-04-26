# --------------------------------------------------------------------------------------------------
# -- Libraries

import re                       # regular expression module
import os                       # walking the filesystem
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class MainPage(BaseHandler):
    def get(self):
    	self.render("vanityPhone-form.html")

    def post(self):
    	has_error = False
    	number = self.request.get('number')
    	params = {}

    	if len(number) != 10:
    		params['error_length'] = "The number you entered is not 10 digits long"
    		has_error = True
    	if not number.isdigit():
    		params['error_chars'] = "You must enter only digits"
    		has_error = True
    	if number.find('0') != -1 or number.find('1') != -1:
    		params['error_digits']	= "The number entered must not contain 1's or 0's"
    		has_error = True

    	if has_error:
    		self.render("vanityPhone-form.html", **params)
    	else:
    		if number in dic:
    			params['result'] = "Words(s) associated with this number: " + str(dic[number])
    		else:
    			params['result'] = "There are no 10 letter english words associated with the number you entered"
    		self.render("vanityPhone-form.html", **params)


# --------------------------------------------------------------------------------------------------
# -- Data Structures
dic = {}

# --------------------------------------------------------------------------------------------------
# -- Helpers

def read_word_list():
    '''Reads file with the 10 letter words and builds a dictionary'''
    dict_file = open('dict.txt')
    for line in dict_file:
        match = re.search("\s*(\w+)\s*$", line)
        if match:
            word = line.strip()
            number = word_to_number(word)
            if number in dic:
                dic[number].append(word)
            else:
                dic[number] = []
                dic[number].append(word)

def word_to_number(word):
    '''Parses a 10 letter word and returns its equivalent 10 digit number'''
    number = ''
    ls = list(word)
    for letter in ls:
        diff = ord(letter) - 96
        if 1 <= diff <= 3:
            number += '2'
        elif 4 <= diff <= 6:
            number += '3'
        elif 7 <= diff <= 9:
            number += '4'
        elif 10 <= diff <= 12:
            number += '5'
        elif 13 <= diff <= 15:
            number += '6'
        elif 16 <= diff <= 19:
            number += '7'
        elif 20 <= diff <= 22:
            number += '8'
        else:
            number += '9'
    return number

# --------------------------------------------------------------------------------------------------
# -- Main Script
read_word_list()

# --------------------------------------------------------------------------------------------------
# -- URL Mapping
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
