# -*- coding: utf-8 -*-
from common.libs.pay.PayService import PayService
from application import app

'''
job模拟回调方法
其实所有回调基本都是校验合法性 然后找到订单id，所以我们模拟就是直接传递 订单id
python manager.py runjob -m pay/callback -p 1
详解可以看博文： http://www.54php.cn/default/281.html
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