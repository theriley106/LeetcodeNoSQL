import requests
import bs4
import os
import json

questions = open("badQuestions.txt").read().split("\n")

def get_question(question):
	if not os.path.exists("{}.json".format(question)):
		with open('tmp', 'w') as f:
			f.write(open("getQuestion.sh").read().replace("$1", question))
		os.system("chmod +x tmp && ./tmp > {}.json".format(question))
		a = json.loads(open("{}.json".format(question)).read())
		with open("{}.json".format(question), 'w') as f:
			f.write(json.dumps(a, indent=4))
	return open("{}.json".format(question)).read()

def ignore_question(question):
	a = json.loads(get_question(question))["data"]["question"]["metaData"]
	information = json.loads(a)
	return information.get('shell', False) or information.get('database', False)

def get_all_questions():
	return requests.get("https://leetcode.com/api/problems/all/").json()['stat_status_pairs']

if __name__ == '__main__':
	for i, val in enumerate(get_all_questions()):
		print i
		try:
			if ignore_question(val['stat']['question__title_slug']):
				if val['stat']['question__title_slug'] not in questions:
					os.system("echo {} >> badQuestions.txt".format(val['stat']['question__title_slug']))
		except Exception as exp:
			print exp
	