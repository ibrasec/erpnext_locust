from locust import HttpLocust,  TaskSet,  task
import json
import random


headers = {
"Host": "192.168.88.10", 
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 61.0) Gecko/20100101 Firefox/61.0", 
"Accept": "application/json,  text/javascript,  */*; q=0.01", 
"Accept-Language": "en-GB, en;q=0.5", 
"Accept-Encoding": "gzip,  deflate", 
"Referer": "http: //192.168.88.10/desk", 
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
"X-Frappe-CSRF-Token": "2b8c1344487cbfabea4df9a111c9197bf103e9ec28414b1954b151b3", 
"X-Requested-With": "XMLHttpRequest", 
"Content-Length": "586", 
"Cookie": "user_image=; user_id=Administrator; system_user=yes; full_name=Administrator; sid=a9010ef96c805b8f30d2e0b94099ada175b69aeb35d752c2a0f53eba; io=MYAQbjI8jP8fLsnOAAAA", 
"Connection": "keep-alive"
}


class UserBehavior(TaskSet):
    def on_start(self): 
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    @task
    def login(self):
        pass

    @task
    class subTaskset(TaskSet):
        @task
        def index(self):
            print "Locust instance (%r) executing my_task" % (self.locust)
            self.client.get("/")
    
        @task
        def profile(self):
            self.client.get("/profile")

        @task
        def projectList(self): 
            response = self.client.get("/desk#List/Project/List", name="Projextlst")
            print "Response status code: ",  response.status_code
    
        @task(2)
        def postlike(self):
            #doctype=Project&name=test 11&add=Yes&cmd=frappe.desk.like.toggle_like
            payload = {'doctype': 'Project', 'name': 'test 11', 'add': 'Yes', 'cmd': 'frappe.desk.like.toggle_like'}
            self.client.post("/desk#List/Project/List",
                             headers=headers,
                             data = payload,
                             name='postlike')
        @task(2)
        def postNolike(self):
            #doctype=Project&name=test 11&add=Yes&cmd=frappe.desk.like.toggle_like
            payload = {'doctype': 'Project', 'name': 'test 11', 'add': 'No', 'cmd': 'frappe.desk.like.toggle_like'}
            self.client.post("/desk#List/Project/List",
                             headers=headers,
                             data = payload,
                             name='postNolike')

        @task(5)
        def postNewProject(self):
            num = str( random.randrange(10, 100) )
            word = "KONAMI"+ num
            payload ={ 'doc': '{"docstatus":0,"doctype":"Project",\
                        "name":"New Project 2","__islocal":1,"__unsaved":1,\
                        "owner":"Administrator","status":"Open","is_active":"Yes",\
                        "project_type_etms":"Internal",\
                        "percent_complete_method":"Task Completion",\
                        "priority":"Medium",\
                        "company":"Ebkar Technology and Management Solutions",\
                        "__run_link_triggers":1,\
                        "project_name":'+'"'+ word +'"' + ' ,\
                        "expected_end_date":"2018-07-31"}',
                         'cmd': 'frappe.client.insert' }
            self.client.post("/desk#List/Project/List",
                headers=headers,
                data = payload,
                name='postNewProject')

   
        @task
        def stop(self):
            self.interrupt()


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000



