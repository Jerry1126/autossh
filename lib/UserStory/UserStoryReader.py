'''
Created on Sep 2, 2014

@author: j19li
'''
import os
import USDescriptor
filter_rules={'not_run_standalone':lambda x:x.run_standalone==0,
              'run_standalone':lambda x:x.run_standalone==1,
              'without_koala_template':lambda x:x.KoalaTemplate is None,
              'without_general_conf_template':lambda x:x.GeneralConfTemplate is None}
class UserStoryReader:
    _user_stories = None
    def __init__(self):
        self._user_story_dir = "%s%s%s" % (os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.path.sep, 'USS')
        UserStoryReader._user_stories = self._read_all_user_stories() if UserStoryReader._user_stories is None else UserStoryReader._user_stories
    def list_user_stories(self):
        return filter(lambda x:os.path.isdir('%s%s%s' % (self._user_story_dir, os.path.sep, x)) 
                           and os.path.exists("%s%s%s%s%s" % (self._user_story_dir, os.path.sep, x, os.path.sep, 'USDescriptor.xml'))
                           and os.path.isfile("%s%s%s%s%s" % (self._user_story_dir, os.path.sep, x, os.path.sep, 'USDescriptor.xml')),
                      os.listdir(self._user_story_dir))
    def _read_user_story(self, us_id):
        us_desc = "%s%s%s%s%s" % (self._user_story_dir, os.path.sep, us_id, os.path.sep, 'USDescriptor.xml')
        f = open(us_desc)
        xml = f.read()
        return USDescriptor.CreateFromDocument(xml)
    def _read_all_user_stories(self):
        return dict(map(lambda x:(x, self._read_user_story(x)), self.list_user_stories()))
    def _get_subset_userstories_by_given_filter_fun(self, uss, filter_fun):
        def f_n(x):
            u=UserStoryReader._user_stories.get(x,None)
            return (u is not None) and (isinstance(u, USDescriptor.USType)) and filter_fun(u)
        return filter(f_n,uss)
    def get_subset_user_stories_by_given_filter_keys(self,uss,keys=[]):
        fs=filter(lambda x:x is not None,map(lambda x:filter_rules.get(x,None),keys))
        filter_fun=lambda x:reduce(lambda a,b:a and b(x),fs,True)
        return self._get_subset_userstories_by_given_filter_fun(uss,filter_fun)
    def get_subset_user_stories_non_standalone(self,uss):
        return self.get_subset_user_stories_by_given_filter_keys(uss, ['not_run_standalone'])
    def get_subset_user_stories_without_koala_template(self,uss):
        return self.get_subset_user_stories_by_given_filter_keys(uss, ['without_koala_template'])
#    def get_non_standalone_userstories_without_koala_and_generalconf_template(self):
        
        
