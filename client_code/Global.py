import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#
# Global Variables
#
main_form = ""
separator = "------------------"
admin_action_list = ["List Users","List Sites","Add Site"]
admin_action_list_not_implemented = [separator]
user_action_list = ["Select Site",separator,
                    "List Contexts","Add Context","Bulk Upload Contexts",separator,
                    "List Finds", "Add Find","Bulk Upload Finds",separator,
                    "List Anomalies","Add Anomaly",separator,
                    "List Interpretations","Add Interpretation"
                   ]
# action_list_not_implemented should always contain the separator
action_list_not_implemented = [separator,"Bulk Upload Finds","Draw","List Areas","Add Area"]
# the list_action_list is a list of the tables in DB (not yet sites)
list_action_dropdown = ["Contexts","Finds","Anomolies","Interpretrations"]
insert_action_dropdown = ["Context","Find","Anomoly","Interpretation"]
file_action_dropdown = ["Import",separator,"Save"]
view_action_dropdown = []
help_action_dropdown = []
admin_action_dropdown = ["List Users","List Sites","Add Site"]
import_table_name_dropdown = ["context","find"]
#
#
action_forms_with_refresh = ["TableList","ListUsers","ListSites","ListContexts","ListFinds","ListAreas","BulkUpload","Add Area","List Areas"]
#action_forms_with_print = ["ListUsers","ListSites","ListContexts","ListFinds","ListAreas","List Areas","View Context","View Find","View Area"]
action_forms_with_print = ["ListContexts","ListFinds","TableList"]
action_forms_with_download = ["ListContexts","ListFinds","TableList"]
action_forms_with_filter = ["ListContexts","ListFinds","TableList"]
#
action_seq_no = {}
csv_file = None
current_work_area = {}
current_work_area_name = ""
current_work_area_type = ""
# variables for work area header
header = {}
header_work_area_name = {}
header_refresh_button = {}
header_print_button = {}
header_download_button = {}
header_filter_button = {}
header_work_area_type= {}
header_site_name = {}
header_site_summary_information = {}
# variables for Global Header dropdown lists
gh_file_list = {}
gh_view_list = {}
gh_help_list = {}
gh_list_list = {}
gh_insert_list = {}
gh_admin_list = {}
#
work_area = {}
#
selected_row = []
selected_highlight_colour = "#66FFFF"
#
menu_select_options = ""
Quill_toolbarOptions = [
['bold', 'italic', 'underline', 'strike'],        # toggled buttons
['link'],
[{ 'header': 1 }, { 'header': 2 }],               # custom button values
[{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
[{ 'script': 'sub'}, { 'script': 'super' }],      # superscript/subscript
[{ 'indent': '-1'}, { 'indent': '+1' }],          # outdent/indent
[{ 'direction': 'rtl' }],                         # text direction
[{ 'size': ['small', 'normal', 'large', 'huge'] }],  # custom dropdown
[{ 'header': [1, 2, 3, 4, 5, 6] }],
[{ 'color': [] }, { 'background': [] }],          # dropdown with defaults from theme
[{ 'font': [] }],
[{ 'align': [] }],
['clean']                                         # remove formatting button
]
#
button_normal_background_clour = "#DCE5DD"
button_highlight_background_clour = "#CBEAD6"
#
action = ""
action_form_type = ""
admin_action = ""
admin_domain = ""
admin_user = ""
admin_user_initials = ""
area_items = {}
area_id = None
area_options = {}
context_id = None
context_items = {}
context_options = {}
context_types = ["Deposit","Cut","Structure"]
copyright = ""
DBAcontrol = ""
field_description_changed = False
file = []
find_id = None
file_list = []
find_items = {}
find_options = {}
find_types = {"Bulk Find","Small Find","Sample","FindGroup"}
google_link = ""
context_help_information = """
Deposit description:
1. Colour 2. Consistency 3. Texture 4. lnclusions (<50%) 5. Thickness and extent, 5. Other comments. 7. Method and conditions
Cut description:
1. Shape in plan (sketch overleaf) 2. Corners 3. Dimensions/depth 4. Break of slope -top 5. Sides, 6. Break of slope -
base 7. Base 8. Orientation 9. Shape of profile (sketch overleaf) 10. Fill Nos 11. Other comments
Masonry description:
1. Materials 2. Size of materials (brick; BLT in mm) 3. Finish of stones,4. Coursing/bond 5. Form 6. Direction of
face(s) 7. Bonding material (brick height of 4 courses and 4 bed joints in mm 8 . Dimensions of masonry as found 9. Other comments 
"""
image_type = ""
ip_address = ""
selected_material_types = {}
material_types = ["CBM Tile","CBM Brick","CBM Drain Pipe","CBM Mortar",
                  "Stone","Roofing Slate","Flint","Worked Flint","Pottery",
                  "Clay Pipe","Metalwork","Nails","Iron Slag","Glass","Animal Bone",
                  "Oyster Shells","Wood","Charcoal"]
login_options = {"Sign in", "Sign out"}
#
organisation = "Berkshire Archaeological Society"
#
# The following variable rows_per_page has to be set to 0, to make sure the print function prints the whole table
# During startup of the client (i.e. browser URL click of website) this value can be overwritten by a value for this
# defined in the server side configuration file
# Note that the 'page' is this context is a webpage and not a physical printing page
rows_per_page = 0 
#
selected_site = ""
sign_in_out_button_text = "Sign in"
site_id = None
site_name = ""
site_options = {}
site_items = {}
header_site_summary_information = {}
system_name = ""
SurveyMethod_options = {"BNG","Aligned to BNG north","Not aligned to BNG north"}
system = "Anchurus-II Web Service Application"
status = ""
table_name = ""
table_items = {}
title = system + "\n" + organisation
sign_in_out_button_text = "Sign in"
username = ""
user_initials = ""
user_role = ""
user_status = ""
user_role_options = {"None","admin","PM","user"}
user_status_options = {"True", "False"}
user_items = {}
version = ""
#
about_us_text = """
<h3>Welcome to the Anchurus-II Web Service for """ + organisation + "</h3>" + """

<p>
This system allows for the digital recording of archaeological excavations.
The software has been developed by Archaeology IT Solutions, an independent 'not-for-profit' or 'nonprofit' organisation developing software solutions for the archaeological community.
It is developed using the <a href="https://anvil.works/" target="_blank>Anvil Framework</a> and is using the open source Anvil App Server to run on your own dedicated server. It uses an external MySQL database to store the excavation details.  
This software is released under Creative Commons license: 
<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target=_blank>Attributions-NonCommercial-ShareAlike 4.0 International (CC BY-NC-AS 4.0) license</a>.
This is version """ + version + """.</p>

<p>
For more information please contact ...</p>
"""
help_page_form = ""
help_page = {}
help_introduction = """
<h3>Introduction</h3>
<p>
You have successfully logged into the Anchurus-II Web service Application of the """ + organisation + """.
</p>
<p>
Please select a site. Once selected you can use the menu items to select your actions.</p>
<p>
<b>Note:</b> When changing/selecting a new site, all current workspaces wil be deleted.</p>
<h3> </h3>
<p>
For more information on recording Archaeological Excavations please go to the
<a href="https://anchurus.co.uk/" target=_blank>Anchurus Website</a></p>
"""