import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from itertools import combinations

def show():
    st.header("Fundamental DOE Concepts")
    
    st.markdown("""
    This section introduces the core principles and mathematical foundations of Design of Experiments (DOE).
    Understanding these fundamentals is essential for effective experimental design in biotechnology applications.
    """)
    
    # Create tabs for different concept areas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Core DOE Principles", 
        "Factorial Design Fundamentals",
        "Interactive Design Matrix",
        "Mathematical Framework"
    ])
    
    # Tab 1: Core DOE Principles
    with tab1:
        st.markdown("""
        ## Core DOE Principles
        
        The fundamental principles that make Design of Experiments a powerful methodology:
        """)
        
        # Use expanders for each principle for cleaner organization
        with st.expander("### Randomization", expanded=True):
            st.markdown("""
            **Concept Anchor**: Randomization is the cornerstone of experimental validity, distributing unknown sources of variation randomly across experimental conditions.

            **Practical Lens**: In biotechnology, randomization helps mitigate the impact of uncontrolled variables such as microheterogeneity in cell populations, subtle equipment variations, and reagent lot differences. For example, in cell culture experiments, randomizing the plate position or incubator shelf location prevents systematic errors from temperature gradients or gas exchange differences.

            **Mathematical Foundation**:
            Randomization transforms systematic errors into random errors that can be quantified as part of experimental error ($\\varepsilon$):

            $$y_{ij} = \\mu + \\tau_i + \\varepsilon_{ij}$$

            Where:
            - $y_{ij}$ is the observed response for the $i$th treatment at the $j$th replicate
            - $\\mu$ is the overall mean
            - $\\tau_i$ is the effect of the $i$th treatment
            - $\\varepsilon_{ij}$ is the random error term, assumed to be independently and identically distributed
            """)
        
        with st.expander("### Replication"):
            st.markdown("""
            **Concept Anchor**: Replication involves repeating experimental runs under identical conditions to quantify experimental variability and increase precision in effect estimates.

            **Practical Lens**: Biological systems exhibit inherent variability, making replication crucial. In protein expression systems, multiple replicate fermentations provide reliable estimates of process variability and distinguishes real effects from noise. For example, triplicate runs of a CHO cell culture allow estimation of production variability for calculation of confidence intervals around titer measurements.

            **Mathematical Foundation**:
            Replication reduces the standard error of the mean by a factor of $\\sqrt{n}$:

            $$SE(\\bar{y}) = \\frac{\\sigma}{\\sqrt{n}}$$

            Where:
            - $SE(\\bar{y})$ is the standard error of the mean
            - $\\sigma$ is the standard deviation
            - $n$ is the number of replicates

            This translates directly to the precision of effect estimates in DOE models:

            $$SE(\\hat{\\beta}) = \\frac{\\sigma}{\\sqrt{N}}$$

            Where:
            - $SE(\\hat{\\beta})$ is the standard error of the estimated effect
            - $\\sigma$ is the standard deviation
            - $N$ is the total number of runs in the experiment
            """)
        
        with st.expander("### Blocking"):
            st.markdown("""
            **Concept Anchor**: Blocking isolates known sources of variability that are not of primary interest, enhancing precision and eliminating confounding from nuisance factors.

            **Practical Lens**: In biotechnology, blocking addresses variations like equipment differences, reagent lots, or operator changes. For example, when testing a purification process, different protein batches (blocks) might be used to evaluate chromatography conditions, preventing batch-to-batch variation from obscuring the effects of interest.

            **Mathematical Foundation**:
            The blocked design model extends the basic model to include block effects:

            $$y_{ijk} = \\mu + \\tau_i + \\beta_j + \\varepsilon_{ijk}$$

            Where:
            - $y_{ijk}$ is the observed response for the $i$th treatment in the $j$th block at the $k$th replicate
            - $\\mu$ is the overall mean
            - $\\tau_i$ is the effect of the $i$th treatment
            - $\\beta_j$ is the effect of the $j$th block
            - $\\varepsilon_{ijk}$ is the random error term

            In the ANOVA table, blocking reduces error variance by partitioning the sum of squares:

            $$SS_{Total} = SS_{Treatment} + SS_{Block} + SS_{Error}$$
            """)
        
        with st.expander("### Orthogonality"):
            st.markdown("""
            **Concept Anchor**: Orthogonality ensures that effect estimates are uncorrelated, maximizing the precision and allowing independent interpretation of factor effects.

            **Practical Lens**: In bioprocess development, orthogonal designs allow independent assessment of critical parameters like pH, temperature, and nutrient concentrations without confounding. This enables clear attribution of effects when optimizing, for example, monoclonal antibody production in bioreactors.

            **Mathematical Foundation**:
            For a design matrix $X$, orthogonality means:

            $$X^TX = nI$$

            Where:
            - $X$ is the design matrix in coded units
            - $I$ is the identity matrix
            - $n$ is the number of runs

            This property ensures that parameter estimates are uncorrelated:

            $$Cov(\\hat{\\beta}_i, \\hat{\\beta}_j) = 0 \\quad \\text{for} \\quad i \\neq j$$

            The variance inflation factor (VIF) quantifies deviations from orthogonality:

            $$VIF_j = \\frac{1}{1-R_j^2}$$

            Where $R_j^2$ is the coefficient of determination when the $j$th factor is regressed on all other factors.
            """)
    
    # Tab 2: Factorial Design Fundamentals
    with tab2:
        st.markdown("""
        ## Factorial Design Fundamentals
        
        The key concepts and mathematical foundations of factorial experimental designs:
        """)
        
        with st.expander("### Main Effects", expanded=True):
            st.markdown("""
            **Concept Anchor**: A main effect quantifies the average change in response when a factor changes from its low to high level, averaged across all conditions of other factors.

            **Practical Lens**: In biotech applications, main effects identify critical process parameters (CPPs) that significantly impact critical quality attributes (CQAs). For example, the main effect of temperature on enzyme activity in a biocatalytic process informs process control strategies and design spaces for regulatory filings.

            **Mathematical Foundation**:
            For a two-level design, the main effect of factor A is calculated as:

            $$E_A = \\frac{\\sum y_{A+} - \\sum y_{A-}}{n/2}$$

            Where:
            - $\\sum y_{A+}$ is the sum of responses when factor A is at high level
            - $\\sum y_{A-}$ is the sum of responses when factor A is at low level
            - $n$ is the total number of runs
            """)
            
            # Add visual example of main effect
            st.markdown("#### Visual Example of Main Effect")
            
            # Generate data for visualization
            x = np.array([-1, 1])
            y_low = np.array([30, 30])
            y_high = np.array([50, 50])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_low, mode='lines+markers', name='Low Level', 
                                    line=dict(color='blue', width=2)))
            fig.add_trace(go.Scatter(x=x, y=y_high, mode='lines+markers', name='High Level', 
                                    line=dict(color='red', width=2)))
            
            fig.update_layout(
                title="Example of a Main Effect",
                xaxis=dict(
                    tickvals=[-1, 1],
                    ticktext=["Low (-1)", "High (+1)"],
                    title="Factor Level"
                ),
                yaxis=dict(title="Response"),
                height=400
            )
            
            st.plotly_chart(fig)
        
        with st.expander("### Interaction Effects"):
            st.markdown("""
            **Concept Anchor**: An interaction effect occurs when the impact of one factor on the response depends on the level of another factor, revealing complex system behaviors beyond additive effects.

            **Practical Lens**: Biological systems are rife with interactions. In cell culture media optimization, glucose and glutamine concentrations often interact strongly as primary carbon and nitrogen sources, requiring simultaneous optimization rather than independent adjustment.

            **Mathematical Foundation**:
            The two-factor interaction effect for factors A and B is calculated as:

            $$E_{AB} = \\frac{\\sum y_{A+B+} + \\sum y_{A-B-} - \\sum y_{A+B-} - \\sum y_{A-B+}}{n/2}$$

            Where:
            - $\\sum y_{A+B+}$ is the sum of responses when both factors are at high levels
            - $\\sum y_{A-B-}$ is the sum of responses when both factors are at low levels
            - $\\sum y_{A+B-}$ is the sum of responses when A is high and B is low
            - $\\sum y_{A-B+}$ is the sum of responses when A is low and B is high
            """)
            
            # Add visual example of interaction effect
            st.markdown("#### Visual Example of Interaction Effect")
            
            # Generate data for visualization
            x = np.array([-1, 1])
            y_b_low = np.array([30, 60])  # B at low level
            y_b_high = np.array([50, 40])  # B at high level
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_b_low, mode='lines+markers', name='B at Low Level', 
                                    line=dict(color='blue', width=2)))
            fig.add_trace(go.Scatter(x=x, y=y_b_high, mode='lines+markers', name='B at High Level', 
                                    line=dict(color='red', width=2)))
            
            fig.update_layout(
                title="Example of an Interaction Effect",
                xaxis=dict(
                    tickvals=[-1, 1],
                    ticktext=["A at Low (-1)", "A at High (+1)"],
                    title="Factor A Level"
                ),
                yaxis=dict(title="Response"),
                height=400
            )
            
            st.plotly_chart(fig)
        
        with st.expander("### Confounding"):
            st.markdown("""
            **Concept Anchor**: Confounding occurs when effect estimates are mixed (aliased), making it impossible to distinguish between certain effects with the given design.

            **Practical Lens**: In biotechnology, confounding must be carefully managed. When designing experiments for bioproduct stability, temperature and light exposure effects might be confounded in an incomplete design, leading to misinterpretation of degradation mechanisms.

            **Mathematical Foundation**:
            In a fractional factorial design, the aliasing pattern is determined by the defining relation. For example, in a 2^(k-p) design, the confounding pattern is given by the generalized interaction:

            $$I = ABC...K$$

            Where I represents the identity column, and the factors on the right define the aliasing structure. The complete aliasing pattern can be derived through modular arithmetic:

            $$E_{estimated} = E_{true} + E_{aliased}$$

            Effect aliasing can be expressed using the alias matrix:

            $$A = (X^TX)^{-1}X^T$$

            Where $X$ is the design matrix.
            """)
        
        with st.expander("### Resolution"):
            st.markdown("""
            **Concept Anchor**: Resolution describes a design's ability to distinguish between different types of effects, with higher resolution indicating less severe confounding patterns.

            **Practical Lens**: In bioanalytical method development, resolution selection balances experimental resources against information needs. A Resolution V design might be selected for developing a critical HPLC assay for drug impurities, ensuring main effects and two-factor interactions are unconfounded.

            **Mathematical Foundation**:
            Resolution is denoted by Roman numerals and defined by the minimum word length in the defining relation:

            - Resolution III: Main effects are not confounded with other main effects but may be confounded with two-factor interactions
            - Resolution IV: Main effects are not confounded with main effects or two-factor interactions, but two-factor interactions may be confounded with each other
            - Resolution V: Main effects and two-factor interactions are not confounded with each other

            For a 2^(k-p) design with defining relation I = ABC...K, the resolution R is:

            $$R = \\min(w_1, w_2, ..., w_m)$$

            Where $w_i$ is the word length (number of letters) in each term of the defining relation.
            """)
            
            # Add visual comparison of different resolution designs
            st.markdown("#### Comparison of Different Resolution Designs")
            
            # Create comparison table
            resolution_comparison = pd.DataFrame({
                "Resolution": ["III", "IV", "V", "Full Factorial"],
                "Main Effects": ["Clear of other main effects", "Clear of main effects and 2FI", "Clear of main effects and 2FI", "All effects clear"],
                "Two-Factor Interactions": ["Confounded with main effects", "Confounded with other 2FI", "Clear of main effects and other 2FI", "All effects clear"],
                "Runs (for 5 factors)": ["8", "16", "16", "32"],
                "Typical Use Case": ["Initial screening", "Characterization", "Detailed characterization", "Complete analysis"]
            })
            
            st.table(resolution_comparison)
    
    # Tab 3: Interactive Design Matrix
    with tab3:
        # Call the interactive function for design matrix visualization
        design_matrix_visualization()
    
    # Tab 4: Mathematical Framework
    with tab4:
        st.markdown("""
        ## Mathematical Framework of DOE
        
        The statistical and mathematical foundations that support Design of Experiments:
        """)
        
        # ANOVA model explanation
        st.markdown("""
        ### Analysis of Variance (ANOVA) Model
        
        The ANOVA model is fundamental to DOE analysis, partitioning observed variation into components attributed to different sources:
        
        $$SS_{Total} = SS_{Factors} + SS_{Error}$$
        
        For a model with multiple factors:
        
        $$SS_{Factors} = SS_A + SS_B + SS_{AB} + ...$$
        
        The significance of effects is tested using F-tests:
        
        $$F_A = \\frac{MS_A}{MS_{Error}} = \\frac{SS_A/df_A}{SS_{Error}/df_{Error}}$$
        
        Where $MS$ represents Mean Squares, and $df$ represents degrees of freedom.
        """)
        
        # Regression model explanation
        st.markdown("""
        ### Regression Model Formulation
        
        DOE can also be expressed as a regression problem:
        
        $$y = X\\beta + \\varepsilon$$
        
        Where:
        - $y$ is the vector of responses
        - $X$ is the design matrix
        - $\\beta$ is the vector of coefficients
        - $\\varepsilon$ is the error vector
        
        The least squares estimator for the coefficients is:
        
        $$\\hat{\\beta} = (X^TX)^{-1}X^Ty$$
        
        For orthogonal designs, this simplifies to:
        
        $$\\hat{\\beta}_j = \\frac{X_j^Ty}{X_j^TX_j}$$
        """)
        
        # Advanced concepts with expandable sections
        with st.expander("### Response Surface Methodology"):
            st.markdown("""
            Response Surface Methodology (RSM) extends factorial designs to model curvature:
            
            $$y = \\beta_0 + \\sum_{i=1}^{k}\\beta_i x_i + \\sum_{i<j}^{k}\\beta_{ij}x_i x_j + \\sum_{i=1}^{k}\\beta_{ii}x_i^2 + \\varepsilon$$
            
            The stationary point of the surface is found by solving:
            
            $$\\frac{\\partial \\hat{y}}{\\partial x_i} = 0 \\quad \\text{for all} \\quad i = 1, 2, ..., k$$
            
            The nature of the stationary point (maximum, minimum, or saddle point) is determined by the eigenvalues of the matrix of second-order coefficients.
            """)
            
        with st.expander("### Mixture Design Mathematics"):
            st.markdown("""
            Mixture designs deal with components that sum to a constant (typically 1 or 100%):
            
            $$\\sum_{i=1}^{q} x_i = 1 \\quad \\text{and} \\quad x_i \\geq 0 \\quad \\forall i$$
            
            The Scheffé canonical polynomial for mixture models:
            
            $$y = \\sum_{i=1}^{q}\\beta_i x_i + \\sum_{i<j}^{q}\\beta_{ij}x_i x_j + \\sum_{i<j<k}^{q}\\beta_{ijk}x_i x_j x_k + ... + \\varepsilon$$
            
            This model is different from standard factorial models as it does not include an intercept term, and the interpretation of linear terms differs.
            """)

