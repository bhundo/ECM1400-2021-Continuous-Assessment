# ECM1400 Programming - Covid Dashboard
Covid Dashboard is coursework for the Computer Science ECM1400 module, it supplies real time data and news relating to Coronavirus.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sched, json, uk_covid19 and flask.
Please use Python 3.10+ as this was programmed in Python 3.10, and some modules may not function as expected in earlier versions of Python.

```bash
pip install sched
pip install json
pip install uk_covid19
pip install flask
```

## Usage
Run the main.py module in the root directory in order to render the covid dashboard.
Open the dashboard by entering 'localhost:5000/index' into the web browser.
Press 'Ctrl+C' to in the terminal to stop rendering the template.

To set a scheduled covid / news update:
    - Enter a time for the update,
    - Give the update a name,
    - Specify what you would like to update by checking the respective boxes.
    - Click submit.

To cancel an update / remove a news article:
    - click the x at the top right of the widget.

## Testing
To run tests on the code use pip to install pytest. Run the testing command in the terminal in the root directory

```bash
pip install pytest
```

```python
pytest test_covid_data_handler.py
pytest test_news_data_handling.py
```


