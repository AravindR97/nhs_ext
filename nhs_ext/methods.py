import frappe

def check_user_permission(doc, method):
    ROLE = "Read Only Full Access"
    user = frappe.session.user

    if user == "Administrator":
        return

    # Allow create, block update
    if ROLE in frappe.get_roles(user) and not doc.is_new():
        frappe.throw(
            "You have read-only access. Editing existing records is not allowed.",
            frappe.PermissionError
        )