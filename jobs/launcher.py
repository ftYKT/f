# -*- coding: utf-8 -*-
from application import app,manager
from flask_script import Command,Option
import argparse,sys,traceback


class runJob( Command ):

    capture_all_args = True
    def run(self,*args,**kwargs):
        args = sys.argv[2:]
        parser = argparse.ArgumentParser( add_help = True )

        parser.add_argument("-m","--name",dest = "name",metavar = "name", help="指定job名",required=True)
        parser.add_argument("-a","--act",dest = "act",metavar = "act", help="Job动作",required=False)
        parser.add_argument("-p","--param",dest = "param",nargs = "*", metavar = "param",help="业务参数",default = '',required=False)
        params = parser.parse_args( args )
        params_dict = params.__dict__
        ret_params = {}
        for item in params_dict.keys():
            ret_params[ item ] = params_dict[ item ]

        if "name" not in ret_params or not ret_params['name']:
            return self.tips()

        module_name = ret_params['name'].replace( "/","." )
        try:
            import_string = "from jobs.tasks.%s import JobTask as  job_target" % ( module_name )
            exec( import_string , globals() )
            target = job_target()
            target.run( ret_params )
        except Exception as e:
            traceback.print_exc()


    def tips(self):
        tip_msg = '''
            请正确调度Job
            python manage runjob -m Test  (  jobs/tasks/Test.py )
            python manage runjob -m test/Index (  jobs/tasks/test/Index.py )
        '''
        app.logger.info( tip_msg )
        return False
