#!/usr/bin/python
#========================================================================================
# Export a google my maps custom map KML file
#
# 5/17/2024 V1.0 Initial version
# 5/17/2024 V1.1 Fixed bad error message code around URL call and file write
#========================================================================================
import sys
import requests
import argparse
import os
from pathlib import Path

PROGRAM_NAME = Path(sys.argv[0]).stem
PROGRAM_VERSION = "1.1"
# This is the magic URL that will initiate a get request to google and get the KML data
# for the specified google map.
GET_URL_PREFIX = "https://www.google.com/maps/d/u/0/kml?forcekml=1&mid="
GET_URL_SUFFIX = ""
#========================================================================================
#========================================================================================
def setupParseCmdLine():
	parser = argparse.ArgumentParser(
	prog=PROGRAM_NAME,
	description="Convert google my maps KML files to OSMAnd style GPX files, including icon conversion.")
	# epilog="text at bottom of help")
	parser.add_argument("map_id",
		help="The google map id - found between the mid= and & in the map url.  Map must have sharing enabled")
	parser.add_argument("output",
		help="path\filename - minus the extension - for the KML file.  The .kml extension will be added by this program")
	return(parser.parse_args())
#========================================================================================
# Main
#========================================================================================
def main():
	# Parse the command line arguments
	args = setupParseCmdLine()
	KMLFilename = args.output + ".kml"
	print("")
	print("Export the KML data for a google my maps custom map.")
	print("  Google map ID:   ",args.map_id)
	print("  Export KML file: ",KMLFilename)

	getURLRequest = GET_URL_PREFIX+str(args.map_id)+GET_URL_SUFFIX
	#print("  URLRequst:       ",getURLRequest)
	response = requests.get(getURLRequest)
	match response.status_code:
		case 200:
			# Successful GET request
			try:
				with open(KMLFilename, 'w', encoding='utf-8') as file:
					file.write(response.text)
				# Text written successfully to {file_path}
				returnCode = 0
			except FileNotFoundError:
				print(f"  Error: The specified file path {KMLFilename} does not exist.")
				returnCode = 1
			except PermissionError:
				print(f"  Error: You do not have permission to write to the file: {KMLFilename}.")
				returnCode = 2
			except Exception as e:
				print(f"  Error: An unexpected error occurred: {str(e)}")
				returnCode = 9
		case 403:
			print("  Error: 403 Share permision for map not set")
			returnCode = 403
		case 404:
			print("  Error: 404 Bad map ID value")
			returnCode = 404
		case _:
			print(f"  Error: An unexpected error occurred: {str(response.status_code)}")
			returnCode = response.status_code
	return(returnCode)
#========================================================================================
#
#========================================================================================
if __name__ == "__main__":
	sys.exit(main())