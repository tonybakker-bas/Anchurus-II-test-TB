from ._anvil_designer import ImportFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Global

class ImportForm(ImportFormTemplate):
  def Import_refresh(self, **event_args):
    # this function does the filling of the table contents
    print("Import refresh button pressed. Current work_area ",Global.current_work_area_name )
    self.message_log.text = ""
    self.upload_file.clear()
    self.select_table_name_dropdown.selected_value = None
  pass
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.Import_title.text = "Here you can import csv files for importing to the Database. You can download a template csv file if needed."
    #self.select_table_name_dropdown.items = Global.import_action_dropdown
    Global.table_name = Global.action.split(" ")[1].rstrip("s").lower()
    self.selected_table.text = "You have selected to import a csv file for the table: " + Global.table_name
    Global.main_form.mb_left.visible = False
    Global.main_form.mb_middle.visible = False
    #Global.main_form.


  def upload_file_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(Global.current_work_area_name)
    if self.select_table_name_dropdown.selected_value is not None:
      table_name = self.select_table_name_dropdown.selected_value
      print(table_name)
      self.selected_file_name.text = "You have selected file: " + file.name
      msg = "No message received."
      # type is database table name
      # call check_DBAcontrol for existing or new DBAcontrol value
      #DBAcontrol = anvil.server.call("check_DBAcontrol",Global.username,"b")
      msg = anvil.server.call("import_file", table_name, file)
      #print(msg)
      self.message_log.text = msg
    else:
      alert(
        content="You have not selected the table name. Please select a table_name.",
        title="Table name selection warning",
        large=True,
        buttons=[("Ok", True)],
      )
    pass

  def select_table_name_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