def factorial_design_matrix(factors, design_type="full", resolution=None):
    """
    Generate a factorial design matrix.
    
    Parameters:
    -----------
    factors : list
        List of factor names
    design_type : str
        'full' for full factorial or 'fractional' for fractional factorial
    resolution : int
        Resolution for fractional factorial design (3, 4, or 5)
        
    Returns:
    --------
    design_df : pandas DataFrame
        Design matrix with factors and interaction columns
    """
    num_factors = len(factors)
    
    if design_type == "full":
        # Full factorial design
        runs = 2**num_factors
        
        # Create basic design in coded units (-1, 1)
        design = np.zeros((runs, num_factors))
        
        for i in range(num_factors):
            # Pattern of -1, 1 with appropriate frequency
            pattern_length = 2**(num_factors - i - 1)
            pattern = np.array([-1] * pattern_length + [1] * pattern_length)
            # Repeat pattern to fill the column
            repeats = runs // (2 * pattern_length)
            design[:, i] = np.tile(pattern, repeats)
            
    elif design_type == "fractional":
        if resolution is None:
            resolution = 3  # Default to Resolution III
            
        # Determine number of runs based on resolution
        if resolution == 3:
            p = num_factors - int(np.ceil(np.log2(num_factors + 1)))
        elif resolution == 4:
            p = num_factors - int(np.ceil(np.log2(2*num_factors + 1)))
        elif resolution == 5:
            p = num_factors - int(np.ceil(np.log2(num_factors**2)))
        else:
            raise ValueError("Resolution must be 3, 4, or 5")
            
        p = max(0, min(p, num_factors-1))  # Ensure p is valid
        
        # Number of base factors
        base_factors = num_factors - p
        runs = 2**base_factors
        
        # Create base design for independent factors
        design = np.zeros((runs, num_factors))
        
        for i in range(base_factors):
            pattern_length = 2**(base_factors - i - 1)
            pattern = np.array([-1] * pattern_length + [1] * pattern_length)
            repeats = runs // (2 * pattern_length)
            design[:, i] = np.tile(pattern, repeats)
            
        # Generate additional factors based on resolution
        for i in range(p):
            idx = base_factors + i
            
            if resolution == 3:
                # Resolution III: confound with 2-factor interaction
                design[:, idx] = design[:, 0] * design[:, i+1]
            elif resolution == 4:
                # Resolution IV: confound with 3-factor interaction
                if i+2 < base_factors:
                    design[:, idx] = design[:, 0] * design[:, i+1] * design[:, i+2]
                else:
                    design[:, idx] = design[:, 0] * design[:, 1] * design[:, 2]
            elif resolution == 5:
                # Resolution V: confound with 4-factor interaction
                if i+3 < base_factors:
                    design[:, idx] = design[:, 0] * design[:, i+1] * design[:, i+2] * design[:, i+3]
                else:
                    design[:, idx] = design[:, 0] * design[:, 1] * design[:, 2] * design[:, 3]
    
    # Create DataFrame with factor names
    design_df = pd.DataFrame(design, columns=factors)
    
    # Add interaction columns for visualization
    if num_factors > 1:
        # Add 2-factor interactions
        for i, j in combinations(range(num_factors), 2):
            interaction_name = f"{factors[i]}×{factors[j]}"
            design_df[interaction_name] = design_df[factors[i]] * design_df[factors[j]]
    
    if num_factors > 2:
        # Add select 3-factor interactions for demonstration
        for i, j, k in combinations(range(min(num_factors, 4)), 3):
            interaction_name = f"{factors[i]}×{factors[j]}×{factors[k]}"
            design_df[interaction_name] = design_df[factors[i]] * design_df[factors[j]] * design_df[factors[k]]
    
    # Add run order and std_order
    design_df.insert(0, 'StdOrder', range(1, runs+1))
    
    return design_df

