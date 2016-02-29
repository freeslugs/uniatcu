import os
import requests
from flask import Flask, request, jsonify, redirect
from bs4 import BeautifulSoup

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return redirect("http://freeslugs.github.io/uniatcu/", code=302)

@app.route('/info')
def main():
	uni = request.args.get('uni')
	person = dict()

	if not uni:
		return error("please enter uni")
		
	else:
		r = requests.get('https://directory.columbia.edu/people/uni?code=' + uni)
		soup = BeautifulSoup(r.text)
		tds = soup.find('div', class_ = 'table_results_indiv').find('tbody').find_all('tr')
		
		for i in range(0,len(tds)):
			td = tds[i]
			if i == 0:
				if len(td.text) < 1:
					return error("person not found")
				else:
					person['name'] = td.text

			for j in range(0, len(td.contents)/2):
				left = td.contents[j*2].text.lower()
				right = td.contents[j*2+1]
				# prettify address
				# replace br tags with ", "
				count = str(right).count("<br/>") - 1
				right = BeautifulSoup(str(right).replace("<br/>", ", ", count))
				
				right = right.text.lower() 
				left = left.replace(":", "")
				right = right.replace(":", "")
				if left and right and left != u"\u00a0" and right != u"\u00a0":
					person[left] = right

			i += 1

		return jsonify({"data": person}) 

@app.route('/exists')
def exist():
	uni = request.args.get('uni')

	if not uni:
		return error("please enter uni")

	elif len(uni) < 6:
		return error("length is too short")

	else:
		r = requests.get('https://directory.columbia.edu/people/uni?code=' + uni)
		if uni in r.text:
			return jsonify({"exists": "true"}) 
		else: 
			return jsonify({"exists": "false"}) 

def error(error="unknown error has occured"):
	return jsonify({"error": error})


if __name__ == '__main__':
	app.run()
