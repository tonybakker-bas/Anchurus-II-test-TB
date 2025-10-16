from ._anvil_designer import RowFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Global

class RowForm(RowFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # we need to find out which table we are dealing with
    print(Global.action)
    print(Global.table_name)
    # get table information
    table_info = anvil.server.call("describe_table",Global.table_name)
    # And then we need to create all the fields based on table information 
    # loop over table columns
    for item in table_info:
      column_name = item["Field"]
      column_type = item["Type"]
      # types can be varchar(length),int(length),text,float,double,date
      # type text can be 65535 char
      # create the label and the input field
      