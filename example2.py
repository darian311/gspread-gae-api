import sys
sys.path.append('gspread/')
import gspread

secrets = eval(open('secret.json').read())

# Login with your Google account
gc = gspread.login(secrets['mail'], secrets['pass'])

# Open a worksheet from spreadsheet with one shot
wks = gc.open('Foo').sheet1

wks.update_acell('B2', "it's down there somewhere, let me take another look.")

# Fetch a cell range
cell_list = wks.range('A1:B7')
print cell_list
