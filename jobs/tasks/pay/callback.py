# -*- coding: utf-8 -*-
from common.libs.pay.PayService import PayService
from application import app

'''
job模拟回调方法

'''

class JobTask():
	def __init__(self):
		pass
	def run(self,params):
		id = params['param'][0] if params['param'] and len(params['param']) else 0
		if not id:
			app.logger.info(" fail ")
			return

		target_pay = PayService()
		target_pay.orderSuccess(pay_order_id=id, params={"pay_sn": ""})

		app.logger.info("it's over~~")