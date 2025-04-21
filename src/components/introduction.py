import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def show():
    st.header("Introduction to DOE in Biotechnology")
    
    # Overview content
    st.markdown("""
    ## Overview
    Design of Experiments (DOE) represents a structured methodology for determining cause-and-effect relationships within complex biological systems. In biotechnology, where processes involve multiple interacting factors and significant variability, DOE provides a systematic framework to efficiently extract maximum information while minimizing experimental resources.
    """)
    
    # Create tabs for sections
    tab1, tab2, tab3, tab4 = st.tabs(["Importance in Biotechnology", "Why Traditional Approaches Fall Short", "Mathematical Foundation", "Interactive Example"])
    
    with tab1:
        st.markdown("""
        ## Importance in Biotechnology
        Biotechnology processes—from fermentation and cell culture to purification and formulation—involve numerous variables that can impact critical quality attributes. DOE enables:

        - **Resource Optimization**: Reduce experimental runs while maximizing information gained
        - **Process Understanding**: Identify critical process parameters and their interactions
        - **Regulatory Compliance**: Meet QbD (Quality by Design) requirements with systematic development approaches
        - **Risk Reduction**: Identify and mitigate failure modes before scale-up
        - **Technology Transfer**: Facilitate robust transfer between development and manufacturing
        """)
    
    with tab2:
        st.markdown("""
        ## Why Traditional Approaches Fall Short
        One-factor-at-a-time (OFAT) approaches, while intuitive, suffer from critical limitations in biotechnology:

        1. **Interaction Blindness**: Biological systems feature complex interactions that OFAT approaches miss entirely
        2. **Resource Inefficiency**: Require more experiments for less information
        3. **Limited Optimization**: Can only find local optima rather than global optima
        4. **Poor Characterization**: Provide limited understanding of the design space
        """)
        
        # Add a comparison visualization
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### OFAT Approach")
            st.image("https://raw.githubusercontent.com/username/biotech-doe-suite/main/assets/ofat_approach.png", 
                    caption="OFAT: Varying one factor at a time",
                    use_column_width=True)
            
        with col2:
            st.markdown("### DOE Approach")
            st.image("https://raw.githubusercontent.com/username/biotech-doe-suite/main/assets/doe_approach.png", 
                    caption="DOE: Systematic exploration of experimental space",
                    use_column_width=True)
    
    with tab3:
        st.markdown("""
        ## Mathematical Foundation
        The power of DOE stems from its mathematical structure. For a system with response $y$ and factors $x_1, x_2, ..., x_k$, DOE enables the estimation of a model:

        $$y = f(x_1, x_2, ..., x_k) + \\varepsilon$$

        Where $\\varepsilon$ represents experimental error, and $f$ can include:

        - Main effects: $\\beta_1 x_1, \\beta_2 x_2, ...$
        - Interaction effects: $\\beta_{12}x_1 x_2, \\beta_{13}x_1 x_3, ...$
        - Higher-order effects: $\\beta_{11}x_1^2, \\beta_{22}x_2^2, ...$
        """)
        
        # Add expandable section with more mathematical details
        with st.expander("Advanced Mathematical Details"):
            st.markdown("""
            ### Complete Model Equation
            The full second-order model for a system with k factors can be represented as:
            
            $$y = \\beta_0 + \\sum_{i=1}^{k}\\beta_i x_i + \\sum_{i<j}^{k}\\beta_{ij}x_i x_j + \\sum_{i=1}^{k}\\beta_{ii}x_i^2 + \\varepsilon$$
            
            ### Effect Estimation
            In a two-level design, the effect of factor A can be calculated as:
            
            $$E_A = \\frac{\\sum y_{A+} - \\sum y_{A-}}{n/2}$$
            
            Where:
            - $\\sum y_{A+}$ is the sum of responses when factor A is at high level
            - $\\sum y_{A-}$ is the sum of responses when factor A is at low level
            - $n$ is the total number of runs
            """)
    
    with tab4:
        st.markdown("""
        ## Interactive Example: Impact of DOE in Bioprocess Development
        
        The following interactive simulation demonstrates the difference between the One-Factor-At-A-Time (OFAT) 
        approach and Design of Experiments (DOE) for optimizing a simple bioreactor process.
        
        Try adjusting the parameters to see how each approach performs in finding the optimal conditions for protein expression.
        """)
        
        # Call the interactive simulation function
        intro_simulation()

