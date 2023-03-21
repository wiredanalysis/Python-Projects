# define the weight and height of the person
weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))

# calculate the BMI
bmi = weight / (height ** 2)

# determine the weight category based on the BMI
if bmi < 18.5:
    category = "Underweight"
    description = "You may be malnourished or underweight. Consider consulting a doctor or a dietitian."
elif bmi < 25:
    category = "Normal weight"
    description = "Congratulations! You have a healthy weight. Keep up the good work!"
elif bmi < 30:
    category = "Overweight"
    description = "You may be at risk of developing health problems such as high blood pressure, diabetes, and heart disease. Consider adopting a healthier lifestyle."
else:
    category = "Obese"
    description = "You may be at high risk of developing health problems such as high blood pressure, diabetes, and heart disease. Consider seeking medical advice and adopting a healthier lifestyle."

# print the BMI and weight category with description
print("Your BMI is:", round(bmi, 2))
print("Your weight category is:", category)
print(description)
