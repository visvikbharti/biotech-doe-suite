# Sample Datasets for Biotech DOE Mastery Suite

This directory contains sample datasets for demonstrating DOE concepts in biotechnology applications.

## Available Datasets

### 1. Protein Expression Optimization (protein_expression.csv)

A 2³ factorial design with center points studying the effects of:
- Temperature (30°C, 37°C)
- pH (6.5, 7.5)
- Inducer Concentration (0.1, 1.0 mM IPTG)

Responses measured:
- Protein Yield (mg/L)
- Cell Density (OD600)
- Purity (%)

### 2. Chromatography Method Development (chromatography_method.csv)

A central composite design studying the effects of:
- Buffer pH (6.0-8.0)
- Salt Concentration (100-500 mM)
- Column Temperature (20-40°C)

Responses measured:
- Resolution
- Retention Time (min)
- Peak Area

### 3. Media Optimization for Cell Culture (media_optimization.csv)

A fractional factorial design studying the effects of:
- Glucose (2.0-6.0 g/L)
- Glutamine (2.0-6.0 mM)
- Serum (0-10%)
- Growth Factor (0-10 ng/mL)
- Buffer Concentration (10-30 mM)

Responses measured:
- Cell Density (million cells/mL)
- Viability (%)
- Productivity (pg/cell/day)

## Data Structure

Each dataset follows a standard format:
- `RunOrder`: The randomized order in which experiments were performed
- `StdOrder`: The standard design order
- Factor columns: Both actual values and coded values (-1, 0, 1)
- Response columns: Measured output variables

## Usage

These datasets can be loaded using the `load_sample_dataset` function in `data_utils.py`:

```python
from src.data_utils import load_sample_dataset

# Load protein expression dataset
data = load_sample_dataset("Protein Expression")
```