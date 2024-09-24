import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CidProject.settings')
django.setup()

from cidApp.models import Nationality

# Create a new Nationality instance
nationality = Nationality.objects.create(name="Timor Leste")

# Print to confirm insertion
print(f"Inserted Nationality: {nationality.name}")


countries=["Afghanistan", "Albania", 
           "Algeria", "Andorra", "Angola", 
           "Antigua and Barbuda", "Argentina", 
           "Armenia",    "Australia", "Austria", 
           "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", 
           "Barbados", "Belarus", "Belgium",    
           "Belize", "Benin", "Bhutan", "Bolivia", 
           "Bosnia and Herzegovina", "Botswana", 
           "Brazil", "Brunei", "Bulgaria",    
           "Burkina Faso", "Burundi", 
           "Cabo Verde", "Cambodia", "Cameroon", 
           "Canada", "Central African Republic", 
           "Chad",    "Chile", "China", "Colombia", 
           "Comoros", "Congo (Congo-Brazzaville)", 
           "Costa Rica", "Croatia", "Cuba", 
           "Cyprus",    "Czech Republic", 
           "Democratic Republic of the Congo",
           "Denmark", "Djibouti", "Dominica", 
           "Dominican Republic",     
           "Ecuador", "Egypt", "El Salvador", 
           "Equatorial Guinea", "Eritrea", 
           "Estonia",    "Eswatini (Swaziland)",
           "Ethiopia", "Fiji", "Finland", "France", 
           "Gabon", "Gambia", "Georgia", "Germany", "Ghana",   
           "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", 
           "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",    
           "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", 
           "Italy", "Ivory Coast (Côte d'Ivoire)", "Jamaica",    "Japan", "Jordan", 
           "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",   
           "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", 
           "Malawi",    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
           "Mexico", "Micronesia",    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)",
           "Namibia", "Nauru",    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", 
           "North Macedonia", "Norway",    "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay",
           "Peru", "Philippines", "Poland", "Portugal",   
           "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
           "Saint Vincent and the Grenadines",    
           "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", 
           "Serbia", "Seychelles", "Sierra Leone",    
           "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
           "Somalia", "South Africa", "South Korea", "South Sudan",    
           "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
           "Syria", "Taiwan", "Tajikistan", "Tanzania",    
           "Thailand", "Timor Leste","Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",    "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

for country in countries:
    Nationality.objects.create(name=country)
    print(f"Inserted Nationality: {country}")