from locust import HttpLocust,  TaskSet,  task
import json
import random

cprojects = []


headers = {
"Host": "192.168.88.20", 
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 61.0) Gecko/20100101 Firefox/61.0", 
"Accept": "application/json,  text/javascript,  */*; q=0.01", 
"Accept-Language": "en-GB, en;q=0.5", 
"Accept-Encoding": "gzip,  deflate", 
"Referer": "http: //192.168.88.20/desk", 
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
"X-Frappe-CSRF-Token": "e67e6f8163c586d15b4f88213fb05176901b8a9ddb17bc266f810a09", 
"X-Requested-With": "XMLHttpRequest", 
"Content-Length": "564", 
"Cookie": "io=Asu0A34qiEic4ZJzAAAI; user_image=; user_id=Administrator; system_user=yes; full_name=Administrator; sid=7232481c005112558f769a040c25de61bdcdb5aa044c579fbfdd87e6", 
"Connection": "keep-alive"
}


class UserBehavior(TaskSet):
    def on_start(self): 
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    @task
    def login(self):
        pass

    @task(1)
    def index(self):
        print "Locust instance (%r) executing my_task" % (self.locust)
        self.client.get("/")
    
    @task(1)
    def profile(self):
        self.client.get("/profile")

    @task(1)
    def projectList(self): 
        self.client.get("/desk#List/Project/List", name="Projextlst") 
               
    @task(1)
    class Projects(TaskSet):
        @task(1)
        def postlike(self):
            #doctype=Project&name=test 11&add=Yes&cmd=frappe.desk.like.toggle_like
            payload = {'doctype': 'Project', 'name': 'test 11', 'add': 'Yes', 'cmd': 'frappe.desk.like.toggle_like'}
            self.client.post("/desk#List/Project/List",
                             headers=headers,
                             data = payload,
                             name='postlike')
        @task(1)
        def postNolike(self):
            #doctype=Project&name=test 11&add=Yes&cmd=frappe.desk.like.toggle_like
            payload = {'doctype': 'Project', 'name': 'test 11', 'add': 'No', 'cmd': 'frappe.desk.like.toggle_like'}
            self.client.post("/desk#List/Project/List",
                             headers=headers,
                             data = payload,
                             name='postNolike')
    
        @task(1)
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
    
        # commented because deleting a single project
        # genreates about 200 of queries
        #@task(1)
        # def deleteProject(self):
        #     if cprojects !=[]:
        #         rproject = cprojects.pop()
        #         print "removing project",rproject
        #         payload ={'items': '["' + rproject + '"]', 
        #                 'cmd': "frappe.desk.reportview.delete_items" ,
        #                 'doctype': "Project" }
        #         self.client.post("/desk#List/Project/List",
        #             headers=headers,
        #             data = payload,
        #             name='deleteProject')
    
        @task(1)
        def stop(self):
            self.interrupt()
    # There is a problem here, because you have to know the 
    # Sales order number of the last ordered product, this
    # requires requests library maybe bautifulsoup
    @task(1)
    class SalesOrder(TaskSet):
        @task(1)
        def GotoSalesOrder(self): 
            self.client.get("/desk#List/Sales Order/List", name="GotoSalesOrder") 
    
        @task(1)
        def NewSalesOrder(self): 
            self.client.get("http://192.168.88.20/desk#Form/Sales%20Order/New%20Sales%20Order%203",
                             name="NewSalesOrder") 
    
        @task(1)
        def MakeSalesOrder(self):
            sales_order_num = str(random.randint(1,100))
            payload = { 'doc': '{"docstatus":0,"doctype":"Sales Order","name":"New Sales Order 2",\
                "__islocal":1,"__unsaved":1,"owner":"Administrator","naming_series":"SO-",\
                "order_type":"Sales","company":"Ebkar Technology and Management Solutions",\
                "transaction_date":"2018-09-11","customer_group":"Individual","territory":"All Territories",\
                "currency":"LYD","selling_price_list":"Standard Selling","price_list_currency":"LYD",\
                "apply_discount_on":"Grand Total","party_account_currency":"LYD","letter_head":"brega",\
                "status":"Draft","delivery_status":"Not Delivered","billing_status":"Not Billed",\
                "items":[{"docstatus":0,"doctype":"Sales Order Item","name":"New Sales Order Item 2",\
                "__islocal":1,"__unsaved":1,"owner":"Administrator","stock_uom":"Unit",\
                "margin_type":"","parent":'+'"'+ "New Sales Order "+sales_order_num +'"' + ',"parentfield":"items",\
                "parenttype":"SalesOrder","idx":1,"qty":1234,"conversion_factor":1,\
                "stock_qty":1234,"price_list_rate":2000,"base_price_list_rate":2000,\
                "margin_rate_or_amount":0,"rate_with_margin":2000,"base_rate_with_margin":2000,\
                "rate":2000,"amount":2468000,"base_rate":2000,"base_amount":2468000,"net_rate":2000,\
                "net_amount":2468000,"base_net_rate":2000,"base_net_amount":2468000,"weight_per_unit":0,\
                "total_weight":0,"projected_qty":-14,"actual_qty":0,"ordered_qty":0,"delivered_qty":0,\
                "returned_qty":0,"billed_amt":0,"valuation_rate":0,"gross_profit":0,"planned_qty":0,\
                "produced_qty":0,"item_code":"camara","barcode":null,"item_group":"All Item Groups",\
                "last_purchase_rate":null,"image":"/files/_b0a50bd888272c27c7d75bc2aaefe2d4621ed4e12e60bd9f04_pimgpsh_fullsize_distr_1.jpg",\
                "expense_account":"Cost of Goods Sold - ETMS","item_tax_rate":"{}",\
                "cost_center":"Main - ETMS","pricing_rule":null,\
                "income_account":"Sales - ETMS","item_name":"camara",\
                "warehouse":"Stores - ETMS","uom":"Unit","description":"camara","brand":null,\
                "supplier":null,"has_serial_no":0,"weight_uom":null,"discount_percentage":0,\
                "min_order_qty":"","update_stock":0,"customer_item_code":null,"has_batch_no":0,\
                "batch_no":null,"delivered_by_supplier":0,"is_fixed_asset":0,"delivery_date":"2018-09-25",\
                "serial_no":null}],"terms":"","conversion_rate":1,"plc_conversion_rate":1,\
                "base_net_total":2468000,"net_total":2468000,"base_total":2468000,"total":2468000,\
                "rounding_adjustment":0,"grand_total":2468000,"base_grand_total":2468000,"total_taxes_and_charges":0,\
                "base_total_taxes_and_charges":0,"base_rounding_adjustment":0,\
                "rounded_total":2468000,"base_rounded_total":2468000,"in_words":"","base_in_words":"",\
                "base_discount_amount":0,"total_commission":null,"customer_name":"Guest","tax_id":null,\
                "customer":"Guest","payment_terms_template":null,"contact_display":"Guest","address_display":null,\
                "taxes_and_charges":null,"customer_address":null,"contact_email":"Guest",\
                "contact_mobile":null,"language":"en","shipping_address_name":"","shipping_address":null,\
                "contact_person":"Guest-Guest","sales_team":[],"total_net_weight":0}',\
                'action': "Save", 'cmd': "frappe.desk.form.save.savedocs" }
            self.client.post("http://192.168.88.20/desk#Form/Sales%20Order/New%20Sales%20Order%20"+sales_order_num,
                 headers=headers,
                 data = payload,
                 name='MakeSalesOrder')
        @task(1)
        def stop(self):
            self.interrupt()



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000



