<a href="https://www.humarobotics.com/">
    <img src="../images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" align="right" height="80" />
</a>

# Doosan Sick

<p align="left">
  <a href="./README.md">English</a> •
  <a href="docs/README-fr.md">Français</a>
</p>

--------------

Interface permettant d'utiliser une caméra SICK avec un robot Doosan

Ce projet est développé par [HumaRobotics](https://www.humarobotics.com/).

Cette classe a été téstée sur une caméra SICK *InspectorP621*.

## Conditions requises

- Un **robot Doosan**
- Une caméra **SICK**

## Mode d'emploi

- Créez un `Custom Code` et importez le fichier [DoosanSick.py](./DoosanSick.py) (il faut remplacer le .py par .txt pour importer le fichier dans un Doosan). N'oubliez pas d'enlever les premières lignes du code (ces lignes sont utilisées pour tester le code sans robot).

- Ensuite, regardez les exemples dans le dossier "examples" pous savoir comment utiliser la classe DoosanSick. Vous pouvez commencer avec le programme [ex_doosan_sick.py](./examples/ex_doosan_sick.py) (n'oubliez pas de changer l'extension .py par .txt avant d'importer le fichier dans le Doosan).

## Calibration du robot

Pour calibrer la caméra avec le robot Doosan, réferez vous au chapitre **7.2.2.Calibration** page 37 de la documentation [PLOC2D-3.3-Operating-Instructions---English.pdf](./documentations/PLOC2D-3.3-Operating-Instructions---English.pdf).

## Calibration Hand eye

Pour procéder à une calibration *Hand eye* de la caméra avec le Doosan, réferez vous au chapitre **7.2.3.2.Robot mounted sensor** page 42 de la documentation [PLOC2D-3.3-Operating-Instructions---English.pdf](./documentations/PLOC2D-3.3-Operating-Instructions---English.pdf).

## Exemples

- [ex_doosan_sick.py](./examples/ex_doosan_sick.py): Exemple basique de communication entre la caméra SICK et le robot Doosan à l'aide du Task Writer.

<div align = "center" >
    <img src="../images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" height="200" />
</div>