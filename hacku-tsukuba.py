# coding: utf-8
import urllib2
import os
import re
import sys
import jinja2
import webapp2

from yconnect import YConnectExplicit

# you must change following variables
client_id     = '';
client_secret = '';
redirect_uri  = 'http://localhost:8080/registration';

# setting jinja
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class TopPage(webapp2.RequestHandler):

	def get(self):

		# パラメータ解析
		mode = self.request.get('mode')

		# テンプレートの準備
		template = jinja_environment.get_template('template/index.html')
		self.response.out.write(template.render())


class RegistrationPage(webapp2.RequestHandler):

	def get(self):

		# YConnectオブジェクト生成
		yconnect = YConnectExplicit(client_id, client_secret)

		# パラメータ解析
		code = self.request.get('code');

		if code == '':
			authrization_uri = yconnect.authorization(redirect_uri)
			self.redirect(authrization_uri, permanent=True)

		else:
			access_token = yconnect.token(code, redirect_uri)
			userinfo = yconnect.userinfo(access_token)

			# テンプレートに入れるパラメータ
			values = {
				'account': userinfo['name'],
				'lastname': userinfo['family_name'],
				'firstname': userinfo['given_name'],
				'lastname_kana': userinfo['family_name#ja-Kana-JP'],
				'firstname_kana': userinfo['given_name#ja-Kana-JP'],
				'birthyear': userinfo['birthday'],
				'sex': userinfo['gender'],
				'email': userinfo['email'],
				'zip': userinfo['address']['postal_code'],
				'state': userinfo['address']['region'],
				'city': userinfo['address']['locality'],
			}

			# テンプレートの準備
			template = jinja_environment.get_template('template/registration.html')
			self.response.out.write(template.render(values))

app = webapp2.WSGIApplication([
		                          ('/', TopPage),
		                          ('/registration', RegistrationPage),
															], debug=True)
