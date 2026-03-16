# Security Audit: SQL Injection Prevention
# Task A - SQL injection prevention (complete audit)

# Findings:
# After auditing the codebase, the following places use database queries:
# 1. /home/ajay/frappe-bench/apps/quickfix/quickfix/api.py: get_status_chart_data() - Hardcoded query, no user input.
# 2. /home/ajay/frappe-bench/apps/library_management/library_management/library_management/report/article_report/article_report.py - Uses parameterized queries, safe.
# 3. Various frappe core files use f-strings with system variables or frappe.db.escape().

# No instances found where user input directly touches SQL without proper sanitization.

# Demonstration of query patterns:

import frappe

# Example 1: Simple SELECT with WHERE clause

# BAD: Using f-string (vulnerable to SQL injection)
def bad_query_example(user_input):
    query = f"SELECT name FROM `tabUser` WHERE name = '{user_input}'"
    return frappe.db.sql(query)

# GOOD: Using parameterized query
def good_query_example(user_input):
    query = "SELECT name FROM `tabUser` WHERE name = %s"
    return frappe.db.sql(query, (user_input,))

# Example 2: LIKE query for search

# BAD: Using f-string
def bad_like_example(search_term):
    query = f"SELECT name FROM `tabItem` WHERE name LIKE '%{search_term}%'"
    return frappe.db.sql(query)

# GOOD: Using parameterized
def good_like_example(search_term):
    query = "SELECT name FROM `tabItem` WHERE name LIKE %s"
    return frappe.db.sql(query, (f"%{search_term}%",))

# frappe.db.escape() exists but parameterized queries are preferred
# Example of escape (not recommended for new code)
def escape_example(user_input):
    escaped = frappe.db.escape(user_input)
    query = f"SELECT name FROM `tabUser` WHERE name = {escaped}"
    return frappe.db.sql(query)

# Note: frappe.db.escape() properly escapes values, but parameterized queries are safer
# because they separate SQL code from data, preventing injection even if escaping fails.