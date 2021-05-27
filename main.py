import os.path
import sys
import time

# Attempts to read a cell from the decoded CSV with appropriate error detection.
def read_cell(data, row, column, type, name, empty_val=list):
	try:
		v = data[row][column]
		if v == "" and empty_val!=list:
			return empty_val
		if type==bool:
			return (v.lower()=="y") or (v.lower()=="yes")
		return type(v)
	except ValueError:
		print(f"Invalid value when reading {name} from row: {row} column: {column}. Expected an {str(type)}. Found '{data[row][column]}'.")
	except IndexError:
		print(f"Tried to read {name} from row: {row} column: {column} but it does not exist.")
	sys.exit()

# Defines constants
FILE_NAME = "citizens.csv"
COLUMN_HEADINGS = ["Name","Balance","Government Paid","Wage"]

NAME_ROW = 0
BALANCE_ROW = 1
GOVERNMENT_PAID_ROW = 2
WAGE_ROW = 3

TAX_ROW = 0
MIN_WAGE_ROW = 1
TREASURY_ROW = 2
LAST_PAY_ROW = 3

# Calculate current day
day = int(time.time()/(60*60*24))

# Title
print('\n    ▬    🇹​​​​​ 🇦​​​​​ 🇽​​​​​   🇨​​​​​ 🇦 ​​​​​🇱​​​​​ 🇨 ​​​​​🇺 ​​​​​🇱 ​​​​​🇦​​​​​ 🇹​​​​​ 🇴​​​​​ 🇷    ▬    \n')

# Check if the file already exists
if os.path.isfile(FILE_NAME):
	print("Reading file")

	data = []
	# Read and parse the CSV file
	with open(FILE_NAME, "r") as f:
		for l in f.read().split("\n"):
			data.append(l.split(","))

	# Read meta rows
	income_tax = read_cell(data, TAX_ROW, 1, float, "Income Tax")/100
	min_wage   = read_cell(data, MIN_WAGE_ROW, 1, int, "Minimum Wage")
	treasury   = read_cell(data, TREASURY_ROW, 1, float, "Treasury")
	last_pay   = read_cell(data, LAST_PAY_ROW, 1, int, "Last pay")
	
	# Check if already payed already today
	if day<=last_pay:
		if input("Already payed today. Press 'y' to continue anyway ").lower() != "y":
			sys.exit()
	else:
		if input("Press 'y' to caluclate today's pay ").lower() != "y":
			sys.exit()

	# Read citizen payment rows
	row = 6
	while row<len(data) and len(data[row])>1:
		name            = read_cell(data, row, NAME_ROW, str, "Name", empty_val="")
		balance         = read_cell(data, row, BALANCE_ROW, float, "Balance", empty_val=0)
		government_paid = read_cell(data, row, GOVERNMENT_PAID_ROW, bool, "Government Paid", empty_val=False)
		wage            = read_cell(data, row, WAGE_ROW, float, "Wage", empty_val=min_wage)

		# Make sure wage is above minimum
		if wage<min_wage:
			wage = min_wage

		# Calculate payments
		if government_paid:
			pay = wage*(1-income_tax)
			tax = wage*income_tax
			print(f"Government paid {name} {wage} cheese coins with {tax} in tax")
			balance+=pay
			treasury-=pay

			# Store data
			data[row] = [name, str(balance), "Y", str(wage)]

		row+=1

	# Store treasury amount
	data[TREASURY_ROW][1] = str(treasury)
	data[LAST_PAY_ROW][1] = str(day)

	# Check if government is in debt
	if treasury<0:
		print("Government in debt")

	# Save the CSV
	print("Writing to file")
	with open(FILE_NAME, "w") as f:
		f.write("\n".join([",".join(x) for x in data]))

else:
	print("Creating New File")

	# Write a sample file
	with open(FILE_NAME, "w") as f:
		f.write(f"Income Tax (%),20,,\nMin Wage,9,,\nTreasury,1000,,\nLast Pay,{day},,\n,,,\n{','.join(COLUMN_HEADINGS)}\nBob,5,Y,10\nJeff,8,,")

	# Provide some information about the file
	print(f"\nCreated file '{FILE_NAME}' in current directory. You can edit this with a spreasheet application like LibreOffice Calc or Excel.")
	print(f"\nData columns should not have symbols in them. Booleans should be 'Y' or 'N'")
	print("\nMeta columns include:")
	print("- Income Tax - A value between 1 and 100 for the taxation percentage")
	print("- Minimum wage - The wage for people with no wage specified. Anyone with a wage lower than this will have their wage increased.")
	print("- Treasury - Amount held by the treasury (government).")
	print("- Last Pay - Days since UNIX timestamp of last pay (do not edit)")
	print("\nCitizen columns include:")
	print("- Name - Name / ID of citizen.")
	print("- Balance - Total cheesecoins. Defaults to 0.")
	print("- Government Paid - Are they payed by the government (deducts wage from treasury). Defaults to no")
	print("- Wage - Money per day. Defaults to minimum wage.")

input()
