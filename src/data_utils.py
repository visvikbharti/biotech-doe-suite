import pandas as pd
import numpy as np
import streamlit as st
import os
from pathlib import Path
from itertools import product

# Path to sample datasets
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_sample_dataset(dataset_name):
    """Load a sample dataset by name.
    
    Parameters:
    -----------
    dataset_name : str
        Name of the dataset to load
        
    Returns:
    --------
    pandas.DataFrame
        The loaded dataset
    """
    dataset_map = {
        "Protein Expression": "protein_expression.csv",
        "Chromatography Method": "chromatography_method.csv",
        "Media Optimization": "media_optimization.csv"
    }
    
    if dataset_name not in dataset_map:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    file_path = DATA_DIR / dataset_map[dataset_name]
    return pd.read_csv(file_path)

def generate_sample_dataset(dataset_type, include_noise=True, **kwargs):
    """Generate a synthetic dataset for demonstration.
    
    Parameters:
    -----------
    dataset_type : str
        Type of dataset to generate (factorial, response_surface, etc.)
    include_noise : bool
        Whether to include random noise in responses
    **kwargs : dict
        Additional parameters specific to the design type
        
    Returns:
    --------
    pandas.DataFrame
        The generated dataset
    """
    if dataset_type == "factorial_2level":
        # Generate 2-level factorial design
        factors = kwargs.get("factors", ["Temperature", "pH", "Time", "Concentration"])
        n_factors = len(factors)
        
        # Generate design matrix in standard order
        runs = 2**n_factors
        design_matrix = np.zeros((runs, n_factors))
        for i in range(runs):
            for j in range(n_factors):
                # Convert run number to binary and assign factor levels
                design_matrix[i, j] = 1 if (i // 2**(n_factors-j-1)) % 2 else -1
        
        # Create dataframe
        df = pd.DataFrame(design_matrix, columns=[f"{factor}_coded" for factor in factors])
        
        # Add actual factor values
        factor_ranges = kwargs.get("factor_ranges", {
            "Temperature": [30, 37],
            "pH": [6.5, 7.5],
            "Time": [24, 48],
            "Concentration": [1.0, 5.0]
        })
        
        for factor in factors:
            if factor in factor_ranges:
                low, high = factor_ranges[factor]
                df[factor] = ((df[f"{factor}_coded"] + 1) / 2) * (high - low) + low
            else:
                # Default to -1=0, 1=1 if range not specified
                df[factor] = (df[f"{factor}_coded"] + 1) / 2
        
        # Add run order and standard order
        df.insert(0, "StdOrder", range(1, runs + 1))
        df.insert(0, "RunOrder", np.random.permutation(runs) + 1)
        
        # Generate responses
        if "Yield" in kwargs.get("responses", ["Yield"]):
            # Example model: Yield affected by all factors with interactions
            temp_effect = 5.0
            ph_effect = -2.0
            time_effect = 3.0
            conc_effect = 4.0
            temp_ph_interaction = -1.5
            
            base_yield = 75.0
            df["Yield"] = (base_yield + 
                         temp_effect * df.get(f"Temperature_coded", 0) + 
                         ph_effect * df.get(f"pH_coded", 0) + 
                         time_effect * df.get(f"Time_coded", 0) + 
                         conc_effect * df.get(f"Concentration_coded", 0))
            
            # Add interaction if we have both temperature and pH
            if "Temperature_coded" in df.columns and "pH_coded" in df.columns:
                df["Yield"] += temp_ph_interaction * df["Temperature_coded"] * df["pH_coded"]
            
            # Add noise if requested
            if include_noise:
                df["Yield"] += np.random.normal(0, 2.0, len(df))
        
        if "Purity" in kwargs.get("responses", []):
            # Example model: Purity mainly affected by pH and Concentration
            base_purity = 90.0
            df["Purity"] = (base_purity +
                          -3.0 * df.get(f"pH_coded", 0) + 
                          2.0 * df.get(f"Concentration_coded", 0))
            
            # Add noise if requested
            if include_noise:
                df["Purity"] += np.random.normal(0, 1.0, len(df))
        
        # Add center points if requested
        n_center = kwargs.get("center_points", 0)
        if n_center > 0:
            center_points = pd.DataFrame({
                "RunOrder": [runs + i + 1 for i in range(n_center)],
                "StdOrder": [runs + i + 1 for i in range(n_center)]
            })
            
            # Add coded values (0 for center points)
            for factor in factors:
                center_points[f"{factor}_coded"] = 0
                
                # Add actual factor values (midpoint)
                if factor in factor_ranges:
                    low, high = factor_ranges[factor]
                    center_points[factor] = (low + high) / 2
                else:
                    center_points[factor] = 0.5
            
            # Add response values
            if "Yield" in kwargs.get("responses", ["Yield"]):
                center_points["Yield"] = base_yield
                if include_noise:
                    center_points["Yield"] += np.random.normal(0, 1.5, n_center)
            
            if "Purity" in kwargs.get("responses", []):
                center_points["Purity"] = base_purity
                if include_noise:
                    center_points["Purity"] += np.random.normal(0, 0.8, n_center)
            
            # Append center points to design
            df = pd.concat([df, center_points], ignore_index=True)
        
        return df
        
    elif dataset_type == "response_surface":
        # Generate central composite design
        factors = kwargs.get("factors", ["Temperature", "pH", "Agitation"])
        n_factors = len(factors)
        
        # Factorial points
        factorial_runs = 2**n_factors
        factorial_matrix = np.zeros((factorial_runs, n_factors))
        for i in range(factorial_runs):
            for j in range(n_factors):
                factorial_matrix[i, j] = 1 if (i // 2**(n_factors-j-1)) % 2 else -1
        
        # Axial points (for rotatability, alpha = (2^n)^(1/4))
        alpha = kwargs.get("alpha", np.sqrt(2)**n_factors)
        axial_points = []
        for j in range(n_factors):
            point_plus = [0] * n_factors
            point_plus[j] = alpha
            axial_points.append(point_plus)
            
            point_minus = [0] * n_factors
            point_minus[j] = -alpha
            axial_points.append(point_minus)
        
        # Center points
        n_center = kwargs.get("center_points", 6)
        center_points = [[0] * n_factors for _ in range(n_center)]
        
        # Combine all points
        design_matrix = np.vstack([factorial_matrix, axial_points, center_points])
        
        # Create dataframe
        df = pd.DataFrame(design_matrix, columns=[f"{factor}_coded" for factor in factors])
        
        # Add actual factor values
        factor_ranges = kwargs.get("factor_ranges", {
            "Temperature": [25, 40],
            "pH": [6.0, 8.0],
            "Agitation": [100, 300]
        })
        
        for factor in factors:
            if factor in factor_ranges:
                low, high = factor_ranges[factor]
                mid = (low + high) / 2
                half_range = (high - low) / 2
                df[factor] = mid + half_range * df[f"{factor}_coded"]
            else:
                # Default to 0=midpoint if range not specified
                df[factor] = df[f"{factor}_coded"]
        
        # Add run order and standard order
        df.insert(0, "StdOrder", range(1, len(df) + 1))
        df.insert(0, "RunOrder", np.random.permutation(len(df)) + 1)
        
        # Generate responses
        if "Yield" in kwargs.get("responses", ["Yield"]):
            # Quadratic model for response surface
            base_yield = 70.0
            
            # Linear effects
            temp_effect = 8.0
            ph_effect = -5.0
            agit_effect = 3.0
            
            # Quadratic effects (negative for concave surface with maximum)
            temp_quad = -4.0
            ph_quad = -3.0
            agit_quad = -2.0
            
            # Interactions
            temp_ph_inter = -2.0
            temp_agit_inter = 1.0
            ph_agit_inter = 0.5
            
            # Calculate response
            df["Yield"] = base_yield
            
            # Add linear effects
            if "Temperature_coded" in df.columns:
                df["Yield"] += temp_effect * df["Temperature_coded"]
            if "pH_coded" in df.columns:
                df["Yield"] += ph_effect * df["pH_coded"]
            if "Agitation_coded" in df.columns:
                df["Yield"] += agit_effect * df["Agitation_coded"]
            
            # Add quadratic effects
            if "Temperature_coded" in df.columns:
                df["Yield"] += temp_quad * df["Temperature_coded"]**2
            if "pH_coded" in df.columns:
                df["Yield"] += ph_quad * df["pH_coded"]**2
            if "Agitation_coded" in df.columns:
                df["Yield"] += agit_quad * df["Agitation_coded"]**2
            
            # Add interactions
            if "Temperature_coded" in df.columns and "pH_coded" in df.columns:
                df["Yield"] += temp_ph_inter * df["Temperature_coded"] * df["pH_coded"]
            if "Temperature_coded" in df.columns and "Agitation_coded" in df.columns:
                df["Yield"] += temp_agit_inter * df["Temperature_coded"] * df["Agitation_coded"]
            if "pH_coded" in df.columns and "Agitation_coded" in df.columns:
                df["Yield"] += ph_agit_inter * df["pH_coded"] * df["Agitation_coded"]
            
            # Add noise if requested
            if include_noise:
                df["Yield"] += np.random.normal(0, 2.5, len(df))
        
        if "Purity" in kwargs.get("responses", []):
            # Another quadratic model for purity
            base_purity = 95.0
            
            # Linear and quadratic effects
            df["Purity"] = (base_purity + 
                          -2.0 * df.get("pH_coded", 0) + 
                          3.0 * df.get("Agitation_coded", 0) +
                          -1.5 * df.get("pH_coded", 0)**2 +
                          -2.0 * df.get("Agitation_coded", 0)**2)
            
            # Add noise if requested
            if include_noise:
                df["Purity"] += np.random.normal(0, 1.2, len(df))
        
        return df
        
    elif dataset_type == "mixture":
        # Generate mixture design (e.g., Simplex Lattice)
        components = kwargs.get("components", ["A", "B", "C"])
        n_components = len(components)
        
        # Determine degree of lattice
        degree = kwargs.get("degree", 3)
        
        # Generate points for simplex lattice design
        points = []
        for combo in product(range(degree + 1), repeat=n_components):
            if sum(combo) == degree:
                # Convert to proportions
                point = [x/degree for x in combo]
                points.append(point)
        
        # Create dataframe
        df = pd.DataFrame(points, columns=components)
        
        # Add run order and design order
        df.insert(0, "DesignOrder", range(1, len(df) + 1))
        df.insert(0, "RunOrder", np.random.permutation(len(df)) + 1)
        
        # Generate response for mixture
        if "Response" in kwargs.get("responses", ["Response"]):
            # Example: Scheffé model for ternary mixture
            # Response = b1*x1 + b2*x2 + b3*x3 + b12*x1*x2 + b13*x1*x3 + b23*x2*x3
            
            # Linear coefficients
            b = [80, 60, 70]  # Component effects
            
            # Binary interaction coefficients (can be positive or negative)
            b_interaction = [15, -10, 5]  # AB, AC, BC interactions
            
            # Calculate response
            df["Response"] = 0
            
            # Add linear terms
            for i, comp in enumerate(components):
                if i < len(b):
                    df["Response"] += b[i] * df[comp]
            
            # Add binary interaction terms
            interaction_idx = 0
            for i in range(n_components):
                for j in range(i+1, n_components):
                    if interaction_idx < len(b_interaction):
                        df["Response"] += b_interaction[interaction_idx] * df[components[i]] * df[components[j]]
                        interaction_idx += 1
            
            # Add noise if requested
            if include_noise:
                df["Response"] += np.random.normal(0, 2.0, len(df))
        
        return df
    
    elif dataset_type == "screening":
        # Generate Plackett-Burman design or Fractional Factorial
        n_factors = kwargs.get("n_factors", 7)
        factors = kwargs.get("factors", [f"Factor{i+1}" for i in range(n_factors)])
        
        if n_factors <= 4:
            # Use full factorial for small factor counts
            return generate_sample_dataset("factorial_2level", include_noise, 
                                         factors=factors, **kwargs)
        
        # Determine appropriate design size (next power of 2 ≥ n_factors + 1)
        k = 1
        while 2**k < n_factors + 1:
            k += 1
        
        # For Plackett-Burman designs, round up to multiple of 4
        design_size = max(2**k, 4 * ((n_factors + 3) // 4))
        
        if kwargs.get("design_type", "Plackett-Burman") == "Plackett-Burman":
            # Use Plackett-Burman design
            # For PB designs, we can construct using a specific algorithm
            # Here we'll simulate with fixed standard designs
            
            if design_size == 8:
                base_row = [1, 1, 1, -1, 1, -1, -1]
            elif design_size == 12:
                base_row = [1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1]
            elif design_size == 16:
                base_row = [1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1]
            else:
                # Fallback to fractional factorial
                return generate_sample_dataset("factorial_2level", include_noise, 
                                             factors=factors[:min(n_factors, 4)], **kwargs)
            
            # Generate design matrix by cyclic permutation of base row
            design_matrix = []
            row = base_row.copy()
            design_matrix.append(row.copy()[:n_factors])
            
            for i in range(1, design_size - 1):
                # Circular shift
                row = row[-1:] + row[:-1]
                design_matrix.append(row.copy()[:n_factors])
            
            # Last row is all -1
            design_matrix.append([-1] * n_factors)
            
        else:
            # Use Fractional Factorial design
            # For simplicity, we'll use a Resolution III design
            # where main effects are confounded with 2-factor interactions
            
            # Create basic factorial design for first k factors
            base_k = min(k-1, n_factors)
            base_runs = 2**base_k
            base_matrix = np.zeros((base_runs, base_k))
            
            for i in range(base_runs):
                for j in range(base_k):
                    base_matrix[i, j] = 1 if (i // 2**(base_k-j-1)) % 2 else -1
            
            # Create design matrix and extend for additional factors using interactions
            design_matrix = np.zeros((base_runs, n_factors))
            design_matrix[:, :base_k] = base_matrix
            
            # Define additional columns as interactions of base columns
            for j in range(base_k, n_factors):
                # Use a simple generator for additional columns
                # In a real implementation, you would use specific generators to ensure
                # higher resolution when possible
                col_idx1 = (j - base_k) % base_k
                col_idx2 = ((j - base_k) // base_k + 1) % base_k
                design_matrix[:, j] = base_matrix[:, col_idx1] * base_matrix[:, col_idx2]
        
        # Create dataframe
        df = pd.DataFrame(design_matrix, columns=[f"{factor}_coded" for factor in factors])
        
        # Add actual factor values
        factor_ranges = kwargs.get("factor_ranges", {})
        
        for factor in factors:
            if factor in factor_ranges:
                low, high = factor_ranges[factor]
                df[factor] = ((df[f"{factor}_coded"] + 1) / 2) * (high - low) + low
            else:
                # Default to -1=low, 1=high if range not specified
                df[factor] = ["High" if x > 0 else "Low" for x in df[f"{factor}_coded"]]
        
        # Add run order and standard order
        df.insert(0, "StdOrder", range(1, len(df) + 1))
        df.insert(0, "RunOrder", np.random.permutation(len(df)) + 1)
        
        # Generate responses
        if "Effect" in kwargs.get("responses", ["Effect"]):
            # For screening designs, usually only a few factors have significant effects
            # Let's make factors 1, 3, and 5 significant (if they exist)
            
            base_effect = 50.0
            df["Effect"] = base_effect
            
            significant_factors = [0, 2, 4]  # 0-indexed factors to have effects
            effect_sizes = [10.0, -7.0, 5.0]
            
            for i, factor_idx in enumerate(significant_factors):
                if factor_idx < n_factors and i < len(effect_sizes):
                    factor = factors[factor_idx]
                    df["Effect"] += effect_sizes[i] * df[f"{factor}_coded"]
            
            # Add noise if requested
            if include_noise:
                df["Effect"] += np.random.normal(0, 2.5, len(df))
        
        return df
    
    # Default case - return empty dataframe with message
    st.warning(f"Unsupported dataset type: {dataset_type}")
    return pd.DataFrame()

def save_dataset(df, filename):
    """Save a dataset to the data directory.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset to save
    filename : str
        Name of the file to save
    """
    file_path = DATA_DIR / filename
    df.to_csv(file_path, index=False)
    
def process_uploaded_csv(uploaded_file):
    """Process an uploaded CSV file.
    
    Parameters:
    -----------
    uploaded_file : streamlit.UploadedFile
        The uploaded file
        
    Returns:
    --------
    pandas.DataFrame
        The processed dataset
    """
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Basic validation
        if df.empty:
            st.error("The uploaded file is empty.")
            return None
            
        # Detect factorial design format
        if all(col in df.columns for col in ["RunOrder", "StdOrder"]):
            st.success("Detected factorial design format.")
            
        # Check for coded variables
        coded_cols = [col for col in df.columns if col.endswith('_coded')]
        if not coded_cols:
            st.info("No coded variables detected. Consider adding them for standard analysis.")
            
        return df
        
    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")
        return None

def identify_factor_response_columns(df):
    """Automatically identify factor and response columns in a dataset.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset to analyze
        
    Returns:
    --------
    tuple
        (factor_columns, response_columns)
    """
    # Skip metadata columns
    metadata_cols = ["RunOrder", "StdOrder", "DesignOrder", "BlockOrder", "Block"]
    
    # Identify coded columns and their base names
    coded_cols = [col for col in df.columns if col.endswith('_coded')]
    factor_bases = [col.replace('_coded', '') for col in coded_cols]
    
    # All columns with matching base names are factor columns
    factor_cols = []
    for base in factor_bases:
        if base in df.columns:
            factor_cols.append(base)
    
    # If no coded columns, try to identify factors by elimination
    if not factor_cols:
        # Guess factor columns based on naming conventions
        excluded_patterns = ['response', 'yield', 'output', 'result', 'purity', 
                           'activity', 'conversion', 'recovery', 'quality']
        
        factor_cols = [col for col in df.columns 
                     if col not in metadata_cols
                     and not any(pattern in col.lower() for pattern in excluded_patterns)]
    
    # Identify response columns (remaining columns that aren't factors or metadata)
    all_factor_related = factor_cols + coded_cols + metadata_cols
    response_cols = [col for col in df.columns if col not in all_factor_related]
    
    return factor_cols, response_cols

def add_coded_variables(df, factor_columns):
    """Add coded variables (-1, 0, 1) for numeric factors if they don't exist.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset to modify
    factor_columns : list
        Names of factor columns to code
        
    Returns:
    --------
    pandas.DataFrame
        Dataset with added coded variables
    """
    result_df = df.copy()
    
    for factor in factor_columns:
        coded_name = f"{factor}_coded"
        
        # Skip if coded column already exists
        if coded_name in result_df.columns:
            continue
            
        # Only code numeric columns
        if pd.api.types.is_numeric_dtype(result_df[factor]):
            # Get min and max values
            min_val = result_df[factor].min()
            max_val = result_df[factor].max()
            
            # Check if this is a 2-level factor
            unique_values = result_df[factor].unique()
            if len(unique_values) == 2:
                # For 2-level factors, use -1 and 1
                result_df[coded_name] = result_df[factor].map({
                    min_val: -1,
                    max_val: 1
                })
            else:
                # For multi-level factors, scale to [-1, 1]
                result_df[coded_name] = -1 + 2 * (result_df[factor] - min_val) / (max_val - min_val)
                
                # For 3-level factors with middle value, ensure it gets coded as 0
                if len(unique_values) == 3:
                    mid_val = sorted(unique_values)[1]
                    mid_coded = -1 + 2 * (mid_val - min_val) / (max_val - min_val)
                    if abs(mid_coded) < 0.1:  # Close to zero
                        result_df.loc[result_df[factor] == mid_val, coded_name] = 0
        else:
            # For categorical factors, use one-hot encoding or similar approach
            st.warning(f"Column '{factor}' is not numeric and wasn't coded. Consider manual coding.")
    
    return result_df