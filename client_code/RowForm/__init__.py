from ._anvil_designer import RowFormTemplate
from anvil import *
import anvil.server
import re
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


from .. import Global

class RowForm(RowFormTemplate):
  def input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    column = event_args["sender"].tag
    self.form_fields[column]["header"].text = column + " (" + str(len(self.form_fields[column]["field"].text)) + "/40):"
  pass
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    # we need to find out which table we are dealing with
    self.title.text = "This form is to " + Global.action
    # get table information
    table_info = anvil.server.call("describe_table",Global.table_name)
    # And then we need to create all the fields based on table information 
    # loop over table columns
    self.row = {}
    self.form_fields = {}
    for item in table_info:
      column_name = item["Field"]
      column_type = item["Type"]
      # types can be varchar(length),int(length),text,float,double,date
      # type text can be 65535 char so need to be a TextArea, other can be a TextBox
      # create the label and the input field
      lab = Label(text=column_name, font_size=14,tag=column_name)
      if column_type == "text":
        input = TextArea(tag=column_name)
        len = 65535
      else:
        input = TextBox(tag=column_name)
        match = re.search(r'.*\(+d\).*',column_type)
        print(match)
        len = match.group()
      input.add_event_handler('change',self.input_change)
      col = column_name + "(0/" + len + ")"
      lab = Label(text=col, font_size=14,tag=column_name)
      row = {"header": lab, "field": input, "length": len}
      self.form_fields[column_name] = row
      self.column_panel_1.add_component(lab)
      self.column_panel_1.add_component(input)
      

