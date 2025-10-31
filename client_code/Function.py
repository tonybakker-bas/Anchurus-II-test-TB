from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#from .ListUsers import ListUsers

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Function
#
#    Function.say_hello()
#
# Global Functions
from . import Global

from ListContexts import ListContexts
from ListFinds import ListFinds
from ListSites import ListSites
from ListAreas import ListAreas
from ListUsers import ListUsers
from TableList import TableList
from ContextForm import ContextForm
from FindForm import FindForm
from AreaForm import AreaForm
from RowForm import RowForm
from SiteForm import SiteForm
from UserForm import UserForm
from ImportForm import ImportForm
from Help import Help

from Draw import Draw
#from Workarea import Workarea

def say_hello():
  print("Hello, world")
  return

def create_work_space(type,data_list):
  #print("Work space to create is: ",type)
  page_info = {}
  table_name = type.split(" ")[1].lower()
  action = type.split(" ")[0].lower()
  print(action, table_name)
  # first param of RowForm and TableList is site_id, but is blanked out. Only used by server print function
  if action == "list":
    work_space = TableList("",table_name,data_list,type,page_info)
    print(work_space)
  elif type == "List Contexts":
    work_space = TableList("","context",data_list,type,page_info)
    #work_space = ListContexts("")
  elif type == "List Areas":
    work_space = ListAreas() 
  elif type == "List Finds":
    work_space = TableList("","find",data_list,type,page_info)
    #work_space = ListFinds("")
  elif type == "List Sites":
    work_space = ListSites()
  elif type == "List Users":
    work_space = ListUsers()
  elif type == "Import":
    work_space = ImportForm()
  elif type == "Add Row":
    work_space = RowForm("","row",data_list,type,page_info)
  elif type == "Add Context":
    work_space = RowForm("","context",data_list,type,page_info)
    #work_space = ContextForm()
  elif type == "Add Area":
    work_space = AreaForm()
  elif type == "Add Find":
    work_space = RowForm("","find",data_list,type,page_info)
    #work_space = FindForm()
  elif type == "Add Site":
    work_space = SiteForm()
  elif type == "Edit Context":
    work_space = RowForm("","context",data_list,type,page_info)
    #work_space = ContextForm()
  elif type == "Edit Find":
    work_space = RowForm("","find",data_list,type,page_info)
  elif type == "Edit Area":
    work_space = AreaForm()
  elif type == "Edit Site":
    work_space = SiteForm()
  elif type == "Edit User":
    work_space = UserForm()
  elif type == "View Row":
    work_space = RowForm("","context",data_list,type,page_info)
  elif type == "View Context":
    work_space = RowForm("","context",data_list,type,page_info)
  elif type == "View Find":
    work_space = RowForm("","find",data_list,type,page_info)
    #work_space = FindForm()
  elif type == "View Area":
    work_space = AreaForm()
  elif type == "View Site":
    work_space = SiteForm()
  elif type == "Draw":
    work_space = Draw()
  elif type == "Help":
    work_space = Help()
  else:
    #print("Unknown Type - no known workspace")
    work_space = "Unknown"
  return work_space

def delete_workspace(work_area_name):
  # remove work_area_name form and work_area_name button
  Global.work_area[work_area_name]["button"].remove_from_parent()
  Global.work_area[work_area_name]["form"].remove_from_parent()
  # now remove (pop) the work_area_name from lists
  Global.work_area.pop(work_area_name)
  # clear header and make it invisible
  Global.header_work_area_name.text = ""
  Global.header_work_area_type.text = ""
  Global.header.visible = False
  return

def delete_all_workspace(work_area_list):
  return

def save_work_areas():
  # need to create a media object of the work_area list 
  
  success = anvil.server.call("save_work_areas", Global.work_area,Global.site_id) 
  return

def update_status_label(self):
  """ Calculates and updates the page control row information label with the current row range."""
  page_num = int(self.table.get_page())
  rows_per_page = int(self.table.rows_per_page)
  total_rows = len(self.repeating_panel_1.items)
  # Calculate the start and end row numbers
  start_row = (page_num) * rows_per_page + 1
  end_row = min((page_num + 1) * rows_per_page, total_rows)
  # The page control buttons are not in self but in main form
  if page_num == 0:
    # disable first_page_btn and prev_page_btn if on page 0
    Global.main_form.first_page.enabled = False
    Global.main_form.prev_page.enabled = False
  else:
    Global.main_form.first_page.enabled = True
    Global.main_form.prev_page.enabled = True
  if (rows_per_page != 0) and (page_num == (total_rows // rows_per_page)):
    # disable last_page_btn and next_page_btn if on last page
    Global.main_form.last_page.enabled = False
    Global.main_form.next_page.enabled = False
  else:
    Global.main_form.last_page.enabled = True
    Global.main_form.next_page.enabled = True

  # Display the formatted string in the status label if 
  if total_rows > rows_per_page and rows_per_page != 0:
    Global.main_form.row_number_info.text = f"{start_row}-{end_row} of {total_rows}"
  else:
    # No need to display page control buttons as nr of rows is less than 
    Global.main_form.last_page.visible = False
    Global.main_form.next_page.visible = False      
    Global.main_form.first_page.visible = False
    Global.main_form.prev_page.visible = False
    Global.main_form.row_number_info.text = "Total " + str(total_rows) + " rows"
  #
  Global.work_area[Global.current_work_area_name]["page_info"] = {"page_num": page_num, "rows_per_page": rows_per_page, "total_rows": total_rows}
  return

def clear_selection(self):
  # clear select checkbox of rows
  for row in self.repeating_panel_1.get_components():
    row.btn_select.checked = False
    row.background = ""

  # clear selection list
  Global.work_area[Global.current_work_area_name]["selected_rows"].clear()

  # clear select_all checkbox
  Global.main_form.select_all.checked = False
  return

def table_list_refresh(self):
  # This function does the filling of the table contents
  # 1. call server function '"table_name"s_get', which retrieves all rows of the table_name for the given site
  self.repeating_panel_1.items = anvil.server.call("table_get",Global.site_id,Global.table_name)

  # 2. set nr of rows per page from Global variable (which is defined by a parameter in the server-side config file)
  #if Global.rows_per_page is not None:
  self.table.rows_per_page = Global.rows_per_page
  if len(self.page_info) != 0:# this means this form is called from the server (print function)
    self.table.rows_per_page = self.page_info["rows_per_page"]
    self.table.set_page(self.page_info["page_num"])

  # 3.save the list of items in the Global 'work-area' dictionary
  if Global.current_work_area_name is not None:
    Global.work_area[Global.current_work_area_name]["data_list"] = self.repeating_panel_1.items

  # Trigger the initial update
  update_status_label(self)

  #self.information.text = Global.table_name
  return
