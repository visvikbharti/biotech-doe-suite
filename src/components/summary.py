import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import base64
import io
from datetime import datetime
import json

def show():
    st.header("Summary and Integration with StickForStats")
    
    # Content from section7-summary artifact
    st.markdown("""
    ## Consolidating DOE Mastery

    Throughout this module, we've explored the structured approach to designing, executing, analyzing, and interpreting experiments in biotechnology contexts. Design of Experiments represents a cornerstone of modern bioprocess development, enabling efficient exploration of complex biological systems while extracting maximum information from limited experimental resources.

    ## Key Principles Revisited

    ### Foundational Elements
    **Concept Anchor**: Design of Experiments fundamentally transforms experimental approaches from reactive trial-and-error to proactive, structured knowledge building.

    **Practical Lens**: In biotechnology applications, where experiments are often resource-intensive and time-consuming, DOE provides a systematic framework that accelerates development, reduces costs, and yields deeper system understanding.

    The key principles that underpin effective experimental design in biotechnology include:

    1. **Randomization**: Distributes uncontrolled variation randomly across conditions, protecting against systematic bias from temporal effects, equipment variations, or operator differences that are common in bioprocessing.

    2. **Replication**: Provides estimates of experimental error and increases precision, essential when dealing with inherently variable biological systems.

    3. **Blocking**: Controls for known sources of variation that cannot be eliminated, such as different cell passages, reagent lots, or equipment units.

    4. **Orthogonality**: Allows independent estimation of effects, enabling clear attribution of responses to specific factors or interactions.

    5. **Effect Sparsity**: Recognizes that most systems are dominated by a relatively small number of main effects and lower-order interactions, allowing efficient screening and characterization.

    ### Design Selection Strategy
    **Concept Anchor**: The experimental objective dictates design selection, with different designs optimized for screening, characterization, optimization, or robustness testing.

    **Practical Lens**: Bioprocess development follows a logical progression from screening many potential factors to detailed characterization of critical parameters to optimization of operating conditions, each stage requiring appropriate design types:

    1. **Screening Designs** (Plackett-Burman, Fractional Factorial, Definitive Screening):
       - Efficiently identify significant factors from many candidates
       - Particularly valuable in early development for media components, culture conditions, or purification parameters

    2. **Characterization Designs** (Full Factorial, High-Resolution Fractional Factorial):
       - Provide detailed understanding of main effects and interactions
       - Essential for regulatory submissions requiring thorough process understanding

    3. **Optimization Designs** (Central Composite, Box-Behnken, Mixture Designs):
       - Map response surfaces to identify optimal operating conditions
       - Critical for maximizing yield, purity, or stability in bioprocesses

    4. **Robustness Designs** (Split-Plot, Optimal Designs):
       - Assess process sensitivity to variations and define control strategies
       - Support process validation and technology transfer activities

    ### Analysis and Interpretation Framework
    **Concept Anchor**: Statistical analysis transforms experimental data into actionable insights through a structured framework of effect estimation, significance testing, model building, and diagnostic verification.

    **Practical Lens**: In biotechnology applications, where decisions have significant commercial and patient implications, rigorous analysis ensures reliable conclusions and defensible claims.

    The comprehensive analytical approach includes:

    1. **Effect Estimation and Significance Testing**:
       - Quantifies factor impacts and identifies critical process parameters
       - Informs control strategies and resource allocation

    2. **Model Building and Validation**:
       - Creates predictive models enabling interpolation across design space
       - Supports process understanding and optimization efforts

    3. **Response Surface Analysis**:
       - Maps the relationship between factors and responses across the experimental space
       - Enables identification of optimal operating conditions and trade-offs

    4. **Design Space Characterization**:
       - Defines the multidimensional combination of variables yielding acceptable quality
       - Supports regulatory filings and provides operational flexibility
    """)
    
    st.markdown("""
    ## Integration with StickForStats Platform

    ### Extending Statistical Capabilities
    **Concept Anchor**: The DOE module serves as a specialized component within the broader StickForStats ecosystem, leveraging core statistical capabilities while adding domain-specific experimental design functionality.

    **Practical Lens**: For biotechnology researchers and engineers, this integration provides a seamless workflow from experimental planning through analysis to process implementation and monitoring.
    """)
    
    # Integration demo
    st.subheader("StickForStats DOE Integration Demo")
    doe_integration_demo()
    
    st.markdown("""
    ### Future Directions

    #### 1. Machine Learning Integration
    Combining DOE with machine learning approaches:
    - **Sequential Learning Designs**: Experiments that adaptively update based on previous results
    - **Bayesian Optimization**: Prior knowledge incorporation into experimental planning
    - **Model-Based Exploration**: Using predictive models to guide experimental focus
    - **Feature Selection**: Advanced methods for identifying critical parameters

    #### 2. High-Throughput Applications
    Supporting miniaturized and parallelized experimentation:
    - **Microbioreactor Arrays**: Designs optimized for highly parallelized systems
    - **Microfluidic Platforms**: Specialized designs for continuous flow systems
    - **Automated Execution**: Integration with laboratory automation systems
    - **Real-Time Analysis**: Processing streaming data during experiment execution

    #### 3. Process Analytical Technology
    Connecting DOE with PAT initiatives:
    - **Multivariate Sensor Integration**: Incorporating spectroscopic and other advanced measurements
    - **Real-Time Process Modeling**: Updating models with continuous data streams
    - **Feedback Control Optimization**: Designs for advanced control strategy development
    - **Digital Twin Development**: Using DOE to build and validate digital process models

    #### 4. Regulatory Science
    Advancing regulatory applications of DOE:
    - **Quality by Design Implementation**: Standardized approaches for design space definition
    - **Continuous Verification**: Experimental designs for ongoing process verification
    - **Accelerated Development**: Efficient experimental strategies for expedited programs
    - **Post-Approval Changes**: Risk-based experimental approaches for process changes

    ## Final Thoughts

    Design of Experiments represents a powerful methodology that transforms biotechnology research and development from art to science. By providing a structured approach to experimentation, DOE enables deeper understanding, more efficient resource utilization, and accelerated development timelines.

    The integration of DOE capabilities within the StickForStats platform creates a comprehensive toolkit for biotechnology professionals, spanning experimental design, data analysis, visualization, and implementation. This unified approach supports the entire product lifecycle from early development through commercialization and continuous improvement.

    As you apply these methods to your own biotechnology challenges, remember that the greatest value comes not just from the statistical rigor, but from the scientific insights that emerge when systematic experimentation is combined with domain knowledge and critical thinking. The tools and techniques presented in this module provide the foundation for that journey of discovery and optimization.
    """)

