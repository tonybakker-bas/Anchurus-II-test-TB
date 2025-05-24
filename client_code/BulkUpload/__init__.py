from ._anvil_designer import BulkUploadTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Global

class BulkUpload(BulkUploadTemplate):
  def bulk_upload_refresh(self, **event_args):
    # this function does the filling of the table contents
    print("Bulk upload refresh button pressed. Current work_area ",Global.current_work_area_name )
    self.message_log.text = ""
    self.upload_file.clear()
  pass
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.BulkUpload_title.text = "This is the feature for " + Global.action + ". You can download a template csv file if needed."

  def upload_file_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(Global.current_work_area_name)
    type = Global.work_area[Global.current_work_area_name]["action"].split()
    print(type)
    self.selected_file_name.text = "You have selected file: " + file.name
    msg = "No message received."
    # type is database table name
    # call check_DBAcontrol for existing or new DBAcontrol value
    DBAcontrol = anvil.server.call("check_DBAcontrol",Global.username,"b")
    msg = anvil.server.call("bulkupload", type[2][:-1], file, DBAcontrol)
    #print(msg)
    self.message_log.text = msg
    pass
