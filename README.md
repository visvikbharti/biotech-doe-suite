# Biotech DOE Mastery Suite

![Biotech DOE Mastery Suite Logo](assets/logo.png)

## Overview

The Biotech DOE Mastery Suite is a comprehensive, interactive web application for learning and applying Design of Experiments (DOE) methods in biotechnology contexts. This application provides researchers, engineers, and students with a structured approach to understand, design, and analyze experiments in bioprocessing, formulation development, and analytical method optimization.

## Features

- **Interactive Learning Modules**: Progressive education from foundational concepts to advanced techniques
- **Real-time Simulations**: Compare traditional vs. DOE approaches with dynamic visualizations
- **Design Selection Tool**: Guided selection of appropriate experimental designs based on objectives and constraints
- **Power & Sample Size Calculator**: Optimize experimental resources while maintaining statistical validity
- **Design Space Visualization**: Interactive contour and surface plots for multivariate optimization
- **Biotechnology-Specific Examples**: Industry-relevant case studies and applications

## Application Structure

1. **Introduction to DOE in Biotechnology**
   - Importance and applications in biotechnology
   - Interactive comparison of traditional vs. DOE approaches

2. **Fundamental DOE Concepts**
   - Randomization, replication, blocking, and orthogonality
   - Interactive design matrix visualization tool

3. **Experimental Design Process**
   - Step-by-step guide from problem definition to execution
   - Interactive experimental planning wizard

4. **Design Types**
   - Full and fractional factorial designs
   - Response surface methodology
   - Mixture designs and specialized approaches

5. **Analysis & Interpretation**
   - Statistical analysis techniques
   - Interactive visualization of results
   - Model validation and optimization

6. **Case Studies**
   - Protein expression optimization
   - Chromatography method development
   - Media composition for cell culture
   - Vaccine formulation stability

7. **Summary & Integration**
   - Knowledge integration with broader bioprocess development
   - Connection to Quality by Design principles

## Technical Requirements

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- SciPy
- Plotly
- Statsmodels

## Installation & Usage

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/visvikbharti/biotech-doe-suite.git
   cd biotech-doe-suite
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Hosted Version

The application is also available online at [https://visvikbharti-biotech-doe-suite.streamlit.app/](https://biotech-doe-suite.streamlit.app/)

## Sample Datasets

The application includes example datasets for common biotechnology applications:

- Protein expression optimization
- Chromatography method development
- Media composition for cell culture

These datasets can be used to explore the features of the application without uploading proprietary data.

## Contributing

Contributions to improve the Biotech DOE Mastery Suite are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Streamlit for the excellent framework for building interactive data applications
- The scientific community for advancing DOE methodologies in biotechnology
- All contributors who helped develop and test this application