def calculate_design_properties(design_df):
    """
    Calculate properties of the design matrix.
    
    Parameters:
    -----------
    design_df : pandas DataFrame
        Design matrix
    
    Returns:
    --------
    properties : dict
        Dictionary of design properties
    """
    # Remove StdOrder column from calculations
    if 'StdOrder' in design_df.columns:
        X = design_df.drop(columns=['StdOrder'])
    else:
        X = design_df.copy()
    
    # Number of runs and factors
    n_runs = X.shape[0]
    n_terms = X.shape[1]
    
    # Factor names (excluding interaction terms)
    factor_names = [col for col in X.columns if '×' not in col]
    n_factors = len(factor_names)
    
    # Interaction terms
    interaction_terms = [col for col in X.columns if '×' in col]
    
    # Design matrix properties
    X_array = X.values
    XtX = X_array.T @ X_array
    
    # Check orthogonality
    is_orthogonal = np.allclose(XtX, n_runs * np.eye(n_terms))
    
    # Calculate correlation matrix
    corr_matrix = np.corrcoef(X_array.T)
    
    # Calculate design efficiency
    try:
        # D-optimality criterion
        det_XtX = np.linalg.det(XtX)
        if det_XtX > 0:
            d_eff = (det_XtX / n_runs**n_terms)**(1/n_terms) * 100
        else:
            d_eff = 0
    except:
        d_eff = 0
    
    # Maximum absolute correlation between factors and 2FI
    max_corr = 0
    if len(factor_names) > 1 and len(interaction_terms) > 0:
        # Get factor indices
        factor_indices = [list(X.columns).index(name) for name in factor_names]
        # Get 2FI indices
        twoway_indices = [list(X.columns).index(name) for name in interaction_terms if name.count('×') == 1]
        
        if twoway_indices:
            # Calculate max absolute correlation between factors and 2FI
            for i in factor_indices:
                for j in twoway_indices:
                    if abs(corr_matrix[i, j]) > max_corr:
                        max_corr = abs(corr_matrix[i, j])
    
    # Calculate aliasing structure (simplified)
    aliasing = {}
    if not is_orthogonal:
        threshold = 0.5  # Correlation threshold for aliasing
        for i, col1 in enumerate(X.columns):
            aliases = []
            for j, col2 in enumerate(X.columns):
                if i != j and abs(corr_matrix[i, j]) > threshold:
                    aliases.append((col2, corr_matrix[i, j]))
            if aliases:
                aliasing[col1] = aliases
    
    return {
        "runs": n_runs,
        "factors": n_factors,
        "terms": n_terms,
        "orthogonal": is_orthogonal,
        "d_efficiency": d_eff,
        "max_correlation": max_corr,
        "correlation_matrix": corr_matrix,
        "aliasing": aliasing,
        "column_names": list(X.columns)
    }

