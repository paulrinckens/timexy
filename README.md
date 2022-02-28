# Timexy 🕙 📅

<a href="https://pypi.org/project/timexy" target="_blank">
    <img src="https://img.shields.io/pypi/v/timexy?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.codecov.io/gh/paulrinckens/timexy" target="_blank">
    <img src="https://img.shields.io/codecov/c/gh/paulrinckens/timexy" alt="Codecov">
</a>


A [spaCy](https://spacy.io/) [custom component](https://spacy.io/usage/processing-pipelines#custom-components) that extracts and normalizes dates and other temporal expressions.

## Features
- :boom: Extract dates and durations for various languages. See [here](#supported-languages) a list of currently supported languages
- :boom: Normalize dates to timestamps or normalize dates and durations to the [TimeML TIMEX3 standard](http://www.timeml.org/publications/timeMLdocs/timeml_1.2.1.html#timex3)

## Supported Languages
- 🇩🇪 German
- :uk: English
- 🇫🇷 French

## Installation
````
pip install timexy
````
## Usage
After installation, simply integrate the timexy component in any of your spaCy pipelines to extract and normalize dates and other temporal expressions:

```py
import spacy
from timexy import Timexy

nlp = spacy.load("en_core_web_sm")

# Optionally add config if varying from default values
config = {
    "kb_id_type": "timex3",  # possible values: 'timex3'(default), 'timestamp'
    "label": "timexy",  # default: 'time'
    "overwrite": False  # default: False
}
nlp.add_pipe("timexy", config=config)

doc = nlp("Today is the 10.10.2010. I was in Paris for six years.")
for e in doc.ents:
    print(f"{e.text}\t{e.label_}\t{e.kb_id_}")    
```

```bash
>>> 10.10.2010    timexy    TIMEX3 type="DATE" value="2010-10-10T00:00:00"
>>> six years     timexy    TIMEX3 type="DURATION" value="P6Y"
```
## Contributing
Please refer to the contributing guidelines [here](https://github.com/paulrinckens/timexy/blob/main/CONTRIBUTING.md).
