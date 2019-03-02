#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from datetime import datetime, timedelta

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
	def to_dict(self):
		return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
	try:
		with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
			conf_parser = SnipsConfigParser()
			conf_parser.readfp(f)
			return conf_parser.to_dict()
	except (IOError, ConfigParser.Error) as e:
		return dict()

def subscribe_intent_callback(hermes, intentMessage):
	conf = read_configuration_file(CONFIG_INI)
	action_wrapper(hermes, intentMessage, conf)

def action_wrapper(hermes, intentMessage, conf):
	current_session_id = intentMessage.session_id
	result_sentence = ""
	if intentMessage.slots.Question:
		if intentMessage.slots.NextPrevDay:
			if intentMessage.slots.NextPrevDay.first().value == "yesterday":
				d = datetime.now() - timedelta(days=1)
				result_sentence = d.strftime("Yesterday was %A")
			elif intentMessage.slots.NextPrevDay.first().value == "today":
				d = datetime.now()
				result_sentence = d.strftime("It's %A")
			elif intentMessage.slots.NextPrevDay.first().value == "tomorrow":
				d = datetime.now() + timedelta(days=1)
				result_sentence = d.strftime("Tomorrow will be %A")
		elif intentMessage.slots.Day:
			d = datetime.now()
			result_sentence = d.strftime("It's %A")
	hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
	conf = read_configuration_file(CONFIG_INI)
	with Hermes(conf['secret']['mqtt_host']+":"+conf['secret']['mqtt_port']) as h:
		h.subscribe_intent("kajdocsi:Day.d", subscribe_intent_callback).start()