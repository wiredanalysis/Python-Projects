# define the investment amount, monthly interest rate, and investment period in months
investment_amount = float(input("Enter the investment amount: "))
monthly_interest_rate = float(input("Enter the monthly interest rate (%): "))
investment_period = int(input("Enter the investment period (in months): "))

# convert the monthly interest rate from percentage to decimal
monthly_interest_rate /= 100


# calculate the total return on investment
total_return = investment_amount * ((1 + monthly_interest_rate) ** investment_period) - investment_amount

# print the monthly and total returns on investment
print("Total return on investment: $", round(total_return, 2))
