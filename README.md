<a href="https://www.humarobotics.com/">
    <img src="./images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" align="right" height="80" />
</a>

# Doosan Sick

<p align="left">
  <a href="./README.md">English</a> •
  <a href="docs/README-fr.md">Français</a>
</p>

--------------

Interface to use a SICK camera with a Doosan robot

This project is developed by [HumaRobotics](https://www.humarobotics.com/).

This class has been tested on a SICK camera *InspectorP621*.

## Requirements

- A **Doosan robot**
- A **SICK** camera

## How to use

- Create a `Custom Code` and import the [DoosanSick.py](./DoosanSick.py) file (replace .py by .txt to import in the Doosan). Don't forget to remove first lines of the code (those lines are used to test the code without a robot).

- Then, look at the examples in the "examples" folder to see how to use the DoosanSick class. You can begin with the [ex_doosan_sick.py](./examples/ex_doosan_sick.py) (don't forget to change the extension '.py' to '.txt' before importing it into the Doosan).

## Robot calibration

In order to calibrate the camera with the Doosan, please refer to chapter **7.2.2.Calibration** page 37 of [PLOC2D-3.3-Operating-Instructions---English.pdf](./documentations/PLOC2D-3.3-Operating-Instructions---English.pdf).

## Hand eye calibration

In order to perform a *Hand eye* calibration of the camera with the Doosan, please refer to chapter **7.2.3.2.Robot mounted sensor** page 42 of [PLOC2D-3.3-Operating-Instructions---English.pdf](./documentations/PLOC2D-3.3-Operating-Instructions---English.pdf).

## Examples files

- [ex_doosan_sick.py](./examples/ex_doosan_sick.py): Basic example for the communication between SICK camera and Doosan robot using Task Writer.

<div align = "center" >
<img src="./images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" height="200" />
</div>