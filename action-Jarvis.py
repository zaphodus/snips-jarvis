#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io
import sys

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
    result_sentence = "I'm Jarvis! Just A Rather Very Intelligent System!"
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
	conf = read_configuration_file(CONFIG_INI)
	mqtt_opts = MqttOptions(
	#	username=conf["secret"]["mqtt_username"], 
	#	password=username=conf["secret"]["mqtt_password"],
		broker_address=conf["secret"]["mqtt_host"]+":"+conf["secret"]["mqtt_port"]
	)
	with Hermes(mqtt_options=mqtt_opts) as h:
		h.subscribe_intent("kajdocsi:Jarvis", subscribe_intent_callback).start()

