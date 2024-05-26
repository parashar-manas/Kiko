import pandas as pd
import ipywidgets as widgets
from IPython.display import display

# Read the CSV file
df = pd.read_excel('/content/disease.xlsx')

# Get all unique symptoms
all_symptoms = set()
for symptoms in df['Disease Symptoms']:
    symptom_list = symptoms.split(', ')
    for symptom in symptom_list:
        all_symptoms.add(symptom)
all_symptoms = list(all_symptoms)
all_symptoms.sort()

# Create checkboxes for symptoms
checkboxes = [widgets.Checkbox(description=symptom) for symptom in all_symptoms]
checkbox_widget = widgets.VBox(checkboxes)

# Display checkboxes
display(checkbox_widget)

# Function to update selected symptoms
def update_symptoms(change):
    selected_symptoms = [checkbox.description for checkbox in checkboxes if checkbox.value]
    output.clear_output()
    with output:
        display(get_disease_table(selected_symptoms))

def get_disease_table(selected_symptoms):
    # Find possible diseases and required lab tests
    df['Match Count'] = df['Disease Symptoms'].apply(lambda x: len(set(x.split(', ')) & set(selected_symptoms)))
    total_matches = sum(df['Match Count'])
    if total_matches == 0:
        return pd.DataFrame({'Disease': [], 'Symptoms Matched': [], 'Lab Tests Required': [], 'Probability (%)': []})

    df['Probability'] = df['Match Count'] / total_matches * 100
    closest_diseases = df.sort_values('Probability', ascending=False).head(3)

    # Normalize probabilities to ensure they sum up to 100%
    closest_diseases['Probability (%)'] = closest_diseases['Probability'] / closest_diseases['Probability'].sum() * 100

    # Create a table with diseases, symptoms, tests, and percentage chance
    disease_table = pd.DataFrame({
        'Disease': closest_diseases['Disease Name'],
        'Symptoms Matched': closest_diseases['Disease Symptoms'],
        'Lab Tests Required': closest_diseases['Lab Tests Required'],
        'Probability (%)': closest_diseases['Probability (%)']
    })

    return disease_table.reset_index(drop=True)  # Reset index and drop it

# Output widget for displaying the disease table
output = widgets.Output()
display(output)

# Update selected symptoms when checkbox value changes
for checkbox in checkboxes:
    checkbox.observe(update_symptoms, 'value')

# Initial display of the disease table
update_symptoms(None)