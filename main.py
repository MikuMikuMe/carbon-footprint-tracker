Creating a complete Python program for a web application like a carbon footprint tracker requires a framework like Flask or Django for creating a web server, handling HTTP requests, and rendering templates for the front-end interface. Additionally, the program will involve data processing to calculate carbon footprints based on user inputs, and suggest alternatives.

Below is a simplified example using Flask:

1. Install Flask and necessary libraries:
   ```
   pip install flask
   ```

2. Create your directory structure:
   ```
   carbon-footprint-tracker/
   ├── app.py
   ├── templates/
   │   ├── base.html
   │   ├── index.html
   │   └── result.html
   └── static/
   ```

3. Implement the application in `app.py`:

```python
from flask import Flask, render_template, request, redirect, url_for, flash
import logging

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for flashing messages

# Default emission factors (in kg CO2 per unit)
EMISSION_FACTORS = {
    'electricity': 0.233,  # kg CO2 per kWh
    'gasoline': 2.31,      # kg CO2 per liter
    'natural_gas': 2.204,  # kg CO2 per cubic meter
}

# Example eco-friendly alternatives
ALTERNATIVES = {
    'electricity': 'Consider switching to renewable energy sources or using energy-efficient appliances.',
    'gasoline': 'Consider using public transportation or switching to an electric vehicle.',
    'natural_gas': 'Consider improving home insulation or using energy-efficient HVAC systems.'
}

# Error logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get input data from the form
        activity_type = request.form.get('activity_type')
        amount = float(request.form.get('amount'))
        
        # Calculate the carbon footprint
        emissions = EMISSION_FACTORS.get(activity_type, 0) * amount
        alternative_suggestion = ALTERNATIVES.get(activity_type, "No suggestion available.")

        return render_template('result.html', emissions=emissions, alternative=alternative_suggestion)

    except ValueError:
        # Handle the case where the input cannot be converted to float
        flash('Invalid input. Please enter a numeric value for amount.')
        logging.error('Invalid input for amount; conversion to float failed.')
        return redirect(url_for('index'))

    except Exception as e:
        # Handle any other exception that might occur
        flash('An error occurred. Please try again.')
        logging.error(f'An unexpected error occurred: {e}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

4. Create the template files:

- `templates/base.html`:
  ```html
  <!doctype html>
  <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Carbon Footprint Tracker</title>
      </head>
      <body>
          <header>
              <h1>Carbon Footprint Tracker</h1>
          </header>
          <main>
              {% block content %}{% endblock %}
          </main>
      </body>
  </html>
  ```

- `templates/index.html`:
  ```html
  {% extends "base.html" %}

  {% block content %}
  <h2>Calculate Your Carbon Footprint</h2>
  <form method="post" action="{{ url_for('calculate') }}">
      <label for="activity_type">Select activity type:</label>
      <select id="activity_type" name="activity_type">
          <option value="electricity">Electricity (kWh)</option>
          <option value="gasoline">Gasoline (liters)</option>
          <option value="natural_gas">Natural Gas (cubic meters)</option>
      </select>
      <br>
      <label for="amount">Amount:</label>
      <input type="text" id="amount" name="amount" required>
      <br>
      <input type="submit" value="Calculate">
  </form>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul>
      {% for message in messages %}
        <li>{{ message }}</li>
      {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  {% endblock %}
  ```

- `templates/result.html`:
  ```html
  {% extends "base.html" %}

  {% block content %}
  <h2>Carbon Footprint Result</h2>
  <p>Your estimated emissions are: {{ emissions }} kg CO2</p>
  <p>{{ alternative }}</p>
  <a href="{{ url_for('index') }}">Calculate again</a>
  {% endblock %}
  ```

5. Run the application:
   ```
   python app.py
   ```

6. Visit `http://127.0.0.1:5000/` in your web browser to see and interact with the application.

This example provides error handling for numeric input conversion and generic error logging, as well as a basic UI presented using HTML templates. This is a simplified application for educational purposes, and further enhancements would involve refining the emissions calculation, enhancing the UI for better user experience, ensuring security aspects, and possibly integrating a database for storing user data.