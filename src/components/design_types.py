import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from itertools import combinations
import math

def show():
    st.header("Types of Experimental Designs")
    
    st.markdown("""
    The selection of an appropriate experimental design is crucial to the success of any DOE initiative. 
    Different designs offer specific advantages and limitations that must be matched to experimental 
    objectives, resource constraints, and the complexity of the system under study.
    """)
    
    # Create tabs for different design categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Design Selection Framework", 
        "Screening Designs",
        "Factorial Designs",
        "Response Surface Designs",
        "Interactive Design Selector"
    ])
    
    # Tab 1: Design Selection Framework
    with tab1:
        st.markdown("""
        ## Design Selection Framework
        
        Selecting the appropriate experimental design requires balancing information needs, 
        resource constraints, and system complexity. This framework provides guidance for 
        matching design types to your specific experimental objectives.
        """)
        
        # Design selection flowchart
        st.markdown("### Design Selection Decision Path")
        
        # Create a decision tree visualization
        fig = go.Figure()
        
        # Define nodes and positions
        nodes = [
            {"id": 1, "text": "Start", "x": 0, "y": 10},
            {"id": 2, "text": "How many factors?", "x": 0, "y": 8},
            {"id": 3, "text": "Many (>6)", "x": -4, "y": 6},
            {"id": 4, "text": "Few (≤6)", "x": 4, "y": 6},
            {"id": 5, "text": "Screening first?", "x": -4, "y": 4},
            {"id": 6, "text": "Purpose?", "x": 4, "y": 4},
            {"id": 7, "text": "Yes", "x": -6, "y": 2},
            {"id": 8, "text": "No", "x": -2, "y": 2},
            {"id": 9, "text": "Characterization", "x": 2, "y": 2},
            {"id": 10, "text": "Optimization", "x": 6, "y": 2},
            {"id": 11, "text": "Plackett-Burman", "x": -6, "y": 0},
            {"id": 12, "text": "Fractional Factorial (Res III/IV)", "x": -2, "y": 0},
            {"id": 13, "text": "Fractional/Full Factorial", "x": 2, "y": 0},
            {"id": 14, "text": "Response Surface (CCD/BBD)", "x": 6, "y": 0}
        ]
        
        # Add nodes
        for node in nodes:
            # Different styling based on node type
            if node["id"] in [11, 12, 13, 14]:  # Design recommendations
                node_color = "rgba(144, 238, 144, 0.8)"  # Light green
                text_size = 12
            elif node["id"] in [3, 4, 7, 8, 9, 10]:  # Decision options
                node_color = "rgba(173, 216, 230, 0.8)"  # Light blue
                text_size = 12
            else:  # Decision points
                node_color = "rgba(255, 165, 0, 0.8)"  # Orange
                text_size = 14
            
            # Add the node
            fig.add_trace(go.Scatter(
                x=[node["x"]],
                y=[node["y"]],
                mode="markers+text",
                marker=dict(size=30, color=node_color, line=dict(width=1, color="black")),
                text=[node["text"]],
                textposition="middle center",
                textfont=dict(size=text_size),
                hoverinfo="text",
                name=node["text"]
            ))
        
        # Add edges (connections between nodes)
        edges = [
            (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), 
            (5, 7), (5, 8), (6, 9), (6, 10), 
            (7, 11), (8, 12), (9, 13), (10, 14)
        ]
        
        for edge in edges:
            start_node = next(node for node in nodes if node["id"] == edge[0])
            end_node = next(node for node in nodes if node["id"] == edge[1])
            
            fig.add_trace(go.Scatter(
                x=[start_node["x"], end_node["x"]],
                y=[start_node["y"], end_node["y"]],
                mode="lines",
                line=dict(width=2, color="black"),
                hoverinfo="none",
                showlegend=False
            ))
        
        # Update layout
        fig.update_layout(
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[-8, 8]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[-1, 11]
            ),
            title="Design Selection Decision Path",
            height=600,
            width=800,
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig)
        
        # Design comparison table
        st.markdown("### Design Comparison")
        
        design_comparison = pd.DataFrame({
            "Design Type": [
                "Plackett-Burman",
                "Fractional Factorial (Res III)",
                "Fractional Factorial (Res IV)",
                "Fractional Factorial (Res V)",
                "Full Factorial",
                "Central Composite (CCD)",
                "Box-Behnken (BBD)",
                "Mixture Designs",
                "Optimal Designs"
            ],
            "Primary Use": [
                "Screening many factors",
                "Screening with some interaction info",
                "Characterization with interaction focus",
                "Comprehensive characterization",
                "Complete effect characterization",
                "Response surface optimization",
                "Response surface optimization",
                "Formulation optimization",
                "Custom constraints/objectives"
            ],
            "Runs for 5 Factors": [
                "12",
                "8-16",
                "16",
                "16",
                "32",
                "≈27",
                "≈41",
                "Varies",
                "Varies"
            ],
            "Detects Interactions": [
                "No",
                "Limited",
                "Yes, with confounding",
                "Yes, clear",
                "Yes, all",
                "Yes, with quadratics",
                "Yes, with quadratics",
                "Yes, specialized",
                "Design dependent"
            ],
            "Biotechnology Application": [
                "Media/buffer component screening",
                "Initial bioprocess parameter screening",
                "Early-stage process characterization",
                "Critical parameter characterization",
                "Method validation, final characterization",
                "Bioreactor optimization, design space",
                "Formulation optimization, stable factors",
                "Media composition, buffer optimization",
                "Complex constraints, special responses"
            ]
        })
        
        st.dataframe(design_comparison)
    
    # Tab 2: Screening Designs
    with tab2:
        st.markdown("""
        ## Screening Designs
        
        Screening designs efficiently identify significant factors from many candidates with minimal runs. 
        These designs are typically used early in development when many potential factors need to be evaluated.
        """)
        
        # Create expandable sections for each design type
        with st.expander("### Plackett-Burman Designs", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Concept Anchor**: Plackett-Burman designs are highly efficient screening designs that allow investigation of up to N-1 factors in N runs, where N is a multiple of 4.

                **Practical Lens**: In early-stage bioprocess development, Plackett-Burman designs efficiently screen many potential factors with minimal runs. For example, when developing a new CHO cell culture medium, 11 components could be screened in just 12 runs to identify the critical few that significantly impact cell growth and protein production.

                **Mathematical Foundation**:
                Plackett-Burman designs are constructed using Hadamard matrices where:

                $$H_N H_N^T = N I_N$$

                For a design with N runs, the construction creates an orthogonal array with the ability to estimate N-1 main effects.
                """)
            
            with col2:
                # Visualize a small Plackett-Burman design
                pb_matrix = np.array([
                    [1, 1, 1, 1, 1, 1, 1],
                    [1, -1, 1, -1, 1, -1, -1],
                    [1, 1, -1, -1, -1, 1, -1],
                    [1, -1, -1, 1, -1, -1, 1],
                    [1, 1, 1, -1, -1, -1, -1],
                    [1, -1, 1, 1, -1, 1, -1],
                    [1, 1, -1, 1, 1, -1, -1],
                    [1, -1, -1, -1, 1, 1, 1]
                ])
                
                # Create a heatmap of the design matrix
                fig = px.imshow(
                    pb_matrix,
                    labels=dict(x="Factor", y="Run", color="Level"),
                    x=["A", "B", "C", "D", "E", "F", "G"],
                    y=[f"Run {i+1}" for i in range(8)],
                    color_continuous_scale=["red", "green"],
                    title="8-Run Plackett-Burman Design"
                )
                
                fig.update_layout(height=300)
                st.plotly_chart(fig)
            
            st.markdown("""
            **When to Use**:
            - Early development stages with many potential factors (5-20+)
            - Limited resources for experimentation
            - Focus on main effects only (interactions are confounded)
            - Situations where factor sparsity is expected (only a few factors are likely significant)

            **Limitations**:
            - Cannot estimate interactions reliably
            - Risk of effect confounding if interactions are significant
            """)
            
            # Biotech example
            st.markdown("""
            **Biotechnology Example**: 
            
            In a monoclonal antibody production process, a team needed to screen 11 media supplements for their effect on antibody titer. Using a 12-run Plackett-Burman design instead of a 2048-run full factorial experiment, they identified that copper sulfate, zinc sulfate, and insulin had significant positive effects, while iron nitrate had a significant negative effect. This focused subsequent optimization efforts on just these four components, saving substantial development time and resources.
            """)
        
        with st.expander("### Definitive Screening Designs"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Concept Anchor**: Definitive screening designs (DSDs) are efficient three-level designs that allow estimation of main effects, two-factor interactions, and quadratic effects with minimal confounding.

                **Practical Lens**: In biologics formulation development, DSDs efficiently screen buffer components, stabilizers, and pH while simultaneously detecting curvature and interactions. This identifies optimal storage conditions for monoclonal antibodies while minimizing sample requirements and experimental runs.

                **Mathematical Foundation**:
                For m factors, a DSD requires 2m+1 runs with the structure:

                $$X = \\begin{bmatrix} 
                F_m \\\\
                -F_m \\\\
                0_{1 \\times m}
                \\end{bmatrix}$$

                Where $F_m$ is an m×m fold-over design and $0_{1 \\times m}$ is a center point.
                """)
            
            with col2:
                # Create a simplified visualization of a DSD
                # Example for 3 factors
                dsd_matrix = np.array([
                    [1, 0, 0],  # First m rows
                    [0, 1, 0],
                    [0, 0, 1],
                    [-1, 0, 0],  # Next m rows (negative of first m)
                    [0, -1, 0],
                    [0, 0, -1],
                    [0, 0, 0]   # Center point
                ])
                
                # Create a heatmap of the design matrix
                fig = px.imshow(
                    dsd_matrix,
                    labels=dict(x="Factor", y="Run", color="Level"),
                    x=["Factor A", "Factor B", "Factor C"],
                    y=[f"Run {i+1}" for i in range(7)],
                    color_continuous_scale="RdBu_r",
                    color_continuous_midpoint=0,
                    title="Definitive Screening Design (3 factors)"
                )
                
                fig.update_layout(height=300)
                st.plotly_chart(fig)
            
            st.markdown("""
            **When to Use**:
            - Medium number of factors (3-8 typically)
            - Need to detect both main effects and curvature efficiently
            - Desire to screen factors while gathering optimization information
            - Limited material or experimental resources

            **Limitations**:
            - Limited resolution of interaction effects with many factors
            - Requires at least 3 levels per factor (not suitable for categorical factors)
            """)
            
            # Biotech example
            st.markdown("""
            **Biotechnology Example**: 
            
            A biopharmaceutical company used a definitive screening design to simultaneously screen and characterize six critical parameters in a freeze-drying process for a protein therapeutic. With just 13 experimental runs, they identified not only the significant main effects (shelf temperature, pressure) but also detected the nonlinear relationship between freezing temperature and protein stability. The DSD approach revealed a critical interaction between annealing time and ramp rate that would have been missed in traditional screening designs, allowing them to establish optimal lyophilization conditions in a single experimental campaign.
            """)
    
    # Tab 3: Factorial Designs
    with tab3:
        st.markdown("""
        ## Factorial Designs
        
        Factorial designs systematically investigate effects and interactions by testing combinations
        of factor levels. These designs form the foundation of DOE and can be adapted to different 
        experimental objectives.
        """)
        
        # Create expandable sections for each design type
        with st.expander("### Full Factorial Designs", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Concept Anchor**: Full factorial designs explore all possible combinations of factor levels, providing complete information about main effects and interactions at the expense of experiment size.

                **Practical Lens**: In analytical method validation, full factorial designs thoroughly investigate method robustness by testing all combinations of factors like pH, temperature, and mobile phase composition, ensuring complete understanding of method performance across the operating range.

                **Mathematical Foundation**:
                For k factors each at 2 levels, a full factorial requires $2^k$ runs. The design allows estimation of:
                - k main effects
                - $\\binom{k}{2}$ two-factor interactions
                - $\\binom{k}{3}$ three-factor interactions
                - ... up to one k-factor interaction
                """)
            
            with col2:
                # Visualization of a 2^3 full factorial
                fig = go.Figure()
                
                # Define the vertices of a cube
                vertices = np.array([
                    [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
                    [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]
                ])
                
                # Add the points (vertices of the cube)
                fig.add_trace(go.Scatter3d(
                    x=vertices[:, 0],
                    y=vertices[:, 1],
                    z=vertices[:, 2],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color='blue'
                    ),
                    name='Design Points'
                ))
                
                # Define the edges of the cube
                edges = [
                    (0, 1), (0, 2), (0, 4), (1, 3), (1, 5),
                    (2, 3), (2, 6), (3, 7), (4, 5), (4, 6),
                    (5, 7), (6, 7)
                ]
                
                # Add the edges
                for edge in edges:
                    fig.add_trace(go.Scatter3d(
                        x=[vertices[edge[0], 0], vertices[edge[1], 0]],
                        y=[vertices[edge[0], 1], vertices[edge[1], 1]],
                        z=[vertices[edge[0], 2], vertices[edge[1], 2]],
                        mode='lines',
                        line=dict(color='black', width=2),
                        showlegend=False
                    ))
                
                # Update layout
                fig.update_layout(
                    title="2³ Full Factorial Design",
                    scene=dict(
                        xaxis_title="Factor A",
                        yaxis_title="Factor B",
                        zaxis_title="Factor C",
                        xaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 1]),
                        yaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 1]),
                        zaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 1])
                    ),
                    margin=dict(l=0, r=0, b=0, t=30),
                    height=300
                )
                
                st.plotly_chart(fig)
            
            st.markdown("""
            **When to Use**:
            - Small number of factors (typically 2-5)
            - Complete characterization of interaction structure is needed
            - Sufficient resources are available
            - High-risk applications where comprehensive understanding is crucial
            - Regulatory studies requiring thorough characterization

            **Limitations**:
            - Experiment size grows exponentially with the number of factors
            - May be resource-intensive for many factors
            """)
            
            # Biotech example
            st.markdown("""
            **Biotechnology Example**: 
            
            For the validation of a critical analytical HPLC method used to quantify product-related impurities in a monoclonal antibody product, a QC team implemented a 2³ full factorial design to evaluate method robustness. The design thoroughly characterized how column temperature (35-45°C), mobile phase pH (6.8-7.2), and flow rate (0.8-1.2 mL/min) affected retention time, resolution, and peak area. The comprehensive nature of the full factorial revealed a significant interaction between pH and temperature that affected critical resolution, informing appropriate control strategy and system suitability criteria for the validated method.
            """)
        
        with st.expander("### Fractional Factorial Designs"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Concept Anchor**: Fractional factorial designs use a carefully selected subset of full factorial runs, sacrificing some information (creating confounding) to reduce experimental size.

                **Practical Lens**: In upstream bioprocess optimization, a 2^(6-2) fractional factorial design could investigate six parameters (temperature, pH, DO, feed rate, inoculum density, and agitation) in just 16 runs instead of 64, quickly identifying the vital few parameters affecting protein production.

                **Mathematical Foundation**:
                A $2^{k-p}$ fractional factorial design requires $2^{k-p}$ runs for k factors, where p represents the fraction (1/2^p of the full factorial). The design is generated using:

                1. A full factorial in k-p factors
                2. Additional p factors created through defining relations
                """)
            
            with col2:
                # Visualize a half-fraction of a 2³ factorial (2³⁻¹)
                # Example: I = ABC (Resolution III)
                # This gives us 4 points (half of the full factorial's 8 points)
                
                # Define the half-fraction (selecting points where ABC = +1)
                half_fraction = np.array([
                    [-1, -1, -1],  # ABC = -1*-1*-1 = -1
                    [-1, 1, 1],    # ABC = -1*1*1 = -1
                    [1, -1, 1],    # ABC = 1*-1*1 = -1
                    [1, 1, -1]     # ABC = 1*1*-1 = -1
                ])
                
                # Create a 3D scatter plot
                fig = go.Figure()
                
                # Add the points
                fig.add_trace(go.Scatter3d(
                    x=half_fraction[:, 0],
                    y=half_fraction[:, 1],
                    z=half_fraction[:, 2],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color='blue'
                    ),
                    name='Design Points'
                ))
                
                # Define the edges that connect these points
                edges = [
                    (0, 1), (0, 2), (1, 3), (2, 3)
                ]
                
                # Add the edges
                for edge in edges:
                    fig.add_trace(go.Scatter3d(
                        x=[half_fraction[edge[0], 0], half_fraction[edge[1], 0]],
                        y=[half_fraction[edge[0], 1], half_fraction[edge[1], 1]],
                        z=[half_fraction[edge[0], 2], half_fraction[edge[1], 2]],
                        mode='lines',
                        line=dict(color='black', width=2),
                        showlegend=False
                    ))
                
                # Update layout
                fig.update_layout(
                    title="2³⁻¹ Fractional Factorial Design",
                    scene=dict(
                        xaxis_title="Factor A",
                        yaxis_title="Factor B",
                        zaxis_title="Factor C",
                        xaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 1]),
                        yaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 1]),
                        zaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 1])
                    ),
                    margin=dict(l=0, r=0, b=0, t=30),
                    height=300
                )
                
                st.plotly_chart(fig)
            
            # Additional explanation on resolution
            st.markdown("""
            **Design Resolution**:
            - Resolution III: Main effects are aliased with two-factor interactions
            - Resolution IV: Main effects are clear, but two-factor interactions are aliased with each other
            - Resolution V: Main effects and two-factor interactions are clear (aliased with three-factor interactions)

            **When to Use**:
            - Medium to large number of factors (4-8+)
            - Resources are limited relative to the number of factors
            - Effect sparsity is expected
            - Resolution can be selected based on importance of interactions

            **Limitations**:
            - Confounding structure requires careful planning
            - Risk of missing important effects due to confounding
            - May require follow-up experiments to resolve ambiguities
            """)
            
            # Biotech example
            st.markdown("""
            **Biotechnology Example**: 
            
            During development of a recombinant protein production process, a bioprocess team needed to evaluate seven critical parameters in the upstream process. Rather than running a full factorial design requiring 128 bioreactor runs, they implemented a 2^(7-3) fractional factorial design with Resolution IV. This design required only 16 bioreactor runs, yet still provided clear estimation of all main effects and some information about interactions. The study identified dissolved oxygen concentration, feed rate timing, and temperature shift as the most significant factors affecting protein titer, enabling targeted optimization in subsequent experiments while saving months of development time and hundreds of thousands of dollars in resources.
            """)
    
    # Tab 4: Response Surface Designs
    with tab4:
        st.markdown("""
        ## Response Surface Designs
        
        Response surface designs extend factorial designs to model curvature and optimize processes.
        These designs are typically used in later development stages to find optimal operating conditions.
        """)
        
        # Create expandable sections for each design type
        with st.expander("### Central Composite Designs", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Concept Anchor**: Central composite designs (CCDs) extend factorial designs to enable quadratic modeling and optimization through the addition of axial and center points.

                **Practical Lens**: In bioreactor optimization, CCDs efficiently map the curved response surface of protein yield with respect to key parameters like temperature, pH, and glucose concentration, identifying optimal setpoints while detecting maximum yield regions that would be missed by linear models.

                **Mathematical Foundation**:
                A CCD consists of three components:
                1. A factorial portion (either $2^k$ or $2^{k-p}$)
                2. Axial points at $(±α, 0, 0, ...)$, $(0, ±α, 0, ...)$, etc.
                3. Center points at $(0, 0, 0, ...)$

                The total number of runs is:
                $$N = 2^k + 2k + n_c \quad \\text{or} \quad N = 2^{k-p} + 2k + n_c$$
                """)
            
            with col2:
                # Visualization of a central composite design for 2 factors
                # Factorial points (4), axial points (4), and center point (1)
                
                # Define the points
                factorial = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])
                alpha = 1.414  # Traditional value for rotatability
                axial = np.array([[-alpha, 0], [alpha, 0], [0, -alpha], [0, alpha]])
                center = np.array([[0, 0]])
                
                # Combine all points
                all_points = np.vstack([factorial, axial, center])
                point_types = ['Factorial']*4 + ['Axial']*4 + ['Center']*1
                
                # Create a scatter plot
                fig = px.scatter(
                    x=all_points[:, 0],
                    y=all_points[:, 1],
                    color=point_types,
                    labels={"x": "Factor A", "y": "Factor B", "color": "Point Type"},
                    title="Central Composite Design (2 factors)",
                    color_discrete_map={
                        "Factorial": "blue",
                        "Axial": "red",
                        "Center": "green"
                    },
                    width=350,
                    height=300
                )
                
                # Update layout
                fig.update_layout(
                    xaxis=dict(range=[-2, 2], tickvals=[-1.414, -1, 0, 1, 1.414]),
                    yaxis=dict(range=[-2, 2], tickvals=[-1.414, -1, 0, 1, 1.414]),
                    shapes=[
                        # Add square for factorial portion
                        dict(
                            type="rect",
                            x0=-1, y0=-1, x1=1, y1=1,
                            line=dict(color="blue", width=1, dash="dash"),
                            fillcolor="rgba(0, 0, 255, 0.1)"
                        ),
                        # Add circle for rotatability
                        dict(
                            type="circle",
                            x0=-1.414, y0=-1.414, x1=1.414, y1=1.414,
                            line=dict(color="red", width=1, dash="dash"),
                            fillcolor="rgba(255, 0, 0, 0.1)"
                        )
                    ]
                )
                
                st.plotly_chart(fig)
            
            st.markdown("""
            **Types of CCDs**:
            - Circumscribed CCD: Uses points outside the factorial space (α > 1)
            - Inscribed CCD: Scales factors to keep all points within original range
            - Face-centered CCD: Sets α = 1, keeping axial points on faces of factorial space

            **When to Use**:
            - Optimization stage after significant factors are identified
            - When quadratic (curved) responses are expected
            - Need to identify optimal factor settings
            - Development of robust operating windows
            - Establishing design space for regulatory submissions

            **Limitations**:
            - Requires more runs than factorial designs
            - Works best with 2-5 factors (becomes large with many factors)
            - Three or more levels required for each factor
            """)
            
            # Biotech example
            st.markdown("""
            **Biotechnology Example**: 
            
            A process development team used a central composite design to optimize a CHO cell culture process for a monoclonal antibody. The CCD investigated temperature (32-38°C), pH (6.6-7.4), and dissolved oxygen (20-60%) with five center points to estimate pure experimental error. The quadratic model revealed a optimal region at 34.5°C, pH 7.0, and 40% DO where productivity was 30% higher than baseline conditions. Importantly, the CCD identified a significant curvature in the temperature response that would have been missed with a linear design, showing decreased productivity at both temperature extremes. The resulting response surface model directly informed the process design space filed with regulatory authorities and guided manufacturing control strategy.
            """)
        
        with st.expander("### Box-Behnken Designs"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Concept Anchor**: Box-Behnken designs are spherical response surface designs that explore factor combinations at midpoints of edges of the design space rather than corners.

                **Practical Lens**: In protein formulation development, Box-Behnken designs efficiently explore pH, ionic strength, and excipient concentrations to optimize protein stability while avoiding extreme corner conditions that might cause precipitation or denaturation.

                **Mathematical Foundation**:
                Box-Behnken designs are formed by combining 2^2 factorial designs with incomplete block designs. For k factors, the design includes:
                - Points where some factors are at their midpoints (0) and others are at (+1) and (-1)
                - Center points (all factors at 0)

                The number of runs is approximately:
                $$N = 2k(k-1) + c_p$$
                """)
            
            with col2:
                # Visualization of a Box-Behnken design for 3 factors
                # For 3 factors, we have 12 edge midpoints + center points
                
                # Define the points
                bbd_points = np.array([
                    # (±1, ±1, 0) - 4 points
                    [-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0],
                    # (±1, 0, ±1) - 4 points
                    [-1, 0, -1], [-1, 0, 1], [1, 0, -1], [1, 0, 1],
                    # (0, ±1, ±1) - 4 points
                    [0, -1, -1], [0, -1, 1], [0, 1, -1], [0, 1, 1],
                    # Center point
                    [0, 0, 0]
                ])
                
                # Create a 3D scatter plot
                fig = go.Figure(data=go.Scatter3d(
                    x=bbd_points[:, 0],
                    y=bbd_points[:, 1],
                    z=bbd_points[:, 2],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=['blue']*12 + ['green'],  # Edge points blue, center point green
                        opacity=0.8
                    ),
                    text=["Edge Point"]*12 + ["Center Point"],
                    hovertemplate='%{text}<br>A: %{x}<br>B: %{y}<br>C: %{z}'
                ))
                
                # Update layout
                fig.update_layout(
                    title="Box-Behnken Design (3 factors)",
                    scene=dict(
                        xaxis_title="Factor A",
                        yaxis_title="Factor B",
                        zaxis_title="Factor C",
                        xaxis=dict(range=[-1.2, 1.2], tickvals=[-1, 0, 1]),
                        yaxis=dict(range=[-1.2, 1.2], tickvals=[-1, 0, 1]),
                        zaxis=dict(range=[-1.2, 1.2], tickvals=[-1, 0, 1])
                    ),
                    margin=dict(l=0, r=0, b=0, t=30),
                    height=350
                )
                
                # Add a sphere to visualize the spherical design region
                phi = np.linspace(0, 2*np.pi, 20)
                theta = np.linspace(-np.pi/2, np.pi/2, 20)
                phi, theta = np.meshgrid(phi, theta)
                
                x = np.cos(theta) * np.sin(phi)
                y = np.cos(theta) * np.cos(phi)
                z = np.sin(theta)
                
                fig.add_trace(go.Surface(
                    x=x, y=y, z=z,
                    opacity=0.2,
                    colorscale=[[0, 'blue'], [1, 'blue']],
                    showscale=False
                ))
                
                st.plotly_chart(fig)
            
            st.markdown("""
            **When to Use**:
            - Optimization with 3-5 factors
            - When corner points of the design space are problematic or infeasible
            - Resource constraints make CCDs too expensive
            - Need for a design with fewer runs than CCD
            - All factors must be quantitative (not categorical)

            **Limitations**:
            - Requires at least 3 factors
            - Cannot estimate pure cubic terms
            - Does not include factorial corners
            - May provide less information about the boundaries of the design space
            """)
            
            # Biotech example
            st.markdown("""
            **Biotechnology Example**: 
            
            A formulation team developing a protein therapeutic used a Box-Behnken design to optimize buffer conditions for maximum stability. The design explored three critical factors: pH (6.0-8.0), ionic strength (50-150 mM), and sucrose concentration (0-10% w/v). The Box-Behnken design was selected specifically because previous experiments showed protein aggregation at extreme combinations of pH and ionic strength (the "corner" conditions of the design space). By using 15 experimental conditions (including 3 center points), the team developed a quadratic model that identified an optimal formulation at pH 7.2, 120 mM ionic strength, and 8% sucrose, with predicted shelf-life exceeding 24 months. The design's efficiency allowed complete formulation development with minimal protein consumption, an important consideration for early-stage development.
            """)
    
    # Tab 5: Interactive Design Selector
    with tab5:
        # Call the interactive function for design selection
        design_selection_guide()

