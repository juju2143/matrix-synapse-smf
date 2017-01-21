# -*- coding: utf-8 -*-

__version__ = "0.0.1"

from twisted.internet import defer
import logging
import bcrypt
import MySQLdb
import atexit

logger = logging.getLogger("synapse") #__name__)

class SmfAuthProvider(object):
	__version__ = "0.0.1"

	def __init__(self, config, account_handler):
		self.account_handler = account_handler
		self.smf_host = config.host
		self.smf_user = config.user
		self.smf_password = config.password
		self.smf_database = config.database
		self.smf_db_prefix = config.db_prefix
		self.smf_minimum_posts = config.minimum_posts
		self.db = MySQLdb.connect(self.smf_host,self.smf_user,self.smf_password,self.smf_database)
		atexit.register(self.cleanup)

	@defer.inlineCallbacks
	def check_password(self, user_id, password):
		if not password:
			defer.returnValue(False)
		localpart = user_id.split(":", 1)[0][1:]
		cursor = self.db.cursor()
		cursor.execute("""SELECT passwd FROM `%s` WHERE member_name = %%s AND posts >= %%s;""" % (self.smf_db_prefix+"members",), (localpart,self.smf_minimum_posts))
		hash = cursor.fetchone()
		if not hash:
			defer.returnValue(False)
		if bcrypt.checkpw(localpart.lower()+password, hash[0]):
			# TODO: check if user is banned
			# TODO: something about spaces
			logger.info("Valid password for user %s: %s", localpart, hash[0])
			if (yield self.account_handler.check_user_exists(user_id)):
				logger.info("User %s exists, logging in", user_id)
				defer.returnValue(True)
			else:
				try:
					user_id, access_token = (
						# TODO: admin
						yield self.account_handler.register(localpart=localpart)
					)
					logger.info("User %s created, logging in", localpart)
					defer.returnValue(True)
				except:
					logger.warning("User %s not created", localpart)
					defer.returnValue(False)
		else:
			logger.warning("Wrong password for user %s", localpart)
			defer.returnValue(False)

	@staticmethod
	def parse_config(config):
		class _SmfConfig(object):
			pass
		smf_config = _SmfConfig()
		smf_config.enabled = config.get("enabled", False)
		smf_config.host = config.get("host", "localhost")
		smf_config.user = config.get("user", "smf")
		smf_config.password = config.get("password", "")
		smf_config.database = config.get("database", "smf")
		smf_config.db_prefix = config.get("db_prefix", "smf_")
		smf_config.minimum_posts = config.get("minimum_posts", "0")

		return smf_config

	def cleanup(self):
		self.db.close()
