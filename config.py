from report import Report


#
# HEADERS
#
headers_desk = {'Authorization': 'Basic NmZhZjdmYTc3Y2I3NWYwMzRhNGE3NWJjZTgwM2QxMGM='}
headers_android = {'Authorization': "Basic OTdjNDVhNDI3Mzg5MmFlNTUxNjc2OWFkMzlkMjM4MDI="}
headers_ios = {'Authorization': "Basic NTc4YzY0ZDM3OTA3YWY3YTUwMDczZTgyMjFiYzU4OWI="}
headers_mobile = {'Authorization': "Basic ODliY2U0NmI1Yjc2MmZjMjI2M2FlYTYyNDk1ZWMzNGE="}
headers = {}

#
# MAIN CONFIG
#
url = 'https://ip-{branch}.api.branch.swapix.com/'
report_errors_path = 'report_errors.txt'
report_logs_path = 'logs.txt'
# Ad config
ad_category_id = 76
ad_location_id = 732
ad_name = "API_GENERATION_TEST"
ad_description = "PYTHON API TEST UNIQUE"
ad_cost = 2000
ad_photos = ["i.jpg"]
path = "add.json"
#
# AD IDs
#
min_ad_id = 0
max_ad_id = 60

ReportHandler = Report(report_errors_path, report_logs_path)