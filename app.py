import streamlit as st
import requests

# Define the URL for your FastAPI app
predict_url = "http://equipmentmaintenancepredictionapp.azurewebsites.net/predict"

# Define the input schema using Streamlit widgets
def get_input():
    st.title("Equipment Fault Prediction")

    # Collect user input
    equipment_name = st.selectbox('Equipment Name', ['Turbine', 'Pump', 'Compressor'])
    location_name = st.selectbox('Location Name', ['Atlanta', 'New York', 'Chicago', 'San Francisco', 'Houston'])
    temperature = st.number_input('Temperature', min_value=10.0, max_value=150.0, step=10)
    pressure = st.number_input('Pressure', min_value=0.0, max_value=80.0, step=5)
    vibration = st.number_input('Vibration', min_value=-1.0, max_value=5.0, step=0.1)
    humidity = st.number_input('Humidity', min_value=10.0, max_value=90.0, step=5)

    # Return the input values
    return equipment_name, location_name, temperature, pressure, vibration, humidity

def predict_fault(equipment_name, location_name, temperature, pressure, vibration, humidity):
    # Prepare the input for the model
    input_data = {
        "equipment_name": equipment_name,
        "location_name": location_name,
        "temperature": temperature,
        "pressure": pressure,
        "vibration": vibration,
        "humidity": humidity
    }
    
    # Send a POST request to the FastAPI server
    response = requests.post(predict_url, json=input_data)
    
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()['faulty']
    else:
        st.error("Error: Unable to get prediction")
        return None

# Main function
def main():
    equipment_name, location_name, temperature, pressure, vibration, humidity = get_input()
    
    if st.button("Predict"):
        # Make the prediction when the button is pressed
        prediction = predict_fault(equipment_name, location_name, temperature, pressure, vibration, humidity)
        
        if prediction is not None:
            # Display the result
            if prediction == 1:
                st.success("The equipment is likely faulty.")
            else:
                st.success("The equipment is functioning properly.")

if __name__ == '__main__':
    main()
