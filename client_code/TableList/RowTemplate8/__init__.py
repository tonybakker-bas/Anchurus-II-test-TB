from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Global

class RowTemplate8(RowTemplate8Template):
  def btn_view_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #print(self.item)
    #print(Global.table_name)
    Global.table_items = self.item
    Global.action = "View " + Global.table_name.capitalize()
    if Global.main_form:  # Important to check if the form exists
      # Create new work_area "View Context" and set focus on this new work_area
      print("From repatingPanel row calling create_new_work_area for:",Global.action)
      Global.main_form.create_new_work_area(Global.action)
    else:
      print("Main form not found!")
  pass

  def btn_edit_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #print(self.item)
    #print(Global.table_name)
    Global.table_items = self.item
    Global.action = "Edit " + Global.table_name.capitalize()
    if Global.main_form:  # Important to check if the form exists
      # Create new work_area "View Context" and set focus on this new work_area 
      Global.main_form.create_new_work_area(Global.action)
    else:
      print("Main form not found!")
  pass

  def btn_delete_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #print(self.item)
    #print(Global.table_name)
    Global.table_items = self.item
    Global.action = "Delete " + Global.table_name.capitalize()
    message = "You have seleted to delete " + Global.table_name.capitalize() + "\n\n" + str(self.item) + "\n\nDo you wish to continue?"
    confirm(message)
  pass
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # create the view and edit button for the row and set button click event handlers
    btn_view = Button(text='',align='left',icon='fa:eye',icon_align='left_edge',tooltip="view row")
    btn_view.set_event_handler('click', self.btn_view_click)
    self.item['view'] = btn_view
    btn_edit = Button(text='', align='left',icon='fa:edit',icon_align='left_edge',tooltip="edit row")
    btn_edit.set_event_handler('click', self.btn_edit_click)
    self.item['edit'] = btn_edit
    btn_delete = Button(text='', align='left',icon='fa:remove',icon_align='left_edge',tooltip="delete row")
    btn_delete.set_event_handler('click', self.btn_delete_click)
    self.item['delete'] = btn_delete

    self.add_component(self.item['view'], column='1')
    self.add_component(self.item['edit'], column='2')
    self.add_component(self.item['delete'], column='3')


