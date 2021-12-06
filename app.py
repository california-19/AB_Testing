from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
p_value = model

@app.route('/', methods=['GET', 'POST'])
def home():
    request_type_str = request.method
    if request_type_str =='GET':
        outcome_text_ = 'Hello World'
        return render_template('index.html')
    else:
        form_data = request.form['Alpha_Value']
        alpha = float(form_data)
        if p_value <= alpha:
            outcome_text_ = 'We reject the null hypothesis since p-value is less than or equal to alpha'
        else:
            outcome_text_ = 'We fail to reject the null hypothesis since p-value is greater than alpha'
        return render_template('index.html', outcome_text = outcome_text_)

if __name__ == '__main__':
    app.run(debug = True)