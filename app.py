import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)
app.debug = True

@app.route('/info')
def main():
	uni = request.args.get('uni')
	person = dict()

	if not uni:
		return error("please enter uni")
		
	
	elif len(uni) < 6:
		return error("length is too short")		

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
				right = td.contents[j*2+1].text.lower()
				left = left.replace(":", "")
				right = right.replace(":", "")
				if left and right and left != u"\u00a0" and right != u"\u00a0":
					person[left] = right

			i += 1
		return jsonify({"data": person}) 

if __name__ == '__main__':
	app.run()


def error(error="unknown error has occured"):
	return jsonify({"error": error})