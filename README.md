# pyqt-lifx-widget

# Description
TODO:

# Installation
No idea how to build PyQt Widgets as an app, let alone to make them work in Plasma. For now get [Anaconda/Miniconda](https://www.anaconda.com/products/individual), then:
```
git clone https://github.com/balbok0/pyqt-lifx-widget.git ~/.lifx-pyqt-widget
cd ~/.lifx-pyqt-widget
conda env create -f environment.yaml
```

# Running
Make sure you are within `lifx-pyqt-widget` conda environment and run:
```
python ~/.lifx-pyqt-widget/src/main.py
```

An alias would look something like this:
```
alias lifx="conda activate lifx-pyqt-widget && python ~/.lifx-pyqt-widget/src/main.py"
```