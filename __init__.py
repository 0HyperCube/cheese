import md

import datetime
today = datetime.date.today()
today_str = today.strftime('%d %b %Y')

def days_to_update(finances):
    if not finances.read_until("Last Updated:"):
        raise RuntimeError("No last updated")
    last_updated = datetime.datetime.strptime(finances.read_until("\n", output=False), "Last Updated: %d %b %Y")
    days_to_update = (today-last_updated.date()).days
    if days_to_update==0:
        print("No days to update finances for. Just formatting will take place:")
    elif days_to_update==1:
        print(f"Calculating finances for the past day.")
    else:
        print(f"Calculating finances for the past {days_to_update} days:")
    finances.output+=f"Last Updated: {today_str}"
    return days_to_update

def wealth(citizens, wealth_mult, days):
    if days==0:
        return citizens
    print("\n\nWealth Tax\n")
    for citizen_id in range(2,len(citizens)):
        # 0: Id    1: name    2: Money    3: Employer Id    4: Wage
        name = citizens[citizen_id][1]
        if wealth_mult<1:
            if citizens[citizen_id][2]>0:
                print(f"{name} pays {citizens[citizen_id][2]*(1-wealth_mult):.2f}\U0001F9C0 wealth tax and is left with {citizens[citizen_id][2]*wealth_mult:.2f}\U0001F9C0")
            else:
                print(f"{name} pays no wealth tax as they are broke")
        citizens[1][2] += citizens[citizen_id][2]*(1-wealth_mult)
        citizens[citizen_id][2] *= wealth_mult
    return citizens

def income(citizens, min_wage, income_mult, days):
    if days==0:
        return citizens
    print("\n\nIncome Tax\n")
    
    for citizen_id in range(1,len(citizens)):
        # 0: Id    1: name    2: Money    3: Employer Id    4: Wage
        citizens[citizen_id][0] = citizen_id-1
        if citizen_id==1:
            continue
        name = citizens[citizen_id][1]
        if citizens[citizen_id]!=None:
            pay = citizens[citizen_id][4] or min_wage
            if pay < min_wage:
                print(f"{name} gets a pay rise to the minimum wage ({min_wage}\U0001F9C0)")
                citizens[citizen_id][4] = min_wage
            pay = max(min_wage,pay)
            pay*=days
            if citizens[citizens[citizen_id][3]+1][2] >= pay:
                print(f"{citizens[citizens[citizen_id][3]+1][1]} pays {name} {pay:.2f}\U0001F9C0")
            elif citizens[citizens[citizen_id][3]+1][2]>0:
                new_pay = citizens[citizens[citizen_id][3]+1][2]
                print(f"{citizens[citizens[citizen_id][3]+1][1]} pays {name} only {new_pay:.2f}\U0001F9C0 out of {pay:.2f}\U0001F9C0 because they are broke.")
                pay = new_pay
            else:
                print(f"{name} is payed nothing because {citizens[citizens[citizen_id][3]+1][1]} is broke.")
                pay=0
            if pay>0:
                citizens[citizens[citizen_id][3]+1][2] = round(citizens[citizens[citizen_id][3]+1][2],2)
                citizens[citizens[citizen_id][3]+1][2]-=pay
                citizens[citizen_id][2] = round(citizens[citizen_id][2],2)
                citizens[citizen_id][2] += pay*income_mult
                tax = pay*(1-income_mult)
                citizens[1][2] += tax
                print(f"Treasury recieves {tax:.2f}\U0001F9C0 in income tax and {name} recieves {pay*income_mult:.2f}\U0001F9C0")
        else:
            print(f"{name} is unemployed so payed nothing")
        
    return citizens

def calculate_finances():
    finances = md.Markdown(
        "Finances.md",
        f"# Finances\nLast Updated: {today_str}\n\n### Current Rates\n|Name|Rate|\n|===|===|\n|Income Tax (%)|20|\n|Wealth Tax (%)|10|\n|Minimum Wage (&#129472;)|5|\n\n### Citizens\n|Id (auto)|Name|Balance (&#129472;)|Employer Id (blank=unemployed 0=state)|Wage (blank=minimum for employed)|\n|===|===|===|===|===|\n|0|Treasury|100|||\n"
    )
    
    days = days_to_update(finances)
    
    rates = finances.read_table(((str,""), (float,False)))
    income_tax = rates[1][1]
    wealth_tax = rates[2][1]
    min_wage   = rates[3][1]

    income_mult = (1 - income_tax / 100) ** days
    wealth_mult = (1 - wealth_tax / 100) ** days

    finances.write_table(rates)

    citizens = finances.read_table(((int,None), (str,""), (float,0),(int,None), (float, None)))

    citizens = wealth(citizens, wealth_mult, days)
    citizens = income(citizens, min_wage, income_mult, days)
    
            
    finances.write_table(citizens)
        
    finances.write_file()
calculate_finances()
