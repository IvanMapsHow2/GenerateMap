#PURPOSE
#   Generates a map (PNG format) from a given APRX file.
#
#   Written to be run as an automated task. Date-stamps current date into output-map file-name.

#README NOTES
#   This script logs its activity to a log file (GenerateMap.log) which is written into the
#   script's directory at execution time. Periodically truncate or delete the log file to
#   preserve disk space.

#HOW TO USE
#   1) Set major variables in section commented as ******************** SET MAJOR VARIABLES HERE ***********.
#
#   2) Run or schedule to run. Run on a machine that has ArcGIS Pro.
#      Run using this command: <program files>\ArcGIS\Pro\bin\Python\scripts\propy.bat <this script file>

#HISTORY
#   DATE         ORGANIZATION     PROGRAMMER          NOTES
#   2021-07-20   VCGI             Ivan Brown          Original coding, using Python 3.7.10 and ArcGIS Pro 2.8.1.

#PSEUDO CODE
#   Set major variables, including:
#      -path of APRX file.
#      -path of a folder that contains output PNG maps.
#   Make sure that given paths are valid.
#   Generate PNG map in output folder; include today's date in file name.

#******************** SET MAJOR VARIABLES HERE ***********

#Set aprx_path to path of APRX file to be used to generate map.
#   Set to a string that begins w/ r so that backslashes work (i.e., r"C:\MyScripts\GenerateMap\pothole_tracking\pothole_tracking.aprx").
aprx_path = r""

#Set layout_name to name of layout in APRX by which map is generated.
layout_name = ""

#Set map_dir to path of directory to contain output PNG maps.
#   Set to a string that begins w/ r so that backslashes work (i.e., r"X:\pothole_tracking\pothole_maps\").
map_dir = r""

#Set map_name to a string with which output PNG-map file names begin; the script automatically appends the current date,
#   in YYYYMMDD pattern, to the string set by this variable.
#
#   For example, if map_name is set to "pothole_tracking_" and the current date is July 20, 2021, the script names the output PNG-map file
#   "pothole_tracking_20210720.png".
map_name = ""
#******************** END SECTION FOR MAJOR VARIABLES ****

#IMPORT MODULES
print("Importing modules...")
import arcpy
import time
import sys
import os.path

#FUNCTIONS

#THIS FUNCTION SIMPLY CAPTURES THE CURRENT DATE AND
#   RETURNS IN TEXT W/ YYYYMMDD PATTERN
#   FOR EXAMPLE:
#      20171201
def tell_the_time():
   the_year = str(time.localtime().tm_year)
   the_month = str(time.localtime().tm_mon)
   the_day = str(time.localtime().tm_mday)
   #FORMAT THE MONTH TO HAVE 2 CHARACTERS
   while len(the_month) < 2:
      the_month = "0" + the_month
   #FORMAT THE DAY TO HAVE 2 CHARACTERS
   while len(the_day) < 2:
      the_day = "0" + the_day
   the_output = the_year + the_month + the_day
   return the_output

#THIS FUNCTION SIMPLY TAKES A STRING ARGUMENT AND THEN
#   WRITES THE GIVEN STRING INTO THE SCRIPT'S LOG FILE (AND
#   OPTIONALLY PRINTS IT).
#   SET FIRST ARGUMENT TO THE STRING. SET THE SECOND
#   ARGUMENT (BOOLEAN) TO True OR False TO INDICATE IF
#   STRING SHOULD ALSO BE PRINTED.
#   ADDS CURRENT DATE TO BEGINNING OF FIRST PARAMETER.
#   ADDS A \n TO FIRST PARAMETER (FOR HARD RETURNS).
def make_note(the_note, print_it = False):
   the_note = tell_the_time() + "  " + the_note
   the_note += "\n"
   log_file = open(sys.path[0] + "\\GenerateMap.log", "a")
   log_file.write(the_note)
   log_file.close()
   if print_it == True:
      print(the_note)

try:
   make_note("-----SCRIPT STARTED.", True)
   
   #MAKE SURE GIVEN APRX EXISTS
   if arcpy.Exists(aprx_path) == False:
      make_note("Given APRX doesn't exist. Script terminated.", True)
      sys.exit()

   #MAKE SURE GIVEN OUTPUT DIRECTORY EXISTS
   if arcpy.Exists(map_dir) == False:
      make_note("Given output directory doesn't exist. Script terminated.", True)
      sys.exit()

   #BUILD PATH OF OUTPUT FILE AND SEE IF IT ALREADY EXISTS
   output_file_path = os.path.join(map_dir, map_name + tell_the_time() + ".png")
   if arcpy.Exists(output_file_path) == True:
      make_note("A map w/ today's date already exists. Rename or remove it and then run script.", True)
      sys.exit()

   #GENERATE PNG MAP
   make_note("Accessing APRX...", True)
   a = arcpy.mp.ArcGISProject(aprx_path)
   make_note("Generating map " + output_file_path + " ...", True)
   #(FIND THE LAYOUT)
   layout_list = a.listLayouts(layout_name)
   if len(layout_list) == 0:
      make_note("Error. Given layout name " + layout_name + " not found in APRX.", True)
      sys.exit()
   #(EXPORT THE LAYOUT)
   layout_list[0].exportToPNG(output_file_path)
   
   make_note("-----SCRIPT COMPLETED.", True)

except:
   make_note("-----SCRIPT TERMINATED DUE TO ERROR CONDITION.", True)
