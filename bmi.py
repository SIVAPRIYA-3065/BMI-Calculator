from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
import json

KV = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        MDTextField:
            id: weight
            hint_text: "Enter your weight (kg)"
            input_filter: 'float'
        MDTextField:
            id: height
            hint_text: "Enter your height (cm)"
            input_filter: 'float'
        MDTextField:
            id: age
            hint_text: "Enter your age"
            input_filter: 'int'
        MDLabel:
            text: "Gender"
            halign: 'left'
        MDDropDownItem:
            id: gender
            text: "Select Gender"
            on_release: app.menu.open()
        MDRaisedButton:
            text: "Calculate BMI"
            on_release: app.calculate_bmi(weight.text, height.text, age.text, gender.text)
        MDLabel:
            id: result
            halign: 'center'
"""

class MainScreen(Screen):
    pass

class BMICalculatorApp(MDApp):
    def build(self):
        screen = Builder.load_string(KV)
        self.menu = MDDropdownMenu(
            caller=screen.get_screen('main').ids.gender,
            items=[
                {"text": "Male", "viewclass": "OneLineListItem", "on_release": lambda x="Male": self.set_gender(x)},
                {"text": "Female", "viewclass": "OneLineListItem", "on_release": lambda x="Female": self.set_gender(x)},
            ],
            width_mult=4,
        )
        return screen

    def set_gender(self, value):
        self.root.get_screen('main').ids.gender.set_item(value)
        self.root.get_screen('main').ids.gender.text = value
        self.menu.dismiss()

    def calculate_bmi(self, weight, height, age, gender):
        try:
            weight = float(weight)
            height = float(height) / 100  # Convert height from cm to meters
            age = int(age)
            if weight <= 0 or height <= 0 or age <= 0:
                raise ValueError("Weight, height, and age must be positive numbers.")
            if gender not in ["Male", "Female"]:
                raise ValueError("Please select a valid gender.")
            bmi = weight / (height ** 2)
            category = self.categorize_bmi(bmi)
            self.root.get_screen('main').ids.result.text = f"Your BMI is {bmi:.2f}. You are {category}."
            self.store_data(weight, height * 100, age, gender, bmi, category)
        except ValueError as e:
            self.show_error_dialog(str(e))

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "underweight"
        elif 18.5 <= bmi < 24.9:
            return "normal weight"
        elif 25 <= bmi < 29.9:
            return "overweight"
        else:
            return "obese"

    def show_error_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def store_data(self, weight, height, age, gender, bmi, category):
        data = {
            'weight': weight,
            'height': height,
            'age': age,
            'gender': gender,
            'bmi': bmi,
            'category': category
        }
        with open('bmi_data.json', 'a') as file:
            file.write(json.dumps(data) + '\n')

if __name__ == '__main__':
    BMICalculatorApp().run()
