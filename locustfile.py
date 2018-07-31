from locust import HttpLocust,  TaskSet,  task
import json
import random

cprojects = []


headers = {
"Host": "192.168.88.10", 
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 61.0) Gecko/20100101 Firefox/61.0", 
"Accept": "application/json,  text/javascript,  */*; q=0.01", 
"Accept-Language": "en-GB, en;q=0.5", 
"Accept-Encoding": "gzip,  deflate", 
"Referer": "http: //192.168.88.10/desk", 
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
"X-Frappe-CSRF-Token": "5c4df4db1a57cd5d4748cd5f3250d9843d39ee62169ec1366e186871", 
"X-Requested-With": "XMLHttpRequest", 
"Content-Length": "586", 
"Cookie": "user_image=; user_id=Administrator; system_user=yes; full_name=Administrator; sid=11826fe27d22af5a0c003cca6261c34ff9216b856ef76d30f76eb1b8; io=y_a8z3KO9YyRH7TdAAAA", 
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
            self.client.get("/desk#List/Project/List", name="Projextlst")
    
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
        
        @task(2)
        def postNewProject(self):
            num = str( random.randrange(10, 100) )
            project = "KONAMI"+ num
            print 'creating a new project',project
            cprojects.append(project)
            payload ={ 'doc': '{"docstatus":0,"doctype":"Project",\
                        "name":"New Project 2","__islocal":1,"__unsaved":1,\
                        "owner":"Administrator","status":"Open","is_active":"Yes",\
                        "project_type_etms":"Internal",\
                        "percent_complete_method":"Task Completion",\
                        "priority":"Medium",\
                        "company":"Ebkar Technology and Management Solutions",\
                        "__run_link_triggers":1,\
                        "project_name":'+'"'+ project +'"' + ' ,\
                        "expected_end_date":"2018-07-31"}',
                         'cmd': 'frappe.client.insert' }
            self.client.post("/desk#List/Project/List",
                headers=headers,
                data = payload,
                name='postNewProject')

        @task(1)
        def deleteProject(self):
            if cprojects !=[]:
                rproject = cprojects.pop()
                print "removing project",rproject
                payload ={'items': '["' + rproject + '"]', 
                        'cmd': "frappe.desk.reportview.delete_items" ,
                        'doctype': "Project" }
                self.client.post("/desk#List/Project/List",
                    headers=headers,
                    data = payload,
                    name='deleteProject')
   
        @task
        def stop(self):
            self.interrupt()


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000