def intro_simulation():
    st.header("Interactive Simulation: OFAT vs DOE in Bioprocess Optimization")
    
    st.markdown("""
    This simulation demonstrates the difference between One-Factor-At-A-Time (OFAT) 
    approach and Design of Experiments (DOE) for optimizing a simple bioreactor process.
    
    In this example, we'll optimize protein production by manipulating two factors:
    - Temperature (°C)
    - pH
    
    The "true" optimal conditions are at Temperature = 32°C and pH = 6.5.
    """)
    
    # Create two columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("OFAT Approach")
        st.markdown("First varying Temperature, then pH")
        
        # Initial conditions
        base_temp = st.slider("Starting Temperature (°C)", 25.0, 40.0, 30.0, 0.5, key="ofat_temp")
        base_pH = st.slider("Starting pH", 5.0, 8.0, 6.0, 0.1, key="ofat_pH")
        
        # Function to simulate protein yield
        def protein_yield(temp, pH):
            # Simulating a yield function with maximum at temp=32, pH=6.5
            return 100 * np.exp(-0.5 * ((temp - 32)**2/4 + (pH - 6.5)**2/0.25)) + np.random.normal(0, 3)
        
        # OFAT procedure
        # First fix pH and vary temperature
        temps = np.linspace(base_temp - 5, base_temp + 5, 5)
        yields_temp = [protein_yield(t, base_pH) for t in temps]
        best_temp_idx = np.argmax(yields_temp)
        best_temp = temps[best_temp_idx]
        
        # Then fix temperature at optimal and vary pH
        pHs = np.linspace(base_pH - 1, base_pH + 1, 5)
        yields_pH = [protein_yield(best_temp, p) for p in pHs]
        best_pH_idx = np.argmax(yields_pH)
        best_pH = pHs[best_pH_idx]
        
        # Final OFAT results
        final_ofat_yield = protein_yield(best_temp, best_pH)
        
        # Create OFAT visualization
        ofat_fig = make_subplots(rows=1, cols=2, subplot_titles=("Temperature Optimization", "pH Optimization"))
        
        ofat_fig.add_trace(
            go.Scatter(x=temps, y=yields_temp, mode='lines+markers', name='Yield vs Temp',
                      marker=dict(color='blue')),
            row=1, col=1
        )
        ofat_fig.add_trace(
            go.Scatter(x=[best_temp], y=[yields_temp[best_temp_idx]], 
                      mode='markers', marker=dict(size=10, color='red'),
                      name='Best Temperature'),
            row=1, col=1
        )
        
        ofat_fig.add_trace(
            go.Scatter(x=pHs, y=yields_pH, mode='lines+markers', name='Yield vs pH',
                      marker=dict(color='green')),
            row=1, col=2
        )
        ofat_fig.add_trace(
            go.Scatter(x=[best_pH], y=[yields_pH[best_pH_idx]], 
                      mode='markers', marker=dict(size=10, color='red'),
                      name='Best pH'),
            row=1, col=2
        )
        
        ofat_fig.update_layout(height=400, width=600, showlegend=False,
                              xaxis_title="Temperature (°C)", 
                              xaxis2_title="pH",
                              yaxis_title="Protein Yield (%)",
                              yaxis2_title="Protein Yield (%)")
        
        st.plotly_chart(ofat_fig)
        
        st.markdown(f"""
        **OFAT Results:**
        - Best Temperature: {best_temp:.2f}°C
        - Best pH: {best_pH:.2f}
        - Protein Yield: {final_ofat_yield:.2f}%
        - Total experiments required: 10 (5 for temperature + 5 for pH)
        """)
        
    with col2:
        st.subheader("DOE Approach")
        st.markdown("Factorial design varying both factors simultaneously")
        
        # Define DOE design space
        doe_temp_range = st.slider("Temperature Range (°C)", 
                                 min_value=25.0, max_value=40.0, 
                                 value=(28.0, 36.0), step=0.5,
                                 key="doe_temp_range")
        
        doe_pH_range = st.slider("pH Range", 
                               min_value=5.0, max_value=8.0, 
                               value=(5.5, 7.5), step=0.1,
                               key="doe_pH_range")
        
        # Generate factorial design with center point
        temp_levels = [doe_temp_range[0], (doe_temp_range[0] + doe_temp_range[1])/2, doe_temp_range[1]]
        pH_levels = [doe_pH_range[0], (doe_pH_range[0] + doe_pH_range[1])/2, doe_pH_range[1]]
        
        # Generate the design matrix
        doe_design = []
        for t in temp_levels:
            for p in pH_levels:
                doe_design.append([t, p])
        
        # Run the experiments
        doe_results = []
        for design_point in doe_design:
            t, p = design_point
            yield_value = protein_yield(t, p)
            doe_results.append([t, p, yield_value])
        
        # Convert to dataframe
        doe_df = pd.DataFrame(doe_results, columns=['Temperature', 'pH', 'Yield'])
        
        # Find the best result
        best_idx = doe_df['Yield'].idxmax()
        best_doe_temp = doe_df.loc[best_idx, 'Temperature']
        best_doe_pH = doe_df.loc[best_idx, 'pH']
        best_doe_yield = doe_df.loc[best_idx, 'Yield']
        
        # Create DOE visualization - contour plot
        temp_range_fine = np.linspace(doe_temp_range[0], doe_temp_range[1], 20)
        pH_range_fine = np.linspace(doe_pH_range[0], doe_pH_range[1], 20)
        
        # Generate grid data for contour
        temp_grid, pH_grid = np.meshgrid(temp_range_fine, pH_range_fine)
        z_grid = np.zeros(temp_grid.shape)
        
        for i in range(temp_grid.shape[0]):
            for j in range(temp_grid.shape[1]):
                z_grid[i, j] = protein_yield(temp_grid[i, j], pH_grid[i, j])
        
        # Create contour plot
        doe_fig = go.Figure(data=[
            go.Contour(z=z_grid, x=temp_range_fine, y=pH_range_fine, 
                      colorscale='Viridis', contours_coloring='heatmap'),
            go.Scatter(x=doe_df['Temperature'], y=doe_df['pH'], 
                      mode='markers', marker=dict(size=10, color='white', line=dict(width=1, color='black')),
                      name='Design Points'),
            go.Scatter(x=[best_doe_temp], y=[best_doe_pH], 
                      mode='markers', marker=dict(size=12, color='red', symbol='star'),
                      name='Optimal Point')
        ])
        
        doe_fig.update_layout(
            height=400, width=600,
            xaxis_title="Temperature (°C)",
            yaxis_title="pH",
            title="Response Surface: Protein Yield (%)"
        )
        
        st.plotly_chart(doe_fig)
        
        st.markdown(f"""
        **DOE Results:**
        - Best Temperature: {best_doe_temp:.2f}°C
        - Best pH: {best_doe_pH:.2f}
        - Protein Yield: {best_doe_yield:.2f}%
        - Total experiments required: 9 (3² factorial design with center point)
        - Additional Insight: Complete response surface visualization
        """)
    
    # Compare the approaches
    st.subheader("Comparison of Approaches")
    
    # Calculate true optimum (for educational purposes)
    true_optimum_yield = protein_yield(32, 6.5)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="OFAT Approach", value=f"{final_ofat_yield:.2f}%", 
                 delta=f"{final_ofat_yield - true_optimum_yield:.2f}%")
    
    with col2:
        st.metric(label="DOE Approach", value=f"{best_doe_yield:.2f}%", 
                 delta=f"{best_doe_yield - true_optimum_yield:.2f}%")
    
    with col3:
        st.metric(label="True Optimum", value=f"{true_optimum_yield:.2f}%")
    
    st.markdown("""
    **Key Advantages of DOE Demonstrated:**
    1. **Efficiency**: DOE required 9 experiments compared to 10 for OFAT (efficiency increases dramatically with more factors)
    2. **Interaction Detection**: DOE reveals how temperature and pH interact (visible in the contour plot)
    3. **Design Space Understanding**: DOE provides a complete map of the response across the experimental space
    4. **Robustness**: DOE helps identify regions of stability, not just optimal points
    
    This simple example uses just two factors, but the advantages of DOE become even more significant as the number of factors increases. For instance, a 5-factor experiment would require 32 runs with OFAT but could be effectively explored with just 16-20 runs using fractional factorial DOE designs.
    """)

if __name__ == "__main__":
    show()