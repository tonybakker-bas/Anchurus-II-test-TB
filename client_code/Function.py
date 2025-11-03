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
  # Make sure any List actions that are notmusing the TableList Form should be listed first
  if type == "List Users":
    work_space = ListUsers()
  elif type == "List Sites":
    work_space = ListSites()
  elif action == "list":
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
  #
  elif action == "import":
    work_space = ImportForm()
  #
  elif type == "Add Row":
    work_space = RowForm("","row",data_list,type,page_info)
  #
  elif type == "Add Context":
    work_space = RowForm("","context",data_list,type,page_info)
    #work_space = ContextForm()
  elif type == "Add Find":
    work_space = RowForm("","find",data_list,type,page_info)
    #work_space = FindForm()
  elif type == "Add Area":
    work_space = AreaForm()
  elif type == "Add Site":
    work_space = SiteForm()
  #
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
  #
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
  #
  elif type == "Draw":
    work_space = Draw()
  #
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

