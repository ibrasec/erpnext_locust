from locust import HttpLocust,  TaskSet,  task
import json, requests, random, names, urllib
import numpy as np

cprojects = []

Host = '192.168.88.12'

headers = {
"Host": Host, 
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 61.0) Gecko/20100101 Firefox/61.0", 
"Accept": "application/json,  text/javascript,  */*; q=0.01", 
"Accept-Language": "en-GB, en;q=0.5", 
"Accept-Encoding": "gzip,  deflate", 
"Referer": "http: //"+Host+"/desk", 
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
"X-Frappe-CSRF-Token": "fa55d368060619c7db9e8a593c5f9f14913beb5bc1de0d9fab0131a4", 
"X-Requested-With": "XMLHttpRequest", 
"Content-Length": "564", 
"Cookie": "io=2zIhpA_F26EhxDkTAAAC; user_image=; user_id=Administrator; system_user=yes; full_name=Administrator; sid=54335379586c5fb26ab872ebe825cb7b6cc1f1540a716a2be4f3c869", 
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
    def BrowseEmployee(self):
        self.client.get("/desk#List/Employee/List", name="BrowseEmployee") 
    
    @task(1)
    def AddEmployee(self):
        desig_list = ['Researcher','Designer','Software Developer','Associate','Engineer','Analyst',"Head of Marketing and Sales", "Project Manager", "HR Manager", "Business Development Manager", "Administrative Officer", "Secretary", "Accountant", "CEO"]
        designation = np.random.choice( desig_list, 1, p =[ 0.025, 0.05, 0.2, 0.2, 0.5 ,0.01 , 0.001 ,0.001 ,0.001, 0.001, 0.002, 0.004, 0.004 ,0.001] )[0]
        gender = random.choice(['Male','Female'])
        name = str( names.get_full_name(gender=gender) )
        email = name[0]+'.'+name.split()[1]+'@gmail.com'
        blood = random.choice(['A+','B+','AB+','O+','A-','B-','AB-','O-'])
        phone = str( 92540000 + random.randrange(1,9999) )
        marital = random.choice(['Married','Single'])
        salutation = random.choice(['Dr','Prof','Master'])
        bdate = str( random.randrange(1970,2000) ) + '-' + str( random.randrange(1,12) ) + '-' + str( random.randrange(1,28) )
        payload= {'action': 'Save', 'doc': '{"docstatus":0,"doctype":"Employee",\
        "name":"New Employee 2","__islocal":1,"__unsaved":1,"owner":"Administrator",\
        "naming_series":"EMP/","company":"Ebkar Technology and Management Solutions","status":"Active",\
        "salary_mode":"Cash","prefered_contact_email":"Personal Email","permanent_accommodation_type":"",\
        "current_accommodation_type":"","marital_status":'+'"'+ marital +'"'+',\
        "blood_group":'+'"'+ blood +'"'+',"leave_encashed":"","reason_for_resignation":"","bio":"",\
        "salutation":'+'"'+ salutation +'"'+',"employee_name":'+'"'+ name +'"'+',"date_of_joining":"2018-09-30",\
        "gender":'+'"'+ gender +'"'+',"employment_type":"Contract","personal_email":'+'"'+ email +'"'+',\
        "prefered_email":'+'"'+ email +'"'+',"cell_number":'+'"'+ phone +'"'+',\
        "date_of_birth":'+'"'+ bdate +'"'+',"date_of_retirement":"2060-09-24",\
        "designation":'+'"'+ designation +'"'+'}', 'cmd': 'frappe.desk.form.save.savedocs'}

        #headers["Content-Length"] = str( len( urllib.urlencode(test2) ) )
        self.client.post("/desk#List/Employee/List",
            headers=headers,
            data = payload,
            name='AddEmloyee')
        
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
            num = str( random.randrange(1, 10) )
            project = "KONAMI"+ num
            print 'creating a new project',project
            cprojects.append(project)
            payload2 =  {'doc': '{"docstatus":0,"doctype":"Project","name":'+'"'+"New Project "+num+'"'+',\
            "__islocal":1,"__unsaved":1,"owner":"Administrator","status":"Open","is_active":"Yes","percent_complete_method":"Task Completion","priority":"Medium","company":"Ebkar Technology and Management Solutions","__run_link_triggers":1,"project_name":'+'"'+ project +'"' + ' ,"expected_end_date":"2018-09-30"}', 'cmd': 'frappe.client.insert'}
            payload ={ 'doc': '{"docstatus":0,"doctype":"Project",\
                        "name":"New Project 2","__islocal":1,"__unsaved":1,\
                        "owner":"Administrator","status":"Open","is_active":"Yes",\
                        "project_type_etms":"Internal",\
                        "percent_complete_method":"Task Completion",\
                        "priority":"Medium",\
                        "company":"Ebkar Technology and Management Solutions",\
                        "__run_link_triggers":1,\
                        "project_name":'+'"'+ project +'"' + ' ,\
                        "expected_end_date":"2010-09-1"}',
                         'cmd': 'frappe.client.insert' }
            self.client.post("/desk#List/Project/List",
                headers=headers,
                data = payload2,
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
            self.client.get("http://"+Host+"/desk#Form/Sales%20Order/New%20Sales%20Order%203",
                             name="NewSalesOrder") 
    
        @task(1)
        def MakeSalesOrder(self):
            sales_order_num = str(random.randint(1,4))
            
            payload2 = {'action': 'Save', 'doc':'{"docstatus":0,"doctype":"Sales Order","name":'+'"'+ "New Sales Order "+sales_order_num +'"' + ',\
            "__islocal":1,"__unsaved":1,"owner":"Administrator",\
            "naming_series":"SO-","order_type":"Sales","company":"Ebkar Technology and Management Solutions",\
            "transaction_date":"2018-09-20","customer_group":"Individual","territory":"All Territories",\
            "currency":"LYD","selling_price_list":"Standard Selling","price_list_currency":"LYD",\
            "apply_discount_on":"Grand Total","party_account_currency":"LYD","status":"Draft",\
            "delivery_status":"Not Delivered","billing_status":"Not Billed",\
            "items":[{"docstatus":0,"doctype":"Sales Order Item",\
            "name":'+'"'+ "New Sales Order Item "+sales_order_num +'"' + ',\
            "__islocal":1,"__unsaved":1,"owner":"Administrator","stock_uom":"Nos",\
            "margin_type":"","parent":'+'"'+ "New Sales Order "+sales_order_num +'"' + ',\
            "parentfield":"items","parenttype":"Sales Order","idx":1,"qty":1234,\
            "conversion_factor":1,"stock_qty":1234,"price_list_rate":2000,\
            "base_price_list_rate":2000,"margin_rate_or_amount":0,"rate_with_margin":2000,"discount_amount":0,\
            "base_rate_with_margin":2000,"rate":2000,"amount":2468000,"base_rate":2000,"base_amount":2468000,\
            "net_rate":2000,"net_amount":2468000,"base_net_rate":2000,"base_net_amount":2468000,\
            "weight_per_unit":0,"total_weight":0,"projected_qty":0,"actual_qty":0,"ordered_qty":0,\
            "delivered_qty":0,"returned_qty":0,"billed_amt":0,"valuation_rate":0,"gross_profit":0,\
            "planned_qty":0,"produced_qty":0,"item_code":"camara",\
            "barcode":null,"item_group":"All Item Groups","last_purchase_rate":null,"image":"",\
            "expense_account":"Cost of Goods Sold - ETMS","item_tax_rate":"{}",\
            "cost_center":"Main - ETMS","pricing_rule":null,"income_account":"Sales - ETMS",\
            "item_name":"camara","warehouse":"Stores - ETMS","uom":"Nos","description":"camara",\
            "brand":null,"supplier":null,"has_serial_no":0,"weight_uom":null,"reserved_qty":0,\
            "discount_percentage":0,"min_order_qty":"","update_stock":0,"customer_item_code":null,\
            "has_batch_no":0,"batch_no":null,"delivered_by_supplier":0,"is_fixed_asset":0,\
            "serial_no":null,"delivery_date":"2018-09-20"}],"terms":"","conversion_rate":1,\
            "plc_conversion_rate":1,"base_net_total":2468000,"net_total":2468000,\
            "base_total":2468000,"total":2468000,"rounding_adjustment":0,"grand_total":2468000,\
            "base_grand_total":2468000,"total_taxes_and_charges":0,\
            "base_total_taxes_and_charges":0,"base_rounding_adjustment":0,"rounded_total":2468000,\
            "base_rounded_total":2468000,"in_words":"","base_in_words":"","base_discount_amount":0,\
            "total_commission":null,"customer_name":"Guest","tax_id":null,"customer":"Guest",\
            "payment_terms_template":null,"contact_display":"Guest","address_display":null,\
            "taxes_and_charges":null,"customer_address":null,"contact_email":"Guest","contact_mobile":null,\
            "language":"en","shipping_address_name":"","shipping_address":null,\
            "contact_person":"Guest-Guest","sales_team":[],"total_net_weight":0,\
            "delivery_date":"2018-09-20"}', 'cmd': 'frappe.desk.form.save.savedocs'}
            
            payload = { 'doc': '{"docstatus":0,"doctype":"Sales Order","name":"New Sales Order 2",\
                "__islocal":1,"__unsaved":1,"owner":"Administrator","naming_series":"SO-",\
                "order_type":"Sales","company":"Ebkar Technology and Management Solutions",\
                "transaction_date":"2018-09-11","customer_group":"Individual","territory":"All Territories",\
                "currency":"LYD","selling_price_list":"Standard Selling","price_list_currency":"LYD",\
                "apply_discount_on":"Grand Total","party_account_currency":"LYD","letter_head":"brega",\
                "status":"Draft","delivery_status":"Not Delivered","billing_status":"Not Billed",\
                "items":[{"docstatus":0,"doctype":"Sales Order Item","name":'+'"'+ "New Sales Order Item "+sales_order_num +'"' + ',\
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
            self.client.post("http://"+Host+"/desk#Form/Sales%20Order/New%20Sales%20Order%20"+sales_order_num,
                 headers=headers,
                 data = payload2,
                 name='MakeSalesOrder')
                 
        @task(1)
        def SubmitSalesOrder(self):
            url = 'http://'+Host+'/'
            sales_order_list = {
            'start':'0','page_length':'20','doctype':'Sales Order',\
            'fields':'["`tabSales Order`.`name`","`tabSales Order`.`owner`","`tabSales Order`.`docstatus`","`tabSales Order`.`_user_tags`","`tabSales Order`.`_comments`","`tabSales Order`.`modified`","`tabSales Order`.`modified_by`","`tabSales Order`.`_assign`","`tabSales Order`.`_liked_by`","`tabSales Order`.`_seen`","`tabSales Order`.`title`","`tabSales Order`.`delivery_date`","`tabSales Order`.`grand_total`","`tabSales Order`.`currency`","`tabSales Order`.`status`","`tabSales Order`.`per_delivered`","`tabSales Order`.`per_billed`","`tabSales Order`.`base_grand_total`","`tabSales Order`.`customer_name`","`tabSales Order`.`order_type`"]','with_comment_count':'true','filters':'[["Sales Order","status","=","Draft"]]',
            'order_by':'`tabSales Order`.`modified` desc','cmd':'frappe.desk.reportview.get','_':'1537013118122'
            }
            r = requests.get(url,cookies=headers,params=sales_order_list)
            if r.content != '{}': 
                j = json.loads(r.content)
                SO_info = dict( zip(j['message']['keys'], j['message']['values'][0]) )
                Goto = url+'desk#Form/Sales%20Order/'+str( SO_info['name'] )
                print Goto
                asd = {'action': 'Submit', 'doc': '{"billing_status":"Not Billed","modified_by":'+'"'+str( SO_info["modified_by"] )+'"'+',\
                "title":'+'"'+str( SO_info["title"] )+'"'+',"packed_items":[],"selling_price_list":"Standard Selling",\
                "base_grand_total":'+'"'+str(SO_info["base_grand_total"])+'"'+',\
                "base_in_words":"","ignore_pricing_rule":0,"base_discount_amount":0,"base_total_taxes_and_charges":0,\
                "discount_amount":0,"name":'+'"'+str( SO_info["name"] )+'"'+',"taxes":[],"base_rounding_adjustment":0,"delivery_date":'+'"'+str( SO_info["delivery_date"] )+'"'+',\
                "creation":'+'"'+str( SO_info["modified"] )+'"'+',"party_account_currency":'+'"'+str( SO_info["currency"] )+'"'+',"modified":'+'"'+str( SO_info["modified"] )+'"'+',"price_list_currency":'+'"'+str( SO_info["currency"] )+'"'+',\
                "contact_display":"Guest","terms":"","advance_paid":0,"total_commission":0,\
                "delivery_status":"Not Delivered","base_net_total":'+'"'+str(SO_info["base_grand_total"])+'"'+',"language":"en",\
                "items":[{"stock_qty":10,"base_price_list_rate":2000,"image":"","creation":'+'"'+str( SO_info["modified"] )+'"'+',\
                "base_amount":'+'"'+str(SO_info["base_grand_total"])+'"'+',"qty":10,"margin_rate_or_amount":0,"rate":2000,"total_weight":0,"owner":'+'"'+str(SO_info["owner"])+'"'+',\
                "stock_uom":"Nos","base_net_amount":'+'"'+str(SO_info["base_grand_total"])+'"'+',"page_break":0,"modified_by":'+'"'+str( SO_info["modified_by"] )+'"'+',"base_net_rate":2000,\
                "discount_percentage":0,"item_name":"camara","amount":'+'"'+str(SO_info["base_grand_total"])+'"'+',"actual_qty":0,"net_rate":2000,"conversion_factor":1,\
                "base_rate_with_margin":0,"docstatus":'+'"'+str( SO_info["docstatus"] )+'"'+',"uom":"Nos","ordered_qty":0,"doctype":"Sales Order Item","description":"camara",\
                "parent":"SO-00030","gross_profit":0,"returned_qty":0,"base_rate":2000,"item_code":"camara",\
                "produced_qty":0,"projected_qty":-2469,"warehouse":"Stores - ETMS","margin_type":"",\
                "billed_amt":0,"rate_with_margin":0,"delivered_qty":0,"delivered_by_supplier":0,\
                "discount_amount":0,"price_list_rate":2000,"transaction_date":"2018-09-20",\
                "name":"27e1ca089c","idx":1,"item_tax_rate":"{}","item_group":"All Item Groups",\
                "planned_qty":0,"modified":'+'"'+str( SO_info["modified"] )+'"'+',"weight_per_unit":0,"parenttype":"Sales Order",\
                "valuation_rate":0,"net_amount":'+'"'+str(SO_info["base_grand_total"])+'"'+',"delivery_date":'+'"'+str( SO_info["delivery_date"] )+'"'+',\
                "parentfield":"items"}],"shipping_address_name":"","apply_discount_on":"Grand Total",\
                "contact_person":"Guest-Guest","in_words":"","additional_discount_percentage":0,\
                "conversion_rate":1,"owner":'+'"'+str(SO_info["owner"])+'"'+',"total":'+'"'+str(SO_info["base_grand_total"])+'"'+',"customer_name":'+'"'+str( SO_info["customer_name"] )+'"'+',\
                "commission_rate":0,"base_total":'+'"'+str(SO_info["base_grand_total"])+'"'+',"territory":"All Territories",\
                "company":"Ebkar Technology and Management Solutions","base_rounded_total":'+'"'+str(SO_info["base_grand_total"])+'"'+',"customer":"Guest",\
                "grand_total":'+'"'+str( SO_info["grand_total"] )+'"'+',"idx":0,"doctype":"Sales Order","rounding_adjustment":0,"rounded_total":'+'"'+str(SO_info["base_grand_total"])+'"'+',\
                "customer_group":"Individual","naming_series":"SO-","currency":'+'"'+str( SO_info["currency"] )+'"'+',\
                "order_type":'+'"'+str( SO_info["order_type"] )+'"'+',"transaction_date":"2018-09-20","docstatus":'+'"'+str( SO_info["docstatus"] )+'"'+',"per_delivered":'+'"'+str( SO_info["per_delivered"] )+'"'+',\
                "status":'+'"'+str( SO_info["status"] )+'"'+',"group_same_items":0,"__onload":{"make_payment_via_journal_entry":0},\
                "per_billed":'+'"'+str(SO_info["per_billed"])+'"'+',"total_net_weight":0,"net_total":'+'"'+str(SO_info["base_grand_total"])+'"'+',"payment_schedule":[{"due_date":"2018-09-20",\
                "name":"ce79795855","parent":"SO-00030","creation":'+'"'+str( SO_info["modified"] )+'"'+',\
                "modified":'+'"'+str( SO_info["modified"] )+'"'+',"doctype":"Payment Schedule","idx":1,\
                "parenttype":"Sales Order","payment_amount":'+'"'+str(SO_info["base_grand_total"])+'"'+',"invoice_portion":100,\
                "docstatus":'+'"'+str( SO_info["docstatus"] )+'"'+',"parentfield":"payment_schedule"}],"plc_conversion_rate":1,\
                "total_taxes_and_charges":0,"contact_email":"Guest","sales_team":[],\
                "__last_sync_on":"2018-09-20T20:51:07.098Z"}', "cmd": "frappe.desk.form.save.savedocs"}
                self.client.post(Goto,
                     headers=headers,
                     data = asd,
                     name='SubmitSalesOrder')
            

        @task(1)
        def stop(self):
            self.interrupt()



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000



