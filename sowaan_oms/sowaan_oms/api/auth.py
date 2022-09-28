import frappe
from frappe import _
from frappe.utils import (
	escape_html
)
import random
# from frappe.core.doctype.user.user import (
#     update_password
# )

from frappe.utils.password import update_password
import json
@frappe.whitelist(allow_guest=True)
def create_new_user(email, mobile_no, full_name, password):
    user = frappe.db.get("User", {"email": email})
    if user:
        if user.enabled:
            return "Already registered"
                
        else:
            return "Registered but disabled"
    else:
        if frappe.db.get_creation_count("User", 60) > 300:
            return "Too many users signed up recently, so the registration is disabled. Please try back in an hour"
                    
            
			

        from frappe.utils import random_string

        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "mobile_no":mobile_no,
                "first_name": escape_html(full_name),
                "enabled": 0,
                "new_password": password,#random_string(10),
                "user_type": "Website User",
                "send_welcome_email":0
            }
        )
        user.flags.ignore_permissions = True
        #user.flags.ignore_password_policy = True
        try:
            user.insert()
        except Exception as e:
            frappe.throw(e)
        # update_password(user=user, pwd=password)
        # set default signup role as per Portal Settings
        default_role = frappe.db.get_value("Portal Settings", None, "default_role")
        if default_role:
            user.add_roles(default_role)

        verification = frappe.get_doc({
            "doctype":"User Verification",
            "user": user.name,
            "email":user.email,
            "code": random.randint(1111,9999),
            "type": "SMS"
        })

        verification.flags.ignore_permissions = True
        verification.insert()

        
        return "Account created successfully, verification code sent via SMS"
                    
            
		# if user.flags.email_sent:
		# 	return 1, _("Please check your email for verification")
		# else:
		# 	return 2, _("Please ask your administrator to verify your sign-up")

@frappe.whitelist(allow_guest=True)
def verify_user(email, code, isSms):
    user = frappe.get_doc("User", email)
    if not user:
        return {"success":False,"message":"No user found"}

    isMatched = False
    veri_list = frappe.get_all("User Verification", 
        filters={"user":email, "expired": 0, "type": "SMS" if isSms == True else "Email"}, fields=["*"])
    if len(veri_list):
        for key, veri in enumerate(veri_list):
            if veri.code == code and not isMatched:
                isMatched = True
                user.enabled = True
                user.flags.ignore_permissions = True
                user.save()
    
    if(isMatched):
        return {"success":True,"message":"Verified successfully!"}
    else:
        return {"success":False,"message":"Verification failed!"}
                    

    
