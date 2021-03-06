#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 29.08.2013

@author: Philipp Schillinger
'''

class FlexibleCalculationState(EventState):
	'''
	Implements a state that can perform a calculation based on multiple userdata inputs provided as a list to the calculation function.
		
	-- calculation  function    The function that performs the desired calculation.
								It could be a private function (self.foo) manually defined in a behavior's source code
								or a lambda function (e.g., lambda x: x[0]^2 + x[1]^2).

	># input_keys   object[]    Input(s) to the calculation function as a list of userdata.
								The individual inputs can be accessed as list elements (see lambda expression example).

	#> output_value object      The result of the calculation.

	<= done                     Indicates completion of the calculation.

	'''


	def __init__(self, calculation, input_keys):
		'''Constructor'''
		super(FlexibleCalculationState, self).__init__(outcomes=['done'],
											   input_keys=input_keys,
											   output_keys=['output_value'])
		
		self._calculation = calculation
		self._calculation_result = None
		self._input_keys = input_keys
		
		
	def execute(self, userdata):
		'''Execute this state'''

		userdata.output_value = self._calculation_result

		# nothing to check
		return 'done'


	def on_enter(self, userdata):
		
		if self._calculation is not None:
			try:
				self._calculation_result = self._calculation(map(lambda key: userdata[key], self._input_keys))
			except Exception as e:
				Logger.logwarn('Failed to execute calculation function!\n%s' % str(e))
		else:
			Logger.logwarn('Passed no calculation!')
