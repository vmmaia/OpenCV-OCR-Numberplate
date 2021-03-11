# Number plate recognizer

This project was developed by Vasco Maia in September 2020.

## Description

This project was developed in Python3 to implement the usecase of number plate recognition by applying the Canny edge detection method.

## Installation

To run this project, first the packages specified in the requirements.txt file must be installed by doing the following:

```
pip install -r requirements.txt
```

## Usage

This is a CLI application that accepts two parameters:

| Argument | Description                                      |
| -------- | ------------------------------------------------ |
| path     | Relative path to the image to be analysed        |
| debug    | Show debug information. Can be 'True' or 'False' |

To run use the following syntax:

```
python main.py <path> <debug>
```

## Todo

- Add a GUI with sliders to adjust parameters on the fly
