from ._anvil_designer import ListUsersTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Global

class ListUsers(ListUsersTemplate):
  def list_users_refresh(self, **event_args):
    # this function does the filling of the table contents
    self.UsersList.items = anvil.server.call('users_get')
    self.User_list_1.rows_per_page = Global.nr_of_rows
    self.total_user_number.text = "Total number of Users: " + str(len(self.UsersList.items))
  pass
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.list_users_refresh()


