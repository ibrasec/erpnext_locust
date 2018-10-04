import urllib

def GetPayload(text):
    """
    To convert 
    doc={"docstatus":0,"doctype":"Project","name":"New Project 5","__islocal":1,"__unsaved":1,"owner":"Administrator","status":"Open","is_active":"Yes","percent_complete_method":"Task Completion","priority":"Medium","company":"Ebkar Technology and Management Solutions","__run_link_triggers":1,"project_name":"assdsd","expected_end_date":"2018-09-20"}&cmd=frappe.client.insert
    
    To
    
    {'doc': '{"docstatus":0,"doctype":"Project","name":"New Project 5","__islocal":1,"__unsaved":1,"owner":"Administrator","status":"Open","is_active":"Yes","percent_complete_method":"Task Completion","priority":"Medium","company":"Ebkar Technology and Management Solutions","__run_link_triggers":1,"project_name":"assdsd","expected_end_date":"2018-09-20"}', 'cmd': 'frappe.client.insert'}

    
    """
    payload = {}
    line = text.split('&')
    for section in line:
        a = section.split('=')
        payload[a[0]]=a[1]
    return payload


    
def URLDecode(url):
    """
    To convert this 
    doc%3D%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Project%22%2C%22name%22%3A%22New%20Project%205%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22Administrator%22%2C%22status%22%3A%22Open%22%2C%22is_active%22%3A%22Yes%22%2C%22percent_complete_method%22%3A%22Task%20Completion%22%2C%22priority%22%3A%22Medium%22%2C%22company%22%3A%22Ebkar%20Technology%20and%20Management%20Solutions%22%2C%22__run_link_triggers%22%3A1%2C%22project_name%22%3A%22assdsd%22%2C%22expected_end_date%22%3A%222018-09-20%22%7D%26cmd%3Dfrappe.client.insert
    into 
    'doc={"docstatus":0,"doctype":"Project","name":"New Project 5","__islocal":1,"__unsaved":1,"owner":"Administrator","status":"Open","is_active":"Yes","percent_complete_method":"Task Completion","priority":"Medium","company":"Ebkar Technology and Management Solutions","__run_link_triggers":1,"project_name":"assdsd","expected_end_date":"2018-09-20"}&cmd=frappe.client.insert'
    """
    url = urllib.unquote(url)
    return url
    

GetPayload(URLDecode(''))
