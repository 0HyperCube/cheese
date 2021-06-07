# Cheese-coin tax

### Features

- Read and write from Markdown
- Easy to edit
- Table formatting
- Intuative design
- All parameters in spreadsheet for ease of access
- Lifelong support (use the issues tab in this repository for features and bugs)

### How to calculate

- Clone or download this via the green button at the top.
- Run `__init__.py`

### How to edit

Edit any of the values in any of the sections. If the table formatting is messy, run the `__init__.py` again to fix.

The Citizens section consists of:
- Id (autofilled) - Used to assign pay
- Name - Identifyer of user
- Balance (&#129472;) - The user's current money
- Employer Id - The id of the person who employs them. If it is blank then the user is unemployed. The state is employer '0'
- Wage - The amount of pay. If it is blank and the user is employed then it is the minimum wage.

You do not have to specify anything any of the fields. An example of what you might type below the auto generated *Citizens* section is below. To format this just run the `__init__.py`.
```
||Henry|4|0|100|
||Jeff|9|0|9|
||Bob|4|||
```
outputs:
| Id (auto) | Name     | Balance (&#129472;) | Employer Id (blank=unemployed 0=state) | Wage (blank=minimum for employed) |
| --------- | -------- | ------------------- | -------------------------------------- | --------------------------------- |
| 0         | Treasury | 100.00              | None                                   | None                              |
| None      | Henry    | 4.00                | 0                                      | 100.00                            |
| None      | Jeff     | 9.00                | 0                                      | 9.00                              |
| None      | Bob      | 4.00                | None                                   | None                              |