def design_selection_guide():
    st.header("DOE Design Selection Guide")
    
    st.markdown("""
    This interactive guide will help you select the most appropriate experimental design 
    for your biotechnology application based on your specific requirements and constraints.
    """)
    
    # Main selection tool
    st.subheader("Design Selection Wizard")
    
    # Use tabs for a step-by-step approach
    tab1, tab2, tab3 = st.tabs(["Step 1: Define Requirements", "Step 2: Compare Options", "Step 3: Design Details"])
    
    # Step 1: Gather requirements
    with tab1:
        st.markdown("### Define Your Experimental Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Key parameters for design selection
            num_factors = st.slider("Number of Factors", 2, 15, 4,
                                 help="How many independent variables do you need to study?")
            
            study_phase = st.radio("Study Phase", 
                                ["Screening", "Characterization", "Optimization"],
                                help="""
                                - Screening: Identify important factors from many candidates
                                - Characterization: Understand effects and interactions
                                - Optimization: Find optimal settings and build response surfaces
                                """)
            
            interactions_importance = st.select_slider(
                "Importance of Interactions",
                options=["Not Important", "Somewhat Important", "Very Important", "Critical"],
                value="Somewhat Important",
                help="How important is it to detect and measure interaction effects?")
            
            curvature_importance = st.select_slider(
                "Importance of Curvature/Nonlinearity",
                options=["Not Important", "Somewhat Important", "Very Important", "Critical"],
                value="Somewhat Important",
                help="How important is it to detect and model nonlinear (quadratic) effects?")
        
        with col2:
            resource_constraint = st.select_slider(
                "Resource Constraint Level",
                options=["Minimal", "Moderate", "Severe", "Extreme"],
                value="Moderate",
                help="How limited are your experimental resources (time, material, budget)?")
            
            hard_to_change = st.checkbox("Includes Hard-to-Change Factors", 
                                       help="Are some factors difficult or time-consuming to change between runs?")
            
            is_mixture = st.checkbox("Mixture Problem (Components Sum to 100%)", 
                                   help="Is this a formulation where components must sum to 100%?")
            
            has_constraints = st.checkbox("Design Space Constraints", 
                                        help="Are there constraints on factor combinations or design space?")
            
            prior_knowledge = st.select_slider(
                "Level of Prior Knowledge",
                options=["Very Limited", "Some Understanding", "Good Understanding", "Extensive"],
                value="Some Understanding",
                help="How much do you already know about the system?")
    
    # Step 2: Compare design options
    with tab2:
        # Calculate design recommendations based on inputs
        designs = []
        
        # Logic for design recommendations
        # Scoring system (0-10 scale, higher is better match)
        
        # Full Factorial scoring
        ff_score = 10
        ff_score -= (num_factors - 3) * 1.5  # Penalty for more factors
        ff_score -= {"Minimal": 0, "Moderate": 2, "Severe": 5, "Extreme": 8}[resource_constraint]
        ff_score += {"Not Important": 0, "Somewhat Important": 1, "Very Important": 2, "Critical": 3}[interactions_importance]
        ff_score = max(0, min(10, ff_score))
        
        designs.append({
            "Design": "Full Factorial",
            "Score": ff_score,
            "Runs": 2**num_factors,
            "Strengths": "Complete information on main effects and interactions",
            "Limitations": "Requires many runs with increased factors",
            "Use Case": "Complete process characterization, method validation"
        })
        
        # Fractional Factorial scoring
        fr_score = 8
        fr_score += min(3, (num_factors - 3) * 0.5)  # Bonus for more factors, up to a point
        fr_score += {"Minimal": 0, "Moderate": 1, "Severe": 2, "Extreme": 3}[resource_constraint]
        fr_score -= {"Not Important": 0, "Somewhat Important": 1, "Very Important": 2, "Critical": 3}[interactions_importance]
        fr_score = max(0, min(10, fr_score))
        
        # Resolution adjustment
        if interactions_importance == "Not Important":
            resolution = "III"
            runs = max(2**(num_factors - max(1, num_factors-4)), 8)
        elif interactions_importance == "Somewhat Important":
            resolution = "IV"
            runs = max(2**(num_factors - max(1, num_factors-5)), 16)
        else:
            resolution = "V" 
            runs = max(2**(num_factors - max(1, num_factors-6)), 16)
            
        designs.append({
            "Design": f"Fractional Factorial (Resolution {resolution})",
            "Score": fr_score,
            "Runs": runs,
            "Strengths": "Efficient with good balance of information and runs",
            "Limitations": f"Some confounding of effects with Resolution {resolution}",
            "Use Case": "Early to mid-stage process development, screening with interactions"
        })
        
        # Plackett-Burman scoring
        pb_score = 6
        pb_score += min(4, (num_factors - 3) * 0.5)  # Bonus for more factors
        pb_score += {"Minimal": 0, "Moderate": 1, "Severe": 2, "Extreme": 3}[resource_constraint]
        pb_score -= {"Not Important": 0, "Somewhat Important": 2, "Very Important": 4, "Critical": 6}[interactions_importance]
        pb_score = max(0, min(10, pb_score))
        
        designs.append({
            "Design": "Plackett-Burman",
            "Score": pb_score,
            "Runs": 4 * (int(num_factors / 4) + (1 if num_factors % 4 > 0 else 0)),
            "Strengths": "Maximum efficiency for main effects screening",
            "Limitations": "Interactions are completely confounded with main effects",
            "Use Case": "Initial screening with many factors, media component screening"
        })
        
        # Definitive Screening Design scoring
        dsd_score = 7
        dsd_score += min(2, (num_factors - 3) * 0.5)  # Small bonus for more factors
        dsd_score -= max(0, (num_factors - 8) * 0.5)  # Penalty for too many factors
        dsd_score += {"Not Important": 0, "Somewhat Important": 0, "Very Important": 1, "Critical": 2}[interactions_importance]
        dsd_score += {"Not Important": 0, "Somewhat Important": 1, "Very Important": 2, "Critical": 3}[curvature_importance]
        dsd_score = max(0, min(10, dsd_score))
        
        designs.append({
            "Design": "Definitive Screening",
            "Score": dsd_score,
            "Runs": 2 * num_factors + 1,
            "Strengths": "Efficient screening with ability to detect curvature",
            "Limitations": "Limited resolution of many interactions",
            "Use Case": "Efficient factor screening with some optimization capability"
        })
        
        # Central Composite Design scoring
        ccd_score = 5
        ccd_score -= max(0, (num_factors - 5) * 0.5)  # Penalty for too many factors
        ccd_score -= {"Minimal": 0, "Moderate": 1, "Severe": 2, "Extreme": 3}[resource_constraint]
        ccd_score += {"Not Important": 0, "Somewhat Important": 1, "Very Important": 3, "Critical": 4}[curvature_importance]
        ccd_score += {"Screening": 0, "Characterization": 2, "Optimization": 4}[study_phase]
        ccd_score = max(0, min(10, ccd_score))
        
        designs.append({
            "Design": "Central Composite",
            "Score": ccd_score,
            "Runs": 2**min(num_factors, 5) + 2*num_factors + 1,
            "Strengths": "Complete quadratic modeling and optimization",
            "Limitations": "Requires more runs than factorial designs",
            "Use Case": "Bioprocess optimization, establishing design space"
        })
        
        # Box-Behnken Design scoring
        bbd_score = 4
        if num_factors >= 3:
            bbd_score += 2
            bbd_score -= max(0, (num_factors - 5) * 0.5)  # Penalty for too many factors
            bbd_score -= {"Minimal": 0, "Moderate": 0, "Severe": 1, "Extreme": 2}[resource_constraint]
            bbd_score += {"Not Important": 0, "Somewhat Important": 1, "Very Important": 2, "Critical": 3}[curvature_importance]
            bbd_score += {"Screening": 0, "Characterization": 1, "Optimization": 3}[study_phase]
        else:
            bbd_score = 0  # Not applicable for fewer than 3 factors
            
        bbd_score = max(0, min(10, bbd_score))
        
        designs.append({
            "Design": "Box-Behnken",
            "Score": bbd_score if num_factors >= 3 else 0,
            "Runs": 2*num_factors*(num_factors-1) + 1 if num_factors >= 3 else "N/A",
            "Strengths": "Efficient quadratic modeling, avoids extreme conditions",
            "Limitations": "Requires at least 3 factors, no factorial corners",
            "Use Case": "Optimization with limited resources, when extreme conditions are problematic"
        })
        
        # Mixture design scoring
        mix_score = 0
        if is_mixture:
            mix_score = 8
            mix_score -= {"Minimal": 0, "Moderate": 1, "Severe": 2, "Extreme": 3}[resource_constraint]
            mix_score += {"Not Important": 0, "Somewhat Important": 1, "Very Important": 2, "Critical": 3}[curvature_importance]
            
            # Extreme vertices adjustments
            if has_constraints:
                mix_score += 2
                mix_design = "Extreme Vertices"
            else:
                mix_design = "Simplex Lattice"
                
            mix_score = max(0, min(10, mix_score))
            
            designs.append({
                "Design": mix_design + " (Mixture)",
                "Score": mix_score,
                "Runs": "Varies",
                "Strengths": "Specialized for formulation optimization",
                "Limitations": "Limited to mixture problems",
                "Use Case": "Media optimization, buffer formulation, excipient studies" 
            })
        
        # Split-plot design scoring
        sp_score = 0
        if hard_to_change:
            sp_score = 7
            sp_score -= {"Minimal": 3, "Moderate": 1, "Severe": 0, "Extreme": 0}[resource_constraint]
            sp_score = max(0, min(10, sp_score))
            
            designs.append({
                "Design": "Split-Plot",
                "Score": sp_score,
                "Runs": "Varies",
                "Strengths": "Accommodates hard-to-change factors",
                "Limitations": "More complex analysis required",
                "Use Case": "Bioreactor experiments, equipment-limited studies"
            })
        
        # Optimal design scoring
        opt_score = 5
        if has_constraints:
            opt_score += 3
        if num_factors > 7:
            opt_score += 2
        if resource_constraint in ["Severe", "Extreme"]:
            opt_score += 2
            
        opt_score = max(0, min(10, opt_score))
        
        designs.append({
            "Design": "Optimal Design (Custom)",
            "Score": opt_score,
            "Runs": "Custom",
            "Strengths": "Maximum flexibility for complex constraints",
            "Limitations": "Requires specialized software, less intuitive",
            "Use Case": "Complex constraints, unusual factor combinations"
        })
        
        # Sort designs by score
        designs.sort(key=lambda x: x["Score"], reverse=True)
        
        # Display design recommendations
        st.markdown("### Recommended Designs")
        st.markdown("Ranked by suitability for your requirements:")
        
        # Create a dataframe for display
        df_display = pd.DataFrame([
            {
                "Design": d["Design"],
                "Suitability Score": d["Score"],
                "Number of Runs": d["Runs"],
                "Key Strengths": d["Strengths"]
            }
            for d in designs if d["Score"] > 0
        ])
        
        # Display as a table
        st.dataframe(df_display)
        
        # Visualize design comparison
        top_designs = [d for d in designs if d["Score"] > 3]
        
        fig = px.bar(
            x=[d["Design"] for d in top_designs],
            y=[d["Score"] for d in top_designs],
            labels={"x": "Design Type", "y": "Suitability Score"},
            title="Design Suitability Comparison",
            color=[d["Score"] for d in top_designs],
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_range=[0, 10]
        )
        
        st.plotly_chart(fig)
        
        # Design efficiency comparison (runs vs information)
        valid_designs = [d for d in designs if d["Score"] > 0 and d["Runs"] != "Varies" and d["Runs"] != "N/A" and d["Runs"] != "Custom"]
        
        if valid_designs:
            st.subheader("Design Efficiency Comparison")
            
            # Normalize scores to represent information content (0-100%)
            information_scores = [d["Score"] * 10 for d in valid_designs]
            run_counts = [d["Runs"] for d in valid_designs]
            design_names = [d["Design"] for d in valid_designs]
            
            # Calculate efficiency ratio (information per run)
            efficiency_ratio = [info / runs for info, runs in zip(information_scores, run_counts)]
            
            fig = go.Figure()
            
            # Add scatter plot for designs
            fig.add_trace(go.Scatter(
                x=run_counts,
                y=information_scores,
                mode='markers+text',
                marker=dict(
                    size=15,
                    color=efficiency_ratio,
                    colorscale='Viridis',
                    colorbar=dict(title="Efficiency"),
                    showscale=True
                ),
                text=design_names,
                textposition="top center",
                name='Designs'
            ))
            
            # Add reference line
            max_runs = max(run_counts)
            fig.add_trace(go.Scatter(
                x=[0, max_runs],
                y=[0, 100],
                mode='lines',
                line=dict(dash='dash', color='gray'),
                name='Linear Reference'
            ))
            
            fig.update_layout(
                title="Information vs. Experimental Runs",
                xaxis_title="Number of Experimental Runs",
                yaxis_title="Relative Information Content (%)",
                height=500
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Interpretation:**
            - **Higher position** = more information
            - **Further left** = fewer runs
            - **Brighter color** = better efficiency (information per run)
            - Designs above the dashed line provide better-than-linear information gain
            """)
    
    # Step 3: Design details
    with tab3:
        # Detailed information about top recommended design
        if designs:
            top_design = designs[0]["Design"]
            
            st.markdown(f"### {top_design} Design Details")
            
            # Design-specific guidance
            if "Full Factorial" in top_design:
                st.markdown("""
                #### Full Factorial Design
                
                **Description**: Explores all possible combinations of factor levels. For a two-level design with k factors, 
                requires 2ᵏ runs.
                
                **Key Properties**:
                - Complete information on main effects and all interactions
                - Orthogonal design (all effects estimated independently)
                - Maximum statistical power for a given factor count
                
                **Best For**:
                - Small number of factors (typically 2-5)
                - Detailed characterization studies
                - Method validation
                - Regulatory submissions requiring comprehensive understanding
                
                **Biotechnology Application Example**:
                In analytical method validation for a therapeutic protein, a full factorial design
                examines how pH (6.5, 7.5), temperature (25°C, 35°C), and buffer concentration 
                (low, high) affect assay performance. All 8 combinations are tested, 
                enabling complete characterization of main effects and interactions to 
                establish method robustness.
                """)
                
                # Visual representation of design
                st.subheader("Design Structure")
                
                if num_factors <= 3:
                    # Create a 3D cube representation for up to 3 factors
                    points = []
                    labels = []
                    
                    # Generate all factorial combinations
                    for i in range(2**min(num_factors, 3)):
                        coords = [(i >> j) & 1 for j in range(min(num_factors, 3))]
                        while len(coords) < 3:
                            coords.append(0)  # Pad to 3D
                        points.append(coords)
                        labels.append(f"Run {i+1}")
                    
                    # Convert to numpy array
                    points = np.array(points)
                    
                    # Create 3D scatter plot
                    fig = go.Figure(data=[go.Scatter3d(
                        x=points[:, 0],
                        y=points[:, 1],
                        z=points[:, 2],
                        mode='markers+text',
                        marker=dict(
                            size=10,
                            color=range(len(points)),
                            colorscale='Viridis',
                        ),
                        text=labels,
                        textposition="top center"
                    )])
                    
                    # Update layout
                    fig.update_layout(
                        title="Full Factorial Design Structure",
                        scene=dict(
                            xaxis_title="Factor A",
                            yaxis_title="Factor B",
                            zaxis_title="Factor C" if num_factors >= 3 else "",
                            xaxis=dict(range=[-0.1, 1.1], tickvals=[0, 1], ticktext=["-1", "+1"]),
                            yaxis=dict(range=[-0.1, 1.1], tickvals=[0, 1], ticktext=["-1", "+1"]),
                            zaxis=dict(range=[-0.1, 1.1], tickvals=[0, 1], ticktext=["-1", "+1"]),
                        ),
                        height=600,
                        width=700
                    )
                    
                    st.plotly_chart(fig)
                else:
                    # For more than 3 factors, show the design matrix
                    design_matrix = np.zeros((2**min(num_factors, 5), min(num_factors, 5)))
                    
                    for i in range(2**min(num_factors, 5)):
                        for j in range(min(num_factors, 5)):
                            design_matrix[i, j] = 2 * ((i >> j) & 1) - 1  # Convert to -1/+1
                    
                    # Convert to dataframe for display
                    factor_names = [f"Factor {chr(65+j)}" for j in range(min(num_factors, 5))]
                    dm_df = pd.DataFrame(design_matrix, columns=factor_names)
                    dm_df.insert(0, "Run", range(1, dm_df.shape[0] + 1))
                    
                    st.dataframe(dm_df)
                    if num_factors > 5:
                        st.info(f"Note: Showing first 5 of {num_factors} factors for readability.")
                
            elif "Fractional Factorial" in top_design:
                # Extract resolution from design name
                resolution = "IV"  # Default
                if "III" in top_design:
                    resolution = "III"
                elif "V" in top_design:
                    resolution = "V"
                
                st.markdown(f"""
                #### Fractional Factorial Design (Resolution {resolution})
                
                **Description**: Uses a fraction of the full factorial runs while maintaining 
                balance and orthogonality. A 2^(k-p) design uses 1/(2^p) of the full factorial runs.
                
                **Key Properties**:
                - Resolution {resolution} design allows estimation of:
                  {"- Main effects (may be confounded with 2-factor interactions)" if resolution == "III" else
                   "- Main effects clear of 2-factor interactions" if resolution == "IV" else
                   "- Main effects and 2-factor interactions clear of each other"}
                - Requires fewer runs than full factorial
                - Maintains orthogonality of design matrix
                
                **Best For**:
                - {"Initial screening of many factors" if resolution == "III" else
                   "Characterization when some interactions may be important" if resolution == "IV" else
                   "Detailed characterization where interactions are important"}
                - Resource-constrained experiments
                - {"Studies where main effects dominate" if resolution == "III" else
                   "Studies where some interactions may be present" if resolution == "IV" else
                   "Studies where interactions are expected to be significant"}
                
                **Biotechnology Application Example**:
                {
                "In a mammalian cell culture media optimization, 7 media components are screened using a Resolution III design with just 8 runs instead of 128. This efficiently identifies the 2-3 components with the largest impact on cell growth for further optimization." if resolution == "III" else
                "In a downstream purification process, a Resolution IV design with 16 runs evaluates 5 chromatography parameters, clearly identifying main effects while providing some information about potential interactions between buffer pH and salt concentration." if resolution == "IV" else
                "During viral vector process characterization, a Resolution V design evaluates 4 critical process parameters with 16 runs, fully resolving both main effects and interactions to support regulatory filing requirements for this high-risk product."
                }
                """)
                
                # Visual representation of the design
                st.subheader("Design Structure")
                
                # Calculate design properties based on resolution
                if resolution == "III":
                    fraction = max(1, num_factors-4)
                elif resolution == "IV":
                    fraction = max(1, num_factors-5)
                else:  # Resolution V
                    fraction = max(1, num_factors-6)
                    
                fraction = min(fraction, num_factors-1)
                runs = 2**(num_factors-fraction)
                
                # Display aliasing pattern
                st.markdown(f"""
                **Generator{'s' if fraction > 1 else ''}:** 
                {
                "E = ABC, F = BCD, G = ACD" if num_factors == 7 and fraction == 3 else
                "E = ABC, F = BCD" if num_factors == 6 and fraction == 2 else
                "E = ABC" if num_factors == 5 and fraction == 1 else
                "Custom generators would be used for this design"
                }
                
                **Defining Relation:** 
                {
                "I = ABCE = BCDF = ACDG = ABCDEFG" if num_factors == 7 and fraction == 3 else
                "I = ABCE = BCDF = ADEF" if num_factors == 6 and fraction == 2 else
                "I = ABCE" if num_factors == 5 and fraction == 1 else
                "Custom defining relation would be used for this design"
                }
                
                **Design Size:** 2^({num_factors}-{fraction}) = {runs} runs
                """)
                
                # Create example design matrix
                if runs <= 32:  # Only show for reasonably sized designs
                    # Create a basic design matrix for visual purposes
                    base_factors = num_factors - fraction
                    design_matrix = np.zeros((runs, num_factors))
                    
                    # Generate the basic design for independent factors
                    for i in range(runs):
                        for j in range(base_factors):
                            # Standard order: alternating -1/+1 with frequency 2^j
                            design_matrix[i, j] = 1 if (i // 2**(base_factors-j-1)) % 2 else -1
                    
                    # Generate dependent factors (simplified for visualization)
                    for i in range(fraction):
                        idx = base_factors + i
                        if idx < num_factors:
                            # Simple generators for demonstration
                            if resolution == "III":
                                # Resolution III: Use 2-factor interaction
                                design_matrix[:, idx] = design_matrix[:, 0] * design_matrix[:, 1]
                            elif resolution == "IV":
                                # Resolution IV: Use 3-factor interaction
                                design_matrix[:, idx] = design_matrix[:, 0] * design_matrix[:, 1] * design_matrix[:, 2]
                            else:
                                # Resolution V: Use 4-factor interaction
                                if base_factors >= 4:
                                    design_matrix[:, idx] = design_matrix[:, 0] * design_matrix[:, 1] * design_matrix[:, 2] * design_matrix[:, 3]
                                else:
                                    design_matrix[:, idx] = design_matrix[:, 0] * design_matrix[:, 1] * design_matrix[:, 2]
                    
                    # Convert to dataframe for display
                    factor_names = [f"Factor {chr(65+j)}" for j in range(num_factors)]
                    dm_df = pd.DataFrame(design_matrix, columns=factor_names)
                    dm_df.insert(0, "Run", range(1, dm_df.shape[0] + 1))
                    
                    st.dataframe(dm_df.style.format("{:.0f}"))
                else:
                    st.info(f"Design matrix would contain {runs} runs. Too large to display in full.")
            
            elif "Plackett-Burman" in top_design:
                st.markdown("""
                #### Plackett-Burman Design
                
                **Description**: Highly efficient screening designs that can evaluate N-1 factors in 
                N runs, where N is a multiple of 4. Based on Hadamard matrices.
                
                **Key Properties**:
                - Maximum efficiency for screening main effects
                - Orthogonal design
                - Minimal run count for given number of factors
                - Resolution III (main effects confounded with two-factor interactions)
                
                **Best For**:
                - Early screening with many potential factors
                - Projects with severe resource constraints
                - Applications where interactions are less likely or less important
                - Identifying significant main effects from many candidates
                
                **Biotechnology Application Example**:
                During early media optimization for a bacterial production strain, a Plackett-Burman
                design screens 11 different media components in just 12 runs, rapidly identifying
                the 3-4 components that significantly affect productivity. This efficient design
                allows the team to focus resources on optimizing only the critical components.
                """)
                
                # Calculate Plackett-Burman size
                pb_size = 4 * (int(num_factors / 4) + (1 if num_factors % 4 > 0 else 0))
                
                # Generate basic PB design
                st.markdown(f"**Design Size:** {pb_size} runs for up to {pb_size-1} factors")
                
                if pb_size <= 20:  # Only show for reasonably sized designs
                    # Create a basic PB design for visual purposes (simplified)
                    if pb_size == 8:
                        # Example 8-run PB design
                        first_row = [1, 1, 1, -1, 1, -1, -1]
                    elif pb_size == 12:
                        # Example 12-run PB design
                        first_row = [1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1]
                    elif pb_size == 16:
                        # Example 16-run PB design
                        first_row = [1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 1, -1]
                    elif pb_size == 20:
                        # Example 20-run PB design
                        first_row = [1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1]
                    else:
                        first_row = [1] * (pb_size - 1)  # Placeholder
                    
                    # Generate the design from the first row
                    pb_design = [first_row]
                    for i in range(1, pb_size-1):
                        # Shift the previous row to the right
                        new_row = [pb_design[i-1][-1]] + pb_design[i-1][:-1]
                        pb_design.append(new_row)
                    
                    # Add the final row of -1s
                    pb_design.append([-1] * (pb_size-1))
                    
                    # Convert to numpy array
                    pb_array = np.array(pb_design)
                    
                    # Truncate to actual number of factors
                    display_factors = min(num_factors, pb_size-1)
                    pb_array = pb_array[:, :display_factors]
                    
                    # Convert to dataframe for display
                    factor_names = [f"Factor {chr(65+j)}" for j in range(display_factors)]
                    pb_df = pd.DataFrame(pb_array, columns=factor_names)
                    pb_df.insert(0, "Run", range(1, pb_df.shape[0] + 1))
                    
                    st.dataframe(pb_df.style.format("{:.0f}"))
                else:
                    st.info(f"Design matrix would contain {pb_size} runs. Too large to display in full.")
            
            elif "Definitive Screening" in top_design:
                st.markdown("""
                #### Definitive Screening Design
                
                **Description**: Advanced three-level screening designs that require only 2k+1 runs 
                (k = number of factors) while providing information about main effects, two-factor 
                interactions, and quadratic effects with minimal confounding.
                
                **Key Properties**:
                - Main effects orthogonal to two-factor interactions
                - Main effects orthogonal to quadratic effects
                - Efficient three-level design
                - Capable of both screening and some optimization
                
                **Best For**:
                - Projects needing both screening and some optimization capability
                - Medium number of factors (3-8)
                - Studies where curvature (quadratic effects) may be important
                - Efficient use of experimental resources
                
                **Biotechnology Application Example**:
                In developing a freeze-drying process for a therapeutic protein, a definitive screening
                design evaluates 6 factors in just 13 runs, screening for important parameters while
                simultaneously detecting the nonlinear relationship between freezing temperature and
                protein stability, allowing rapid process optimization in a single experiment.
                """)
                
                # Visual representation
                st.subheader("Design Structure")
                
                # Generate a simple visualization of the DSD pattern
                dsd_runs = 2 * num_factors + 1
                st.markdown(f"**Design Size:** 2 × {num_factors} + 1 = {dsd_runs} runs")
                
                # DSD structure visualization
                cols = ["Run"] + [f"Factor {chr(65+i)}" for i in range(min(num_factors, 6))]
                rows = []
                
                # First block (fold-over pairs)
                for i in range(num_factors):
                    row = [i+1] + [0] * min(num_factors, 6)
                    row[i+1] = 1  # Diagonal structure
                    rows.append(row)
                
                # Second block (negative fold-over)
                for i in range(num_factors):
                    row = [i+num_factors+1] + [0] * min(num_factors, 6)
                    row[i+1] = -1  # Negative diagonal
                    rows.append(row)
                
                # Center point
                rows.append([dsd_runs] + [0] * min(num_factors, 6))
                
                # Convert to dataframe
                dsd_df = pd.DataFrame(rows, columns=cols)
                
                # Display with appropriate styling
                def highlight_cells(val):
                    if val == 1:
                        return 'background-color: #a8d08d'
                    elif val == -1:
                        return 'background-color: #f4b084'
                    elif val == 0:
                        return 'background-color: #e2efda'
                    else:
                        return ''
                
                # Apply styling only to factor columns
                styled_dsd = dsd_df.style.applymap(highlight_cells, subset=cols[1:])
                
                st.dataframe(styled_dsd)
                
                if num_factors > 6:
                    st.info(f"Showing only the first 6 of {num_factors} factors for readability.")
            
            elif "Central Composite" in top_design:
                st.markdown("""
                #### Central Composite Design (CCD)
                
                **Description**: A response surface design that extends factorial designs to estimate
                full quadratic models by adding axial (star) points and center points to a factorial core.
                
                **Key Properties**:
                - Enables estimation of complete quadratic models
                - Can be made rotatable (prediction variance depends only on distance from center)
                - Provides good prediction throughout the design space
                - Consists of factorial points, axial points, and center points
                
                **Best For**:
                - Process optimization
                - Detailed characterization of response surfaces
                - Identifying optimal operating conditions
                - Establishing design space for regulatory purposes
                - Applications where curvature (quadratic effects) is important
                
                **Biotechnology Application Example**:
                In bioreactor optimization for a CHO cell culture process, a central composite design
                explores critical parameters (temperature, pH, DO, feed strategy) to maximize protein
                production while maintaining quality attributes. The design reveals optimal conditions
                and an operating window where productivity exceeds 3 g/L while maintaining >90% product
                quality, supporting process validation and regulatory filings.
                """)
                
                # Visual representation
                st.subheader("Design Structure")
                
                # Calculate CCD size
                factorial_points = min(2**num_factors, 16)  # Cap factorial portion
                axial_points = 2 * num_factors
                center_points = 3  # Typical value
                total_points = factorial_points + axial_points + center_points
                
                st.markdown(f"""
                **Design Components:**
                - Factorial portion: {factorial_points} points
                - Axial (star) points: {axial_points} points
                - Center points: {center_points} points
                - Total runs: {total_points} runs
                """)
                
                # CCD visualization for 2 or 3 factors
                if num_factors == 2:
                    # Create points for 2D CCD
                    factorial = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])
                    axial = np.array([[-1.414, 0], [1.414, 0], [0, -1.414], [0, 1.414]])
                    center = np.array([[0, 0]])
                    
                    # Create figure
                    fig = go.Figure()
                    
                    # Add factorial points
                    fig.add_trace(go.Scatter(
                        x=factorial[:, 0], y=factorial[:, 1],
                        mode='markers',
                        marker=dict(size=10, color='blue'),
                        name='Factorial Points'
                    ))
                    
                    # Add axial points
                    fig.add_trace(go.Scatter(
                        x=axial[:, 0], y=axial[:, 1],
                        mode='markers',
                        marker=dict(size=10, color='red'),
                        name='Axial Points'
                    ))
                    
                    # Add center point
                    fig.add_trace(go.Scatter(
                        x=center[:, 0], y=center[:, 1],
                        mode='markers',
                        marker=dict(size=10, color='green'),
                        name='Center Points'
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title="Central Composite Design (2 Factors)",
                        xaxis_title="Factor A",
                        yaxis_title="Factor B",
                        xaxis=dict(range=[-1.6, 1.6]),
                        yaxis=dict(range=[-1.6, 1.6]),
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig)
                    
                elif num_factors == 3:
                    # Create points for 3D CCD
                    factorial = np.array([
                        [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
                        [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]
                    ])
                    
                    axial = np.zeros((6, 3))
                    axial[0] = [-1.682, 0, 0]
                    axial[1] = [1.682, 0, 0]
                    axial[2] = [0, -1.682, 0]
                    axial[3] = [0, 1.682, 0]
                    axial[4] = [0, 0, -1.682]
                    axial[5] = [0, 0, 1.682]
                    
                    center = np.array([[0, 0, 0]])
                    
                    # Create figure
                    fig = go.Figure()
                    
                    # Add factorial points
                    fig.add_trace(go.Scatter3d(
                        x=factorial[:, 0], y=factorial[:, 1], z=factorial[:, 2],
                        mode='markers',
                        marker=dict(size=5, color='blue'),
                        name='Factorial Points'
                    ))
                    
                    # Add axial points
                    fig.add_trace(go.Scatter3d(
                        x=axial[:, 0], y=axial[:, 1], z=axial[:, 2],
                        mode='markers',
                        marker=dict(size=5, color='red'),
                        name='Axial Points'
                    ))
                    
                    # Add center point
                    fig.add_trace(go.Scatter3d(
                        x=center[:, 0], y=center[:, 1], z=center[:, 2],
                        mode='markers',
                        marker=dict(size=5, color='green'),
                        name='Center Points'
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title="Central Composite Design (3 Factors)",
                        scene=dict(
                            xaxis_title="Factor A",
                            yaxis_title="Factor B",
                            zaxis_title="Factor C",
                            xaxis=dict(range=[-2, 2]),
                            yaxis=dict(range=[-2, 2]),
                            zaxis=dict(range=[-2, 2])
                        ),
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig)
                else:
                    # For more factors, show the design table
                    st.info(f"CCD for {num_factors} factors would have {total_points} runs. Showing conceptual design structure.")
                    
                    # Create a conceptual design table
                    design_types = ["Factorial"] * 4 + ["Axial"] * (min(num_factors, 4) * 2) + ["Center"] * 3
                    factor_values = []
                    
                    # Add a few factorial points
                    factor_values.append([-1] * num_factors)
                    factor_values.append([-1] * (num_factors-1) + [1])
                    factor_values.append([1] * (num_factors-1) + [-1])
                    factor_values.append([1] * num_factors)
                    
                    # Add axial points for a few factors
                    for i in range(min(num_factors, 4)):
                        axial_minus = [0] * num_factors
                        axial_minus[i] = -1.682
                        factor_values.append(axial_minus)
                        
                        axial_plus = [0] * num_factors
                        axial_plus[i] = 1.682
                        factor_values.append(axial_plus)
                    
                    # Add center points
                    for _ in range(3):
                        factor_values.append([0] * num_factors)
                    
                    # Create dataframe
                    design_data = {
                        "Run Type": design_types
                    }
                    
                    for i in range(min(num_factors, 5)):
                        design_data[f"Factor {chr(65+i)}"] = [row[i] for row in factor_values]
                    
                    design_df = pd.DataFrame(design_data)
                    
                    # Display with color coding
                    def highlight_run_type(val):
                        if val == "Factorial":
                            return 'background-color: #a8d08d'
                        elif val == "Axial":
                            return 'background-color: #f4b084'
                        elif val == "Center":
                            return 'background-color: #e2efda'
                        else:
                            return ''
                    
                    styled_design = design_df.style.applymap(highlight_run_type, subset=["Run Type"])
                    
                    st.dataframe(styled_design)
                    
                    if num_factors > 5:
                        st.info(f"Showing only the first 5 of {num_factors} factors for readability.")
            
            elif "Box-Behnken" in top_design:
                st.markdown("""
                #### Box-Behnken Design
                
                **Description**: A response surface design that explores combinations at the midpoints
                of edges of the design space rather than the corners, requiring fewer runs than CCD
                for the same number of factors.
                
                **Key Properties**:
                - Requires 3 levels for each factor
                - Avoids extreme factor combinations (corners)
                - More efficient than CCD for 3-5 factors
                - Good prediction throughout the experimental region
                - All points equidistant from center
                
                **Best For**:
                - Process optimization with 3-5 factors
                - Applications where extreme conditions are undesirable
                - Situations with resource constraints
                - When a quadratic model is needed
                - Applications where spherical design region is appropriate
                
                **Biotechnology Application Example**:
                During protein formulation development, a Box-Behnken design optimizes stability
                by exploring pH (6.0, 7.0, 8.0), ionic strength (50, 150, 250 mM), and excipient
                concentration (0%, 5%, 10%) while avoiding extreme combinations that might cause
                precipitation. This design identifies an optimal formulation with 2-year stability
                while requiring 33% fewer experiments than a comparable CCD.
                """)
                
                # Visual representation
                st.subheader("Design Structure")
                
                # Calculate BBD size
                if num_factors >= 3:
                    bbd_runs = 2*num_factors*(num_factors-1) + 1
                    
                    st.markdown(f"""
                    **Design Size:** 2 × {num_factors} × ({num_factors}-1) + 1 = {bbd_runs} runs
                    
                    **Level Requirements:** Each factor at 3 levels (-1, 0, +1)
                    """)
                    
                    # BBD visualization for 3 factors
                    if num_factors == 3:
                        # Create points for 3D BBD
                        bbd_points = np.array([
                            [-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0],
                            [-1, 0, -1], [-1, 0, 1], [1, 0, -1], [1, 0, 1],
                            [0, -1, -1], [0, -1, 1], [0, 1, -1], [0, 1, 1],
                            [0, 0, 0]  # Center point
                        ])
                        
                        # Create figure
                        fig = go.Figure()
                        
                        # Add BBD points
                        fig.add_trace(go.Scatter3d(
                            x=bbd_points[:-1, 0], y=bbd_points[:-1, 1], z=bbd_points[:-1, 2],
                            mode='markers',
                            marker=dict(size=5, color='blue'),
                            name='Design Points'
                        ))
                        
                        # Add center point
                        fig.add_trace(go.Scatter3d(
                            x=[bbd_points[-1, 0]], y=[bbd_points[-1, 1]], z=[bbd_points[-1, 2]],
                            mode='markers',
                            marker=dict(size=5, color='red'),
                            name='Center Point'
                        ))
                        
                        # Update layout
                        fig.update_layout(
                            title="Box-Behnken Design (3 Factors)",
                            scene=dict(
                                xaxis_title="Factor A",
                                yaxis_title="Factor B",
                                zaxis_title="Factor C",
                                xaxis=dict(range=[-1.2, 1.2], tickvals=[-1, 0, 1]),
                                yaxis=dict(range=[-1.2, 1.2], tickvals=[-1, 0, 1]),
                                zaxis=dict(range=[-1.2, 1.2], tickvals=[-1, 0, 1])
                            ),
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig)
                    else:
                        # For more factors, show the design table
                        st.info(f"Box-Behnken design for {num_factors} factors would have {bbd_runs} runs.")
                        
                        # Create a conceptual design table with a subset of runs
                        # Generate some example BBD runs
                        factor_values = []
                        
                        # For each pair of factors, add the 4 combinations at midpoint of other factors
                        for i in range(min(num_factors, 4)):
                            for j in range(i+1, min(num_factors, 4)):
                                run1 = [0] * num_factors
                                run1[i], run1[j] = -1, -1
                                factor_values.append(run1)
                                
                                run2 = [0] * num_factors
                                run2[i], run2[j] = -1, 1
                                factor_values.append(run2)
                                
                                run3 = [0] * num_factors
                                run3[i], run3[j] = 1, -1
                                factor_values.append(run3)
                                
                                run4 = [0] * num_factors
                                run4[i], run4[j] = 1, 1
                                factor_values.append(run4)
                                
                                # Only show a subset of runs
                                if len(factor_values) >= 12:
                                    break
                            if len(factor_values) >= 12:
                                break
                        
                        # Add center point
                        factor_values.append([0] * num_factors)
                        
                        # Create run numbers
                        run_numbers = list(range(1, len(factor_values) + 1))
                        
                        # Create dataframe
                        design_data = {
                            "Run": run_numbers
                        }
                        
                        for i in range(min(num_factors, 5)):
                            design_data[f"Factor {chr(65+i)}"] = [row[i] for row in factor_values]
                        
                        design_df = pd.DataFrame(design_data)
                        
                        st.dataframe(design_df)
                        
                        if num_factors > 5:
                            st.info(f"Showing only the first 5 of {num_factors} factors for readability.")
                else:
                    st.warning("Box-Behnken designs require at least 3 factors.")
            
            elif "Mixture" in top_design:
                mixture_type = "Simplex Lattice" if "Simplex Lattice" in top_design else "Extreme Vertices"
                
                st.markdown(f"""
                #### {mixture_type} Design (Mixture)
                
                **Description**: Specialized design for mixture experiments where component proportions
                must sum to 100% (or 1). {
                "Simplex lattice designs provide uniform coverage across the mixture space." if mixture_type == "Simplex Lattice" else
                "Extreme vertices designs handle constrained mixture spaces with additional limits on components."
                }
                
                **Key Properties**:
                - Components must sum to 1 (or 100%)
                - {
                "Uniform distribution of points in mixture space" if mixture_type == "Simplex Lattice" else
                "Focuses on vertices (corners) of constrained mixture space"
                }
                - Enables modeling of blending properties
                - Requires specialized mixture models
                
                **Best For**:
                - Formulation development
                - Buffer composition optimization
                - Media development
                - Excipient studies
                - Any experiment where components must sum to a constant total
                {
                "" if mixture_type == "Simplex Lattice" else
                "- Mixture problems with additional constraints (min/max levels for components)"
                }
                
                **Biotechnology Application Example**:
                {
                "In development of a cryopreservation medium for stem cells, a simplex lattice design optimizes the mixture of three cryoprotectants (DMSO, glycerol, and trehalose) while maintaining a constant total concentration. The design identifies a synergistic blend of 7% DMSO, 3% glycerol, and 2% trehalose that provides superior cell viability compared to single-component formulations." if mixture_type == "Simplex Lattice" else
                "In formulating a biologic drug product, an extreme vertices design optimizes the buffer composition with constraints: pH must remain 6.0-7.0, total buffer concentration 50-100 mM, and specific excipients have minimum required concentrations. The optimized formulation improves stability by 30% while meeting all pharmaceutical requirements."
                }
                """)
                
                # Visual representation
                st.subheader("Design Structure")
                
                # Simplex visualization for 3 components
                if num_factors <= 3:
                    # Create ternary plot
                    if mixture_type == "Simplex Lattice":
                        # Create simplex lattice points for ternary plot
                        points = []
                        # Full factorial at 0, 0.5, 1
                        for i in range(3):
                            for j in range(3):
                                for k in range(3):
                                    if i/2 + j/2 + k/2 == 1:  # Ensure points sum to 1
                                        points.append([i/2, j/2, k/2])
                    else:  # Extreme vertices
                        # Create constrained points for ternary plot
                        points = []
                        # Vertices
                        points.append([0.7, 0.2, 0.1])  # Max A, min B, min C
                        points.append([0.2, 0.7, 0.1])  # Min A, max B, min C
                        points.append([0.2, 0.1, 0.7])  # Min A, min B, max C
                        # Edge centers
                        points.append([0.45, 0.45, 0.1])  # Midpoint AB edge
                        points.append([0.45, 0.1, 0.45])  # Midpoint AC edge
                        points.append([0.2, 0.4, 0.4])    # Midpoint BC edge
                        # Overall centroid
                        points.append([0.35, 0.35, 0.3])
                    
                    points = np.array(points)
                    
                    # Create ternary plot using plotly
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterternary(
                        a=points[:, 0],
                        b=points[:, 1],
                        c=points[:, 2],
                        mode='markers',
                        marker=dict(size=10, color='blue'),
                        text=[f"({a:.1f}, {b:.1f}, {c:.1f})" for a, b, c in points],
                        hoverinfo="text"
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title=f"{mixture_type} Design (3 Components)",
                        ternary=dict(
                            aaxis=dict(title="Component A", min=0, linewidth=2, ticks='outside'),
                            baxis=dict(title="Component B", min=0, linewidth=2, ticks='outside'),
                            caxis=dict(title="Component C", min=0, linewidth=2, ticks='outside'),
                            sum=1
                        ),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig)
                    
                    if mixture_type == "Extreme Vertices":
                        st.markdown("""
                        **Example Constraints Visualized:**
                        - Component A: 0.2 ≤ A ≤ 0.7
                        - Component B: 0.1 ≤ B ≤ 0.7
                        - Component C: 0.1 ≤ C ≤ 0.7
                        - Sum of all components = 1.0
                        """)
                else:
                    st.info(f"Mixture designs with {num_factors} components are harder to visualize. In practice, these would be generated using specialized software.")
                    
                    # Show conceptual table structure
                    st.subheader("Conceptual Design Structure")
                    
                    # Create example mixture design table
                    if mixture_type == "Simplex Lattice":
                        # Generate simplex lattice for first 4 components
                        display_factors = min(num_factors, 4)
                        mixture_points = []
                        
                        # Pure components
                        for i in range(display_factors):
                            point = [0] * display_factors
                            point[i] = 1
                            mixture_points.append(point)
                        
                        # Binary blends (50/50)
                        for i in range(display_factors):
                            for j in range(i+1, display_factors):
                                point = [0] * display_factors
                                point[i] = 0.5
                                point[j] = 0.5
                                mixture_points.append(point)
                        
                        # Overall centroid
                        mixture_points.append([1/display_factors] * display_factors)
                    else:
                        # Generate extreme vertices for first 4 components
                        display_factors = min(num_factors, 4)
                        mixture_points = []
                        
                        # Assume constraints: 0.1 ≤ x_i ≤ 0.7
                        
                        # Some vertices
                        for i in range(display_factors):
                            point = [0.1] * display_factors
                            point[i] = 0.7
                            # Adjust to ensure sum = 1
                            total = sum(point)
                            if total != 1:
                                for j in range(display_factors):
                                    point[j] = point[j] / total
                            mixture_points.append(point)
                        
                        # Some edge centers
                        for i in range(display_factors):
                            for j in range(i+1, display_factors):
                                point = [0.1] * display_factors
                                point[i] = 0.4
                                point[j] = 0.4
                                # Adjust to ensure sum = 1
                                total = sum(point)
                                if total != 1:
                                    for k in range(display_factors):
                                        point[k] = point[k] / total
                                mixture_points.append(point)
                        
                        # Overall centroid
                        mixture_points.append([1/display_factors] * display_factors)
                    
                    # Create dataframe
                    component_names = [f"Component {chr(65+i)}" for i in range(display_factors)]
                    mixture_df = pd.DataFrame(mixture_points, columns=component_names)
                    
                    # Add run numbers and format
                    mixture_df.insert(0, "Run", range(1, len(mixture_points) + 1))
                    mixture_df = mixture_df.round(2)
                    
                    # Add sum column to validate
                    mixture_df["Sum"] = mixture_df[component_names].sum(axis=1).round(2)
                    
                    st.dataframe(mixture_df)
                    
                    if num_factors > 4:
                        st.info(f"Showing only the first 4 of {num_factors} components for readability.")
            
            elif "Split-Plot" in top_design:
                st.markdown("""
                #### Split-Plot Design
                
                **Description**: A design structure that accommodates hard-to-change factors by 
                organizing runs into whole plots (where hard-to-change factors are constant) and 
                subplots (where easy-to-change factors vary).
                
                **Key Properties**:
                - Two levels of randomization
                - Accommodates hard-to-change factors
                - More efficient use of resources
                - Requires special analysis methods
                - Can be applied to any base design (factorial, response surface, etc.)
                
                **Best For**:
                - Experiments with hard-to-change factors
                - Bioreactor or equipment-intensive studies
                - Processes with significant setup/changeover time
                - Studies where complete randomization is impractical
                - Large-scale or time-intensive experiments
                
                **Biotechnology Application Example**:
                In a viral vector manufacturing process, temperature and bioreactor type are 
                difficult to change, while feeding strategy and harvest time are easily varied.
                A split-plot design organizes runs by temperature-bioreactor combinations (whole plots),
                with different feeding-harvest combinations (subplots) randomized within each.
                This approach reduces setup time by 60% while still characterizing all critical
                process parameters effectively.
                """)
                
                # Visual representation
                st.subheader("Design Structure")
                
                # Calculate number of hard-to-change factors
                hard_factors = 2  # Assume 2 for example
                easy_factors = num_factors - hard_factors
                
                st.markdown(f"""
                **Example Split-Plot Structure:**
                - Hard-to-change factors: 2 (e.g., Temperature, Equipment Type)
                - Easy-to-change factors: {num_factors - 2} (e.g., pH, Feed Rate, etc.)
                """)
                
                # Create conceptual split-plot visualization
                # Create a table representation
                whole_plots = 4  # 2^2 for 2 hard factors
                sub_plots = 4  # Simplified example
                
                # Create whole plot factors
                hard_factor_values = []
                for i in range(whole_plots):
                    hard_factor_values.append([
                        -1 if (i // 2**(j)) % 2 == 0 else 1 
                        for j in range(hard_factors)
                    ])
                
                # Create subplot factors (simplified)
                easy_factor_values = []
                for i in range(sub_plots):
                    easy_factor_values.append([
                        -1 if (i // 2**(j)) % 2 == 0 else 1 
                        for j in range(min(easy_factors, 2))
                    ])
                
                # Build the full design
                runs = []
                run_number = 1
                
                for wp, hard_vals in enumerate(hard_factor_values):
                    for sp, easy_vals in enumerate(easy_factor_values):
                        # Combine hard and easy factors
                        full_vals = hard_vals + easy_vals
                        # Pad if needed
                        while len(full_vals) < min(num_factors, 4):
                            full_vals.append(0)
                        
                        runs.append([run_number, f"WP{wp+1}", f"SP{sp+1}"] + full_vals)
                        run_number += 1
                
                # Create column names
                cols = ["Run", "Whole Plot", "Subplot"]
                factor_cols = []
                for i in range(hard_factors):
                    factor_cols.append(f"Hard Factor {chr(65+i)}")
                for i in range(min(easy_factors, 2)):
                    factor_cols.append(f"Easy Factor {chr(65+hard_factors+i)}")
                
                # Fill any remaining factors
                while len(cols) + len(factor_cols) < 7:  # Target 7 columns total
                    factor_cols.append(f"Factor {chr(65+len(factor_cols))}")
                
                cols = cols + factor_cols
                
                # Create dataframe
                sp_df = pd.DataFrame(runs, columns=cols)
                
                # Color coding for whole plots
                def highlight_wp(df):
                    styles = []
                    for i in range(len(df)):
                        row_style = [''] * len(df.columns)
                        wp = df.iloc[i, 1]  # Whole Plot column
                        if wp == 'WP1':
                            row_style = ['background-color: #e2efda'] * len(df.columns)
                        elif wp == 'WP2':
                            row_style = ['background-color: #f8cbad'] * len(df.columns)
                        elif wp == 'WP3':
                            row_style = ['background-color: #c5e0b4'] * len(df.columns)
                        elif wp == 'WP4':
                            row_style = ['background-color: #f4b084'] * len(df.columns)
                        styles.append(row_style)
                    return styles
                
                st.dataframe(sp_df.style.apply(highlight_wp, axis=None))
                
                st.markdown("""
                **Note on Analysis:** Split-plot designs require specialized statistical analysis 
                methods that account for the two different error structures (whole-plot error and 
                subplot error). Standard ANOVA or regression techniques are not appropriate.
                """)
            
            elif "Optimal Design" in top_design:
                st.markdown("""
                #### Optimal Design (Custom)
                
                **Description**: Computer-generated designs that optimize specific statistical 
                criteria while accommodating complex constraints, irregular factor ranges, or 
                unusual models.
                
                **Key Properties**:
                - Maximizes statistical efficiency for specific criteria
                - Accommodates irregular design spaces and constraints
                - Works with non-standard models
                - Highly flexible but less structured
                - Several optimality criteria available (D, A, I, G)
                
                **Best For**:
                - Experiments with complex constraints
                - Non-standard models or response surfaces
                - Augmenting existing designs
                - Highly resource-constrained applications
                - Unique factor level combinations
                - Mixed categorical and continuous factors
                
                **Biotechnology Application Example**:
                In developing a chromatography method for a complex biologic, a D-optimal design
                investigates 6 factors (pH, salt concentration, resin type, flow rate, load density,
                wash volume) with constraints: pH must be lower during loading than elution, 
                and flow rate limits vary by resin type. The optimal design provides maximum
                information about critical parameters while respecting all physical constraints,
                reducing development time by 40%.
                """)
                
                # Visual representation
                st.subheader("Design Approach")
                
                st.markdown("""
                **Optimal Design Criteria:**
                
                - **D-optimal**: Maximizes determinant of information matrix (X'X)
                  * Minimizes the volume of the joint confidence region for parameter estimates
                  * Most commonly used criterion
                
                - **A-optimal**: Minimizes the trace of the inverse information matrix
                  * Minimizes the average variance of parameter estimates
                
                - **I-optimal**: Minimizes average prediction variance across design region
                  * Best for prediction purposes
                
                - **G-optimal**: Minimizes maximum prediction variance across design region
                  * Ensures no region has excessively high prediction uncertainty
                """)
                
                # Visualization of D-optimal vs standard design
                st.subheader("Example: D-optimal vs. Standard Design")
                
                # Create example visualization
                if num_factors <= 2:
                    # Create constraint boundary for 2D example
                    x = np.linspace(-1, 1, 100)
                    y_upper = 0.8 * np.sqrt(1 - x**2)
                    y_lower = -0.4 - 0.2 * x
                    
                    # Create standard design points (factorial)
                    std_points = np.array([
                        [-1, -1], [-1, 1], [1, -1], [1, 1], [0, 0]
                    ])
                    
                    # Create optimal design points (respecting constraints)
                    opt_points = np.array([
                        [-1, -0.4], [-0.6, 0.7], [0.5, 0.7], [1, -0.3], [0, 0.3]
                    ])
                    
                    # Create figure
                    fig = go.Figure()
                    
                    # Add constraint boundaries
                    fig.add_trace(go.Scatter(
                        x=x, y=y_upper,
                        mode='lines',
                        line=dict(color='red', dash='dash'),
                        name='Upper Constraint'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=x, y=y_lower,
                        mode='lines',
                        line=dict(color='red', dash='dash'),
                        name='Lower Constraint',
                        fill='tonexty', 
                        fillcolor='rgba(255, 200, 200, 0.2)'
                    ))
                    
                    # Add standard design points
                    fig.add_trace(go.Scatter(
                        x=std_points[:, 0], y=std_points[:, 1],
                        mode='markers',
                        marker=dict(size=10, color='blue', symbol='circle-open'),
                        name='Standard Design (Invalid)'
                    ))
                    
                    # Add optimal design points
                    fig.add_trace(go.Scatter(
                        x=opt_points[:, 0], y=opt_points[:, 1],
                        mode='markers',
                        marker=dict(size=10, color='green'),
                        name='D-optimal Design'
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title="D-optimal vs. Standard Design with Constraints",
                        xaxis_title="Factor A",
                        yaxis_title="Factor B",
                        xaxis=dict(range=[-1.2, 1.2]),
                        yaxis=dict(range=[-0.6, 0.9])
                    )
                    
                    st.plotly_chart(fig)
                    
                    st.markdown("""
                    **Interpretation:**
                    - The red dashed lines represent constraints in the design space
                    - Standard factorial design points (blue) fall outside the feasible region
                    - D-optimal design points (green) are placed to maximize information while respecting constraints
                    """)
                else:
                    st.info(f"Optimal designs for {num_factors} factors would typically be generated using specialized software.")
                    
                    st.markdown("""
                    **Examples of Complex Constraints in Biotechnology:**
                    
                    1. **Process Constraints:**
                       - Temperature must increase gradually between steps
                       - pH must be lower during loading than elution
                       - Mixing time must increase with viscosity
                    
                    2. **Physical Constraints:**
                       - Total buffer concentration must remain within osmolality limits
                       - Combined excipient levels must not exceed solubility limits
                       - Operating parameters must stay within equipment capabilities
                    
                    3. **Logical Constraints:**
                       - If using Resin A, flow rate must be below X
                       - When Temperature > Y, holding time must be less than Z
                       - For live cell processes, viable cell density must be above threshold
                    """)
            
            # Include implementation guidance based on design
            st.subheader("Implementation Guidance")
            
            # General implementation steps
            st.markdown("""
            1. **Finalize Factor Ranges:** Ensure levels are practically achievable
            2. **Create Randomization Schedule:** Generate randomized run order
            3. **Prepare Detailed Protocol:** Document detailed procedures for each step
            4. **Pilot Test:** Validate methods with a small number of runs if possible
            5. **Execute with Careful Documentation:** Record all observations, even unexpected ones
            6. **Analyze Systematically:** Follow appropriate statistical methods for your design
            7. **Validate Findings:** Confirm key results with confirmation runs
            """)
            
            # Add design-specific analysis tips
            if "Response Surface" in top_design or "Box-Behnken" in top_design:
                st.markdown("""
                **Analysis Tips for Response Surface Designs:**
                - Begin with full quadratic model
                - Use backward elimination to remove non-significant terms
                - Check for adequate model fit (R², PRESS, lack-of-fit)
                - Create response surface plots for visualization
                - Perform numerical optimization to find optimal factor settings
                """)
            elif "Fractional Factorial" in top_design:
                st.markdown("""
                **Analysis Tips for Fractional Factorial Designs:**
                - Check aliasing patterns when interpreting effects
                - Use normal probability plots to identify significant effects
                - Consider follow-up experiments to resolve ambiguities
                - Be cautious about interactions confounded with main effects
                - Use effect sparsity principle as screening guideline
                """)
            elif "Split-Plot" in top_design:
                st.markdown("""
                **Analysis Tips for Split-Plot Designs:**
                - Use appropriate mixed model analysis techniques
                - Account for different error structures for whole plots vs. subplots
                - Expect lower precision for hard-to-change factors
                - Consider consulting with a statistician for complex designs
                - Use restricted maximum likelihood (REML) estimation methods
                """)
            elif "Mixture" in top_design:
                st.markdown("""
                **Analysis Tips for Mixture Designs:**
                - Use specialized mixture models (Scheffé polynomials)
                - Remember linear terms have different interpretation than standard designs
                - Visualize results with ternary plots or contour plots
                - Consider component effects and interaction effects separately
                - Validate optimal formulations with confirmation experiments
                """)
            
            # Diagnostic checks
            st.markdown("""
            **Important Diagnostic Checks:**
            - Residual normality (Q-Q plots)
            - Homogeneity of variance (residual vs. predicted plots)
            - Independence (residual vs. run order)
            - Outlier detection (studentized residuals)
            - Influential observations (Cook's distance)
            """)
            
            # Additional resources
            with st.expander("Additional Resources"):
                st.markdown("""
                **Recommended Software:**
                - JMP (SAS Institute)
                - Design Expert (Stat-Ease)
                - Minitab
                - R (packages: DoE.base, rsm, AlgDesign)
                - Python (pyDOE, scikit-learn)
                
                **Reference Books:**
                - "Design and Analysis of Experiments" by Douglas Montgomery
                - "Response Surface Methodology" by Raymond Myers
                - "Design of Experiments in Protein Production and Purification" by Charles Cooney
                - "Optimal Design of Experiments" by Berger and Wong
                """)

if __name__ == "__main__":
    show()