def doe_integration_demo():
    st.markdown("""
    This interactive demonstration shows how the DOE module integrates with the broader 
    StickForStats platform, providing a seamless workflow from experimental design 
    through analysis to process implementation.
    """)
    
    # Main navigation tabs
    tabs = st.tabs([
        "Overview", 
        "Design Creation", 
        "Data Analysis",
        "Integration Features",
        "Export & Report"
    ])
    
    # Tab 1: Overview
    with tabs[0]:
        st.subheader("DOE Module Integration")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            The DOE module extends StickForStats with specialized experimental design capabilities 
            while leveraging the platform's core statistical and visualization features. This integration 
            provides a comprehensive toolkit for biotechnology researchers and engineers.
            
            ### Key Integration Points
            
            1. **Data Flow Integration**
               - Seamless transfer of designs and results
               - Consistent data structures and formats
               - Version tracking and experiment history
            
            2. **Statistical Analysis Pipeline**
               - Connected analysis workflows
               - Shared statistical methods and tests
               - Unified modeling approaches
            
            3. **Visualization Framework**
               - Common plotting libraries and styles
               - Interactive visualization capabilities
               - Customizable reporting outputs
            
            4. **User Experience**
               - Consistent interface across modules
               - Shared project management
               - Unified documentation and help
            """)
        
        with col2:
            # Simple diagram showing integration
            st.markdown("""
            ```
            ┌───────────────────────┐
            │    StickForStats      │
            │    Core Platform      │
            └───────────┬───────────┘
                        │
                ┌───────┴───────┐
                │               │
            ┌───▼───┐       ┌───▼───┐
            │  DOE  │◄─────►│ Other │
            │ Module│       │Modules│
            └───┬───┘       └───────┘
                │
           ┌────┴─────┐
           │ Biotech  │
           │ Projects │
           └──────────┘
            ```
            
            ### Supported Applications
            
            - **Process Development**
            - **Analytical Methods**
            - **Formulation Design**
            - **Technology Transfer**
            - **Product Characterization**
            - **Stability Studies**
            - **Process Validation**
            """)
        
        # Demo dataset selector
        st.markdown("### Explore with Example Dataset")
        
        dataset_options = {
            "Protein Expression Optimization": {
                "description": "A factorial experiment studying effects of temperature, pH, and inducer concentration on protein expression in E. coli.",
                "design_type": "Full Factorial",
                "use_case": "Process Development"
            },
            "Chromatography Method Development": {
                "description": "A response surface design optimizing mobile phase composition, flow rate, and column temperature for protein separation.",
                "design_type": "Central Composite",
                "use_case": "Analytical Method Development"
            },
            "Vaccine Formulation Stability": {
                "description": "A screening design evaluating formulation components' effects on vaccine stability under various storage conditions.",
                "design_type": "Fractional Factorial",
                "use_case": "Formulation Development"
            }
        }
        
        selected_dataset = st.selectbox(
            "Select Example Dataset",
            list(dataset_options.keys())
        )
        
        st.info(f"**{dataset_options[selected_dataset]['design_type']}:** {dataset_options[selected_dataset]['description']}")
        
        # Initialize session state for the selected dataset
        if 'dataset' not in st.session_state or st.session_state.dataset_name != selected_dataset:
            st.session_state.dataset_name = selected_dataset
            
            # Generate dataset based on selection
            if selected_dataset == "Protein Expression Optimization":
                # Create 2³ factorial design for protein expression
                factors = ["Temperature", "pH", "Inducer"]
                factor_levels = {
                    "Temperature": [30, 37],  # °C
                    "pH": [6.5, 7.5],
                    "Inducer": [0.1, 1.0]     # mM IPTG
                }
                
                # Generate full factorial design
                design_matrix = []
                for temp in factor_levels["Temperature"]:
                    for ph in factor_levels["pH"]:
                        for inducer in factor_levels["Inducer"]:
                            design_matrix.append([temp, ph, inducer])
                
                # Create design dataframe
                design_df = pd.DataFrame(design_matrix, columns=factors)
                
                # Add coded values (-1, +1)
                for factor in factors:
                    low, high = factor_levels[factor]
                    design_df[f"{factor}_coded"] = design_df[factor].map({low: -1, high: 1})
                
                # Add run order and std order
                runs = len(design_df)
                design_df.insert(0, "RunOrder", np.random.permutation(runs) + 1)
                design_df.insert(1, "StdOrder", range(1, runs + 1))
                
                # Generate response data with known effects and some noise
                # Protein Yield: Positive effects for Temperature, Inducer, and Temp*Inducer interaction
                base_yield = 500
                temp_effect = 150
                ph_effect = -30
                inducer_effect = 200
                temp_inducer_effect = 100
                
                # Generate responses
                design_df["Protein_Yield"] = (base_yield + 
                                           temp_effect * design_df["Temperature_coded"] + 
                                           ph_effect * design_df["pH_coded"] + 
                                           inducer_effect * design_df["Inducer_coded"] + 
                                           temp_inducer_effect * design_df["Temperature_coded"] * design_df["Inducer_coded"] + 
                                           np.random.normal(0, 25, runs))
                
                design_df["Cell_Density"] = 5.0 + 0.8 * design_df["pH_coded"] - 1.2 * design_df["Inducer_coded"] + np.random.normal(0, 0.2, runs)
                design_df["Purity"] = 90 + 3 * design_df["Temperature_coded"] + 2 * design_df["pH_coded"] + np.random.normal(0, 1, runs)
                
                # Add center points
                center_points = pd.DataFrame({
                    "RunOrder": [runs + i + 1 for i in range(3)],
                    "StdOrder": [runs + i + 1 for i in range(3)],
                    "Temperature": [33.5] * 3,
                    "pH": [7.0] * 3,
                    "Inducer": [0.55] * 3,
                    "Temperature_coded": [0] * 3,
                    "pH_coded": [0] * 3,
                    "Inducer_coded": [0] * 3,
                    "Protein_Yield": [base_yield + np.random.normal(0, 20) for _ in range(3)],
                    "Cell_Density": [5.0 + np.random.normal(0, 0.15) for _ in range(3)],
                    "Purity": [90 + np.random.normal(0, 0.8) for _ in range(3)]
                })
                
                design_df = pd.concat([design_df, center_points], ignore_index=True)
                
                # Set metadata
                metadata = {
                    "design_type": "Full Factorial with Center Points",
                    "factors": factors,
                    "responses": ["Protein_Yield", "Cell_Density", "Purity"],
                    "factor_levels": factor_levels,
                    "center_points": 3,
                    "replicates": 1,
                    "creation_date": datetime.now().strftime("%Y-%m-%d"),
                    "created_by": "StickForStats DOE Module",
                    "project": "Recombinant Protein Process Development",
                    "notes": "Example dataset for demonstration purposes"
                }
                
                st.session_state.design_df = design_df
                st.session_state.metadata = metadata
            
            elif selected_dataset == "Chromatography Method Development":
                # Create central composite design for chromatography
                factors = ["pH", "Salt", "Temperature"]
                factor_ranges = {
                    "pH": [6.0, 8.0],         # Buffer pH
                    "Salt": [100, 500],       # mM NaCl
                    "Temperature": [20, 40]    # °C
                }
                
                # Factorial points
                factorial_points = np.array([
                    [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
                    [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]
                ])
                
                # Axial points (alpha = 1.682 for rotatable design)
                alpha = 1.682
                axial_points = np.array([
                    [-alpha, 0, 0], [alpha, 0, 0],
                    [0, -alpha, 0], [0, alpha, 0],
                    [0, 0, -alpha], [0, 0, alpha]
                ])
                
                # Center points
                center_points = np.array([[0, 0, 0]] * 6)
                
                # Combine all points
                design_matrix = np.vstack([factorial_points, axial_points, center_points])
                
                # Create dataframe with coded values
                coded_df = pd.DataFrame(design_matrix, columns=[f"{factor}_coded" for factor in factors])
                
                # Convert coded to actual values
                design_df = pd.DataFrame()
                for factor in factors:
                    low, high = factor_ranges[factor]
                    mid = (low + high) / 2
                    half_range = (high - low) / 2
                    design_df[factor] = mid + half_range * coded_df[f"{factor}_coded"]
                
                # Add coded columns
                for factor in factors:
                    design_df[f"{factor}_coded"] = coded_df[f"{factor}_coded"]
                
                # Add run order and std order
                runs = len(design_df)
                design_df.insert(0, "RunOrder", np.random.permutation(runs) + 1)
                design_df.insert(1, "StdOrder", range(1, runs + 1))
                
                # Generate response data with quadratic effects
                # Define coded variables for response generation
                x1 = coded_df["pH_coded"]
                x2 = coded_df["Salt_coded"]
                x3 = coded_df["Temperature_coded"]
                
                # Resolution: Optimal at pH 7.0, decreases with Salt, quadratic with Temperature
                design_df["Resolution"] = 2.5 - 0.3 * x2 - 0.5 * x1**2 - 0.2 * x2**2 - 0.7 * x3**2 - 0.2 * x1 * x2 + np.random.normal(0, 0.1, runs)
                
                # Retention Time: Affected by pH and Temperature with interaction
                design_df["Retention_Time"] = 5.0 - 0.8 * x1 + 0.5 * x3 - 0.3 * x1 * x3 + 0.2 * x1**2 + np.random.normal(0, 0.2, runs)
                
                # Peak Area: Mostly affected by Salt and Temperature
                design_df["Peak_Area"] = 150000 + 20000 * x2 - 5000 * x3 - 10000 * x2 * x3 - 8000 * x2**2 + np.random.normal(0, 5000, runs)
                
                # Set metadata
                metadata = {
                    "design_type": "Central Composite Design",
                    "factors": factors,
                    "responses": ["Resolution", "Retention_Time", "Peak_Area"],
                    "factor_ranges": factor_ranges,
                    "alpha": alpha,
                    "center_points": 6,
                    "creation_date": datetime.now().strftime("%Y-%m-%d"),
                    "created_by": "StickForStats DOE Module",
                    "project": "Protein Chromatography Method Development",
                    "notes": "Example dataset for demonstration purposes"
                }
                
                st.session_state.design_df = design_df
                st.session_state.metadata = metadata
            
            elif selected_dataset == "Vaccine Formulation Stability":
                # Create fractional factorial design for vaccine formulation
                factors = ["Antigen", "Adjuvant", "Buffer", "pH", "Preservative"]
                factor_levels = {
                    "Antigen": [50, 100],      # µg/mL
                    "Adjuvant": [0.5, 2.0],    # mg/mL
                    "Buffer": ["Phosphate", "Tris"],
                    "pH": [6.5, 7.5],
                    "Preservative": [0.01, 0.05]  # % w/v
                }
                
                # Create fractional factorial design (2^5-1)
                # Use Resolution V design (I = ABCDE)
                runs = 16
                
                # Create base design (2^4)
                base_design = np.zeros((runs, 4))
                for i in range(runs):
                    for j in range(4):
                        base_design[i, j] = 1 if (i // 2**(4-j-1)) % 2 else -1
                
                # Create design matrix with the fifth factor as interaction of the others
                design_matrix = np.zeros((runs, 5))
                design_matrix[:, :4] = base_design
                # Fifth factor is the product of the other four (Resolution V)
                design_matrix[:, 4] = base_design[:, 0] * base_design[:, 1] * base_design[:, 2] * base_design[:, 3]
                
                # Create dataframe with coded values
                coded_df = pd.DataFrame(design_matrix, columns=[f"{factor}_coded" for factor in factors])
                
                # Create design dataframe
                design_df = pd.DataFrame()
                
                # Convert coded to actual values
                for i, factor in enumerate(factors):
                    if factor == "Buffer":
                        # Categorical factor
                        design_df[factor] = coded_df[f"{factor}_coded"].map({-1: "Phosphate", 1: "Tris"})
                    else:
                        # Numerical factor
                        low, high = factor_levels[factor]
                        design_df[factor] = low + (coded_df[f"{factor}_coded"] + 1) * (high - low) / 2
                
                # Add coded columns
                for factor in factors:
                    design_df[f"{factor}_coded"] = coded_df[f"{factor}_coded"]
                
                # Add run order and std order
                design_df.insert(0, "RunOrder", np.random.permutation(runs) + 1)
                design_df.insert(1, "StdOrder", range(1, runs + 1))
                
                # Generate response data
                x1 = coded_df["Antigen_coded"]
                x2 = coded_df["Adjuvant_coded"]
                x3 = coded_df["Buffer_coded"]
                x4 = coded_df["pH_coded"]
                x5 = coded_df["Preservative_coded"]
                
                # Potency: Affected by Antigen, Adjuvant, and their interaction
                design_df["Potency"] = 100 + 15 * x1 + 25 * x2 + 8 * x1 * x2 - 5 * x3 + np.random.normal(0, 3, runs)
                
                # Stability_4C: Long-term stability at 4°C (weeks)
                design_df["Stability_4C"] = 52 - 6 * x5 - 4 * x3 + 8 * x4 - 3 * x3 * x4 + np.random.normal(0, 2, runs)
                
                # Stability_25C: Accelerated stability at 25°C (weeks)
                design_df["Stability_25C"] = 12 - 2 * x5 - 3 * x3 + 4 * x4 - 1 * x1 + np.random.normal(0, 1, runs)
                
                # Add center points
                center_points = pd.DataFrame({
                    "RunOrder": [runs + i + 1 for i in range(3)],
                    "StdOrder": [runs + i + 1 for i in range(3)],
                    "Antigen": [75] * 3,
                    "Adjuvant": [1.25] * 3,
                    "Buffer": ["Mixed"] * 3,  # Special center point for categorical
                    "pH": [7.0] * 3,
                    "Preservative": [0.03] * 3,
                    "Antigen_coded": [0] * 3,
                    "Adjuvant_coded": [0] * 3,
                    "Buffer_coded": [0] * 3,
                    "pH_coded": [0] * 3,
                    "Preservative_coded": [0] * 3,
                    "Potency": [100 + np.random.normal(0, 3) for _ in range(3)],
                    "Stability_4C": [52 + np.random.normal(0, 2) for _ in range(3)],
                    "Stability_25C": [12 + np.random.normal(0, 1) for _ in range(3)]
                })
                
                design_df = pd.concat([design_df, center_points], ignore_index=True)
                
                # Set metadata
                metadata = {
                    "design_type": "Fractional Factorial Design (Resolution V)",
                    "factors": factors,
                    "responses": ["Potency", "Stability_4C", "Stability_25C"],
                    "factor_levels": factor_levels,
                    "center_points": 3,
                    "creation_date": datetime.now().strftime("%Y-%m-%d"),
                    "created_by": "StickForStats DOE Module",
                    "project": "Vaccine Formulation Development",
                    "notes": "Example dataset for demonstration purposes"
                }
                
                st.session_state.design_df = design_df
                st.session_state.metadata = metadata
    
    # Tab 2: Design Creation
    with tabs[1]:
        st.subheader("Integrated Design Creation")
        
        if 'design_df' in st.session_state:
            # Display the design summary
            st.markdown("### Design Matrix")
            st.dataframe(st.session_state.design_df.head())
            
            # Design visualization
            st.markdown("### Design Visualization")
            
            if 'metadata' in st.session_state:
                factors = st.session_state.metadata["factors"]
                if len(factors) >= 2:
                    selected_factors = st.multiselect(
                        "Select factors to visualize (max 2)",
                        factors,
                        default=factors[:2]
                    )
                    
                    if len(selected_factors) == 2:
                        # Create design space plot
                        df = st.session_state.design_df
                        
                        fig = px.scatter(
                            df, 
                            x=selected_factors[0], 
                            y=selected_factors[1],
                            color="StdOrder",
                            hover_data=["RunOrder"],
                            title=f"Design Points in {selected_factors[0]} vs {selected_factors[1]} Space"
                        )
                        
                        # Add center points if present
                        if "metadata" in st.session_state and "center_points" in st.session_state.metadata:
                            center_points = st.session_state.metadata["center_points"]
                            if center_points > 0:
                                # Identify center points (typically the last few runs)
                                n = len(df)
                                center_indices = range(n - center_points, n)
                                center_df = df.iloc[center_indices]
                                
                                fig.add_trace(
                                    go.Scatter(
                                        x=center_df[selected_factors[0]],
                                        y=center_df[selected_factors[1]],
                                        mode='markers',
                                        marker=dict(
                                            color='red',
                                            size=12,
                                            symbol='star',
                                            line=dict(color='black', width=1)
                                        ),
                                        name='Center Points'
                                    )
                                )
                        
                        st.plotly_chart(fig)
                    
                    elif len(selected_factors) == 1:
                        # Create one-factor design visualization
                        df = st.session_state.design_df
                        
                        fig = px.box(
                            df,
                            x=selected_factors[0],
                            title=f"Distribution of {selected_factors[0]} Levels"
                        )
                        
                        st.plotly_chart(fig)
                
                # Display design properties
                st.markdown("### Design Properties")
                
                metadata = st.session_state.metadata
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Design Type", metadata["design_type"])
                with col2:
                    st.metric("Number of Factors", len(metadata["factors"]))
                with col3:
                    st.metric("Number of Runs", len(st.session_state.design_df))
                
                st.markdown("**Design Metadata:**")
                for key, value in metadata.items():
                    if key not in ["design_type", "factors", "responses", "factor_levels"]:
                        st.write(f"- **{key.replace('_', ' ').title()}:** {value}")
                
                # Export options
                st.markdown("### Export Design")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Export as CSV"):
                        # Set up file download
                        csv = st.session_state.design_df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="design_matrix.csv">Download CSV File</a>'
                        st.markdown(href, unsafe_allow_html=True)
                
                with col2:
                    if st.button("Export as JSON"):
                        # Combine design matrix and metadata
                        export_data = {
                            "metadata": metadata,
                            "design_matrix": st.session_state.design_df.to_dict('records')
                        }
                        
                        json_str = json.dumps(export_data, indent=2)
                        b64 = base64.b64encode(json_str.encode()).decode()
                        href = f'<a href="data:file/json;base64,{b64}" download="design_data.json">Download JSON File</a>'
                        st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("Please select a dataset in the Overview tab to continue.")
    
    # Tab 3: Data Analysis
    with tabs[2]:
        st.subheader("Integrated Data Analysis")
        
        if 'design_df' in st.session_state and 'metadata' in st.session_state:
            # Get dataset and metadata
            df = st.session_state.design_df
            metadata = st.session_state.metadata
            
            # Select response for analysis
            response = st.selectbox(
                "Select Response Variable for Analysis",
                metadata["responses"]
            )
            
            # Analysis options
            analysis_type = st.radio(
                "Select Analysis Type",
                ["Effect Estimation", "ANOVA", "Response Surface", "Diagnostic Plots"]
            )
            
            # Perform analysis based on selection
            if analysis_type == "Effect Estimation":
                st.markdown("### Effect Estimation")
                
                # Get factors and coded factors
                factors = metadata["factors"]
                coded_factors = [f"{factor}_coded" for factor in factors]
                
                # Create model formula
                formula_terms = [f"{factor}_coded" for factor in factors]
                
                # Add interaction terms
                include_interactions = st.checkbox("Include 2-factor interactions", value=True)
                if include_interactions and len(factors) >= 2:
                    for i, j in combinations(range(len(factors)), 2):
                        formula_terms.append(f"{coded_factors[i]}:{coded_factors[j]}")
                
                # Add squared terms for response surface designs
                if metadata["design_type"] in ["Central Composite Design", "Box-Behnken Design"]:
                    include_squared = st.checkbox("Include squared terms", value=True)
                    if include_squared:
                        for factor in coded_factors:
                            formula_terms.append(f"I({factor}**2)")
                
                # Create formula
                formula = f"{response} ~ {' + '.join(formula_terms)}"
                
                st.code(formula, language="python")
                
                # Fit model
                try:
                    model = ols(formula, data=df).fit()
                    
                    # Display summary
                    st.markdown("### Model Summary")
                    
                    # Create custom summary table
                    summary_df = pd.DataFrame({
                        'Coefficient': model.params,
                        'Std Error': model.bse,
                        't-value': model.tvalues,
                        'p-value': model.pvalues
                    })
                    
                    # Calculate effects from coefficients (effect = 2 * coefficient for coded variables)
                    effects = summary_df['Coefficient'] * 2
                    effects.iloc[0] = summary_df['Coefficient'].iloc[0]  # Intercept is not multiplied
                    summary_df['Effect'] = effects
                    
                    # Reorder columns
                    summary_df = summary_df[['Effect', 'Coefficient', 'Std Error', 't-value', 'p-value']]
                    
                    # Display summary
                    st.dataframe(summary_df.style.format({
                        'Effect': '{:.4f}',
                        'Coefficient': '{:.4f}',
                        'Std Error': '{:.4f}',
                        't-value': '{:.3f}',
                        'p-value': '{:.4f}'
                    }).background_gradient(subset=['p-value'], cmap='Reds_r'))
                    
                    # Display model statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("R² Value", f"{model.rsquared:.4f}")
                    with col2:
                        st.metric("Adjusted R²", f"{model.rsquared_adj:.4f}")
                    with col3:
                        st.metric("F-statistic p-value", f"{model.f_pvalue:.4g}")
                    
                    # Create Pareto chart of effects
                    effect_df = summary_df.iloc[1:].copy()  # Skip intercept
                    effect_df['Absolute Effect'] = effect_df['Effect'].abs()
                    effect_df = effect_df.sort_values('Absolute Effect', ascending=False)
                    
                    fig = px.bar(
                        effect_df,
                        y=effect_df.index,
                        x='Absolute Effect',
                        orientation='h',
                        title="Pareto Chart of Effects",
                        color='p-value',
                        color_continuous_scale='Viridis_r'
                    )
                    
                    # Add significance line
                    alpha = 0.05
                    t_crit = stats.t.ppf(1-alpha/2, model.df_resid)
                    se = summary_df['Std Error'].iloc[1]  # Standard error for effects
                    sig_line = t_crit * se * 2  # Convert to effect scale
                    
                    fig.add_vline(x=sig_line, line_dash="dash", line_color="red")
                    fig.add_annotation(x=sig_line, y=0, text=f"Significance Line (α={alpha})", 
                                    showarrow=True, arrowhead=1, ax=40, ay=40)
                    
                    st.plotly_chart(fig)
                    
                except Exception as e:
                    st.error(f"Error in model fitting: {str(e)}")
            
            elif analysis_type == "ANOVA":
                st.markdown("### Analysis of Variance (ANOVA)")
                
                # Get factors and coded factors
                factors = metadata["factors"]
                coded_factors = [f"{factor}_coded" for factor in factors]
                
                # Create model formula similar to Effect Estimation
                formula_terms = [f"{factor}_coded" for factor in factors]
                
                # Add interaction terms
                include_interactions = st.checkbox("Include 2-factor interactions", value=True)
                if include_interactions and len(factors) >= 2:
                    for i, j in combinations(range(len(factors)), 2):
                        formula_terms.append(f"{coded_factors[i]}:{coded_factors[j]}")
                
                # Add squared terms for response surface designs
                if metadata["design_type"] in ["Central Composite Design", "Box-Behnken Design"]:
                    include_squared = st.checkbox("Include squared terms", value=True)
                    if include_squared:
                        for factor in coded_factors:
                            formula_terms.append(f"I({factor}**2)")
                
                # Create formula
                formula = f"{response} ~ {' + '.join(formula_terms)}"
                
                try:
                    # Fit model
                    model = ols(formula, data=df).fit()
                    
                    # Create ANOVA table
                    anova_table = sm.stats.anova_lm(model, typ=2)
                    
                    # Add mean square column
                    anova_table['MS'] = anova_table['sum_sq'] / anova_table['df']
                    
                    # Reorder columns
                    anova_table = anova_table[['df', 'sum_sq', 'MS', 'F', 'PR(>F)']]
                    
                    # Rename columns for clarity
                    anova_table.columns = ['DF', 'Sum of Squares', 'Mean Square', 'F-value', 'p-value']
                    
                    # Display table
                    st.dataframe(anova_table.style.format({
                        'Sum of Squares': '{:.4f}',
                        'Mean Square': '{:.4f}',
                        'F-value': '{:.3f}',
                        'p-value': '{:.4g}'
                    }).background_gradient(subset=['p-value'], cmap='Reds_r'))
                    
                    # Visualization of Sum of Squares
                    fig = px.pie(
                        names=anova_table.index,
                        values=anova_table['Sum of Squares'],
                        title="Distribution of Sum of Squares"
                    )
                    
                    st.plotly_chart(fig)
                    
                    # Effect size calculation
                    st.markdown("### Effect Size (η²)")
                    
                    # Calculate eta-squared
                    total_ss = anova_table['Sum of Squares'].sum()
                    eta_squared = anova_table['Sum of Squares'] / total_ss
                    
                    # Create dataframe for display
                    eta_df = pd.DataFrame({
                        'Term': anova_table.index,
                        'η²': eta_squared,
                        'Interpretation': eta_squared.map(lambda x: 
                            'Large (>0.14)' if x > 0.14 else 
                            'Medium (>0.06)' if x > 0.06 else 
                            'Small (>0.01)' if x > 0.01 else 
                            'Negligible'
                        )
                    })
                    
                    st.dataframe(eta_df.style.format({
                        'η²': '{:.4f}'
                    }).background_gradient(subset=['η²'], cmap='viridis'))
                    
                except Exception as e:
                    st.error(f"Error in ANOVA: {str(e)}")
            
            elif analysis_type == "Response Surface":
                if metadata["design_type"] in ["Central Composite Design", "Box-Behnken Design", "Response Surface"]:
                    st.markdown("### Response Surface Analysis")
                    
                    # Get factors and coded factors
                    factors = metadata["factors"]
                    
                    if len(factors) >= 2:
                        # Select two factors for surface plot
                        selected_factors = st.multiselect(
                            "Select factors for response surface plot (select 2)",
                            factors,
                            default=factors[:2] if len(factors) >= 2 else [],
                            max_selections=2
                        )
                        
                        if len(selected_factors) == 2:
                            # Create model formula with quadratic terms
                            coded_factors = [f"{factor}_coded" for factor in factors]
                            formula_terms = coded_factors.copy()
                            
                            # Add interaction terms
                            for i, j in combinations(range(len(factors)), 2):
                                formula_terms.append(f"{coded_factors[i]}:{coded_factors[j]}")
                            
                            # Add squared terms
                            for factor in coded_factors:
                                formula_terms.append(f"I({factor}**2)")
                            
                            formula = f"{response} ~ {' + '.join(formula_terms)}"
                            
                            try:
                                # Fit model
                                model = ols(formula, data=df).fit()
                                
                                # Create grid for prediction
                                factor1, factor2 = selected_factors
                                x1_min, x1_max = df[factor1].min(), df[factor1].max()
                                x2_min, x2_max = df[factor2].min(), df[factor2].max()
                                
                                x1_grid = np.linspace(x1_min, x1_max, 20)
                                x2_grid = np.linspace(x2_min, x2_max, 20)
                                x1_mesh, x2_mesh = np.meshgrid(x1_grid, x2_grid)
                                
                                # Create prediction data
                                pred_data = pd.DataFrame({
                                    factor1: x1_mesh.flatten(),
                                    factor2: x2_mesh.flatten()
                                })
                                
                                # Add coded variables
                                for f in [factor1, factor2]:
                                    f_min, f_max = df[f].min(), df[f].max()
                                    pred_data[f"{f}_coded"] = 2 * (pred_data[f] - f_min) / (f_max - f_min) - 1
                                
                                # Set other factors to center (0)
                                for f in factors:
                                    if f not in [factor1, factor2]:
                                        pred_data[f] = df[f].mean()
                                        pred_data[f"{f}_coded"] = 0
                                
                                # Add interaction terms
                                for i, j in combinations(range(len(factors)), 2):
                                    f1 = f"{factors[i]}_coded"
                                    f2 = f"{factors[j]}_coded"
                                    if f1 in pred_data.columns and f2 in pred_data.columns:
                                        pred_data[f"{f1}:{f2}"] = pred_data[f1] * pred_data[f2]
                                
                                # Add squared terms
                                for f in coded_factors:
                                    if f in pred_data.columns:
                                        pred_data[f"I({f}**2)"] = pred_data[f]**2
                                
                                # Predict response
                                try:
                                    # Use patsy to create design matrix
                                    import patsy
                                    X_pred = patsy.dmatrix(model.model.formula, pred_data, return_type='dataframe')
                                    y_pred = model.predict(X_pred)
                                    
                                    # Reshape for contour plot
                                    z_mesh = y_pred.values.reshape(x2_grid.shape)
                                    
                                    # Create visualization
                                    plot_type = st.radio(
                                        "Select plot type",
                                        ["Contour Plot", "3D Surface Plot"],
                                        horizontal=True
                                    )
                                    
                                    if plot_type == "Contour Plot":
                                        fig = go.Figure(data=go.Contour(
                                            z=z_mesh,
                                            x=x1_grid,
                                            y=x2_grid,
                                            colorscale='Viridis',
                                            contours=dict(
                                                showlabels=True,
                                                labelfont=dict(size=12, color='white')
                                            ),
                                            colorbar=dict(title=response)
                                        ))
                                        
                                        # Add data points
                                        fig.add_trace(go.Scatter(
                                            x=df[factor1],
                                            y=df[factor2],
                                            mode='markers',
                                            marker=dict(
                                                color='red',
                                                size=8,
                                                line=dict(color='black', width=1)
                                            ),
                                            name='Experimental Points'
                                        ))
                                        
                                        fig.update_layout(
                                            title=f"Contour Plot of {response}",
                                            xaxis_title=factor1,
                                            yaxis_title=factor2,
                                            height=600
                                        )
                                        
                                    else:  # 3D Surface Plot
                                        fig = go.Figure(data=go.Surface(
                                            z=z_mesh,
                                            x=x1_grid,
                                            y=x2_grid,
                                            colorscale='Viridis',
                                            colorbar=dict(title=response)
                                        ))
                                        
                                        # Add data points
                                        fig.add_trace(go.Scatter3d(
                                            x=df[factor1],
                                            y=df[factor2],
                                            z=df[response],
                                            mode='markers',
                                            marker=dict(
                                                color='red',
                                                size=5,
                                                line=dict(color='black', width=1)
                                            ),
                                            name='Experimental Points'
                                        ))
                                        
                                        fig.update_layout(
                                            title=f"Surface Plot of {response}",
                                            scene=dict(
                                                xaxis_title=factor1,
                                                yaxis_title=factor2,
                                                zaxis_title=response
                                            ),
                                            height=700
                                        )
                                    
                                    st.plotly_chart(fig)
                                    
                                    # Find optimal point
                                    max_idx = np.argmax(y_pred)
                                    min_idx = np.argmin(y_pred)
                                    
                                    max_x1 = pred_data[factor1].iloc[max_idx]
                                    max_x2 = pred_data[factor2].iloc[max_idx]
                                    max_y = y_pred[max_idx]
                                    
                                    min_x1 = pred_data[factor1].iloc[min_idx]
                                    min_x2 = pred_data[factor2].iloc[min_idx]
                                    min_y = y_pred[min_idx]
                                    
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.markdown("### Maximum Point")
                                        st.markdown(f"""
                                        **Optimal Settings:**
                                        - {factor1}: {max_x1:.4g}
                                        - {factor2}: {max_x2:.4g}
                                        - Predicted {response}: {max_y:.4g}
                                        """)
                                    
                                    with col2:
                                        st.markdown("### Minimum Point")
                                        st.markdown(f"""
                                        **Minimum Settings:**
                                        - {factor1}: {min_x1:.4g}
                                        - {factor2}: {min_x2:.4g}
                                        - Predicted {response}: {min_y:.4g}
                                        """)
                                
                                except Exception as e:
                                    st.error(f"Error in surface plot: {str(e)}")
                            
                            except Exception as e:
                                st.error(f"Error in model fitting: {str(e)}")
                        else:
                            st.info("Please select exactly 2 factors for the response surface plot.")
                    else:
                        st.info("Please select at least 2 factors for visualization.")
                else:
                    st.warning("Response Surface Analysis is most suitable for designs with at least 3 levels per factor, such as Central Composite or Box-Behnken designs.")
            
            elif analysis_type == "Diagnostic Plots":
                st.markdown("### Model Diagnostic Plots")
                
                # Get factors and coded factors
                factors = metadata["factors"]
                coded_factors = [f"{factor}_coded" for factor in factors]
                
                # Create model formula
                formula_terms = [f"{factor}_coded" for factor in factors]
                
                # Add interaction terms
                include_interactions = st.checkbox("Include 2-factor interactions", value=True)
                if include_interactions and len(factors) >= 2:
                    for i, j in combinations(range(len(factors)), 2):
                        formula_terms.append(f"{coded_factors[i]}:{coded_factors[j]}")
                
                # Add squared terms for response surface designs
                if metadata["design_type"] in ["Central Composite Design", "Box-Behnken Design"]:
                    include_squared = st.checkbox("Include squared terms", value=True)
                    if include_squared:
                        for factor in coded_factors:
                            formula_terms.append(f"I({factor}**2)")
                
                # Create formula
                formula = f"{response} ~ {' + '.join(formula_terms)}"
                
                try:
                    # Fit model
                    model = ols(formula, data=df).fit()
                    
                    # Calculate fitted values and residuals
                    fitted = model.fittedvalues
                    residuals = model.resid
                    std_residuals = model.get_influence().resid_studentized_internal
                    
                    # Create diagnostic dataframe
                    diag_df = pd.DataFrame({
                        'Fitted': fitted,
                        'Residual': residuals,
                        'Standardized Residual': std_residuals,
                        'Run Order': df['RunOrder'],
                        'Actual': df[response]
                    })
                    
                    # Select diagnostic plot type
                    diag_plot_type = st.selectbox(
                        "Select Diagnostic Plot",
                        [
                            "Residuals vs. Fitted Values",
                            "Normal Q-Q Plot",
                            "Residuals vs. Run Order",
                            "Actual vs. Predicted"
                        ]
                    )
                    
                    if diag_plot_type == "Residuals vs. Fitted Values":
                        fig = px.scatter(
                            diag_df,
                            x='Fitted',
                            y='Residual',
                            title="Residuals vs. Fitted Values",
                            labels={"Fitted": "Fitted Values", "Residual": "Residuals"},
                            hover_data=['Run Order', 'Actual'],
                            color='Standardized Residual',
                            color_continuous_scale='RdBu_r',
                            color_continuous_midpoint=0
                        )
                        
                        # Add horizontal line at y=0
                        fig.add_hline(y=0, line_dash="dash", line_color="gray")
                        
                        # Add outlier thresholds
                        fig.add_hline(y=2*np.std(residuals), line_dash="dot", line_color="red")
                        fig.add_hline(y=-2*np.std(residuals), line_dash="dot", line_color="red")
                        
                        st.plotly_chart(fig)
                        
                        st.markdown("""
                        **Interpretation:**
                        - Random scatter around zero line indicates good model fit
                        - Patterns suggest non-linearity or heteroscedasticity
                        - Points outside red dotted lines may be outliers
                        """)
                        
                    elif diag_plot_type == "Normal Q-Q Plot":
                        # Calculate theoretical quantiles
                        n = len(residuals)
                        p = (np.arange(1, n + 1) - 0.5) / n
                        theoretical_quantiles = stats.norm.ppf(p)
                        
                        # Sort residuals
                        sorted_residuals = np.sort(std_residuals)
                        
                        # Create QQ plot
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=theoretical_quantiles,
                            y=sorted_residuals,
                            mode='markers',
                            marker=dict(
                                color=sorted_residuals,
                                colorscale='RdBu_r',
                                colorbar=dict(title="Standardized Residuals"),
                                size=8,
                                line=dict(width=1, color='black')
                            ),
                            name='Residuals'
                        ))
                        
                        # Add reference line
                        min_q = min(theoretical_quantiles)
                        max_q = max(theoretical_quantiles)
                        
                        # Calculate line parameters based on the first and third quartiles
                        q1_theoretical = np.percentile(theoretical_quantiles, 25)
                        q3_theoretical = np.percentile(theoretical_quantiles, 75)
                        q1_residual = np.percentile(sorted_residuals, 25)
                        q3_residual = np.percentile(sorted_residuals, 75)
                        
                        slope = (q3_residual - q1_residual) / (q3_theoretical - q1_theoretical)
                        intercept = q1_residual - slope * q1_theoretical
                        
                        fig.add_trace(go.Scatter(
                            x=[min_q, max_q],
                            y=[intercept + slope * min_q, intercept + slope * max_q],
                            mode='lines',
                            line=dict(color='black', dash='dash'),
                            name='Reference Line'
                        ))
                        
                        fig.update_layout(
                            title="Normal Q-Q Plot",
                            xaxis_title="Theoretical Quantiles",
                            yaxis_title="Standardized Residuals",
                            height=500
                        )
                        
                        st.plotly_chart(fig)
                        
                        # Test normality
                        stat, p_value = stats.shapiro(residuals)
                        
                        st.markdown(f"""
                        **Shapiro-Wilk Test for Normality:**
                        - Test Statistic: {stat:.4f}
                        - p-value: {p_value:.4g}
                        - {"Residuals appear normally distributed (p > 0.05)" if p_value > 0.05 else "Residuals may not be normally distributed (p < 0.05)"}
                        
                        **Interpretation:**
                        - Points following the diagonal line indicate normality
                        - Deviations suggest non-normal distribution
                        - S-shaped curve may indicate skewness
                        """)
                        
                    elif diag_plot_type == "Residuals vs. Run Order":
                        fig = px.scatter(
                            diag_df.sort_values('Run Order'),
                            x='Run Order',
                            y='Residual',
                            title="Residuals vs. Run Order",
                            labels={"Run Order": "Run Order", "Residual": "Residuals"},
                            color='Standardized Residual',
                            color_continuous_scale='RdBu_r',
                            color_continuous_midpoint=0
                        )
                        
                        # Add horizontal line at y=0
                        fig.add_hline(y=0, line_dash="dash", line_color="gray")
                        
                        st.plotly_chart(fig)
                        
                        # Calculate Durbin-Watson statistic
                        from statsmodels.stats.stattools import durbin_watson
                        dw_stat = durbin_watson(diag_df.sort_values('Run Order')['Residual'])
                        
                        st.markdown(f"""
                        **Durbin-Watson Statistic: {dw_stat:.4f}**
                        - Values near 2: No autocorrelation
                        - Values < 1.5: Possible positive autocorrelation
                        - Values > 2.5: Possible negative autocorrelation
                        
                        **Interpretation:**
                        - Random scatter suggests no time-dependent effects
                        - Patterns may indicate drift or learning effects
                        - Time-based trends require investigation of experimental execution
                        """)
                        
                    elif diag_plot_type == "Actual vs. Predicted":
                        fig = px.scatter(
                            diag_df,
                            x='Fitted',
                            y='Actual',
                            title="Actual vs. Predicted Values",
                            labels={"Fitted": "Predicted Values", "Actual": f"Actual {response}"},
                            hover_data=['Run Order'],
                            color='Standardized Residual',
                            color_continuous_scale='RdBu_r',
                            color_continuous_midpoint=0
                        )
                        
                        # Add 45-degree reference line
                        min_val = min(diag_df['Fitted'].min(), diag_df['Actual'].min())
                        max_val = max(diag_df['Fitted'].max(), diag_df['Actual'].max())
                        
                        fig.add_trace(go.Scatter(
                            x=[min_val, max_val],
                            y=[min_val, max_val],
                            mode='lines',
                            line=dict(color='black', dash='dash'),
                            name='Perfect Prediction'
                        ))
                        
                        st.plotly_chart(fig)
                        
                        # Calculate R² and RMSE
                        r2 = model.rsquared
                        rmse = np.sqrt(np.mean(residuals**2))
                        
                        st.markdown(f"""
                        **Model Accuracy Metrics:**
                        - R²: {r2:.4f}
                        - RMSE: {rmse:.4f}
                        
                        **Interpretation:**
                        - Points along the diagonal indicate good model fit
                        - Scatter shows prediction variability
                        - Systematic deviations suggest model inadequacy
                        """)
                
                except Exception as e:
                    st.error(f"Error in diagnostic plots: {str(e)}")
        else:
            st.info("Please select a dataset in the Overview tab to continue.")
    
    # Tab 4: Integration Features
    with tabs[3]:
        st.subheader("Integration with StickForStats Platform")
        
        st.markdown("""
        The DOE module seamlessly integrates with other StickForStats components,
        enabling a complete workflow from experimental design to data analysis
        and visualization.
        """)
        
        # Show integration options
        integration_option = st.selectbox(
            "Explore Integration with:",
            [
                "Statistical Analysis Module",
                "Visualization Tools",
                "Data Management System",
                "Reporting Engine"
            ]
        )
        
        if integration_option == "Statistical Analysis Module":
            st.markdown("""
            ### Integration with Statistical Analysis Module
            
            The DOE module shares data structures and analysis methods with the core
            Statistical Analysis Module, enabling seamless transitions between:
            
            - **ANOVA and Regression**: DOE analysis results can be directly used for deeper statistical analyses
            - **Distribution Fitting**: Response data can be analyzed for distributional properties
            - **Multivariate Analysis**: DOE results can feed into PCA, PLS, and other multivariate methods
            - **Time Series Analysis**: Process monitoring data can be linked to experimental conditions
            
            **Example Integration Workflow:**
            1. Design and execute factorial experiment
            2. Analyze main effects and interactions in DOE module
            3. Feed significant factors into regression analysis for detailed modeling
            4. Apply distribution fitting to residuals for process capability analysis
            """)
            
            # Show mock integration UI
            st.image("https://via.placeholder.com/800x400?text=StickForStats+Integration+Mockup", 
                    caption="Statistical Analysis Module Integration UI")
            
        elif integration_option == "Visualization Tools":
            st.markdown("""
            ### Integration with Visualization Tools
            
            DOE results can be directly visualized using the advanced plotting capabilities:
            
            - **Interactive Plots**: Dynamic visualization of response surfaces and contour plots
            - **Custom Dashboards**: Creating experiment-specific monitoring dashboards
            - **Automated Reports**: Generating comprehensive DOE reports with interactive elements
            - **Comparative Visualization**: Comparing results across multiple experiments
            
            **Example Integration Workflow:**
            1. Complete DOE analysis in the DOE module
            2. Send effect estimates and model to the Visualization Tool
            3. Create custom dashboard with interactive response optimizer
            4. Share results with stakeholders via interactive web report
            """)
            
            # Mock visualization integration
            if 'design_df' in st.session_state and 'metadata' in st.session_state:
                st.markdown("### Sample Visualization Integration")
                
                df = st.session_state.design_df
                metadata = st.session_state.metadata
                factors = metadata["factors"]
                responses = metadata["responses"]
                
                if len(responses) >= 2:
                    # Create multi-response visualization
                    fig = make_subplots(rows=1, cols=len(responses), 
                                      subplot_titles=responses)
                    
                    for i, response in enumerate(responses):
                        # Add main factors as color and size
                        if len(factors) >= 2:
                            fig.add_trace(
                                go.Scatter(
                                    x=df[factors[0]],
                                    y=df[response],
                                    mode='markers',
                                    marker=dict(
                                        size=df[response] / df[response].max() * 20 + 5,
                                        color=df[factors[1]],
                                        colorscale='Viridis',
                                        colorbar=dict(title=factors[1]) if i == len(responses)-1 else None,
                                        showscale=i == len(responses)-1
                                    ),
                                    name=response
                                ),
                                row=1, col=i+1
                            )
                            
                            fig.update_xaxes(title_text=factors[0], row=1, col=i+1)
                            fig.update_yaxes(title_text=response, row=1, col=i+1)
                    
                    fig.update_layout(
                        title="Multi-Response Visualization Dashboard",
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig)
                    
                    st.markdown("*This visualization shows the integration between DOE results and the StickForStats advanced visualization system.*")
            else:
                st.info("Please select a dataset in the Overview tab to see example visualizations.")
            
        elif integration_option == "Data Management System":
            st.markdown("""
            ### Integration with Data Management System
            
            The DOE module connects with the central data repository:
            
            - **Experiment Database**: Store and retrieve experimental designs and results
            - **Version Control**: Track design iterations and analysis evolution
            - **Metadata Management**: Maintain comprehensive experiment metadata
            - **Data Lineage**: Track relationships between experiments and analyses
            
            **Example Integration Workflow:**
            1. Save experimental design to central repository
            2. Link raw data uploads to design conditions
            3. Track analysis versions as process understanding evolves
            4. Connect findings to related experiments and projects
            """)
            
            # Mock data management UI
            st.markdown("### Data Management Interface")
            
            # Create mock experiment database UI
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### Experiment Repository")
                
                # Mock experiment list
                experiments = [
                    {"id": "DOE-2025-001", "title": "Media Optimization", "date": "2025-01-15", "type": "Full Factorial", "status": "Completed"},
                    {"id": "DOE-2025-002", "title": "Chromatography Method Development", "date": "2025-02-03", "type": "Central Composite", "status": "In Progress"},
                    {"id": "DOE-2025-003", "title": "Formulation Stability", "date": "2025-02-22", "type": "Fractional Factorial", "status": "Planned"},
                    {"id": "DOE-2025-004", "title": "Cell Line Selection", "date": "2025-03-10", "type": "Screening Design", "status": "Completed"},
                ]
                
                # Display as table
                experiments_df = pd.DataFrame(experiments)
                st.dataframe(experiments_df)
            
            with col2:
                st.markdown("#### Data Operations")
                st.markdown("""
                - 📋 Import from LIMS
                - 📤 Export to Analysis
                - 🔄 Sync with ELN
                - 🔍 Find Related Data
                - 📊 Generate Report
                - 🔒 Access Control
                """)
            
            st.info("This mock interface demonstrates how DOE data integrates with the broader data management system.")
        
        elif integration_option == "Reporting Engine":
            st.markdown("""
            ### Integration with Reporting Engine
            
            The DOE module works with the reporting system to create customized reports:
            
            - **Automatic Report Generation**: Create comprehensive DOE reports with minimal effort
            - **Customizable Templates**: Choose from regulatory, technical, or executive report formats
            - **Dynamic Content**: Interactive elements that respond to reader interactions
            - **Collaborative Reviews**: Share and collect feedback on results
            
            **Example Integration Workflow:**
            1. Complete DOE analysis in the DOE module
            2. Select appropriate report template (e.g., Regulatory Filing, Technical Transfer)
            3. Customize sections and visualization preferences
            4. Generate and distribute interactive or static reports
            """)
            
            # Mock report generation interface
            st.markdown("### Report Generation Interface")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Report Configuration")
                
                report_template = st.selectbox(
                    "Report Template",
                    ["Technical Report", "Regulatory Submission", "Method Transfer", "Executive Summary"]
                )
                
                report_sections = st.multiselect(
                    "Include Sections",
                    ["Experimental Design", "Design Evaluation", "Effect Analysis", "ANOVA", 
                     "Response Surface Analysis", "Optimization", "Robustness Assessment", 
                     "Conclusions", "Recommendations", "Raw Data Appendix"],
                    default=["Experimental Design", "Effect Analysis", "ANOVA", "Conclusions"]
                )
                
                output_format = st.radio(
                    "Output Format",
                    ["Interactive HTML", "PDF Document", "PowerPoint Presentation", "Word Document"],
                    horizontal=True
                )
                
                visualization_style = st.selectbox(
                    "Visualization Style",
                    ["Technical (Detailed)", "Presentation (Simplified)", "Publication Quality", "Corporate Template"]
                )
            
            with col2:
                st.markdown("#### Preview")
                
                # Mock report preview
                st.markdown(f"""
                ### {report_template} Preview

                **Selected Sections:**
                """ + "\n".join([f"- {section}" for section in report_sections]) + f"""

                **Format:** {output_format}

                **Style:** {visualization_style}
                """)
                
                if st.button("Generate Report"):
                    st.success("Report generation initiated. The completed report will be available in your document library.")
            
            st.info("This interface demonstrates how DOE results can be turned into comprehensive reports via the StickForStats reporting engine.")
    
    # Tab 5: Export & Report
    with tabs[4]:
        st.subheader("Export and Reporting")
        
        st.markdown("""
        This section demonstrates how to export DOE designs, analysis results, and
        comprehensive reports from the integrated StickForStats platform.
        """)
        
        # Check if we have data to export
        if 'design_df' in st.session_state and 'metadata' in st.session_state:
            export_type = st.selectbox(
                "Select Export Type",
                ["Design Matrix", "Analysis Results", "Complete Project", "Visualization"]
            )
            
            if export_type == "Design Matrix":
                st.markdown("### Design Matrix Export")
                
                # Export options
                col1, col2 = st.columns(2)
                
                with col1:
                    include_metadata = st.checkbox("Include Metadata", value=True)
                    include_coded = st.checkbox("Include Coded Values", value=True)
                    
                    file_format = st.radio(
                        "File Format",
                        ["CSV", "Excel", "JSON"],
                        horizontal=True
                    )
                
                with col2:
                    st.markdown("#### Preview")
                    
                    # Create preview based on selections
                    preview_df = st.session_state.design_df.copy()
                    if not include_coded:
                        coded_cols = [col for col in preview_df.columns if '_coded' in col]
                        preview_df = preview_df.drop(columns=coded_cols)
                    
                    st.dataframe(preview_df.head())
                
                # Export button
                if st.button("Export Design Matrix"):
                    # In a real application, this would generate and download the file
                    # For this demo, we'll just show a success message
                    file_extension = ".csv" if file_format == "CSV" else ".xlsx" if file_format == "Excel" else ".json"
                    filename = f"design_matrix{file_extension}"
                    
                    # Mock download button
                    st.success(f"Design matrix exported as {filename}")
                    st.markdown(f"*In the actual application, the file would be downloaded automatically.*")
                    
                    # Create a mock download button
                    if file_format == "CSV":
                        csv = preview_df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="design_matrix.csv">Download CSV File</a>'
                        st.markdown(href, unsafe_allow_html=True)
            
            elif export_type == "Analysis Results":
                st.markdown("### Analysis Results Export")
                
                # Select response for analysis export
                response = st.selectbox(
                    "Select Response Variable",
                    st.session_state.metadata["responses"]
                )
                
                # Select analysis components to export
                analysis_components = st.multiselect(
                    "Select Analysis Components to Include",
                    ["Effect Estimates", "ANOVA Table", "Model Coefficients", 
                     "Diagnostic Plots", "Response Surface", "Optimization Results"],
                    default=["Effect Estimates", "ANOVA Table", "Model Coefficients"]
                )
                
                # File format options
                file_format = st.radio(
                    "File Format",
                    ["PDF Report", "Excel Workbook", "HTML Report", "R Markdown"],
                    horizontal=True
                )
                
                # Export button
                if st.button("Export Analysis Results"):
                    # Mock export behavior
                    file_extension = ".pdf" if file_format == "PDF Report" else ".xlsx" if file_format == "Excel Workbook" else ".html" if file_format == "HTML Report" else ".Rmd"
                    filename = f"{response}_analysis{file_extension}"
                    
                    st.success(f"Analysis results for {response} exported as {filename}")
                    st.markdown(f"*The export includes: {', '.join(analysis_components)}*")
            
            elif export_type == "Complete Project":
                st.markdown("### Complete Project Export")
                
                # Project metadata
                col1, col2 = st.columns(2)
                
                with col1:
                    project_title = st.text_input("Project Title", value=f"DOE Analysis - {st.session_state.dataset_name}")
                    project_author = st.text_input("Project Author", value="StickForStats User")
                    project_date = st.date_input("Project Date")
                
                with col2:
                    project_description = st.text_area("Project Description", value=f"Analysis of {st.session_state.dataset_name} using DOE methodology")
                
                # Export components
                export_components = st.multiselect(
                    "Select Components to Include",
                    ["Design Information", "Raw Data", "Effect Analysis", "ANOVA Results", 
                     "Model Diagnostics", "Response Surface Analysis", "Design Space Mapping",
                     "Optimization Results", "Conclusions", "Recommendations"],
                    default=["Design Information", "Raw Data", "Effect Analysis", "ANOVA Results"]
                )
                
                # Export format
                export_format = st.selectbox(
                    "Export Format",
                    ["Full Report (PDF)", "Interactive Report (HTML)", "Analysis Package (ZIP)", 
                     "Presentation Slides (PPTX)", "Technical Document (DOCX)"]
                )
                
                # Export button
                if st.button("Export Complete Project"):
                    # Mock export behavior
                    format_extensions = {
                        "Full Report (PDF)": ".pdf",
                        "Interactive Report (HTML)": ".html",
                        "Analysis Package (ZIP)": ".zip",
                        "Presentation Slides (PPTX)": ".pptx",
                        "Technical Document (DOCX)": ".docx"
                    }
                    
                    filename = f"{project_title.replace(' ', '_')}{format_extensions[export_format]}"
                    
                    st.success(f"Complete project exported as {filename}")
                    st.markdown(f"*The project export includes {len(export_components)} components and is ready for sharing.*")
            
            elif export_type == "Visualization":
                st.markdown("### Visualization Export")
                
                # Select visualization type
                viz_type = st.selectbox(
                    "Select Visualization Type",
                    ["Response Surface", "Pareto Chart of Effects", "Interaction Plots", 
                     "Main Effects Plot", "Contour Plot", "Custom Combination"]
                )
                
                # Visualization options
                col1, col2 = st.columns(2)
                
                with col1:
                    # Options depend on visualization type
                    if viz_type in ["Response Surface", "Contour Plot"]:
                        # For surface/contour plots, need to select factors and response
                        factors = st.session_state.metadata["factors"]
                        responses = st.session_state.metadata["responses"]
                        
                        if len(factors) >= 2:
                            factor_x = st.selectbox("X-Axis Factor", factors, index=0)
                            factor_y = st.selectbox("Y-Axis Factor", factors, index=min(1, len(factors)-1))
                            response_var = st.selectbox("Response Variable", responses)
                        else:
                            st.warning("Need at least 2 factors for this visualization type.")
                    
                    elif viz_type in ["Pareto Chart of Effects", "Main Effects Plot"]:
                        responses = st.session_state.metadata["responses"]
                        response_var = st.selectbox("Response Variable", responses)
                        
                        # For Pareto, can select significance level
                        if viz_type == "Pareto Chart of Effects":
                            alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)
                
                with col2:
                    # Visualization settings
                    viz_width = st.number_input("Width (pixels)", min_value=400, max_value=2000, value=800)
                    viz_height = st.number_input("Height (pixels)", min_value=300, max_value=1500, value=600)
                    
                    viz_format = st.radio(
                        "Export Format",
                        ["PNG", "SVG", "HTML", "PDF"],
                        horizontal=True
                    )
                    
                    high_resolution = st.checkbox("High Resolution", value=True)
                
                # Mock visualization preview
                st.markdown("### Visualization Preview")
                
                # Create a mock visualization based on the type
                if viz_type in ["Response Surface", "Contour Plot"] and 'factor_x' in locals() and 'factor_y' in locals():
                    # Create a mock surface or contour plot
                    if viz_type == "Response Surface":
                        # 3D Surface plot
                        # Generate some mock data
                        x = np.linspace(-1, 1, 20)
                        y = np.linspace(-1, 1, 20)
                        X, Y = np.meshgrid(x, y)
                        Z = 2 + 0.5*X - 0.3*Y + 0.5*X*Y - 0.2*X**2 - 0.4*Y**2
                        
                        fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y)])
                        fig.update_layout(
                            title=f"{response_var} vs {factor_x} and {factor_y}",
                            scene=dict(
                                xaxis_title=factor_x,
                                yaxis_title=factor_y,
                                zaxis_title=response_var
                            ),
                            width=viz_width,
                            height=viz_height
                        )
                        
                    else:  # Contour Plot
                        # Generate some mock data
                        x = np.linspace(-1, 1, 20)
                        y = np.linspace(-1, 1, 20)
                        X, Y = np.meshgrid(x, y)
                        Z = 2 + 0.5*X - 0.3*Y + 0.5*X*Y - 0.2*X**2 - 0.4*Y**2
                        
                        fig = go.Figure(data=go.Contour(
                            z=Z,
                            x=x,
                            y=y,
                            contours=dict(
                                showlabels=True,
                                labelfont=dict(size=12, color='white')
                            ),
                            colorscale='Viridis'
                        ))
                        fig.update_layout(
                            title=f"Contour Plot of {response_var}",
                            xaxis_title=factor_x,
                            yaxis_title=factor_y,
                            width=viz_width,
                            height=viz_height
                        )
                    
                    st.plotly_chart(fig)
                
                elif viz_type == "Pareto Chart of Effects" and 'response_var' in locals():
                    # Generate some mock effect data
                    effects = [
                        {"term": "Factor A", "effect": 2.5, "p_value": 0.001},
                        {"term": "Factor B", "effect": 1.8, "p_value": 0.012},
                        {"term": "Factor C", "effect": 0.9, "p_value": 0.089},
                        {"term": "AB", "effect": 1.2, "p_value": 0.042},
                        {"term": "AC", "effect": 0.5, "p_value": 0.22},
                        {"term": "BC", "effect": 0.3, "p_value": 0.45},
                    ]
                    
                    effects_df = pd.DataFrame(effects)
                    effects_df['abs_effect'] = abs(effects_df['effect'])
                    effects_df = effects_df.sort_values('abs_effect', ascending=False)
                    
                    fig = px.bar(
                        effects_df,
                        y='term',
                        x='abs_effect',
                        color='p_value',
                        color_continuous_scale='RdBu_r',
                        color_continuous_midpoint=0.05,
                        labels={'abs_effect': 'Absolute Effect', 'term': 'Term'},
                        title=f"Pareto Chart of Effects for {response_var}",
                        orientation='h'
                    )
                    
                    # Add significance line
                    sig_line = 1.0  # Mock value
                    fig.add_vline(x=sig_line, line_dash="dash", line_color="red")
                    fig.update_layout(width=viz_width, height=viz_height)
                    
                    st.plotly_chart(fig)
                
                elif viz_type == "Main Effects Plot" and 'response_var' in locals():
                    # Generate mock main effects data
                    factors = st.session_state.metadata["factors"]
                    
                    fig = make_subplots(rows=1, cols=len(factors), 
                                      subplot_titles=factors)
                    
                    for i, factor in enumerate(factors):
                        # Mock data
                        x = [-1, 1]
                        y = [75 + np.random.normal(0, 5), 90 + np.random.normal(0, 5)]
                        
                        fig.add_trace(
                            go.Scatter(
                                x=x,
                                y=y,
                                mode='lines+markers',
                                name=factor
                            ),
                            row=1, col=i+1
                        )
                        
                        fig.update_xaxes(title_text="Level", row=1, col=i+1)
                        
                        if i == 0:
                            fig.update_yaxes(title_text=response_var, row=1, col=i+1)
                    
                    fig.update_layout(
                        title=f"Main Effects Plot for {response_var}",
                        showlegend=False,
                        width=viz_width,
                        height=viz_height
                    )
                    
                    st.plotly_chart(fig)
                
                elif viz_type == "Interaction Plots":
                    # Generate mock interaction data
                    factors = st.session_state.metadata["factors"]
                    responses = st.session_state.metadata["responses"]
                    response_var = st.selectbox("Response Variable", responses)
                    
                    if len(factors) >= 2:
                        factor_pairs = list(combinations(factors, 2))
                        if len(factor_pairs) > 3:
                            factor_pairs = factor_pairs[:3]  # Limit to 3 pairs for display
                        
                        fig = make_subplots(rows=1, cols=len(factor_pairs), 
                                         subplot_titles=[f"{a} × {b}" for a, b in factor_pairs])
                        
                        for i, (factor1, factor2) in enumerate(factor_pairs):
                            # Generate mock interaction data
                            # Low-low, low-high, high-low, high-high
                            y = [70, 85, 80, 110]
                            
                            # Plot lines for each level of factor2
                            fig.add_trace(
                                go.Scatter(
                                    x=[-1, 1],
                                    y=y[:2],
                                    mode='lines+markers',
                                    name=f"{factor2}=-1",
                                    line=dict(color='blue')
                                ),
                                row=1, col=i+1
                            )
                            
                            fig.add_trace(
                                go.Scatter(
                                    x=[-1, 1],
                                    y=y[2:],
                                    mode='lines+markers',
                                    name=f"{factor2}=+1",
                                    line=dict(color='red')
                                ),
                                row=1, col=i+1
                            )
                            
                            fig.update_xaxes(title_text=factor1, row=1, col=i+1)
                            
                            if i == 0:
                                fig.update_yaxes(title_text=response_var, row=1, col=i+1)
                        
                        fig.update_layout(
                            title=f"Interaction Plots for {response_var}",
                            width=viz_width,
                            height=viz_height
                        )
                        
                        st.plotly_chart(fig)
                    else:
                        st.warning("Need at least 2 factors for interaction plots.")
                
                elif viz_type == "Custom Combination":
                    st.info("Custom visualization combination would be created here based on user selections.")
                
                # Export button
                if st.button("Export Visualization"):
                    # Mock export behavior
                    format_extensions = {
                        "PNG": ".png",
                        "SVG": ".svg",
                        "HTML": ".html",
                        "PDF": ".pdf"
                    }
                    
                    resolution_text = "high-resolution " if high_resolution else ""
                    filename = f"{viz_type.replace(' ', '_').lower()}{format_extensions[viz_format]}"
                    
                    st.success(f"Visualization exported as {resolution_text}{filename}")
        else:
            st.info("Please select a dataset in the Overview tab to enable export functionality.")

def make_subplots(rows=1, cols=1, subplot_titles=None):
    """
    Simple function to create a subplot figure for the demonstration
    This is a simplified version of plotly's make_subplots
    """
    fig = go.Figure()
    fig.update_layout(
        title="Multiple Subplots",
        grid=dict(rows=rows, columns=cols),
    )
    return fig

def combinations(iterable, r):
    """
    Simple implementation of itertools.combinations for the demonstration
    """
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)