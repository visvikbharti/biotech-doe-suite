import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import scipy.stats as stats
from statsmodels.formula.api import ols
import statsmodels.api as sm
from itertools import combinations
import math
import io
import base64

def show():
    st.header("Biotechnology Case Studies")
    
    st.markdown("""
    ## Application of DOE in Bioprocess Development

    This section presents detailed case studies demonstrating the practical application of DOE principles in diverse biotechnology contexts. 
    Each case illustrates how DOE bridges theory and practice, transforming complex bioprocess challenges into structured, data-driven solutions.
    """)
    
    # Create tabs for case studies
    case_studies = [
        "Protein Expression Optimization",
        "Chromatography Purification",
        "Cell Culture Media Optimization",
        "Lyophilization Process",
        "Scale-Down Model Development",
        "Liposomal Formulation",
        "Analytical Method Validation",
        "Vaccine Adjuvant Formulation"
    ]
    
    tabs = st.tabs(case_studies)
    
    # Case Study 1: Recombinant Protein Expression
    with tabs[0]:
        st.subheader("Case Study 1: Optimization of Recombinant Protein Expression")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Expression of recombinant proteins in microbial systems requires balancing numerous interacting factors that affect both quantity and quality of the target protein.

        **Practical Lens**: A biopharmaceutical company developing a therapeutic protein in *E. coli* faced low expression yields and significant batch-to-batch variability. Traditional one-factor-at-a-time approaches had reached a plateau at ~0.8 g/L, well below commercially viable levels.
        """)
        
        # Show timeline/process
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Experimental Design Selection**:
            - Initial screening: Fractional factorial design (2^7-3, Resolution IV)
            - Factors: Temperature, Inducer concentration, pH, Dissolved oxygen, Media composition, Induction timing, Feed strategy
            - Responses: Protein yield, Cell density, Product purity, Inclusion body formation
            
            **Design Rationale**:
            - Resolution IV ensured main effects were not confounded with two-factor interactions
            - 16 runs plus 4 center points provided good statistical power while remaining practical for lab-scale fermentations
            - Center points allowed detection of curvature in the response surface
            """)
        
        with col2:
            # Create a visualization of the experimental process
            st.markdown("### Experimental Process")
            
            process_steps = [
                "Screening Experiment (Fractional Factorial)",
                "Data Analysis & Significant Factor Identification",
                "Characterization Experiment (Central Composite Design)",
                "Response Surface Modeling",
                "Process Optimization",
                "Confirmation Runs",
                "Implementation & Scale-up"
            ]
            
            # Create a timeline visualization
            fig = go.Figure()
            
            # Add timeline steps
            y_pos = 0
            for i, step in enumerate(process_steps):
                fig.add_trace(go.Scatter(
                    x=[i],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=20, color='royalblue'),
                    name=step,
                    hoverinfo='text',
                    text=step
                ))
                
                # Add connecting lines except for the last point
                if i < len(process_steps) - 1:
                    fig.add_trace(go.Scatter(
                        x=[i, i+1],
                        y=[y_pos, y_pos],
                        mode='lines',
                        line=dict(width=2, color='royalblue'),
                        showlegend=False
                    ))
            
            # Update layout
            fig.update_layout(
                showlegend=False,
                yaxis=dict(
                    showticklabels=False,
                    zeroline=False,
                    showgrid=False
                ),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(len(process_steps))),
                    ticktext=process_steps,
                    tickangle=45
                ),
                height=300,
                margin=dict(l=20, r=20, t=20, b=120)
            )
            
            st.plotly_chart(fig)
        
        # Results visualization
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a Pareto chart of effects
            st.markdown("**Significant Factors (Screening Phase)**")
            
            effects = {
                'Temperature': 150,
                'Inducer': 200,
                'pH': -30,
                'Dissolved Oxygen': 45,
                'Media Composition': 20,
                'Induction Timing': 75,
                'Feed Strategy': 125,
                'Temp × Inducer': 100,
                'pH × Inducer': 15,
                'Temp × Feed': 25
            }
            
            # Sort effects by absolute magnitude
            sorted_effects = sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Create dataframe for plotting
            effect_df = pd.DataFrame({
                'Factor': [item[0] for item in sorted_effects],
                'Effect': [item[1] for item in sorted_effects],
                'Absolute Effect': [abs(item[1]) for item in sorted_effects]
            })
            
            # Mark significant effects
            significant = ['Temperature', 'Inducer', 'Feed Strategy', 'Temp × Inducer', 'Induction Timing', 'Dissolved Oxygen']
            effect_df['Significant'] = effect_df['Factor'].isin(significant)
            
            # Create Pareto chart
            fig = px.bar(
                effect_df,
                y='Factor',
                x='Absolute Effect',
                orientation='h',
                color='Significant',
                color_discrete_map={True: 'royalblue', False: 'lightgray'},
                title="Pareto Chart of Effects on Protein Yield"
            )
            
            # Add significance line
            sig_line = 50  # Hypothetical significance threshold
            fig.add_vline(x=sig_line, line_dash="dash", line_color="red")
            
            st.plotly_chart(fig)
        
        with col2:
            # Create response surface contour plot
            st.markdown("**Response Surface from Follow-up Experiment**")
            
            # Generate a grid for the contour plot
            temperature = np.linspace(25, 40, 50)
            inducer = np.linspace(0.1, 1.0, 50)
            temp_grid, inducer_grid = np.meshgrid(temperature, inducer)
            
            # Generate response surface (hypothetical model)
            def protein_yield_model(temp, ind):
                base = 500
                return base + 150*(temp-32.5)/7.5 + 200*(ind-0.55)/0.45 + 100*(temp-32.5)/7.5*(ind-0.55)/0.45 - 40*((temp-32.5)/7.5)**2 - 30*((ind-0.55)/0.45)**2
            
            z_grid = np.zeros_like(temp_grid)
            for i in range(temp_grid.shape[0]):
                for j in range(temp_grid.shape[1]):
                    z_grid[i, j] = protein_yield_model(temp_grid[i, j], inducer_grid[i, j])
            
            # Create contour plot
            fig = go.Figure(data=go.Contour(
                z=z_grid,
                x=temperature,
                y=inducer,
                colorscale='Viridis',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=12, color='white')
                ),
                colorbar=dict(title="Protein Yield (mg/L)"),
            ))
            
            # Add optimal point
            fig.add_trace(go.Scatter(
                x=[28],
                y=[0.4],
                mode='markers',
                marker=dict(
                    color='red',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Conditions'
            ))
            
            # Update layout
            fig.update_layout(
                title="Protein Yield vs. Temperature and Inducer",
                xaxis_title="Temperature (°C)",
                yaxis_title="Inducer Concentration (mM)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Confirmation Experiments**:
            - Three confirmation runs at optimal conditions yielded 2.0 ± 0.2 g/L
            - Results within prediction interval, validating the model
            - Product quality attributes (purity, potency, glycosylation pattern) all within specifications

            **Process Implementation**:
            - Design space defined as: Temperature (26-30°C), Inducer (0.3-0.5 mM), Induction OD (0.9-1.1), Feed rate (0.08-0.12 h⁻¹)
            - Control strategy developed with tighter control on temperature (±1°C) based on sensitivity analysis
            - Scale-up to 200L maintained critical parameter setpoints and achieved comparable yields
            """)
        
        with col2:
            # Create a bar chart comparing before and after optimization
            st.markdown("**Process Performance Improvement**")
            
            comparison_data = pd.DataFrame({
                'Metric': ['Protein Yield (g/L)', 'Batch-to-Batch CV (%)', 'Scale-up Batches', 'Annual Cost ($M)'],
                'Before': [0.8, 25, 4, 6.5],
                'After': [2.0, 15, 1, 2.7]
            })
            
            # Melt the dataframe for easier plotting
            plot_data = pd.melt(comparison_data, id_vars=['Metric'], var_name='Stage', value_name='Value')
            
            # Create bar chart
            fig = px.bar(
                plot_data,
                x='Metric',
                y='Value',
                color='Stage',
                barmode='group',
                title="Process Performance Before and After DOE Optimization",
                color_discrete_map={'Before': 'lightgray', 'After': 'royalblue'}
            )
            
            # Update layout
            fig.update_layout(height=400)
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Sequential DOE Approach**: Progressing from screening to characterization to optimization enabled efficient resource utilization
        2. **Interaction Detection**: The temperature by inducer interaction would have been missed with OFAT approaches
        3. **Quantifiable Business Impact**: 2.5-fold yield improvement and 40% reduction in variability delivered $3.8M annual savings
        4. **Technology Transfer**: Well-characterized design space enabled smooth transfer to manufacturing
        """)
    
    # Case Study 2: Chromatography Purification
    with tabs[1]:
        st.subheader("Case Study 2: Chromatography Method Development for Monoclonal Antibody Purification")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Chromatographic separation of monoclonal antibodies requires optimization of multiple operating parameters to maximize product purity, yield, and process robustness.

        **Practical Lens**: A biotech company developing a therapeutic monoclonal antibody needed to optimize their protein A affinity chromatography step to reduce host cell protein (HCP) impurities while maintaining high recovery. The challenge was compounded by limited material availability for experiments.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Experimental Design Selection**:
            - Design: D-optimal design with 18 runs
            - Factors: Load pH (6.0-7.5), Wash buffer pH (6.0-8.0), Wash buffer salt concentration (0-500 mM), Column load density (20-50 g/L), Number of column volumes in wash step (3-10 CV)
            - Responses: mAb recovery (%), HCP reduction (log₁₀), DNA reduction (log₁₀), Protein A leaching (ppm)

            **Design Rationale**:
            - D-optimal design selected to accommodate constraints:
              - Material limitations restricted total number of experiments
              - Custom factor level combinations needed (pH vs. salt concentration)
              - Irregular experimental region (certain pH-salt combinations cause precipitation)
            """)
        
        with col2:
            # Create a visualization of the design region and experimental points
            st.markdown("### Experimental Design")
            
            # Generate data for a D-optimal design
            np.random.seed(42)
            
            # Generate hypothetical D-optimal design points focusing on corners, edges, and center
            # For visualization purposes only
            d_optimal_points = np.array([
                [6.0, 6.0, 0, 20, 3],    # Corner
                [7.5, 8.0, 500, 50, 10],  # Corner
                [6.0, 8.0, 500, 20, 10],  # Corner
                [7.5, 6.0, 0, 50, 3],     # Corner
                [6.0, 7.0, 250, 35, 6.5],  # Edge
                [7.5, 7.0, 250, 35, 6.5],  # Edge
                [6.75, 6.0, 250, 35, 6.5],  # Edge
                [6.75, 8.0, 250, 35, 6.5],  # Edge
                [6.75, 7.0, 0, 35, 6.5],    # Edge
                [6.75, 7.0, 500, 35, 6.5],  # Edge
                [6.75, 7.0, 250, 20, 6.5],  # Edge
                [6.75, 7.0, 250, 50, 6.5],  # Edge
                [6.75, 7.0, 250, 35, 3],    # Edge
                [6.75, 7.0, 250, 35, 10],   # Edge
                [6.75, 7.0, 250, 35, 6.5],  # Center
                [6.75, 7.0, 250, 35, 6.5],  # Center (replicated)
                [6.75, 7.0, 250, 35, 6.5],  # Center (replicated)
                [6.75, 7.0, 250, 35, 6.5],  # Center (replicated)
            ])
            
            # Create a 3D scatter plot to visualize the design in the main 3 dimensions
            fig = go.Figure()
            
            # Add the D-optimal points
            fig.add_trace(go.Scatter3d(
                x=d_optimal_points[:, 0],  # Load pH
                y=d_optimal_points[:, 1],  # Wash pH
                z=d_optimal_points[:, 2],  # Salt concentration
                mode='markers',
                marker=dict(
                    size=8,
                    color='royalblue',
                    opacity=0.8
                ),
                text=["Run " + str(i+1) for i in range(len(d_optimal_points))],
                name="Experimental Points"
            ))
            
            # Update layout
            fig.update_layout(
                title="D-Optimal Design for Chromatography Optimization",
                scene=dict(
                    xaxis_title="Load pH",
                    yaxis_title="Wash pH",
                    zaxis_title="Salt Concentration (mM)",
                    xaxis=dict(range=[6.0, 7.5]),
                    yaxis=dict(range=[6.0, 8.0]),
                    zaxis=dict(range=[0, 500])
                ),
                height=500
            )
            
            st.plotly_chart(fig)
        
        # Results and analysis
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create coefficient plot
            st.markdown("**Model Coefficients for HCP Reduction**")
            
            # Hypothetical coefficients
            coefficients = {
                'Load pH': 0.4,
                'Wash pH': 0.7,
                'Salt': 0.3,
                'Load Density': -0.2,
                'Wash CV': 0.5,
                'Wash pH × Salt': 0.45,
                'Load pH × Wash pH': 0.15,
                'Wash pH²': -0.6,
                'Salt²': -0.2
            }
            
            # Create dataframe for plotting
            coef_df = pd.DataFrame({
                'Term': list(coefficients.keys()),
                'Coefficient': list(coefficients.values())
            })
            
            # Sort by absolute value
            coef_df['Absolute'] = coef_df['Coefficient'].abs()
            coef_df = coef_df.sort_values('Absolute', ascending=False)
            
            # Create horizontal bar chart
            fig = px.bar(
                coef_df,
                y='Term',
                x='Coefficient',
                orientation='h',
                color='Coefficient',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title="Model Terms for HCP Reduction"
            )
            
            # Update layout
            fig.update_layout(height=400)
            
            st.plotly_chart(fig)
        
        with col2:
            # Create contour plot for optimal region
            st.markdown("**HCP Reduction vs. Wash pH and Salt**")
            
            # Create grid
            wash_pH = np.linspace(6.0, 8.0, 50)
            salt = np.linspace(0, 500, 50)
            pH_grid, salt_grid = np.meshgrid(wash_pH, salt)
            
            # Hypothetical model
            def hcp_reduction_model(pH, salt):
                return 2.0 + 0.7*(pH-7.0) + 0.3*(salt-250)/250 + 0.45*(pH-7.0)*(salt-250)/250 - 0.6*((pH-7.0)**2) - 0.2*((salt-250)/250)**2
            
            z_grid = np.zeros_like(pH_grid)
            for i in range(pH_grid.shape[0]):
                for j in range(pH_grid.shape[1]):
                    z_grid[i, j] = hcp_reduction_model(pH_grid[i, j], salt_grid[i, j])
            
            # Create contour plot
            fig = go.Figure(data=go.Contour(
                z=z_grid,
                x=wash_pH,
                y=salt,
                colorscale='Viridis',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=12, color='white')
                ),
                colorbar=dict(title="HCP Reduction (log₁₀)"),
            ))
            
            # Add optimal point
            fig.add_trace(go.Scatter(
                x=[7.3],
                y=[350],
                mode='markers',
                marker=dict(
                    color='red',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Conditions'
            ))
            
            # Add sweet spot region
            # Assuming HCP reduction > 3.0 log and mAb recovery > 95%
            sweet_spot = np.array([
                [7.1, 300], [7.4, 300], [7.4, 400], [7.1, 400], [7.1, 300]
            ])
            
            fig.add_trace(go.Scatter(
                x=sweet_spot[:, 0],
                y=sweet_spot[:, 1],
                mode='lines',
                line=dict(color='red', width=2, dash='dot'),
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.1)',
                name='Design Space'
            ))
            
            # Update layout
            fig.update_layout(
                title="HCP Reduction vs. Wash pH and Salt",
                xaxis_title="Wash pH",
                yaxis_title="Salt Concentration (mM)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Scale-Up and Verification**:
            - Method transferred to 20 mL column scale with three confirmation runs
            - Results consistent with model predictions: 98.5% recovery, 3.7 log₁₀ HCP reduction
            - Method robustness verified via deliberate small perturbations around setpoints

            **Control Strategy Development**:
            - Critical process parameters: Load pH (6.9 ± 0.1), Wash pH (7.3 ± 0.2)
            - Key process parameters: Salt concentration (350 ± 50 mM), Wash volume (9 ± 1 CV)
            - Online pH monitoring implemented based on sensitivity analysis
            - Load density range expanded to 20-60 g/L based on robustness study
            """)
        
        with col2:
            # Create a radar chart showing multiple response optimization
            st.markdown("**Multi-Response Optimization Results**")
            
            # Create data for radar chart
            categories = ['mAb Recovery (%)', 'HCP Reduction (log₁₀)', 'DNA Reduction (log₁₀)', 'Protein A Leaching (ppm)', 'Process Time (h)']
            
            # Values for before and after optimization (scaled for radar chart visualization)
            before_values = [92, 2.5, 3.0, 25, 3.5]
            after_values = [98.5, 3.7, 4.2, 8, 2.8]
            
            # Create radar chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=before_values,
                theta=categories,
                fill='toself',
                name='Before Optimization',
                line_color='lightgray'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=after_values,
                theta=categories,
                fill='toself',
                name='After Optimization',
                line_color='royalblue'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    )
                ),
                title="Performance Before and After Optimization",
                height=400
            )
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Design Efficiency**: D-optimal design enabled comprehensive chromatography optimization with limited material
        2. **Critical Interactions**: The interaction between wash pH and salt concentration was critical for HCP removal
        3. **Robust Design Space**: Well-defined operating ranges enabled flexible manufacturing with consistent quality
        4. **Business Impact**: 2-fold reduction in HCP levels and method robust across three different mAb candidates
        """)
    
    # Case Study 3: Cell Culture Media Optimization
    with tabs[2]:
        st.subheader("Case Study 3: Cell Culture Media Optimization for CHO Cell Production")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Mammalian cell culture media formulation involves complex interactions among numerous components that collectively impact cell growth, productivity, and product quality attributes.

        **Practical Lens**: A biotechnology company developing a glycoprotein therapeutic needed to optimize their CHO cell culture media to increase product titer while maintaining critical quality attributes, particularly glycosylation patterns essential for biological activity.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Sequential Approach with Multiple Designs**:
            1. **Screening**: Plackett-Burman design (20 runs)
               - 19 media components varied ±50% from baseline
               - Responses: Viable cell density, viability, titer, specific productivity
            
            2. **Characterization**: Fractional factorial (2^6-1, Resolution VI) with 4 center points
               - Six significant components identified from screening
               - Additional responses: Glycosylation pattern, charge variants
            
            3. **Optimization**: I-optimal mixture design (21 runs)
               - Final optimization of ratios between key components
               - Focus on interaction effects and quality attributes
            
            **Design Rationale**:
            - Sequential approach conserved resources while systematically building knowledge
            - High-resolution follow-up ensured clear separation of main effects and interactions
            """)
        
        with col2:
            # Create visualization of the screening phase
            st.markdown("### Screening Phase Visualization")
            
            # Create a heatmap of component effects on multiple responses
            # Hypothetical data for visualization
            components = [
                'Glucose', 'Glutamine', 'Asparagine', 'Serine', 'Copper', 
                'Zinc', 'Iron', 'Vitamins', 'Lipids', 'Buffer'
            ]
            
            responses = ['Cell Density', 'Viability', 'Titer', 'Productivity', 'Glycosylation']
            
            # Effect matrix (random values for visualization)
            np.random.seed(42)
            effect_matrix = np.random.normal(0, 1, (len(components), len(responses)))
            
            # Highlight important components (copper, glutamine, asparagine, glucose, zinc, iron)
            important_idx = [1, 2, 4, 5, 6, 0]
            for i in important_idx:
                effect_matrix[i] = effect_matrix[i] * 2.5
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=effect_matrix,
                x=responses,
                y=components,
                colorscale='RdBu_r',
                zmid=0,
                colorbar=dict(title="Standardized Effect")
            ))
            
            # Update layout
            fig.update_layout(
                title="Media Component Effects on Cell Culture Responses",
                xaxis_title="Responses",
                yaxis_title="Media Components",
                height=500
            )
            
            st.plotly_chart(fig)
        
        # Results and analysis
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create interaction plot
            st.markdown("**Key Interaction: Glutamine × Copper**")
            
            # Create data for interaction plot
            glutamine_levels = ['Low', 'High']
            copper_levels = ['Low', 'High']
            
            # Hypothetical glycosylation values
            glycosylation = np.array([
                [80, 65],  # Low glutamine, [Low copper, High copper]
                [70, 90]   # High glutamine, [Low copper, High copper]
            ])
            
            # Create plot
            fig = go.Figure()
            
            # Add traces for each level of glutamine
            for i, gln_level in enumerate(glutamine_levels):
                fig.add_trace(go.Scatter(
                    x=copper_levels,
                    y=glycosylation[i],
                    mode='lines+markers',
                    name=f'Glutamine = {gln_level}',
                    line=dict(width=2),
                    marker=dict(size=10)
                ))
            
            # Update layout
            fig.update_layout(
                title="Interaction Effect on Glycosylation",
                xaxis_title="Copper Level",
                yaxis_title="Glycosylation (%)",
                height=350
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Interpretation**: The interaction between glutamine and copper significantly impacts glycosylation patterns. 
            High levels of both components produce the optimal glycosylation profile, while high copper with low glutamine 
            produces the worst outcome. This interaction would be missed by one-factor-at-a-time approaches.
            """)
        
        with col2:
            # Create contour plot for optimization phase
            st.markdown("**Optimization Phase Results**")
            
            # Create grid for contour plot
            glutamine = np.linspace(2, 8, 50)  # mM
            asparagine = np.linspace(2, 8, 50)  # mM
            gln_grid, asn_grid = np.meshgrid(glutamine, asparagine)
            
            # Hypothetical model for titer
            def titer_model(gln, asn):
                return 3.0 + 0.8*(gln-5)/3 + 0.5*(asn-5)/3 + 0.4*(gln-5)/3*(asn-5)/3 - 0.6*((gln-5)/3)**2 - 0.3*((asn-5)/3)**2
            
            # Hypothetical model for glycosylation
            def glycosylation_model(gln, asn):
                return 85 + 5*(gln-5)/3 - 3*(asn-5)/3 - 0.3*(gln-5)/3*(asn-5)/3 - 4*((gln-5)/3)**2 - 2*((asn-5)/3)**2
            
            # Calculate responses
            titer_grid = np.zeros_like(gln_grid)
            glyco_grid = np.zeros_like(gln_grid)
            
            for i in range(gln_grid.shape[0]):
                for j in range(gln_grid.shape[1]):
                    titer_grid[i, j] = titer_model(gln_grid[i, j], asn_grid[i, j])
                    glyco_grid[i, j] = glycosylation_model(gln_grid[i, j], asn_grid[i, j])
            
            # Create contour plot with overlaid sweet spot
            fig = go.Figure()
            
            # Add titer contours
            fig.add_trace(go.Contour(
                z=titer_grid,
                x=glutamine,
                y=asparagine,
                colorscale='Blues',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=10, color='white')
                ),
                colorbar=dict(title="Titer (g/L)", x=0.45),
                name="Titer"
            ))
            
            # Add glycosylation contour lines
            fig.add_trace(go.Contour(
                z=glyco_grid,
                x=glutamine,
                y=asparagine,
                colorscale='Greens',
                contours=dict(
                    coloring='lines',
                    showlabels=True
                ),
                line=dict(width=2),
                colorbar=dict(title="Glycosylation (%)", x=1.0),
                name="Glycosylation"
            ))
            
            # Add sweet spot (intersection of high titer and optimal glycosylation)
            # Assuming titer > 4.5 g/L and glycosylation > 85%
            sweet_spot = np.array([
                [5.5, 4.5], [6.5, 4.5], [6.5, 5.5], [5.5, 5.5], [5.5, 4.5]
            ])
            
            fig.add_trace(go.Scatter(
                x=sweet_spot[:, 0],
                y=sweet_spot[:, 1],
                mode='lines',
                line=dict(color='red', width=2, dash='dot'),
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.2)',
                name='Design Space'
            ))
            
            # Add optimal point
            fig.add_trace(go.Scatter(
                x=[6.0],
                y=[5.0],
                mode='markers',
                marker=dict(
                    color='red',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Formulation'
            ))
            
            # Update layout
            fig.update_layout(
                title="Overlay Plot of Titer and Glycosylation",
                xaxis_title="Glutamine (mM)",
                yaxis_title="Asparagine (mM)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        # Implementation and validation section
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Media Formulation Development**:
            - Optimized formulation: 6 mM glutamine, 4 mM asparagine, 2 μM copper, 3 μM zinc (with optimized ratios to other components)
            - Predicted performance: 5.8 g/L titer, >95% viability, target glycosylation profile

            **Confirmation and Scale-Up**:
            - Three replicate runs in 2L bioreactors validated performance: 5.5 ± 0.3 g/L titer
            - Glycosylation pattern within target range for all quality attributes
            - Design space verified at 50L scale with comparable results
            
            **Robustness Assessment**:
            - Monte Carlo simulation of component variability conducted
            - Raw material specifications tightened for critical components
            - Control strategy implemented with in-process testing
            """)
        
        with col2:
            # Create visualization of before/after performance
            st.markdown("**Performance Impact**")
            
            # Create data for performance comparison
            metrics = ['Titer (g/L)', 'Glycosylation CV (%)', 'Process Time (days)', 'Cost of Goods (relative)']
            before = [3.5, 15, 14, 1.0]
            after = [5.5, 6, 12, 0.75]
            
            # Create bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=metrics,
                y=before,
                name='Before Optimization',
                marker_color='lightgray'
            ))
            
            fig.add_trace(go.Bar(
                x=metrics,
                y=after,
                name='After Optimization',
                marker_color='royalblue'
            ))
            
            # Update layout
            fig.update_layout(
                title="Process Performance Comparison",
                xaxis_title="Metric",
                yaxis_title="Value",
                barmode='group',
                height=350
            )
            
            st.plotly_chart(fig)
            
            # Add a line chart showing growth curve improvement
            st.markdown("**Cell Growth Profile Improvement**")
            
            # Time data
            days = np.array([0, 2, 4, 6, 8, 10, 12, 14])
            
            # Create hypothetical growth curves
            base_vcd = 2 * np.exp(0.3 * days) / (1 + np.exp(0.3 * days) / 12)
            optimized_vcd = 2 * np.exp(0.4 * days) / (1 + np.exp(0.4 * days) / 18)
            
            # Create line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=days,
                y=base_vcd,
                mode='lines+markers',
                name='Baseline Media',
                line=dict(color='lightgray', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=days,
                y=optimized_vcd,
                mode='lines+markers',
                name='Optimized Media',
                line=dict(color='royalblue', width=2)
            ))
            
            # Update layout
            fig.update_layout(
                title="Cell Growth Profiles",
                xaxis_title="Day",
                yaxis_title="Viable Cell Density (10^6 cells/mL)",
                height=350
            )
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Sequential Strategy**: Progressive experimental designs enabled efficient exploration of a complex media formulation space
        2. **Component Interactions**: Copper-glutamine interaction highlighted the importance of multi-factor optimization
        3. **Quality Integration**: Simultaneous optimization of titer and glycosylation ensured product efficacy
        4. **Business Impact**: 40% increase in titer and more consistent quality led to 25% reduction in cost of goods
        """)
    
    # Case Study 4: Lyophilization Process
    with tabs[3]:
        st.subheader("Case Study 4: Lyophilization Process Development for Protein Formulation")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Lyophilization (freeze-drying) preserves protein therapeutics but involves complex interactions between formulation components and process parameters that affect both product quality and process efficiency.

        **Practical Lens**: A biopharmaceutical company developing a sensitive protein therapeutic faced stability challenges during lyophilization. The traditional approach resulted in inconsistent cake appearance, high residual moisture, and significant activity loss after reconstitution.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Experimental Design Selection**:
            - Split-plot design with 36 runs
            - Whole-plot factors (hard to change): Shelf temperature (-45°C to -25°C), Primary drying temperature (-25°C to -5°C)
            - Sub-plot factors (easy to change): Ramp rate (0.5-2°C/min), Annealing (yes/no), Sucrose:mannitol ratio (1:0 to 1:3), Protein concentration (1-10 mg/mL)
            - Responses: Residual moisture, Reconstitution time, Protein activity, Cake appearance, Process time

            **Design Rationale**:
            - Split-plot design accommodated lyophilization equipment constraints
            - Multiple vials could be processed in each lyophilization cycle
            - Design balanced statistical power with practical execution constraints
            """)
        
        with col2:
            # Create visualization of split-plot design
            st.markdown("### Split-Plot Design Structure")
            
            # Create diagram illustrating split-plot structure
            fig = go.Figure()
            
            # Define whole plots (different lyophilization cycles)
            whole_plots = [
                {"temp": -45, "dry": -25, "color": "blue", "name": "Cycle 1"},
                {"temp": -45, "dry": -15, "color": "green", "name": "Cycle 2"},
                {"temp": -35, "dry": -25, "color": "red", "name": "Cycle 3"},
                {"temp": -35, "dry": -15, "color": "purple", "name": "Cycle 4"},
                {"temp": -25, "dry": -25, "color": "orange", "name": "Cycle 5"},
                {"temp": -25, "dry": -15, "color": "brown", "name": "Cycle 6"}
            ]
            
            # Create layout with whole plots and subplots
            for i, wp in enumerate(whole_plots):
                # Position whole plots in a 3×2 grid
                x_base = (i % 2) * 10
                y_base = (i // 2) * 10
                
                # Draw whole plot box
                fig.add_shape(
                    type="rect",
                    x0=x_base, y0=y_base,
                    x1=x_base+8, y1=y_base+8,
                    line=dict(color=wp["color"], width=2),
                    fillcolor=f"rgba({','.join([str(int(i*255)) for i in px.colors.hex_to_rgb(px.colors.qualitative.Plotly[i % 10])])},0.1)"
                )
                
                # Add whole plot label
                fig.add_annotation(
                    x=x_base+4, y=y_base+7.5,
                    text=f"{wp['name']}: Shelf Temp = {wp['temp']}°C, Dry Temp = {wp['dry']}°C",
                    showarrow=False,
                    font=dict(size=10, color=wp["color"])
                )
                
                # Add sub-plot points (vials with different formulations)
                for j in range(6):  # 6 subplots per whole plot
                    x_sub = x_base + 1 + (j % 3) * 2
                    y_sub = y_base + 1 + (j // 3) * 2
                    
                    fig.add_trace(go.Scatter(
                        x=[x_sub],
                        y=[y_sub],
                        mode='markers',
                        marker=dict(
                            color=wp["color"],
                            size=12,
                            line=dict(color='white', width=1)
                        ),
                        name=wp["name"] if j == 0 else None,
                        showlegend=(j == 0)
                    ))
                    
                    # Add subplot label (vial number)
                    fig.add_annotation(
                        x=x_sub, y=y_sub-0.5,
                        text=f"Vial {i*6+j+1}",
                        showarrow=False,
                        font=dict(size=8)
                    )
            
            # Update layout
            fig.update_layout(
                title="Split-Plot Design Structure",
                xaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[-1, 20]
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[-1, 30],
                    scaleanchor="x",
                    scaleratio=1
                ),
                height=600,
                showlegend=True
            )
            
            st.plotly_chart(fig)
        
        # Results visualization
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create half-normal plot of effects
            st.markdown("**Half-Normal Plot of Effects**")
            
            # Create hypothetical effect data
            effects = {
                'A: Shelf Temp': 0.4,
                'B: Primary Drying Temp': 1.8,
                'C: Ramp Rate': 0.2,
                'D: Annealing': 1.2,
                'E: Sucrose:Mannitol': 0.8,
                'F: Protein Conc': 0.3,
                'AB': 0.25,
                'AD': 0.7,
                'AE': 0.15,
                'BD': 0.9,
                'BE': 0.45,
                'DE': 1.1
            }
            
            # Create sorted array of absolute effects
            abs_effects = np.array([abs(val) for val in effects.values()])
            sorted_idx = np.argsort(abs_effects)
            terms = list(effects.keys())
            
            sorted_abs_effects = abs_effects[sorted_idx]
            sorted_terms = [terms[i] for i in sorted_idx]
            
            # Calculate half-normal quantiles
            n = len(abs_effects)
            p = (np.arange(1, n + 1) - 0.5) / (2 * n)
            z = stats.norm.ppf((1 + p) / 2)
            
            # Create half-normal plot
            fig = go.Figure()
            
            # Add effects points
            fig.add_trace(go.Scatter(
                x=z,
                y=sorted_abs_effects,
                mode='markers+text',
                marker=dict(
                    size=10,
                    color='royalblue'
                ),
                text=sorted_terms,
                textposition="top right",
                name="Effects"
            ))
            
            # Add reference line for noise
            # Use first half of points to establish noise trend
            noise_points = len(sorted_abs_effects) // 2
            slope, intercept, _, _, _ = stats.linregress(z[:noise_points], sorted_abs_effects[:noise_points])
            
            line_x = np.linspace(0, max(z), 100)
            line_y = slope * line_x + intercept
            
            fig.add_trace(go.Scatter(
                x=line_x,
                y=line_y,
                mode='lines',
                line=dict(
                    color='red',
                    dash='dash'
                ),
                name="Reference Line"
            ))
            
            # Update layout
            fig.update_layout(
                title="Half-Normal Plot of Standardized Effects on Protein Activity",
                xaxis_title="Half-Normal Quantile",
                yaxis_title="|Standardized Effect|",
                height=450
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Interpretation**: The half-normal plot identifies significant effects that deviate from the noise trend line.
            Primary drying temperature (B), annealing (D), the annealing-sucrose:mannitol interaction (DE), and the
            primary drying temperature-annealing interaction (BD) show the largest effects on protein activity after reconstitution.
            """)
        
        with col2:
            # Create interaction plot of critical interaction
            st.markdown("**Critical Interaction: Annealing × Excipient Ratio**")
            
            # Create data for the interaction plot
            annealing_levels = ['No', 'Yes']
            ratio_levels = ['1:0', '1:1', '1:3']
            
            # Hypothetical data for protein activity
            activity_data = np.array([
                [82, 78, 65],  # No annealing
                [85, 90, 95]   # With annealing
            ])
            
            # Create interaction plot
            fig = go.Figure()
            
            # Add traces for each annealing level
            for i, level in enumerate(annealing_levels):
                fig.add_trace(go.Scatter(
                    x=ratio_levels,
                    y=activity_data[i],
                    mode='lines+markers',
                    name=f'Annealing = {level}',
                    line=dict(width=2),
                    marker=dict(size=10)
                ))
            
            # Update layout
            fig.update_layout(
                title="Annealing × Sucrose:Mannitol Interaction",
                xaxis_title="Sucrose:Mannitol Ratio",
                yaxis_title="Protein Activity (%)",
                height=350
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Key Finding**: Without annealing, increasing mannitol content reduces protein activity. 
            With annealing, the opposite occurs - higher mannitol content improves activity. 
            This interaction is due to mannitol crystallization during annealing, which improves 
            cake structure and protein stabilization.
            """)
        
        # Process optimization results
        st.markdown("### Process Modeling and Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create process model visualization
            st.markdown("**Process Parameter Optimization**")
            
            # Create contour plot for primary drying temp vs. shelf temperature
            shelf_temp = np.linspace(-45, -25, 50)
            drying_temp = np.linspace(-25, -5, 50)
            
            shelf_grid, drying_grid = np.meshgrid(shelf_temp, drying_temp)
            
            # Hypothetical model for cycle time
            def cycle_time_model(shelf, drying):
                return 36 - 0.3*(shelf+35) - 0.6*(drying+15)
            
            # Hypothetical model for product activity
            def activity_model(shelf, drying):
                return 95 - 0.2*(shelf+35)**2 - 0.4*(drying+15)
            
            # Calculate response surfaces
            time_grid = np.zeros_like(shelf_grid)
            activity_grid = np.zeros_like(shelf_grid)
            
            for i in range(shelf_grid.shape[0]):
                for j in range(shelf_grid.shape[1]):
                    time_grid[i, j] = cycle_time_model(shelf_grid[i, j], drying_grid[i, j])
                    activity_grid[i, j] = activity_model(shelf_grid[i, j], drying_grid[i, j])
            
            # Create contour plot
            fig = go.Figure()
            
            # Add cycle time contours
            fig.add_trace(go.Contour(
                z=time_grid,
                x=shelf_temp,
                y=drying_temp,
                colorscale='Blues',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=10, color='white')
                ),
                colorbar=dict(title="Cycle Time (h)", x=0.45),
                name="Cycle Time"
            ))
            
            # Add product activity contour lines
            fig.add_trace(go.Contour(
                z=activity_grid,
                x=shelf_temp,
                y=drying_temp,
                colorscale='Reds',
                contours=dict(
                    coloring='lines',
                    showlabels=True
                ),
                line=dict(width=2),
                colorbar=dict(title="Activity (%)", x=1.0),
                name="Product Activity"
            ))
            
            # Add optimal point
            fig.add_trace(go.Scatter(
                x=[-40],
                y=[-20],
                mode='markers',
                marker=dict(
                    color='green',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Conditions'
            ))
            
            # Update layout
            fig.update_layout(
                title="Process Parameters Optimization",
                xaxis_title="Shelf Temperature (°C)",
                yaxis_title="Primary Drying Temperature (°C)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        with col2:
            # Create formulation optimization visualization
            st.markdown("**Formulation Optimization**")
            
            # Create scatter plot of residual moisture vs. protein activity with bubbles sized by reconstitution time
            # Hypothetical data
            np.random.seed(42)
            
            n_points = 10
            residual_moisture = np.random.uniform(0.2, 3.0, n_points)
            protein_activity = np.random.uniform(75, 98, n_points)
            recon_time = np.random.uniform(10, 60, n_points)
            
            # Formulation labels (for hover information)
            formulations = [
                "1:0, No Annealing",
                "1:0, With Annealing",
                "1:1, No Annealing",
                "1:1, With Annealing",
                "1:3, No Annealing",
                "1:3, With Annealing",
                "1:0, 5 mg/mL",
                "1:1, 5 mg/mL",
                "1:3, 5 mg/mL",
                "Optimized Formulation"
            ]
            
            # Manually set optimized formulation point
            residual_moisture[-1] = 0.5
            protein_activity[-1] = 96
            recon_time[-1] = 12
            
            # Create customized marker colors
            marker_colors = ['gray'] * (n_points-1) + ['green']
            
            # Create bubble chart
            fig = px.scatter(
                x=residual_moisture,
                y=protein_activity,
                size=recon_time,
                size_max=30,
                hover_name=formulations,
                labels={
                    "x": "Residual Moisture (%)",
                    "y": "Protein Activity (%)",
                    "size": "Reconstitution Time (s)"
                },
                title="Formulation Performance"
            )
            
            # Update marker colors
            fig.update_traces(marker=dict(color=marker_colors))
            
            # Add annotations for optimal point
            fig.add_annotation(
                x=residual_moisture[-1],
                y=protein_activity[-1],
                text="Optimal Formulation",
                showarrow=True,
                arrowhead=1,
                ax=40,
                ay=-40
            )
            
            # Update layout
            fig.update_layout(height=400)
            
            st.plotly_chart(fig)
            
            # Add table of optimal formulation
            st.markdown("**Optimized Formulation and Process**")
            
            optimal_params = pd.DataFrame({
                'Parameter': [
                    'Shelf Temperature', 
                    'Primary Drying Temperature', 
                    'Ramp Rate', 
                    'Annealing',
                    'Sucrose:Mannitol Ratio',
                    'Protein Concentration'
                ],
                'Value': [
                    '-40°C',
                    '-20°C',
                    '1°C/min',
                    'Yes (2h at -20°C)',
                    '1:2',
                    '5 mg/mL'
                ]
            })
            
            st.dataframe(optimal_params)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Process Parameter Selection**:
            - Optimized parameters: Freezing at -40°C, annealing at -20°C for 2h, primary drying at -20°C
            - Formulation: 1:2 sucrose:mannitol ratio, 5 mg/mL protein concentration
            - Predicted performance: <1% residual moisture, >95% protein activity, 24h cycle time

            **Verification and Scale-Up**:
            - Laboratory verification confirmed model predictions
            - Scale-up to production lyophilizer with adjusted shelf temperature setpoints
            - Heat transfer coefficient measured and used to refine process parameters
            
            **Design Space Mapping**:
            - Process design space defined around critical parameters
            - Chamber pressure identified as additional critical parameter during scale-up
            - Edge of failure analysis performed to establish safe operating ranges
            """)
        
        with col2:
            # Create before/after comparison chart
            st.markdown("**Process Improvement Results**")
            
            # Data for comparison
            metrics = ['Residual Moisture (%)', 'Protein Activity (%)', 'Cycle Time (h)', 'Cake Appearance (1-10)']
            before = [2.5, 85, 36, 5]
            after = [0.8, 96, 24, 9]
            
            # Create side-by-side bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=metrics,
                y=before,
                name='Before Optimization',
                marker_color='lightgray'
            ))
            
            fig.add_trace(go.Bar(
                x=metrics,
                y=after,
                name='After Optimization',
                marker_color='royalblue'
            ))
            
            # Update layout
            fig.update_layout(
                title="Process Performance Comparison",
                xaxis_title="Metric",
                yaxis_title="Value",
                barmode='group',
                height=350
            )
            
            st.plotly_chart(fig)
            
            # Add lyophilization cake images (simulated)
            st.markdown("**Cake Appearance Improvement**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Before:**")
                st.image("https://via.placeholder.com/300x200.png?text=Uneven+Cake+Structure", caption="Poor uniformity, partial collapse")
            
            with col2:
                st.markdown("**After:**")
                st.image("https://via.placeholder.com/300x200.png?text=Uniform+Elegant+Cake", caption="Uniform, elegant cake structure")
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Split-Plot Efficiency**: Split-plot design maximized experimental efficiency given equipment constraints
        2. **Critical Interactions**: Annealing by excipient ratio interaction was key to product stability
        3. **Process-Formulation Integration**: Simultaneous optimization of process and formulation led to superior results
        4. **Business Impact**: 30% reduction in cycle time while improving product quality
        """)
    
    # Case Study 5: Scale-Down Model Development
    with tabs[4]:
        st.subheader("Case Study 5: Scale-Down Model Development for Tech Transfer")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Scale-down models enable efficient process characterization and troubleshooting by replicating large-scale manufacturing behavior in laboratory-scale systems through careful parameter mapping.

        **Practical Lens**: A biotechnology company needed to transfer a complex mammalian cell culture process from a contract manufacturer to their new in-house facility. Key challenges included differences in bioreactor geometry, sparger design, and control systems that could impact process performance and product quality.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Multi-stage Experimental Strategy**:
            1. **Parameter Screening**: Definitive screening design (13 runs)
               - Factors: Power input per volume (P/V), Gas flow rate, Sparger type, Impeller configuration, Control strategy, Media preparation method
               - Responses: kLa, mixing time, cell growth profile, metabolite profiles
            
            2. **Scale-Down Model Refinement**: Central composite design (20 runs)
               - Focused on significant parameters from screening
               - Additional responses: Dissolved oxygen profiles, shear stress indicators, product quality attributes
            
            3. **Robustness Verification**: Custom D-optimal design (15 runs)
               - Stress testing around nominal operating points
               - Challenge conditions beyond normal manufacturing ranges
            
            **Design Rationale**:
            - Definitive screening efficiently identified critical scaling parameters with minimal runs
            - CCD enabled response surface modeling to map the relationship between scales
            - D-optimal design accommodated irregular experimental region and practical constraints
            """)
        
        with col2:
            # Create visualization of scale-down model development process
            st.markdown("### Scale-Down Model Development Process")
            
            # Create process diagram
            fig = go.Figure()
            
            # Create diagram boxes
            steps = [
                {"x": 0.5, "y": 0.9, "text": "Commercial Scale\nProcess Data Analysis", "width": 0.8, "height": 0.1, "color": "lightgrey"},
                {"x": 0.2, "y": 0.7, "text": "Geometric\nSimilarity", "width": 0.3, "height": 0.1, "color": "lightblue"},
                {"x": 0.5, "y": 0.7, "text": "Process\nScaling Rules", "width": 0.3, "height": 0.1, "color": "lightblue"},
                {"x": 0.8, "y": 0.7, "text": "Equipment\nDifferences", "width": 0.3, "height": 0.1, "color": "lightblue"},
                {"x": 0.5, "y": 0.5, "text": "DOE Screening\n(13 runs)", "width": 0.8, "height": 0.1, "color": "lightgreen"},
                {"x": 0.5, "y": 0.3, "text": "DOE Refinement\n(20 runs)", "width": 0.8, "height": 0.1, "color": "lightgreen"},
                {"x": 0.3, "y": 0.1, "text": "DOE Robustness\n(15 runs)", "width": 0.4, "height": 0.1, "color": "lightgreen"},
                {"x": 0.7, "y": 0.1, "text": "Qualified\nScale-Down Model", "width": 0.4, "height": 0.1, "color": "gold"}
            ]
            
            # Add boxes
            for step in steps:
                fig.add_shape(
                    type="rect",
                    x0=step["x"] - step["width"]/2,
                    y0=step["y"] - step["height"]/2,
                    x1=step["x"] + step["width"]/2,
                    y1=step["y"] + step["height"]/2,
                    line=dict(color="black", width=2),
                    fillcolor=step["color"],
                )
                
                fig.add_annotation(
                    x=step["x"],
                    y=step["y"],
                    text=step["text"],
                    showarrow=False,
                    font=dict(size=12)
                )
            
            # Add arrows connecting steps
            arrows = [
                {"x": 0.5, "y": 0.84, "ax": 0, "ay": -40},  # Top to middle
                {"x": 0.2, "y": 0.64, "ax": 80, "ay": -40},  # Upper left to middle
                {"x": 0.5, "y": 0.64, "ax": 0, "ay": -40},   # Upper middle to middle
                {"x": 0.8, "y": 0.64, "ax": -80, "ay": -40}, # Upper right to middle
                {"x": 0.5, "y": 0.44, "ax": 0, "ay": -40},   # Middle to lower middle
                {"x": 0.5, "y": 0.24, "ax": -60, "ay": -40}, # Lower middle to lower left
                {"x": 0.5, "y": 0.24, "ax": 60, "ay": -40},  # Lower middle to lower right
                {"x": 0.5, "y": 0.1, "ax": 60, "ay": 0}      # Lower left to lower right
            ]
            
            for arrow in arrows:
                fig.add_annotation(
                    x=arrow["x"],
                    y=arrow["y"],
                    ax=arrow["ax"],
                    ay=arrow["ay"],
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowwidth=2
                )
            
            # Update layout
            fig.update_layout(
                showlegend=False,
                xaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[0, 1]
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[0, 1]
                ),
                height=500,
                title="Scale-Down Model Development Process"
            )
            
            st.plotly_chart(fig)
        
        # Results and analysis section
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create effect importance visualization from screening phase
            st.markdown("**Critical Scaling Parameters Identified**")
            
            # Hypothetical effect data from screening
            parameters = [
                'Power Input (P/V)', 
                'Gas Flow Rate', 
                'Sparger Type',
                'Impeller Configuration',
                'Control Strategy',
                'Media Preparation'
            ]
            
            importance = [0.85, 0.92, 0.76, 0.65, 0.45, 0.22]
            
            # Create horizontal bar chart
            fig = px.bar(
                x=importance,
                y=parameters,
                orientation='h',
                color=importance,
                color_continuous_scale='Blues',
                title="Parameter Importance for Scale-Down Model"
            )
            
            # Add a vertical line for significance threshold
            fig.add_vline(x=0.5, line_dash="dash", line_color="red")
            
            # Update layout
            fig.update_layout(
                xaxis_title="Relative Importance",
                yaxis_title="Scale-Down Parameter",
                height=350
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Interpretation**: The screening phase identified power input per volume (P/V) and gas flow rate 
            as the most critical parameters for matching large-scale behavior, followed by sparger type and impeller
            configuration. These factors have the strongest influence on oxygen transfer (kLa) and mixing patterns
            that directly impact cell growth and metabolism.
            """)
        
        with col2:
            # Create correlation visualization for scale-up parameters
            st.markdown("**Parameter Correlation Analysis**")
            
            # Create hypothetical correlation data
            responses = ['VCD', 'Viability', 'Titer', 'Glycosylation', 'Charge Variants']
            
            # Correlation matrix between kLa and responses
            correlation_data = np.array([
                [0.92, 0.45, 0.78, 0.38, 0.25],  # P/V correlations
                [0.85, 0.52, 0.71, 0.41, 0.22],  # Gas flow correlations
                [0.65, 0.81, 0.57, 0.74, 0.68],  # DO profile correlations
                [0.44, 0.39, 0.82, 0.89, 0.91]   # Mixing time correlations
            ])
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=correlation_data,
                x=responses,
                y=['P/V', 'Gas Flow Rate', 'DO Profile', 'Mixing Time'],
                colorscale='Viridis',
                zmin=0,
                zmax=1,
                colorbar=dict(title="Correlation")
            ))
            
            # Update layout
            fig.update_layout(
                title="Commercial Scale Parameter Correlations with Responses",
                xaxis_title="Response",
                yaxis_title="Scale-Up Parameter",
                height=350
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Key Finding**: The correlation analysis reveals that power input per volume (P/V) and gas flow rate 
            strongly correlate with cell growth (VCD) and productivity (Titer), while mixing time correlations most 
            strongly with product quality attributes (glycosylation and charge variants). These insights guided the
            refinement of the scale-down model to ensure comparable product quality.
            """)
        
        # Scale-down model refinement
        st.markdown("### Scale-Down Model Refinement")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create visualization of response surface model
            st.markdown("**Response Surface Model**")
            
            # Create grid for contour plot
            p_v_range = np.linspace(20, 60, 50)  # W/m³
            gas_range = np.linspace(0.01, 0.1, 50)  # vvm
            p_v_grid, gas_grid = np.meshgrid(p_v_range, gas_range)
            
            # Hypothetical model for kLa mapping
            def kla_model(p_v, gas):
                return 10 + 0.2*p_v + 250*gas + 0.1*p_v*gas - 0.001*p_v**2 - 400*gas**2
            
            # Calculate kLa surface
            kla_grid = np.zeros_like(p_v_grid)
            for i in range(p_v_grid.shape[0]):
                for j in range(p_v_grid.shape[1]):
                    kla_grid[i, j] = kla_model(p_v_grid[i, j], gas_grid[i, j])
            
            # Create contour plot
            fig = go.Figure(data=go.Contour(
                z=kla_grid,
                x=p_v_range,
                y=gas_range,
                colorscale='Viridis',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=12, color='white')
                ),
                colorbar=dict(title="kLa (h⁻¹)"),
            ))
            
            # Add target kLa line (e.g., from commercial scale)
            target_kla = 25  # h⁻¹
            
            fig.add_trace(go.Contour(
                z=kla_grid,
                x=p_v_range,
                y=gas_range,
                contours=dict(
                    start=target_kla,
                    end=target_kla,
                    coloring='lines',
                    showlabels=True,
                    labelfont=dict(color='red')
                ),
                line=dict(color='red', width=3),
                showscale=False,
                name="Target kLa"
            ))
            
            # Add optimal operating point
            fig.add_trace(go.Scatter(
                x=[30],
                y=[0.05],
                mode='markers',
                marker=dict(
                    color='red',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Selected Operating Point'
            ))
            
            # Update layout
            fig.update_layout(
                title="Scale-Down Model Parameter Map",
                xaxis_title="Power Input (W/m³)",
                yaxis_title="Gas Flow Rate (vvm)",
                height=450
            )
            
            st.plotly_chart(fig)
        
        with col2:
            # Create model qualification metrics
            st.markdown("**Scale-Down Model Qualification**")
            
            # Create data for qualification metrics
            metrics = [
                'Cell Growth Rate', 
                'Maximum VCD', 
                'Titer', 
                'Glycosylation', 
                'Charge Variants',
                'Metabolic Profile'
            ]
            
            similarity = [92, 95, 90, 88, 85, 91]
            
            # Create horizontal gauge chart
            fig = go.Figure()
            
            # Add bars
            for i, metric in enumerate(metrics):
                fig.add_trace(go.Bar(
                    x=[similarity[i]],
                    y=[metric],
                    orientation='h',
                    marker=dict(
                        color=px.colors.sequential.Blues[int(similarity[i]/20)],
                        line=dict(color='black', width=1)
                    ),
                    text=[f"{similarity[i]}%"],
                    textposition='inside',
                    name=metric
                ))
            
            # Add qualification threshold line
            fig.add_vline(x=85, line_dash="dash", line_color="red")
            
            # Update layout
            fig.update_layout(
                title="Scale-Down Model Qualification Metrics",
                xaxis=dict(
                    title="Similarity to Commercial Scale (%)",
                    range=[0, 100]
                ),
                yaxis=dict(
                    title="Process Characteristic"
                ),
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Qualification Results**: The qualified scale-down model achieves >85% similarity to the commercial scale
            process across all critical quality attributes and performance metrics. Cell growth and productivity profiles
            show excellent correlation (>90%), while product quality attributes like glycosylation pattern and charge variant
            distribution show good correlation (>85%).
            """)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Scale-Down Model Qualification**:
            - Final model: 5L bioreactor with matched P/V (30 W/m³), modified sparger design, adjusted gassing strategy
            - Performance criteria: Cell growth within ±15%, titer within ±20%, all quality attributes within commercial specifications
            - Model qualified through three replicate runs against historical commercial data

            **Knowledge Transfer Application**:
            - Process characterization studies executed in qualified scale-down model
            - 25 DOE runs completed to define design space for new facility
            - Critical process parameters identified: DO control strategy, feed rate, temperature shift timing
            - Normal operating ranges established with 95% confidence
            
            **Manufacturing Implementation**:
            - Scale-up to 2000L production bioreactor with adjusted parameters based on scale-down model
            - First three engineering runs all met specifications
            - Process performance comparable to contract manufacturer results
            - Successful regulatory filing with scale-down model data
            """)
        
        with col2:
            # Create growth curve comparison
            st.markdown("**Growth Curve Comparison Across Scales**")
            
            # Create hypothetical growth curve data
            days = np.arange(0, 15)
            
            # Growth curves for different scales
            commercial_vcd = 10 * np.exp(0.5 * days) / (1 + np.exp(0.5 * days - 4))
            scale_down_vcd = 10.5 * np.exp(0.52 * days) / (1 + np.exp(0.52 * days - 4))
            new_facility_vcd = 9.8 * np.exp(0.49 * days) / (1 + np.exp(0.49 * days - 4))
            
            # Create line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=days,
                y=commercial_vcd,
                mode='lines+markers',
                name='Commercial Scale (2000L)',
                line=dict(width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=days,
                y=scale_down_vcd,
                mode='lines+markers',
                name='Scale-Down Model (5L)',
                line=dict(width=2, dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=days,
                y=new_facility_vcd,
                mode='lines+markers',
                name='New Facility (2000L)',
                line=dict(width=2, dash='dot')
            ))
            
            # Update layout
            fig.update_layout(
                title="Cell Growth Profile Comparison",
                xaxis_title="Process Day",
                yaxis_title="Viable Cell Density (10⁶ cells/mL)",
                height=400
            )
            
            st.plotly_chart(fig)
            
            # Create quality attribute comparison
            st.markdown("**Product Quality Comparison**")
            
            # Create hypothetical quality attribute data
            attributes = ['Main Peak', 'Acidic Variants', 'Basic Variants', 'HMW', 'LMW']
            
            commercial = [75, 12, 8, 3, 2]
            scale_down = [74, 13, 7, 3.5, 2.5]
            new_facility = [76, 12, 8, 2.8, 1.9]
            
            # Create grouped bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=attributes,
                y=commercial,
                name='Commercial Scale',
                marker_color='rgb(55, 83, 109)'
            ))
            
            fig.add_trace(go.Bar(
                x=attributes,
                y=scale_down,
                name='Scale-Down Model',
                marker_color='rgb(26, 118, 255)'
            ))
            
            fig.add_trace(go.Bar(
                x=attributes,
                y=new_facility,
                name='New Facility',
                marker_color='rgb(15, 187, 105)'
            ))
            
            # Update layout
            fig.update_layout(
                title="Product Quality Attribute Comparison",
                xaxis_title="Quality Attribute",
                yaxis_title="Percentage (%)",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Parameter Correlation**: DOE identified key parameters (P/V, gas flow rate) that drive process similarity across scales
        2. **Sequential Approach**: Screening-to-refinement strategy efficiently established scale-down model with minimal resources
        3. **Quality Mapping**: Focus on product quality attributes ensured comparable product from the new facility
        4. **Business Impact**: Tech transfer timeline reduced by 40% with $4.5M savings in engineering batch costs
        """)
    
    # Case Study 6: Liposomal Formulation
    with tabs[5]:
        st.subheader("Case Study 6: Formulation Optimization for Liposomal Drug Delivery")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Liposomal drug formulations require careful balance of lipid composition, manufacturing parameters, and active ingredient properties to achieve target particle size, encapsulation efficiency, and stability.

        **Practical Lens**: A pharmaceutical company developing a liposomal formulation of a small molecule oncology drug faced challenges with inconsistent particle size distribution, low encapsulation efficiency, and poor stability, limiting both efficacy and shelf life.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Experimental Design Selection**:
            - Mixture-process variable design:
            - Mixture components (5 total, constrained): Phosphatidylcholine (30-70%), Cholesterol (20-40%), PEG-lipid (2-8%), Cationic lipid (0-10%), Helper lipid (0-15%)
            - Process variables (4): Hydration temperature (25-65°C), Sonication time (5-20 min), Drug:lipid ratio (1:10-1:30), Buffer pH (5.5-7.5)
            - Responses: Particle size, Polydispersity index, Zeta potential, Encapsulation efficiency, Drug release rate, Stability (4°C, 25°C)

            **Design Rationale**:
            - Combined mixture-process design allowed simultaneous optimization of formulation composition and manufacturing process
            - Constrained mixture space reflected physical and stability limitations
            - I-optimal design chosen to maximize prediction precision across experimental space
            """)
        
        with col2:
            # Create visualization of constrained mixture space
            st.markdown("### Constrained Mixture Space Visualization")
            
            # Create ternary plot for the three main components
            # Since we can only show 3 components in a ternary plot, we'll use PC, Cholesterol, and PEG-lipid
            
            # Generate mixture points within constraints
            np.random.seed(42)
            n_points = 50
            
            # Start with random valid mixtures of PC and Cholesterol
            pc = np.random.uniform(0.3, 0.7, n_points)
            chol = np.random.uniform(0.2, 0.4, n_points)
            
            # Ensure PC + Chol <= 0.9 to leave room for other components
            valid_idx = pc + chol <= 0.9
            pc = pc[valid_idx]
            chol = chol[valid_idx]
            n_points = len(pc)
            
            # Calculate PEG-lipid as remaining space (up to 0.08)
            peg = np.random.uniform(0.02, 0.08, n_points)
            
            # Ensure sum doesn't exceed 1
            valid_idx = pc + chol + peg <= 1.0
            pc = pc[valid_idx]
            chol = chol[valid_idx]
            peg = peg[valid_idx]
            n_points = len(pc)
            
            # Calculate other components (not shown in ternary but needed for response)
            cationic = np.random.uniform(0, 0.1, n_points)
            helper = 1 - pc - chol - peg - cationic
            
            # Generate a hypothetical response (encapsulation efficiency)
            enc_eff = 40 + 30*pc + 15*chol - 20*peg + 40*cationic + 10*helper
            enc_eff += 60*pc*chol + 100*pc*cationic - 50*chol*peg
            enc_eff = np.clip(enc_eff, 30, 95)
            
            # Normalize to ternary coordinates (sum to 1)
            total = pc + chol + peg
            pc_norm = pc / total
            chol_norm = chol / total
            peg_norm = peg / total
            
            # Create ternary contour plot
            fig = go.Figure()
            
            # Add scatter points colored by encapsulation efficiency
            fig.add_trace(go.Scatterternary(
                a=pc_norm*100,
                b=chol_norm*100,
                c=peg_norm*100,
                mode='markers',
                marker=dict(
                    size=10,
                    color=enc_eff,
                    colorscale='Viridis',
                    colorbar=dict(title="Encapsulation Efficiency (%)"),
                    line=dict(width=1, color='black')
                ),
                text=[f"PC: {p:.2f}, Chol: {c:.2f}, PEG: {pg:.2f}, EE: {e:.1f}%" 
                     for p, c, pg, e in zip(pc, chol, peg, enc_eff)],
                hoverinfo='text'
            ))
            
            # Update layout
            fig.update_layout(
                ternary=dict(
                    aaxis=dict(title="Phosphatidylcholine (PC)", min=0, linewidth=2, ticksuffix="%"),
                    baxis=dict(title="Cholesterol", min=0, linewidth=2, ticksuffix="%"),
                    caxis=dict(title="PEG-Lipid", min=0, linewidth=2, ticksuffix="%"),
                    bgcolor='rgba(240, 240, 240, 0.5)'
                ),
                title="Lipid Composition Space (Normalized to 100%)",
                height=500
            )
            
            st.plotly_chart(fig)
        
        # Results and analysis
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create coefficients visualization
            st.markdown("**Significant Model Terms for Encapsulation Efficiency**")
            
            # Hypothetical model coefficients
            coefficients = {
                'PC': 45,
                'Cholesterol': 25,
                'PEG-Lipid': -15,
                'Cationic Lipid': 60,
                'Helper Lipid': 10,
                'PC × Cationic': 80,
                'Cholesterol × Cationic': 40,
                'Hydration Temp': 15,
                'Sonication Time': -20,
                'Drug:Lipid Ratio': -30,
                'Buffer pH': 5,
                'Temp × Drug:Lipid': 25
            }
            
            # Sort by absolute magnitude
            sorted_coeffs = sorted(coefficients.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Create dataframe for plotting
            coef_df = pd.DataFrame({
                'Term': [item[0] for item in sorted_coeffs[:8]],  # Show top 8 for clarity
                'Coefficient': [item[1] for item in sorted_coeffs[:8]]
            })
            
            # Create bar chart
            fig = px.bar(
                coef_df,
                y='Term',
                x='Coefficient',
                orientation='h',
                color='Coefficient',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title="Model Terms for Encapsulation Efficiency"
            )
            
            # Update layout
            fig.update_layout(height=400)
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Key Finding**: The cationic lipid content and its interaction with phosphatidylcholine (PC) 
            have the strongest positive effects on encapsulation efficiency, likely due to electrostatic 
            interactions with the drug. The drug:lipid ratio shows a negative effect, indicating that 
            higher drug loading leads to lower encapsulation efficiency, a common trade-off in liposomal formulations.
            """)
        
        with col2:
            # Create process-mixture interaction visualization
            st.markdown("**Interaction Between Formulation and Process Variables**")
            
            # Create data for interaction plot
            temp_levels = ["25°C", "45°C", "65°C"]
            drug_ratios = ["1:10", "1:20", "1:30"]
            
            # Hypothetical encapsulation efficiency data
            enc_eff_data = np.array([
                [50, 65, 75],  # Low temp
                [60, 72, 78],  # Medium temp
                [70, 75, 72]   # High temp
            ])
            
            # Create interaction plot
            fig = go.Figure()
            
            # Add traces for each temperature level
            for i, temp in enumerate(temp_levels):
                fig.add_trace(go.Scatter(
                    x=drug_ratios,
                    y=enc_eff_data[i],
                    mode='lines+markers',
                    name=f'Temperature = {temp}',
                    line=dict(width=2),
                    marker=dict(size=10)
                ))
            
            # Update layout
            fig.update_layout(
                title="Temperature × Drug:Lipid Ratio Interaction",
                xaxis_title="Drug:Lipid Ratio",
                yaxis_title="Encapsulation Efficiency (%)",
                height=350
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Interaction Interpretation**: At low temperatures (25°C), increasing the drug:lipid ratio from 1:10 to 1:30
            substantially improves encapsulation efficiency. However, at high temperatures (65°C), the optimal ratio is 
            around 1:20, with higher ratios showing decreased efficiency. This interaction highlights the importance of
            simultaneously optimizing formulation and process parameters.
            """)
        
        # Optimization results
        st.markdown("### Multi-Response Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create contour plot for optimal region
            st.markdown("**Sweet Spot Analysis**")
            
            # Create grids for contour plot
            cationic = np.linspace(0, 0.1, 50)
            pc = np.linspace(0.3, 0.7, 50)
            cationic_grid, pc_grid = np.meshgrid(cationic, pc)
            
            # Hypothetical models
            def enc_eff_model(pc, cat):
                return 55 + 45*pc + 60*cat + 80*pc*cat - 40*pc**2
            
            def stability_model(pc, cat):
                return 12 + 8*pc - 15*cat + 5*pc*cat - 5*pc**2 - 40*cat**2
            
            # Calculate response surfaces
            enc_eff_grid = np.zeros_like(cationic_grid)
            stability_grid = np.zeros_like(cationic_grid)
            
            for i in range(cationic_grid.shape[0]):
                for j in range(cationic_grid.shape[1]):
                    enc_eff_grid[i, j] = enc_eff_model(pc_grid[i, j], cationic_grid[i, j])
                    stability_grid[i, j] = stability_model(pc_grid[i, j], cationic_grid[i, j])
            
            # Create contour plot
            fig = go.Figure()
            
            # Add encapsulation efficiency contours
            fig.add_trace(go.Contour(
                z=enc_eff_grid,
                x=cationic*100,  # Convert to percentage
                y=pc*100,        # Convert to percentage
                colorscale='Blues',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=10, color='white')
                ),
                colorbar=dict(title="Encapsulation (%)", x=0.45),
                name="Encapsulation"
            ))
            
            # Add stability contour lines
            fig.add_trace(go.Contour(
                z=stability_grid,
                x=cationic*100,  # Convert to percentage
                y=pc*100,        # Convert to percentage
                colorscale='Reds',
                contours=dict(
                    coloring='lines',
                    showlabels=True
                ),
                line=dict(width=2),
                colorbar=dict(title="Stability (months)", x=1.0),
                name="Stability"
            ))
            
            # Add sweet spot (intersection of high encapsulation and good stability)
            # Assuming encapsulation > 80% and stability > 12 months
            sweet_spot = np.array([
                [5, 45], [7, 45], [7, 50], [5, 50], [5, 45]
            ])
            
            fig.add_trace(go.Scatter(
                x=sweet_spot[:, 0],
                y=sweet_spot[:, 1],
                mode='lines',
                line=dict(color='green', width=2, dash='dot'),
                fill='toself',
                fillcolor='rgba(0, 255, 0, 0.2)',
                name='Design Space'
            ))
            
            # Add optimal point
            fig.add_trace(go.Scatter(
                x=[5.5],
                y=[47],
                mode='markers',
                marker=dict(
                    color='green',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Formulation'
            ))
            
            # Update layout
            fig.update_layout(
                title="Formulation Optimization",
                xaxis_title="Cationic Lipid (%)",
                yaxis_title="Phosphatidylcholine (%)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        with col2:
            # Create radar chart comparing optimized formulation performance
            st.markdown("**Performance Comparison**")
            
            # Create data for radar chart
            categories = ['Encapsulation Efficiency (%)', 'Particle Size (nm)', 'PDI (×10)', 
                         'Zeta Potential (mV)', 'Drug Release 24h (%)', 'Stability (months)']
            
            # Values for initial and optimized formulations
            initial_values = [45, 180, 0.25*10, 10, 35, 6]
            optimized_values = [85, 120, 0.12*10, 25, 15, 18]
            
            # Create radar chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=initial_values,
                theta=categories,
                fill='toself',
                name='Initial Formulation',
                line_color='lightgray'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=optimized_values,
                theta=categories,
                fill='toself',
                name='Optimized Formulation',
                line_color='royalblue'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    )
                ),
                title="Formulation Performance Comparison",
                height=400
            )
            
            st.plotly_chart(fig)
            
            # Add particle size distribution comparison
            st.markdown("**Particle Size Distribution**")
            
            # Create hypothetical size distribution data
            size_range = np.linspace(10, 400, 100)
            
            # Log-normal distributions
            initial_dist = stats.lognorm.pdf(size_range, s=0.4, scale=np.exp(5.1))
            optimized_dist = stats.lognorm.pdf(size_range, s=0.2, scale=np.exp(4.7))
            
            # Scale to make visually comparable
            initial_dist = initial_dist / np.max(initial_dist) * 100
            optimized_dist = optimized_dist / np.max(optimized_dist) * 100
            
            # Create line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=size_range,
                y=initial_dist,
                mode='lines',
                name='Initial Formulation',
                line=dict(color='lightgray', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=size_range,
                y=optimized_dist,
                mode='lines',
                name='Optimized Formulation',
                line=dict(color='royalblue', width=2)
            ))
            
            # Update layout
            fig.update_layout(
                title="Particle Size Distribution",
                xaxis_title="Particle Size (nm)",
                yaxis_title="Relative Intensity (%)",
                height=350
            )
            
            st.plotly_chart(fig)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Optimized Formulation**:
            - Final composition: 45% PC, 30% cholesterol, 5% PEG-lipid, 5% cationic lipid, 15% helper lipid
            - Process parameters: 45°C hydration temperature, 15 min sonication, 1:20 drug:lipid ratio, pH 6.5
            - Predicted performance: 120 nm particle size, >80% encapsulation, <15% drug release at 24h, >12 month stability at 4°C

            **Scale-Up and Verification**:
            - Laboratory verification batches confirmed model predictions
            - Scale-up to 10L using geometric similarity principles
            - Process adjusted to maintain constant energy dissipation rate
            - Quality attributes maintained within target specifications
            
            **Robustness Assessment**:
            - 12 confirmation runs around optimal point verified design space
            - Edge-of-failure analysis identified critical control points
            - Sensitivity to raw material variability quantified
            - Stability model developed from accelerated testing data
            """)
        
        with col2:
            # Create in vivo efficacy comparison
            st.markdown("**In Vivo Efficacy Comparison**")
            
            # Create hypothetical tumor growth data
            days = np.arange(0, 22, 2)
            
            # Growth curves for different treatments
            control = 100 * np.exp(0.15 * days)
            free_drug = 100 * np.exp(0.15 * days) * np.exp(-0.08 * days)
            initial_lipo = 100 * np.exp(0.15 * days) * np.exp(-0.12 * days)
            optimized_lipo = 100 * np.exp(0.15 * days) * np.exp(-0.22 * days)
            
            # Create line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=days,
                y=control,
                mode='lines+markers',
                name='Control',
                line=dict(width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=days,
                y=free_drug,
                mode='lines+markers',
                name='Free Drug',
                line=dict(width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=days,
                y=initial_lipo,
                mode='lines+markers',
                name='Initial Liposome',
                line=dict(width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=days,
                y=optimized_lipo,
                mode='lines+markers',
                name='Optimized Liposome',
                line=dict(width=2)
            ))
            
            # Update layout
            fig.update_layout(
                title="Tumor Growth Inhibition Study",
                xaxis_title="Days After Treatment",
                yaxis_title="Relative Tumor Volume (%)",
                height=400
            )
            
            st.plotly_chart(fig)
            
            # Add stability data
            st.markdown("**Long-Term Stability**")
            
            # Create hypothetical stability data
            months = np.arange(0, 19, 3)
            
            # Stability metrics over time
            initial_size = np.array([120, 130, 150, 185, 240, 310, 380])
            optimized_size = np.array([120, 122, 125, 130, 138, 145, 155])
            
            initial_ee = np.array([45, 42, 36, 30, 22, 15, 10])
            optimized_ee = np.array([85, 83, 80, 78, 75, 72, 68])
            
            # Create multi-Y-axis plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add size traces
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=initial_size,
                    mode='lines+markers',
                    name='Initial Size',
                    line=dict(color='lightgray', width=2, dash='dot')
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=optimized_size,
                    mode='lines+markers',
                    name='Optimized Size',
                    line=dict(color='royalblue', width=2, dash='dot')
                ),
                secondary_y=False
            )
            
            # Add encapsulation traces
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=initial_ee,
                    mode='lines+markers',
                    name='Initial EE',
                    line=dict(color='lightgray', width=2)
                ),
                secondary_y=True
            )
            
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=optimized_ee,
                    mode='lines+markers',
                    name='Optimized EE',
                    line=dict(color='royalblue', width=2)
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title="Long-Term Stability at 4°C",
                xaxis_title="Time (months)",
                height=400
            )
            
            fig.update_yaxes(title_text="Particle Size (nm)", secondary_y=False)
            fig.update_yaxes(title_text="Encapsulation Efficiency (%)", secondary_y=True)
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Mixture-Process Integration**: DOE enabled simultaneous optimization of formulation composition and manufacturing process
        2. **Critical Interactions**: Discovered key interactions between cationic lipid content and hydration conditions
        3. **Multi-Response Optimization**: Balanced encapsulation efficiency, particle size, and stability objectives
        4. **Business Impact**: 90% increase in encapsulation efficiency and 3-fold extension in shelf-life
        """)
    
    # Case Study 7: Analytical Method Validation
    with tabs[6]:
        st.subheader("Case Study 7: Analytical Method Validation for Process Impurities")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Analytical method validation requires demonstration of specificity, accuracy, precision, linearity, range, and robustness to ensure reliable quantification of process-related impurities in biopharmaceuticals.

        **Practical Lens**: A biotechnology company developing an enzyme replacement therapy needed to validate a high-performance liquid chromatography (HPLC) method for detection and quantification of host cell proteins (HCPs) and aggregates, which were critical quality attributes with strict regulatory limits.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Experimental Design Selection**:
            - Full factorial design for robustness testing (2^4 with 3 center points = 19 runs)
            - Factors: Column temperature (30-40°C), Flow rate (0.8-1.2 mL/min), Mobile phase pH (6.8-7.2), Buffer concentration (45-55 mM)
            - Responses: Retention time, Peak resolution, Peak area, Signal-to-noise ratio, Theoretical plates

            **Design Rationale**:
            - Full factorial design allowed complete characterization of main effects and interactions
            - Center points enabled assessment of method linearity across operating range
            - Design focused on robustness factors most likely to vary in routine operation
            """)
        
        with col2:
            # Create visualization of chromatographic method development
            st.markdown("### Method Development Process")
            
            # Create simulated chromatograms for different conditions
            time = np.linspace(0, 10, 500)
            
            # Gaussian peaks with different conditions
            def chromatogram(time, conditions):
                peaks = []
                
                # Main peak
                main_rt = 5.0 + 0.2 * conditions.get('temp_effect', 0) - 0.3 * conditions.get('ph_effect', 0)
                main_width = 0.2 + 0.05 * conditions.get('flow_effect', 0)
                main_area = 1.0
                peaks.append(main_area * np.exp(-0.5 * ((time - main_rt) / main_width)**2))
                
                # Impurity 1
                imp1_rt = 4.2 + 0.15 * conditions.get('temp_effect', 0) - 0.25 * conditions.get('ph_effect', 0)
                imp1_width = 0.15 + 0.03 * conditions.get('flow_effect', 0)
                imp1_area = 0.05
                peaks.append(imp1_area * np.exp(-0.5 * ((time - imp1_rt) / imp1_width)**2))
                
                # Impurity 2
                imp2_rt = 5.8 + 0.25 * conditions.get('temp_effect', 0) - 0.35 * conditions.get('ph_effect', 0)
                imp2_width = 0.18 + 0.04 * conditions.get('flow_effect', 0)
                imp2_area = 0.08
                peaks.append(imp2_area * np.exp(-0.5 * ((time - imp2_rt) / imp2_width)**2))
                
                # Sum all peaks
                chromatogram = sum(peaks)
                
                # Add noise
                noise_level = 0.002 * (1 + conditions.get('buffer_effect', 0))
                chromatogram += np.random.normal(0, noise_level, len(time))
                
                return chromatogram
            
            # Create three different conditions
            conditions = [
                {'name': 'Poor Conditions', 'temp_effect': -1, 'ph_effect': -1, 'flow_effect': 1, 'buffer_effect': 1},
                {'name': 'Center Point', 'temp_effect': 0, 'ph_effect': 0, 'flow_effect': 0, 'buffer_effect': 0},
                {'name': 'Optimal Conditions', 'temp_effect': 1, 'ph_effect': 1, 'flow_effect': -0.5, 'buffer_effect': -0.5}
            ]
            
            # Generate chromatograms
            chromatograms = [chromatogram(time, cond) for cond in conditions]
            
            # Create plot
            fig = go.Figure()
            
            # Add each chromatogram
            colors = ['lightgray', 'gray', 'royalblue']
            for i, (chrom, cond) in enumerate(zip(chromatograms, conditions)):
                fig.add_trace(go.Scatter(
                    x=time,
                    y=chrom + i*0.2,  # Offset for visibility
                    mode='lines',
                    name=cond['name'],
                    line=dict(color=colors[i], width=2)
                ))
                
                # Add annotations for resolution
                if i == 2:  # Only annotate optimal conditions
                    # Calculate peak positions
                    main_rt = 5.0 + 0.2 * cond['temp_effect'] - 0.3 * cond['ph_effect']
                    imp1_rt = 4.2 + 0.15 * cond['temp_effect'] - 0.25 * cond['ph_effect']
                    imp2_rt = 5.8 + 0.25 * cond['temp_effect'] - 0.35 * cond['ph_effect']
                    
                    # Add resolution annotations
                    fig.add_annotation(
                        x=(main_rt + imp1_rt)/2,
                        y=chrom.max() + i*0.2 + 0.05,
                        text=f"Rs = 2.8",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-30
                    )
                    
                    fig.add_annotation(
                        x=(main_rt + imp2_rt)/2,
                        y=chrom.max() + i*0.2 + 0.05,
                        text=f"Rs = 3.2",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-30
                    )
            
            # Update layout
            fig.update_layout(
                title="HPLC Method Optimization",
                xaxis_title="Retention Time (min)",
                yaxis_title="Absorbance (AU)",
                yaxis=dict(
                    showticklabels=False
                ),
                height=400,
                annotations=[
                    dict(
                        x=time[np.argmax(chromatograms[0])],
                        y=chromatograms[0].max() + 0*0.2,
                        text="Poor Resolution",
                        showarrow=False,
                        yshift=20
                    ),
                    dict(
                        x=time[np.argmax(chromatograms[2])],
                        y=chromatograms[2].max() + 2*0.2,
                        text="Optimal Resolution",
                        showarrow=False,
                        yshift=20
                    )
                ]
            )
            
            st.plotly_chart(fig)
        
        # Results and analysis
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create effect visualization for resolution
            st.markdown("**Effects on Peak Resolution**")
            
            # Hypothetical effects on resolution
            effects = {
                'Column Temperature': 0.4,
                'Flow Rate': -0.2,
                'Mobile Phase pH': 0.8,
                'Buffer Concentration': -0.1,
                'Temp × pH': 0.3,
                'Flow × pH': -0.15,
                'Temp × Flow': -0.05,
                'pH × Buffer': 0.1
            }
            
            # Sort by absolute magnitude
            sorted_effects = sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Create dataframe for plotting
            effect_df = pd.DataFrame({
                'Factor': [item[0] for item in sorted_effects],
                'Effect': [item[1] for item in sorted_effects]
            })
            
            # Create horizontal bar chart
            fig = px.bar(
                effect_df,
                y='Factor',
                x='Effect',
                orientation='h',
                color='Effect',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title="Effects on Peak Resolution"
            )
            
            # Add reference line
            fig.add_vline(x=0, line_dash="solid", line_color="gray")
            
            # Update layout
            fig.update_layout(height=400)
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Key Finding**: Mobile phase pH has the strongest effect on peak resolution, 
            followed by column temperature. The positive pH-temperature interaction indicates 
            that the effect of pH is even stronger at higher temperatures. Flow rate has a 
            negative effect, indicating that slower flow rates improve resolution, but at the 
            cost of longer run times.
            """)
        
        with col2:
            # Create contour plot for optimal conditions
            st.markdown("**Method Optimization Surface**")
            
            # Create grid for contour plot
            ph = np.linspace(6.8, 7.2, 50)
            temp = np.linspace(30, 40, 50)
            ph_grid, temp_grid = np.meshgrid(ph, temp)
            
            # Hypothetical model for resolution
            def resolution_model(ph, temp):
                return 2.0 + 0.8*(ph-7.0)/0.2 + 0.4*(temp-35)/5 + 0.3*(ph-7.0)/0.2*(temp-35)/5 - 0.2*((ph-7.0)/0.2)**2 - 0.1*((temp-35)/5)**2
            
            # Hypothetical model for retention time
            def retention_model(ph, temp):
                return 5.0 - 0.3*(ph-7.0)/0.2 + 0.2*(temp-35)/5 - 0.1*((ph-7.0)/0.2)**2
            
            # Calculate response surfaces
            resolution_grid = np.zeros_like(ph_grid)
            retention_grid = np.zeros_like(ph_grid)
            
            for i in range(ph_grid.shape[0]):
                for j in range(ph_grid.shape[1]):
                    resolution_grid[i, j] = resolution_model(ph_grid[i, j], temp_grid[i, j])
                    retention_grid[i, j] = retention_model(ph_grid[i, j], temp_grid[i, j])
            
            # Create contour plot
            fig = go.Figure()
            
            # Add resolution contours
            fig.add_trace(go.Contour(
                z=resolution_grid,
                x=ph,
                y=temp,
                colorscale='Viridis',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=12, color='white')
                ),
                colorbar=dict(title="Resolution"),
            ))
            
            # Add retention time contour lines
            fig.add_trace(go.Contour(
                z=retention_grid,
                x=ph,
                y=temp,
                contours=dict(
                    coloring='lines',
                    showlabels=True
                ),
                line=dict(color='white', width=2),
                showscale=False,
                name="Retention Time"
            ))
            
            # Add method operating point
            fig.add_trace(go.Scatter(
                x=[7.1],
                y=[37.5],
                mode='markers',
                marker=dict(
                    color='red',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Method'
            ))
            
            # Add center point
            fig.add_trace(go.Scatter(
                x=[7.0],
                y=[35.0],
                mode='markers',
                marker=dict(
                    color='white',
                    size=10,
                    symbol='circle',
                    line=dict(width=1, color='black')
                ),
                name='Center Point'
            ))
            
            # Add control range (robust operating window)
            control_range = np.array([
                [7.05, 36], [7.15, 36], [7.15, 39], [7.05, 39], [7.05, 36]
            ])
            
            fig.add_trace(go.Scatter(
                x=control_range[:, 0],
                y=control_range[:, 1],
                mode='lines',
                line=dict(color='red', width=2, dash='dot'),
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.1)',
                name='Control Range'
            ))
            
            # Update layout
            fig.update_layout(
                title="Method Robustness: pH vs. Temperature",
                xaxis_title="Mobile Phase pH",
                yaxis_title="Column Temperature (°C)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        # Method validation results
        st.markdown("### Method Validation Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Create linearity plot
            st.markdown("**Linearity**")
            
            # Hypothetical linearity data
            conc = np.array([0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
            area = conc * 10000 + np.random.normal(0, 100, len(conc))
            
            # Calculate regression line
            slope, intercept, r_value, p_value, std_err = stats.linregress(conc, area)
            line = slope * conc + intercept
            
            # Create scatter plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=conc,
                y=area,
                mode='markers',
                name='Data Points',
                marker=dict(
                    color='royalblue',
                    size=10,
                    line=dict(width=1, color='black')
                )
            ))
            
            fig.add_trace(go.Scatter(
                x=conc,
                y=line,
                mode='lines',
                name=f'Regression Line<br>R² = {r_value**2:.4f}',
                line=dict(color='red', width=2)
            ))
            
            # Update layout
            fig.update_layout(
                title="Method Linearity",
                xaxis_title="Concentration (μg/mL)",
                yaxis_title="Peak Area",
                height=300
            )
            
            st.plotly_chart(fig)
        
        with col2:
            # Create accuracy plot
            st.markdown("**Accuracy (Recovery)**")
            
            # Hypothetical recovery data
            levels = ["0.1 μg/mL", "1.0 μg/mL", "10.0 μg/mL"]
            recovery = [98.5, 100.2, 97.8]
            error = [3.2, 1.5, 2.1]
            
            # Create bar chart with error bars
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=levels,
                y=recovery,
                error_y=dict(
                    type='data',
                    array=error,
                    visible=True
                ),
                marker_color='royalblue',
                name='Recovery'
            ))
            
            # Add acceptance limits
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=90,
                x1=2.5,
                y1=90,
                line=dict(color="red", width=2, dash="dash"),
            )
            
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=110,
                x1=2.5,
                y1=110,
                line=dict(color="red", width=2, dash="dash"),
            )
            
            # Update layout
            fig.update_layout(
                title="Method Accuracy",
                xaxis_title="Concentration Level",
                yaxis_title="Recovery (%)",
                yaxis=dict(range=[85, 115]),
                height=300
            )
            
            st.plotly_chart(fig)
        
        with col3:
            # Create precision plot
            st.markdown("**Precision**")
            
            # Hypothetical precision data
            precision_types = ["Repeatability", "Intermediate Precision", "Reproducibility"]
            rsd_values = [1.8, 2.9, 3.5]
            
            # Create bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=precision_types,
                y=rsd_values,
                marker_color='royalblue',
                name='RSD (%)'
            ))
            
            # Add acceptance limit
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=5.0,
                x1=2.5,
                y1=5.0,
                line=dict(color="red", width=2, dash="dash"),
            )
            
            # Add annotation
            fig.add_annotation(
                x=1,
                y=5.0,
                text="Acceptance Limit",
                showarrow=False,
                yshift=10
            )
            
            # Update layout
            fig.update_layout(
                title="Method Precision",
                xaxis_title="Precision Type",
                yaxis_title="RSD (%)",
                yaxis=dict(range=[0, 7]),
                height=300
            )
            
            st.plotly_chart(fig)
        
        # Robustness analysis
        st.markdown("### Method Robustness Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create robustness contour plot
            st.markdown("**Method Control Strategy**")
            
            # Create grid for heat map
            ph = np.linspace(6.7, 7.3, 50)
            flow = np.linspace(0.7, 1.3, 50)
            ph_grid, flow_grid = np.meshgrid(ph, flow)
            
            # Hypothetical model for resolution
            def system_suitability(ph, flow):
                # 1 = pass, 0 = fail
                res = 2.0 + 0.8*(ph-7.0)/0.2 - 0.2*(flow-1.0)/0.2 - 0.2*((ph-7.0)/0.2)**2 - 0.1*((flow-1.0)/0.2)**2
                return (res >= 1.5).astype(float)
            
            # Calculate suitability surface
            suitability_grid = np.zeros_like(ph_grid)
            for i in range(ph_grid.shape[0]):
                for j in range(ph_grid.shape[1]):
                    suitability_grid[i, j] = system_suitability(ph_grid[i, j], flow_grid[i, j])
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=suitability_grid,
                x=ph,
                y=flow,
                colorscale=[[0, 'white'], [1, 'green']],
                showscale=False
            ))
            
            # Add nominal point
            fig.add_trace(go.Scatter(
                x=[7.0],
                y=[1.0],
                mode='markers',
                marker=dict(
                    color='red',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Nominal Condition'
            ))
            
            # Add control limits
            control_limits = np.array([
                [6.9, 0.9], [7.1, 0.9], [7.1, 1.1], [6.9, 1.1], [6.9, 0.9]
            ])
            
            fig.add_trace(go.Scatter(
                x=control_limits[:, 0],
                y=control_limits[:, 1],
                mode='lines',
                line=dict(color='blue', width=2),
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.1)',
                name='Control Limits'
            ))
            
            # Add system limits
            system_limits = np.array([
                [6.8, 0.8], [7.2, 0.8], [7.2, 1.2], [6.8, 1.2], [6.8, 0.8]
            ])
            
            fig.add_trace(go.Scatter(
                x=system_limits[:, 0],
                y=system_limits[:, 1],
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.05)',
                name='System Limits'
            ))
            
            # Update layout
            fig.update_layout(
                title="Method Robustness: System Suitability Map",
                xaxis_title="Mobile Phase pH",
                yaxis_title="Flow Rate (mL/min)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        with col2:
            # Create method robustness results
            st.markdown("**Method Performance Across Labs**")
            
            # Create sample data
            labs = ["Development", "QC Lab 1", "QC Lab 2", "Contract Lab"]
            
            # Hypothetical results for resolution and retention time
            resolution = [2.2, 2.1, 1.9, 2.0]
            retention = [5.2, 5.1, 5.4, 5.3]
            
            # Create dual-axis plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add resolution bars
            fig.add_trace(
                go.Bar(
                    x=labs,
                    y=resolution,
                    name="Resolution",
                    marker_color="royalblue",
                    opacity=0.7
                ),
                secondary_y=False
            )
            
            # Add retention time points
            fig.add_trace(
                go.Scatter(
                    x=labs,
                    y=retention,
                    mode='markers+lines',
                    name="Retention Time",
                    marker=dict(color="red", size=10),
                    line=dict(color="red", width=2)
                ),
                secondary_y=True
            )
            
            # Add limits
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=1.5,
                x1=3.5,
                y1=1.5,
                line=dict(color="red", width=2, dash="dash"),
                secondary_y=False
            )
            
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=5.0,
                x1=3.5,
                y1=5.0,
                line=dict(color="red", width=2, dash="dash"),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title="Method Performance Across Laboratories",
                height=400
            )
            
            fig.update_yaxes(title_text="Resolution", secondary_y=False)
            fig.update_yaxes(title_text="Retention Time (min)", secondary_y=True)
            
            st.plotly_chart(fig)
            
            # Add system suitability criteria
            st.markdown("**System Suitability Criteria**")
            
            criteria = pd.DataFrame({
                'Parameter': ['Resolution', 'Theoretical Plates', 'Tailing Factor', 'Retention Time'],
                'Criteria': ['>1.5', '>5000', '<1.5', '5.0 ± 0.5 min'],
                'Development': ['2.2 ✓', '6500 ✓', '1.2 ✓', '5.2 ✓'],
                'QC Lab 1': ['2.1 ✓', '6200 ✓', '1.3 ✓', '5.1 ✓'],
                'QC Lab 2': ['1.9 ✓', '5800 ✓', '1.4 ✓', '5.4 ✓'],
                'Contract Lab': ['2.0 ✓', '5500 ✓', '1.4 ✓', '5.3 ✓']
            })
            
            st.dataframe(criteria)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Method Validation Protocol**:
            - Comprehensive validation protocol based on ICH guidelines
            - System suitability criteria: Resolution > 2.0, Theoretical plates > 5000, Tailing factor < 1.5
            - Method control ranges: pH (7.0 ± 0.1), Temperature (35 ± 2°C), Flow rate (1.0 ± 0.1 mL/min)
            - Validation acceptance criteria met for all parameters

            **Laboratory Implementation**:
            - Method transferred to QC laboratory with training program
            - Method robustness verified across three different HPLC systems
            - Instrument qualification requirements defined
            - Standard operating procedure developed with troubleshooting guide
            
            **Regulatory Submission**:
            - Validation package submitted as part of regulatory filing
            - DOE approach specifically highlighted as best practice
            - No major findings from regulatory review
            - Method approved for release and stability testing
            """)
        
        with col2:
            # Create milestone visualization
            st.markdown("**Method Implementation Timeline**")
            
            # Timeline data
            milestones = [
                {"task": "Method Development", "start": 0, "end": 4, "color": "lightblue"},
                {"task": "DOE Optimization", "start": 2, "end": 6, "color": "royalblue"},
                {"task": "Method Validation", "start": 6, "end": 10, "color": "lightgreen"},
                {"task": "Tech Transfer", "start": 9, "end": 12, "color": "green"},
                {"task": "Regulatory Filing", "start": 11, "end": 13, "color": "orange"},
                {"task": "Method Implementation", "start": 13, "end": 15, "color": "red"}
            ]
            
            # Create Gantt chart
            fig = go.Figure()
            
            for milestone in milestones:
                fig.add_trace(go.Bar(
                    x=[milestone["end"] - milestone["start"]],
                    y=[milestone["task"]],
                    orientation='h',
                    marker=dict(color=milestone["color"]),
                    base=milestone["start"],
                    width=0.6,
                    name=milestone["task"]
                ))
            
            # Add vertical line for current status
            fig.add_shape(
                type="line",
                x0=13,
                y0=-0.5,
                x1=13,
                y1=5.5,
                line=dict(color="black", width=2, dash="dash")
            )
            
            fig.add_annotation(
                x=13,
                y=6,
                text="Current Status",
                showarrow=False,
                yshift=10
            )
            
            # Update layout
            fig.update_layout(
                title="Method Development and Implementation Timeline",
                xaxis_title="Month",
                yaxis=dict(
                    categoryorder='array',
                    categoryarray=["Regulatory Filing", "Method Implementation", "Tech Transfer", 
                                 "Method Validation", "DOE Optimization", "Method Development"]
                ),
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Comprehensive Design**: Full factorial design enabled complete characterization of method robustness
        2. **Critical Parameters**: pH identified as most critical parameter requiring tight control
        3. **Design Space Mapping**: Well-defined operating ranges established for all parameters
        4. **Business Impact**: Robust method reduced out-of-specification investigations by 85%
        """)
    
    # Case Study 8: Vaccine Adjuvant Formulation
    with tabs[7]:
        st.subheader("Case Study 8: Vaccine Adjuvant Formulation Development")
        
        st.markdown("""
        ### Process Context and Challenge
        **Concept Anchor**: Vaccine adjuvant formulations enhance immune response but require precise control of particle properties, stability, and immunostimulatory characteristics to ensure both efficacy and safety.

        **Practical Lens**: A vaccine developer needed to optimize a novel lipid nanoparticle (LNP) adjuvant formulation for a recombinant protein vaccine. Key challenges included inconsistent particle size, variable antigen loading, and unpredictable immune response profiles in preliminary studies.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### DOE Approach")
            st.markdown("""
            **Multi-stage Experimental Strategy**:
            1. **Screening**: Fractional factorial design (2^7-3, Resolution IV, 16 runs)
               - Factors: Lipid composition (4 types), Lipid:antigen ratio, Buffer system, Homogenization pressure, Temperature, pH, Cryoprotectant type
               - Responses: Particle size, PDI, Zeta potential, Antigen loading
            
            2. **Optimization**: Box-Behnken design (27 runs)
               - Focused on significant factors from screening
               - Additional responses: Particle stability, In vitro immunogenicity markers
            
            3. **Formulation Robustness**: Central composite design (20 runs)
               - Detailed characterization around optimal formulation
               - Final responses included accelerated stability indicators
            
            **Design Rationale**:
            - Fractional factorial efficiently screened many potential factors
            - Box-Behnken selected to avoid extreme combinations that might cause formulation instability
            - CCD provided detailed response surface around optimal region
            """)
        
        with col2:
            # Create visualization of experimental strategy
            st.markdown("### Sequential Optimization Strategy")
            
            # Create sequential experiments diagram
            fig = go.Figure()
            
            # Define experiment stages
            stages = [
                {
                    "name": "Screening",
                    "design": "Fractional Factorial (2^7-3)",
                    "runs": 16,
                    "color": "lightblue",
                    "outcome": "Identify significant factors"
                },
                {
                    "name": "Optimization",
                    "design": "Box-Behnken Design",
                    "runs": 27,
                    "color": "royalblue",
                    "outcome": "Map response surface"
                },
                {
                    "name": "Robustness",
                    "design": "Central Composite Design",
                    "runs": 20,
                    "color": "navy",
                    "outcome": "Define design space"
                }
            ]
            
            # Create boxes for each stage
            height = 1.0
            spacing = 0.3
            
            for i, stage in enumerate(stages):
                # Add stage box
                fig.add_shape(
                    type="rect",
                    x0=0.1,
                    y0=i * (height + spacing),
                    x1=0.9,
                    y1=i * (height + spacing) + height,
                    line=dict(color="black", width=2),
                    fillcolor=stage["color"],
                    opacity=0.8
                )
                
                # Add stage name
                fig.add_annotation(
                    x=0.5,
                    y=i * (height + spacing) + height * 0.25,
                    text=f"<b>{stage['name']}</b><br>{stage['design']}",
                    showarrow=False,
                    font=dict(size=14, color="white")
                )
                
                # Add number of runs
                fig.add_annotation(
                    x=0.2,
                    y=i * (height + spacing) + height * 0.75,
                    text=f"{stage['runs']} runs",
                    showarrow=False,
                    font=dict(size=12, color="white")
                )
                
                # Add outcome
                fig.add_annotation(
                    x=0.7,
                    y=i * (height + spacing) + height * 0.75,
                    text=stage["outcome"],
                    showarrow=False,
                    font=dict(size=12, color="white")
                )
                
                # Add arrow connecting stages
                if i < len(stages) - 1:
                    fig.add_shape(
                        type="line",
                        x0=0.5,
                        y0=i * (height + spacing) + height,
                        x1=0.5,
                        y1=i * (height + spacing) + height + spacing,
                        line=dict(color="black", width=2),
                        opacity=1
                    )
                    
                    # Add arrowhead
                    fig.add_annotation(
                        x=0.5,
                        y=i * (height + spacing) + height + spacing,
                        text="▼",
                        showarrow=False,
                        font=dict(size=20, color="black")
                    )
            
            # Update layout
            fig.update_layout(
                showlegend=False,
                xaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[0, 1]
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[0, 3 * (height + spacing)]
                ),
                height=500,
                title="Sequential Experimental Strategy",
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig)
        
        # Results and analysis
        st.markdown("### Results and Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create Pareto chart of screening effects
            st.markdown("**Screening Phase Results**")
            
            # Hypothetical effects data
            effects = {
                'Cationic Lipid %': 75,
                'Lipid:Antigen Ratio': 60,
                'Homogenization Pressure': 45,
                'pH': 35,
                'Temperature': 30,
                'Buffer System': 15,
                'Cryoprotectant': 12,
                'Cat Lipid × Lipid:Antigen': 50,
                'Pressure × Temperature': 25,
                'pH × Temperature': 20
            }
            
            # Sort effects by absolute magnitude
            sorted_effects = sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Create dataframe for plotting
            effect_df = pd.DataFrame({
                'Factor': [item[0] for item in sorted_effects],
                'Effect Size': [item[1] for item in sorted_effects]
            })
            
            # Create Pareto chart
            fig = px.bar(
                effect_df,
                y='Factor',
                x='Effect Size',
                orientation='h',
                title="Pareto Chart of Effects on Antigen Loading",
                color='Effect Size',
                color_continuous_scale='Blues'
            )
            
            # Add significance line
            fig.add_vline(x=20, line_dash="dash", line_color="red")
            fig.add_annotation(
                x=20,
                y=10,
                text="Significance Threshold",
                showarrow=True,
                arrowhead=1,
                ax=50,
                ay=0
            )
            
            # Update layout
            fig.update_layout(height=400)
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Key Findings**: The screening phase identified cationic lipid content and lipid:antigen ratio
            as the most significant factors affecting antigen loading. The interaction between these two factors
            was also significant, indicating that their optimal levels are interdependent. Homogenization pressure
            and pH showed moderate effects, while buffer system and cryoprotectant type had minimal impact.
            """)
        
        with col2:
            # Create interaction plot
            st.markdown("**Critical Interaction from Optimization Phase**")
            
            # Create data for interaction plot
            cationic_lipid_levels = ["10%", "20%", "30%"]
            lipid_ratio_levels = ["1:10", "1:20", "1:30"]
            
            # Hypothetical antigen loading data
            antigen_loading = np.array([
                [35, 45, 40],  # 10% cationic lipid
                [50, 70, 65],  # 20% cationic lipid
                [60, 65, 55]   # 30% cationic lipid
            ])
            
            # Create interaction plot
            fig = go.Figure()
            
            # Add traces for each cationic lipid level
            for i, level in enumerate(cationic_lipid_levels):
                fig.add_trace(go.Scatter(
                    x=lipid_ratio_levels,
                    y=antigen_loading[i],
                    mode='lines+markers',
                    name=f'Cationic Lipid = {level}',
                    line=dict(width=2),
                    marker=dict(size=10)
                ))
            
            # Update layout
            fig.update_layout(
                title="Cationic Lipid × Lipid:Antigen Ratio Interaction",
                xaxis_title="Lipid:Antigen Ratio",
                yaxis_title="Antigen Loading (%)",
                height=350
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Interaction Interpretation**: The effect of lipid:antigen ratio depends strongly on the cationic lipid
            content. At 20% cationic lipid, increasing the lipid:antigen ratio to 1:20 substantially improves loading,
            but further increases provide minimal benefit. At lower (10%) or higher (30%) cationic lipid levels,
            the optimal lipid:antigen ratio shifts, and the maximum achievable loading is reduced. This interaction
            highlights the importance of optimizing these parameters together.
            """)
        
        # Optimization and formulation characterization
        st.markdown("### Formulation Optimization and Characterization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create contour plot for optimal region
            st.markdown("**Particle Characteristics Optimization**")
            
            # Create grid for contour plot
            cationic = np.linspace(10, 30, 50)
            pressure = np.linspace(6000, 18000, 50)
            cationic_grid, pressure_grid = np.meshgrid(cationic, pressure)
            
            # Hypothetical models
            def particle_size_model(cat, press):
                return 150 - 15*(cat-20)/10 - 25*(press-12000)/6000 + 10*(cat-20)/10*(press-12000)/6000 + 20*((cat-20)/10)**2 + 10*((press-12000)/6000)**2
            
            def pdi_model(cat, press):
                return 0.15 + 0.02*(cat-20)/10 - 0.05*(press-12000)/6000 + 0.01*((cat-20)/10)**2 + 0.03*((press-12000)/6000)**2
            
            # Calculate response surfaces
            size_grid = np.zeros_like(cationic_grid)
            pdi_grid = np.zeros_like(cationic_grid)
            
            for i in range(cationic_grid.shape[0]):
                for j in range(cationic_grid.shape[1]):
                    size_grid[i, j] = particle_size_model(cationic_grid[i, j], pressure_grid[i, j])
                    pdi_grid[i, j] = pdi_model(cationic_grid[i, j], pressure_grid[i, j]) * 100  # Scale PDI for visualization
            
            # Create contour plot
            fig = go.Figure()
            
            # Add particle size contours
            fig.add_trace(go.Contour(
                z=size_grid,
                x=cationic,
                y=pressure,
                colorscale='Blues',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=10, color='white')
                ),
                colorbar=dict(title="Particle Size (nm)", x=0.45),
                name="Particle Size"
            ))
            
            # Add PDI contour lines
            fig.add_trace(go.Contour(
                z=pdi_grid,
                x=cationic,
                y=pressure,
                colorscale='Reds',
                contours=dict(
                    coloring='lines',
                    showlabels=True
                ),
                line=dict(width=2),
                colorbar=dict(title="PDI (×100)", x=1.0),
                name="PDI"
            ))
            
            # Add sweet spot
            # Assuming size 80-120 nm and PDI < 0.15
            sweet_spot = np.array([
                [18, 11000], [22, 11000], [22, 14000], [18, 14000], [18, 11000]
            ])
            
            fig.add_trace(go.Scatter(
                x=sweet_spot[:, 0],
                y=sweet_spot[:, 1],
                mode='lines',
                line=dict(color='green', width=2, dash='dot'),
                fill='toself',
                fillcolor='rgba(0, 255, 0, 0.2)',
                name='Design Space'
            ))
            
            # Add optimal point
            fig.add_trace(go.Scatter(
                x=[20],
                y=[12000],
                mode='markers',
                marker=dict(
                    color='green',
                    size=12,
                    symbol='star',
                    line=dict(width=1, color='black')
                ),
                name='Optimal Formulation'
            ))
            
            # Update layout
            fig.update_layout(
                title="Particle Size and PDI Optimization",
                xaxis_title="Cationic Lipid (%)",
                yaxis_title="Homogenization Pressure (psi)",
                height=400
            )
            
            st.plotly_chart(fig)
        
        with col2:
            # Create particle size distribution comparison
            st.markdown("**Particle Size Distribution**")
            
            # Create size distribution data
            size_range = np.linspace(10, 300, 100)
            
            # Log-normal distributions
            initial_dist = stats.lognorm.pdf(size_range, s=0.4, scale=np.exp(5.0))
            optimized_dist = stats.lognorm.pdf(size_range, s=0.2, scale=np.exp(4.6))
            
            # Scale for visualization
            initial_dist = initial_dist / np.max(initial_dist)
            optimized_dist = optimized_dist / np.max(optimized_dist)
            
            # Create line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=size_range,
                y=initial_dist,
                mode='lines',
                name='Initial Formulation',
                line=dict(color='lightgray', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=size_range,
                y=optimized_dist,
                mode='lines',
                name='Optimized Formulation',
                line=dict(color='royalblue', width=2)
            ))
            
            # Add annotations
            fig.add_annotation(
                x=180,
                y=0.3,
                text="Initial: 175 ± 65 nm<br>PDI = 0.30",
                showarrow=True,
                arrowhead=1,
                ax=-40,
                ay=-40
            )
            
            fig.add_annotation(
                x=95,
                y=0.8,
                text="Optimized: 95 ± 15 nm<br>PDI = 0.12",
                showarrow=True,
                arrowhead=1,
                ax=-40,
                ay=-40
            )
            
            # Update layout
            fig.update_layout(
                title="Particle Size Distribution Comparison",
                xaxis_title="Particle Size (nm)",
                yaxis_title="Normalized Intensity",
                height=350
            )
            
            st.plotly_chart(fig)
            
            # Add stability data
            st.markdown("**Accelerated Stability (40°C)**")
            
            # Create stability data
            days = [0, 7, 14, 28, 42]
            
            # Stability metrics
            initial_size = np.array([175, 185, 210, 250, 310])
            optimized_size = np.array([95, 98, 102, 110, 125])
            
            initial_pdi = np.array([0.30, 0.35, 0.42, 0.50, 0.65])
            optimized_pdi = np.array([0.12, 0.13, 0.15, 0.18, 0.22])
            
            # Create multi-Y-axis plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add size traces
            fig.add_trace(
                go.Scatter(
                    x=days,
                    y=initial_size,
                    mode='lines+markers',
                    name='Initial Size',
                    line=dict(color='lightgray', width=2),
                    marker=dict(size=8)
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=days,
                    y=optimized_size,
                    mode='lines+markers',
                    name='Optimized Size',
                    line=dict(color='royalblue', width=2),
                    marker=dict(size=8)
                ),
                secondary_y=False
            )
            
            # Add PDI traces
            fig.add_trace(
                go.Scatter(
                    x=days,
                    y=initial_pdi,
                    mode='lines+markers',
                    name='Initial PDI',
                    line=dict(color='lightgray', width=2, dash='dot'),
                    marker=dict(size=8, symbol='square')
                ),
                secondary_y=True
            )
            
            fig.add_trace(
                go.Scatter(
                    x=days,
                    y=optimized_pdi,
                    mode='lines+markers',
                    name='Optimized PDI',
                    line=dict(color='royalblue', width=2, dash='dot'),
                    marker=dict(size=8, symbol='square')
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title="Accelerated Stability (40°C)",
                xaxis_title="Time (days)",
                height=350
            )
            
            fig.update_yaxes(title_text="Particle Size (nm)", secondary_y=False)
            fig.update_yaxes(title_text="Polydispersity Index (PDI)", secondary_y=True)
            
            st.plotly_chart(fig)
        
        # Implementation and validation
        st.markdown("### Implementation and Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Final Formulation Development**:
            - Optimized formulation: 20% cationic lipid, 60% phospholipid, 20% cholesterol, 1:20 antigen:lipid ratio
            - Process parameters: pH 6.8, 12,000 psi homogenization, 25°C processing temperature
            - Performance: 95 nm particle size, 0.15 PDI, +25 mV zeta potential, 85% antigen loading

            **In Vivo Validation**:
            - Animal studies confirmed enhanced immune response compared to baseline formulation
            - Antibody titers increased 4-fold with optimized adjuvant
            - T-cell response showed balanced Th1/Th2 profile
            - No significant adverse events observed
            
            **Manufacturing Implementation**:
            - Process scaled to 5L batch size using constant pressure-volume principles
            - Quality attributes maintained within target specifications
            - Reproducible production established across three manufacturing lots
            - Stability confirmed for 12 months at 2-8°C
            """)
        
        with col2:
            # Create immune response visualization
            st.markdown("**Immune Response Comparison**")
            
            # Create grouped bar chart for immune responses
            categories = ["IgG Titer (×10³)", "IgG1:IgG2a Ratio", "IFN-γ (pg/mL)", "IL-4 (pg/mL)"]
            
            # Hypothetical data
            antigen_alone = [2.5, 4.5, 120, 80]
            initial_formulation = [5.0, 3.2, 250, 150]
            optimized_formulation = [20.0, 1.8, 650, 220]
            
            # Create grouped bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=categories,
                y=antigen_alone,
                name='Antigen Alone',
                marker_color='lightgray'
            ))
            
            fig.add_trace(go.Bar(
                x=categories,
                y=initial_formulation,
                name='Initial Formulation',
                marker_color='gray'
            ))
            
            fig.add_trace(go.Bar(
                x=categories,
                y=optimized_formulation,
                name='Optimized Formulation',
                marker_color='royalblue'
            ))
            
            # Update layout
            fig.update_layout(
                title="Immune Response Comparison",
                xaxis_title="Immune Parameter",
                yaxis_title="Value",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig)
            
            # Add manufacturing batch consistency
            st.markdown("**Manufacturing Batch Consistency**")
            
            # Create box plots for batch consistency
            parameters = ["Particle Size (nm)", "PDI (×100)", "Zeta Potential (mV)", "Antigen Loading (%)"]
            
            # Hypothetical batch data (3 batches, 3 samples each)
            np.random.seed(42)
            
            size_data = np.random.normal(95, 5, 9)
            pdi_data = np.random.normal(15, 2, 9)  # ×100 for visualization
            zeta_data = np.random.normal(25, 3, 9)
            loading_data = np.random.normal(85, 4, 9)
            
            # Create figure
            fig = go.Figure()
            
            # Add box plots
            fig.add_trace(go.Box(
                y=size_data,
                name=parameters[0],
                boxmean=True,
                marker_color='royalblue'
            ))
            
            fig.add_trace(go.Box(
                y=pdi_data,
                name=parameters[1],
                boxmean=True,
                marker_color='royalblue'
            ))
            
            fig.add_trace(go.Box(
                y=zeta_data,
                name=parameters[2],
                boxmean=True,
                marker_color='royalblue'
            ))
            
            fig.add_trace(go.Box(
                y=loading_data,
                name=parameters[3],
                boxmean=True,
                marker_color='royalblue'
            ))
            
            # Update layout
            fig.update_layout(
                title="Manufacturing Batch Consistency",
                xaxis_title="Parameter",
                yaxis_title="Value",
                height=350
            )
            
            st.plotly_chart(fig)
        
        # Key takeaways
        st.markdown("### Key Takeaways")
        st.markdown("""
        1. **Sequential Approach**: Systematic progression from screening to optimization to robust formulation development
        2. **Critical Interactions**: Identification of key interaction between cationic lipid content and lipid:antigen ratio
        3. **Multi-Objective Optimization**: Balanced particle characteristics, antigen loading, and stability
        4. **Business Impact**: Development timeline accelerated by 6 months and antigen dose reduced by 50% while maintaining efficacy
        """)