def design_matrix_visualization():
    st.header("Interactive Design Matrix Visualization")
    
    st.markdown("""
    This tool helps you visualize and understand factorial design matrices and their properties.
    Explore how different design choices affect the information content and efficiency of your experiments.
    """)
    
    # Design setup
    st.subheader("Design Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_factors = st.slider("Number of Factors", 2, 6, 3, 
                               help="Number of independent variables in your experiment")
        
        design_type = st.radio("Design Type", 
                             ["Full Factorial", "Fractional Factorial"],
                             help="Full factorial includes all possible combinations. Fractional factorial uses a subset.")
    
    with col2:
        # Default biotechnology factor names
        default_factors = ["Temperature", "pH", "Stirring", "Nutrient", "Oxygen", "Inducer"]
        
        # Allow user to customize factor names
        factor_names = []
        for i in range(num_factors):
            default_name = default_factors[i] if i < len(default_factors) else f"Factor {i+1}"
            factor_name = st.text_input(f"Factor {i+1} Name", default_name, key=f"factor_{i}")
            factor_names.append(factor_name)
        
    # Additional options for fractional factorial
    if design_type == "Fractional Factorial":
        resolution = st.radio("Design Resolution", 
                            ["III", "IV", "V"], 
                            index=1,
                            help="""Resolution determines confounding patterns:
                            - III: Main effects not confounded with each other
                            - IV: Main effects not confounded with 2-factor interactions
                            - V: 2-factor interactions not confounded with each other""")
        
        resolution_map = {"III": 3, "IV": 4, "V": 5}
        resolution_num = resolution_map[resolution]
    else:
        resolution_num = None
    
    # Generate design matrix
    design_type_lower = design_type.split()[0].lower()
    design_df = factorial_design_matrix(factor_names, design_type_lower, resolution_num)
    
    # Calculate design properties
    properties = calculate_design_properties(design_df)
    
    # Display design matrix with styling
    st.subheader("Design Matrix (Coded Units)")
    
    # Convert -1 and 1 to Low and High for better readability
    display_df = design_df.copy()
    # Only convert factor columns, not interaction terms
    for col in factor_names:
        display_df[col] = display_df[col].map({-1: "Low", 1: "High"})
    
    # Format for display
    st.dataframe(display_df)
    
    # Add download button for the design
    csv = design_df.to_csv(index=False)
    st.download_button(
        label="Download Design Matrix (CSV)",
        data=csv,
        file_name="factorial_design.csv",
        mime="text/csv"
    )
    
    # Visualize design properties
    st.subheader("Design Properties")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Number of Runs", properties["runs"])
    
    with col2:
        orthogonality = "Yes" if properties["orthogonal"] else "No"
        st.metric("Orthogonal Design", orthogonality)
    
    with col3:
        st.metric("D-Efficiency (%)", f"{properties['d_efficiency']:.1f}")
    
    # Correlation heatmap
    st.subheader("Correlation Matrix")
    
    fig = go.Figure(data=go.Heatmap(
        z=properties["correlation_matrix"],
        x=properties["column_names"],
        y=properties["column_names"],
        colorscale='RdBu_r',
        zmin=-1, zmax=1,
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        height=500,
        width=700,
        title="Term Correlations (Orthogonal Design = No Correlation)",
        xaxis=dict(tickangle=-45),
    )
    
    st.plotly_chart(fig)
    
    # Display aliasing structure if present
    if properties["aliasing"]:
        st.subheader("Aliasing Structure")
        st.markdown("The following terms are partially confounded:")
        
        for term, aliases in properties["aliasing"].items():
            alias_str = ", ".join([f"{alias[0]} (r={alias[1]:.2f})" for alias in aliases])
            st.markdown(f"- **{term}** is aliased with: {alias_str}")
    
    # Information about design properties
    with st.expander("Design Matrix Interpretation"):
        st.markdown("""
        ### Understanding the Design Matrix
        
        The design matrix represents your experimental plan with each row being an experimental run and each column a factor or interaction term.
        
        **Key Properties:**
        
        1. **Orthogonality**: In an orthogonal design, all factors and interactions are uncorrelated, making effect estimates independent. This maximizes statistical efficiency.
        
        2. **D-Efficiency**: Measures the quality of the design relative to an ideal orthogonal design (100% = perfect).
        
        3. **Aliasing/Confounding**: When effects are mixed together and cannot be estimated separately. In fractional designs, aliasing is inevitable but can be managed.
        
        4. **Resolution**: Indicates what types of effects are confounded:
           - Resolution III: Main effects can be confounded with 2-factor interactions
           - Resolution IV: Main effects are clear but 2-factor interactions may be confounded with each other
           - Resolution V: Both main effects and 2-factor interactions are clear
        
        ### Biotechnology Application
        
        In bioprocess development, orthogonal designs help isolate the effects of critical parameters like temperature, pH, and nutrient concentration. Higher resolution designs are important when interactions are expected, as is common in biological systems where, for example, temperature and pH often interact to affect enzyme activity or cell growth.
        """)

if __name__ == "__main__":
    show()