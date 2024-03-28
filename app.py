from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory


app = Flask(__name__)


available_parameters = {
    "q1": "Charge 1 (q1)",
    "q2": "Charge 2 (q2)",
    "r": "Distance (r)",
    "F": "Force (F)",
}


available_formulas = {
    "coulomb_force": "Coulomb's Law: F = k(q_1×q_2)/r^2 ",
    "electric_field": "Electric Field: E = F/q",
    "voltage": "Voltage: V = W/Q",
}


@app.route('/')
def index():
    return render_template('index.html', available_parameters=available_parameters,
                           available_formulas=available_formulas)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', available_parameters=available_parameters,
                           available_formulas=available_formulas)


@app.route('/about')
def about():
    return render_template('about.html', available_parameters=available_parameters,
                           available_formulas=available_formulas)


@app.route('/electrostatics_calculator')
def electrostatics_calculator():
    return render_template('electrostatics_calculator.html', available_parameters=available_parameters,
                           available_formulas=available_formulas)


@app.route('/result', methods=['POST'])
def result():
    selected_parameters = {}
    for key, value in request.form.items():
        if key.startswith("param_name_"):
            param_name = value
            param_value = request.form.get(f"param_value_{param_name}", "")
            selected_parameters[param_name] = param_value

    selected_formula = request.form['formula']
    result = calculate_formula(selected_formula, selected_parameters)
    return render_template('result.html', result=result)


def calculate_formula(formula_name, parameters):
    if formula_name == 'coulomb_force':
        try:
            q1 = float(parameters.get('q1', 0))
            q2 = float(parameters.get('q2', 0))
            r = float(parameters.get('r', 1))
            k = 8.9875 * (10**9)
            force = k * q1 * q2 / (r**2)
            return force
        except ValueError:
            return "Invalid input. Please enter numeric values for charges and distance."
    elif formula_name == 'electric_field':
        try:
            force = float(parameters.get('force', 0))
            q = float(parameters.get('q', 1))
            electric_field = force / q
            return electric_field
        except ValueError:
            return "Invalid input. Please enter numeric values for force and charge."
    elif formula_name == 'voltage':
        try:
            work = float(parameters.get('work', 0))
            charge = float(parameters.get('charge', 1))
            voltage = work / charge
            return voltage
        except ValueError:
            return "Invalid input. Please enter numeric values for work and charge."


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(debug=True)
