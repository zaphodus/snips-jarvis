#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io
import sys
from datetime import datetime

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
	except:
		return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)

def action_wrapper(hermes, intentMessage, conf):
	current_session_id = intentMessage.session_id
	result_sentence = "It is wibbily wobbly timey wimey"
	if intentMessage.slots.Question:
		if intentMessage.slots.PartsOfTheDay or intentMessage.slots.TimeOfDay:
			now = datetime.now()
			h = now.hour
			if h < 4:
				result_sentence = "It is quarter very early"
			elif h < 5:
				result_sentence = "It is half past very early"
			elif h < 6:
				result_sentence = "It is quarter to very early"
			elif h < 7:
				result_sentence = "It is very early"
			elif h < 8:
				result_sentence = "It is breakfast time"
			elif h < 9:
				result_sentence = "It is morning"
			elif h < 10:
				result_sentence = "It is snack time"
			elif h < 11:
				result_sentence = "It is morning"
			elif h < 12:
				result_sentence = "It is lunch time"
			elif h < 13:
				result_sentence = "It is afternoon"
			elif h < 14:
				result_sentence = "It is afternoon"
			elif h < 15:
				result_sentence = "It is snack time"
			elif h < 16:
				result_sentence = "It is afternoon"
			elif h < 17:
				result_sentence = "It is afternoon"
			elif h < 18:
				result_sentence = "It is afternoon"
			elif h < 19:
				result_sentence = "It is dinner time"
			elif h < 20:
				result_sentence = "It is evening"
			elif h < 21:
				result_sentence = "It is quarter very late"
			elif h < 22:
				result_sentence = "It is half past very late"
			elif h < 23:
				result_sentence = "It isquarter to very late"
			elif h < 24:
				result_sentence = "It is very late"
	hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
	conf = read_configuration_file(CONFIG_INI)
	mqtt_opts = MqttOptions(
		#username=conf["secret"]["mqtt_username"], 
		#password=conf["secret"]["mqtt_password"],
		#tls_hostname=conf["secret"]["mqtt_host"],
		broker_address=conf["secret"]["mqtt_host"]+":"+conf["secret"]["mqtt_port"]
	)
	with Hermes(mqtt_options=mqtt_opts) as h:
		h.subscribe_intent("kajdocsi:GoblinTime", subscribe_intent_callback).start()

