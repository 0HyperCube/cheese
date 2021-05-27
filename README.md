# Cheese-coin tax

### Features

- Read and write from a spreadsheet
- Intuative design
- Fully documented code
- Check if already payed on that day
- All parameters in spreadsheet for ease of access
- Lifelong support (use the issues tab in this repository for features and bugs)

### How to use

- Clone or download this via the green button at the top.
- Run this python file.
- Locate the `citizens.csv` file in the current directory.
- You can edit this with a spreasheet application like LibreOffice Calc or Excel
- Run file again to calculate tax

### Spreadsheet Information

Data columns should not have symbols in them. Booleans should be 'Y' or 'N'

Meta columns include:
- Income Tax - A value between 1 and 100 for the taxation percentage
- Minimum wage - The wage for people with no wage specified. Anyone with a wage lower than this will have their wage increased.
- Treasury - Amount held by the treasury (government).
- Last Pay - Days since UNIX timestamp of last pay (do not edit)

Citizen columns include:
- Name - Name / ID of citizen.
- Balance - Total cheesecoins. Defaults to 0.
- Government Paid - Are they payed by the government (deducts wage from treasury). Defaults to no
- Wage - Money per day. Defaults to minimum wage.