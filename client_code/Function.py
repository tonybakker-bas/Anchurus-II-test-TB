from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from . import Global
#from .ListUsers import ListUsers

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Function
#
#    Function.say_hello()
#
# Global Functions

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

def create_work_space(type):
  print("Work space to create is: ",type)
  if type == "List Contexts":
    work_space = TableList("","context")
    #work_space = ListContexts("")
  elif type == "List Areas":
    work_space = ListAreas() 
  elif type == "List Finds":
    work_space = TableList("","find")
    #work_space = ListFinds("")
  elif type == "List Sites":
    work_space = ListSites()
  elif type == "List Users":
    work_space = ListUsers()
  elif type == "Import":
    work_space = ImportForm()
  elif type == "Add Row":
    work_space = RowForm()
  elif type == "Add Context":
    work_space = ContextForm()
  elif type == "Add Area":
    work_space = AreaForm()
  elif type == "Add Find":
    work_space = FindForm()
  elif type == "Add Site":
    work_space = SiteForm()
  elif type == "Edit Context":
    work_space = ContextForm()
  elif type == "Edit Find":
    work_space = FindForm()
  elif type == "Edit Area":
    work_space = AreaForm()
  elif type == "Edit Site":
    work_space = SiteForm()
  elif type == "Edit User":
    work_space = UserForm()
  elif type == "View Row":
    work_space = RowForm()
  elif type == "View Context":
    work_space = ContextForm()
  elif type == "View Find":
    work_space = FindForm()
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
  print("List of work_area:")
  print(Global.work_area)
  for name in Global.work_area:
    print("Details of work_area")
    print(Global.work_area[name])
  return