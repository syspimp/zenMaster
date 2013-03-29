# connect to ec2
import sys
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import Trigger
from boto.ec2.elb import ELBConnection
from boto.ec2.elb import HealthCheck

from optparse import OptionParser

class aws:
    def __init__(self,PREFIX='tfound-',ENV='dev',AMI='',TYPE='',SIZE='',
                 DOMAIN='tfound',SSHKEY='myprivatekey',AWSKEY='',AWSSECRET='',AVAIL_ZONES=["us-east-1a","us-east-1b","us-east-1c","us-east-1d"]):
        '''
        Shows examples
        Create load balancer group 'tfound-dev-web-lb' for web servers, in dev group for tfound:
            python control-lb-and-groups.py --createlb --env dev --aws SC --type web
        Add an instance to the load balancer group:
            python control-lb-and-groups.py --addtolb=true --env dev --aws SC --type web --instance=i-999999
        Create launch config using ami ami-fa6b8393 (default), medium sized instance, and Autoscale Group 'tfound-dev-web-group' with a min of 2 instances, max 5, with health check on port 80:
            python control-lb-and-groups.py  --createlc --ami ami-fa6b8393 --size c1.medium --env dev --aws SC --type web --createag --min 2 --max 5
        Triggers/Health checks are hard coded to spawn new instances when total cpu reaches 60 percent or health check fails.
        '''
        self.PREFIX=PREFIX+DOMAIN+'-'+ENV+'-'+TYPE
        self.ENV=ENV
        self.AMI=AMI
        self.TYPE=TYPE
        self.DOMAIN=DOMAIN
        self.SIZE=SIZE
        self.MIN=MIN
        self.MAX=MAX
        self.SSHKEY=SSHKEY
        self.AWSKEY=AWSKEY
        self.AWSSECRET=AWSSECRET
        self.AVAIL_ZONES=AVAIL_ZONES
        self.LBNAME=self.PREFIX+'-lb'
        self.AGNAME=self.PREFIX+'-group'
        self.TRNAME=self.PREFIX+'-trigger'
        self.LCNAME=self.PREFIX+'-launch_config'
        self.asconn=AutoScaleConnection(self.AWSKEY, self.AWSSECRET)
        self.elbconn = ELBConnection(aws_access_key_id=AWSKEY,aws_secret_access_key=AWSSECRET)
        self.lc = self._buildLaunchConfig()
        self.ag = self._buildAutoscaleGroup()
        
    
    def _buildLaunchConfig(self):
        return LaunchConfiguration(name=self.LCNAME, 
                                   image_id=self.AMI,
                                   key_name=self.SSHKEY,
                                   security_groups=[self.ENV+'.'+self.TYPE],
                                   user_data='LAUNCHTAGS="'+self.ENV+' '
                                   +self.TYPE+' '+self.DOMAIN+'";',
                                   instance_type=self.SIZE)

    def _buildAutoscaleGroup(self):
        return AutoScalingGroup(group_name=self.AGNAME,
                              load_balancers=[self.LBNAME],
                              availability_zones=self.AVAIL_ZONES,
                              launch_config=self.lc, 
                              min_size=self.MIN,
                              max_size=self.MAX)

    def getGroups(self):
        '''get existing lb groups'''
        # conn = AutoScaleConnection(AWSKEY, AWSSECRET)
        #conn = AutoScaleConnection()
        return self.asconn.get_all_groups()

    def getActivities(self,AUTOSCALE_GROUP=None):
        return self.asconn.get_all_activities(AUTOSCALE_GROUP)
                        
    def createLaunchConfig(self):
        '''create Launch Configuration to define initial startup params
        '''
        #conn = AutoScaleConnection(AWSKEY, AWSSECRET)
        #lc = self.buildLaunchConfig()
        return self.asconn.create_launch_configuration(self.lc)
    

        
    def createAutoscaleGroup(self):
        '''We now have created a launch configuration called tfound...launch-config.
        We are now ready to associate it with our new autoscale group.
        returns autoscale object
        '''
        #conn = AutoScaleConnection(AWSKEY, AWSSECRET) 
        #lc = self.buildLaunchConfig()
        
        return self.asconn.create_auto_scaling_group(self.ag)
        #conn.get_all_activities(ag)
        
    def createTrigger(self,AUTOSCALE_GROUP=None):
        ''' 
        you create a trigger on a group, pass in a group object
        this creates a trigger that scales up to MAX instances if average cpu utilitzation goes over 60, 
        scales down to MIN instances if under 40 avg cpu
        '''
        #conn = AutoScaleConnection(AWSKEY, AWSSECRET)
        tr = Trigger(name=self.TRNAME, 
                     autoscale_group=AUTOSCALE_GROUP,
                     measure_name='CPUUtilization', statistic='Average',
                     unit='Percent',
                     dimensions=[('AutoScalingGroupName', AUTOSCALE_GROUP.name),
                                 ('Namespace','AWS/EC2')],
                                 period=120, lower_threshold=10,
                                 lower_breach_scale_increment='-1',
                                 upper_threshold=30,
                                 upper_breach_scale_increment='1',
                                 breach_duration=360)
        return self.asconn.create_trigger(tr)
    
    def createHealthCheck(self):
        return HealthCheck('instance_health', 
                           interval=20, 
                           target='TCP:8080', 
                           timeout='5')
    
    def createLoadbalancer(self):
        #elbconn = ELBConnection(aws_access_key_id=AWSKEY,aws_secret_access_key=AWSSECRET)
        #conn = ELBConnection(aws_access_key_id=AWSKEY,aws_secret_access_key=AWSSECRET,
        #  host='us-east-1a.elasticloadbalancing.amazonaws.com')
        #  hc = HealthCheck('instance_health', interval=20, target='HTTP:80/index.php', timeout='5')
        #  lb = conn.create_load_balancer('tfound-'+options.ENV+'-'+options.TYPE+'-lb', [options.ZONE],
        #                                   [(80, 80, 'http'),(8000,8000, 'tcp')])
        ##  lb.delete()
        hc = self.createHealthCheck()
        lb = self.elbconn.create_load_balancer(self.LBNAME, 
                                               [self.ZONE],
                                               [(8080,8080, 'tcp')])

        lb.configure_health_check(hc)
        return lb.dns_name
    
    def addToLoadbalancer(self,INSTANCE=None):
        #from boto.ec2.elb import ELBConnection
        #from boto.ec2.elb import HealthCheck
        #conn = ELBConnection(aws_access_key_id=AWSKEY,aws_secret_access_key=AWSSECRET)
        #  conn = ELBConnection(aws_access_key_id=AWSKEY,aws_secret_access_key=AWSSECRET,
        #  host='us-east-1a.elasticloadbalancing.amazonaws.com')
        if INSTANCE == None:
            sys.stderr.write("Please provide instance id to add. not acceptble: %s\n" % options.INSTANCE )
            raise SystemExit(1)
        lb = self.elbconn.register_instances(self.LBNAME, 
                                             INSTANCE)
        #lbgroup = 'tfound-'+options.ENV+'-'+options.TYPE+'-lb'
        print "Added instance %s to %s\n" % (INSTANCE, self.LBNAME)

    def getLoadbalancers(self):
        return self.elbconn.get_all_load_balancers()

    def startInstances(self,TYPE='',NUM='',SIZE=''):
        return
