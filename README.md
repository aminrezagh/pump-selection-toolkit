# Pump Selection Toolkit

Pump Selection Toolkit, a comprehensive solution for selecting the optimal centrifugal pump. This toolkit is based on a database of mechanical and process data for centrifugal pumps purchased over the course of 25 years by one of the major EPC companies in MENA.

One of the key features of the toolkit is multiple machine learning models that have been trained to automatically determine the API type , the number of stages, the impeller diameter, and the efficiency of the pump based on head (H) and capacity (Q) data.

It also includes separate modules for mechanical seal and material selection, ensuring that every aspect of the pump selection process is covered.

## Features

- Comprehensive database of mechanical data for more than 500 pump tags.
- Easy-to-use UI facilitates advanced search through more than 40 operational data such as Q, H, Liquid, Seal Plan, Material, NPSH, Power, GAD, etc.
- Mechanical Seal Plan and Material Class suggestions based on liquid type and operating temperature
- Automatic API type selection from Q and H
- Automatic estimation of impeller diameter and efficiency from Q and H

## Requirements

The following dependencies are required to run this toolkit:

- Python 3
- Pandas
- Scikit-learn
- Plotly express
- Streamlit

## License

This repository is licensed under the MIT License.
