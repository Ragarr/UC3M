"""Global constants for finding the path"""
import os
# path to src folder + "/JsonFiles/"
JSON_FILES_PATH = os.path.join(os.path.dirname(__file__), "../../../../JsonFiles/")
JSON_FILES_RF2_PATH = JSON_FILES_PATH + "/FR2InputFiles/"

"""Global Errors"""
ERRORDATAORDERSMANIPULATED = "Orders' data have been manipulated"
ERRORFOUND = "File is not found"
ERRORFORMAT = "JSON Decode Error - Wrong JSON Format"
ERRORNOTFOUNDID = "order_id not found"
ERRORREGISTEDORDER = "order_id is already registered in orders_store"
ERRORFILEPATH = "Wrong file or file path"
ERRORSHIPNOTFOUND = "shipments_store not found"
ERRORTRAKINGNOTFOUND = "tracking_code is not found"
ERRORDELIVERYDATE = "Today is not the delivery date"
ERRORLABEL = "Bad label"
