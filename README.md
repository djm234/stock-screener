# stock-screener
A package that enables screening to UK stocks using data downloaded from ADVFN.

## Features
This tool calculates metrics such as Z-score, Greenblatt's Magic Formula, and F score (approximation), then uses this data together with other metrics obtained from ADVFN to filter stocks.

Stocks are filtered according to a few preset 'styles', including:
- `dividend`
- `value`
- `momentum`
- `quality`
- `cash_rich`
- `magic_formula`
- And more.
These screen styles can be chained together to create a custom screen.

## Installation
```
pip install . -r requirements.txt
```

## Usage
To obtain the latest data:
```
python perform_screen.py
```
Results are output to terminal, and also stored locally in a directory named `_results`.
