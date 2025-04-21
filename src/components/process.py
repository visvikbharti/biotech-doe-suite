import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from itertools import combinations
import math

def show():
    st.header("Experimental Design Process")
    
    st.markdown("""
    The design and execution of experiments in biotechnology follows a structured process 
    that maximizes information gain while minimizing resource expenditure. This section explores
    the systematic approach to DOE from problem definition through execution to analysis and interpretation.
    """)
    
    # Create tabs for different sections of the process
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Stage 1: Problem Definition", 
        "Stage 2: Design Selection",
        "Stage 3: Execution & Analysis",
        "Stage 4: Interpretation & Decision Making",
        "Interactive Planning Tool"
    ])
    
    # Tab 1: Problem Definition
    with tab1:
        st.markdown("""
        ## Stage 1: Problem Definition
        
        The foundation of effective experimental design is a clear definition of the problem, including objectives, responses, and factors.
        """)
        
        with st.expander("### Defining Experimental Objectives", expanded=True):
            st.markdown("""
            **Concept Anchor**: Clear experimental objectives translate scientific questions into measurable outcomes, providing direction for the entire experimental process.

            **Practical Lens**: In biopharmaceutical development, objectives might include "Identify critical process parameters affecting monoclonal antibody titer" or "Establish a design space for enzyme stability across manufacturing conditions." The specificity of objectives directly influences design choices and analytical approaches.

            **Key Components**:
            1. **Scientific Question**: What fundamental knowledge gap are you addressing?
            2. **Technical Purpose**: What specific information will the experiment provide?
            3. **Decision Criteria**: How will results influence subsequent development decisions?
            """)
            
            # Example objectives table
            objective_examples = pd.DataFrame({
                "Development Phase": ["Early Research", "Process Development", "Process Characterization", "Validation"],
                "Example Objective": [
                    "Identify key media components affecting cell growth",
                    "Optimize critical process parameters for maximum protein yield",
                    "Define design space for chromatography step with ≥90% confidence",
                    "Demonstrate process robustness across manufacturing control ranges"
                ],
                "Typical Approach": [
                    "Screening designs with many factors",
                    "Response surface designs for optimization",
                    "Full factorial designs with center points",
                    "Edge-of-failure designs testing control limits"
                ]
            })
            
            st.table(objective_examples)
        
        with st.expander("### Selecting Response Variables"):
            st.markdown("""
            **Concept Anchor**: Response variables are the quantifiable outcomes that reflect the experimental objectives and serve as the basis for statistical analysis.

            **Practical Lens**: In bioprocess development, response variables might include product yield, purity, biological activity, or process-related impurities. For example, in a cell-based vaccine production process, response variables might include cell density, viability, antigen expression, and host cell protein content.

            **Selection Criteria**:
            1. **Relevance**: Directly addresses experimental objectives
            2. **Measurability**: Can be quantified with appropriate precision and accuracy
            3. **Sensitivity**: Capable of detecting meaningful changes in experimental conditions
            4. **Practical Constraints**: Considers resource limitations, time, and technical feasibility
            """)
            
            # Example of common response variables in biotech
            st.markdown("#### Common Response Variables in Biotechnology")
            
            response_categories = {
                "Upstream Processing": [
                    "Cell density (cells/mL)",
                    "Cell viability (%)",
                    "Product titer (g/L)",
                    "Specific productivity (pg/cell/day)",
                    "Metabolite concentrations (mM)"
                ],
                "Downstream Processing": [
                    "Step yield (%)",
                    "Product purity (%)",
                    "Host cell protein (ppm)",
                    "Aggregates (%)",
                    "DNA content (ng/mg)"
                ],
                "Product Quality": [
                    "Potency (% of reference)",
                    "Glycosylation pattern (%)",
                    "Charge variants (%)",
                    "Thermal stability (°C)",
                    "Particulate matter (counts/mL)"
                ]
            }
            
            for category, responses in response_categories.items():
                st.markdown(f"**{category}**")
                for response in responses:
                    st.markdown(f"- {response}")
        
        with st.expander("### Identifying Factors and Levels"):
            st.markdown("""
            **Concept Anchor**: Experimental factors are the controllable variables manipulated to observe their effects on responses, while levels represent the specific values or settings for these factors.

            **Practical Lens**: In bioreactor optimization, typical factors include temperature (28-37°C), pH (6.8-7.2), dissolved oxygen (30-60%), agitation rate (200-400 RPM), and media component concentrations. Level selection balances current knowledge, physical constraints, and the need to explore a relevant design space.

            **Selection Process**:
            1. **Factor Identification**: Brainstorming potential factors through:
               - Prior knowledge and literature
               - Process understanding and mechanistic knowledge
               - Risk assessment (FMEA or similar approaches)
               - Subject matter expert input

            2. **Factor Screening**: Prioritizing factors based on:
               - Expected impact on responses
               - Control capability during experimentation
               - Resource constraints

            3. **Level Determination**: Setting appropriate ranges by considering:
               - Current operating ranges and historical data
               - Physical/biological constraints
               - Resolution requirements for detecting effects
               - Practical limitations of measurement systems
            """)
            
            # Factor selection framework
            st.markdown("#### Factor Selection Framework")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Factor Categories in Bioprocessing**")
                factor_categories = [
                    "Physical parameters (temperature, pressure)",
                    "Chemical parameters (pH, ionic strength)",
                    "Biological inputs (cell density, viability)",
                    "Equipment settings (agitation, flow rate)",
                    "Material attributes (raw material properties)",
                    "Timing parameters (induction time, harvest time)"
                ]
                
                for category in factor_categories:
                    st.markdown(f"- {category}")
            
            with col2:
                st.markdown("**Level Selection Considerations**")
                level_considerations = [
                    "Experimental objective (screening vs. optimization)",
                    "Expected relationship (linear vs. non-linear)",
                    "Process constraints (equipment limitations)",
                    "Biological constraints (cellular tolerances)",
                    "Practical feasibility (measurement precision)",
                    "Statistical power requirements"
                ]
                
                for consideration in level_considerations:
                    st.markdown(f"- {consideration}")
    
    # Tab 2: Design Selection
    with tab2:
        st.markdown("""
        ## Stage 2: Design Selection
        
        Selecting the appropriate experimental design is critical to achieving experimental objectives efficiently.
        """)
        
        with st.expander("### Design Type Selection", expanded=True):
            st.markdown("""
            **Concept Anchor**: Design type determines the pattern of experimental runs and directly influences the information content, efficiency, and statistical power of the experiment.

            **Practical Lens**: In early-stage biopharmaceutical development, screening designs (fractional factorials) help identify significant factors from many candidates. As development progresses, more comprehensive designs (full factorials, response surface designs) enable detailed characterization and optimization of critical parameters.
            """)
            
            # Design selection decision tree
            st.markdown("#### Design Selection Decision Tree")
            
            design_selection = pd.DataFrame({
                "Development Phase": ["Screening", "Screening", "Characterization", "Characterization", "Optimization", "Optimization", "Robustness"],
                "Key Question": [
                    "Which factors matter?", 
                    "Which factors matter with some interaction info?",
                    "How do factors interact?",
                    "What is the complete effect structure?",
                    "What are the optimal settings?",
                    "What is the optimal formulation?",
                    "How robust is the process?"
                ],
                "Recommended Design": [
                    "Plackett-Burman",
                    "Fractional Factorial (Res III/IV)",
                    "Fractional Factorial (Res V)",
                    "Full Factorial",
                    "Central Composite/Box-Behnken",
                    "Mixture Designs",
                    "Split-Plot/Robust Designs"
                ],
                "Typical Application": [
                    "Media component screening",
                    "Upstream parameter screening",
                    "Critical parameter characterization",
                    "Method validation studies",
                    "Bioreactor optimization",
                    "Buffer/formulation optimization",
                    "Process validation support"
                ]
            })
            
            st.table(design_selection)
        
        with st.expander("### Sample Size and Power Determination"):
            st.markdown("""
            **Concept Anchor**: Statistical power represents the experiment's ability to detect true effects, while sample size determines the precision of effect estimates.

            **Practical Lens**: In bioanalytical method validation, statistical power calculations help determine the number of replicates needed to detect a specified minimum important difference. This ensures that method transfer studies have sufficient replication to confidently validate the method's performance across different laboratories.

            **Mathematical Foundation**:
            The power of a t-test to detect a difference $\\delta$ with significance level $\\alpha$ is:

            $$\\text{Power} = 1 - \\beta = P\\left(t > t_{\\alpha/2, \\nu} - \\frac{\\delta}{\\sigma\\sqrt{2/n}}\\right) + P\\left(t < -t_{\\alpha/2, \\nu} - \\frac{\\delta}{\\sigma\\sqrt{2/n}}\\right)$$

            Where:
            - $\\beta$ is the probability of Type II error
            - $t_{\\alpha/2, \\nu}$ is the critical value of the t-distribution
            - $\\sigma$ is the standard deviation
            - $n$ is the sample size per group
            - $\\nu$ is the degrees of freedom
            """)
            
            # Interactive power calculation example
            st.markdown("#### Interactive Power Calculation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                effect_size = st.slider("Minimum Detectable Effect Size (standardized)", 0.2, 2.0, 0.8, 0.1,
                                      help="Effect size in standard deviation units. 0.2=small, 0.5=medium, 0.8=large")
                alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01,
                                help="Probability of Type I error (false positive)")
                
            with col2:
                n_factors = st.slider("Number of Factors", 1, 10, 3, 1,
                                    help="Number of experimental factors")
                desired_power = st.slider("Desired Power (1-β)", 0.7, 0.99, 0.8, 0.05,
                                        help="Probability of detecting a true effect (1 minus Type II error)")
            
            # Calculate required sample size (simplified)
            # This is a very simplified calculation for demonstration purposes
            if n_factors <= 5:
                base_runs = 2**n_factors  # Full factorial
            else:
                base_runs = 2**(n_factors-1)  # Fractional factorial
            
            # Approximate power calculation
            import scipy.stats as stats
            
            # Degrees of freedom
            df = base_runs - n_factors - 1
            
            # Non-centrality parameter
            lambda_nc = effect_size * np.sqrt(base_runs / (2**n_factors))
            
            # Calculate power (approximate)
            if df > 0:
                t_crit = stats.t.ppf(1-alpha/2, df)
                power = 1 - stats.nct.cdf(t_crit, df, lambda_nc)
                power = min(power, 0.9999)  # Cap at realistic maximum
            else:
                power = 0.0
            
            # Display results
            st.markdown("#### Estimated Power Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Minimum Runs Required", base_runs)
                st.metric("Degrees of Freedom", df)
            
            with col2:
                st.metric("Estimated Power", f"{power:.2f}")
                
                # Traffic light indicator for power
                if power >= desired_power:
                    st.success(f"✅ Sufficient power to detect effect size of {effect_size:.1f}")
                elif power >= 0.6:
                    st.warning(f"⚠️ Borderline power. Consider adding replicates or center points.")
                else:
                    st.error(f"❌ Insufficient power. Increase sample size or effect size.")
            
            # Recommendation based on power analysis
            if power < desired_power:
                additional_runs = np.ceil((desired_power / power - 1) * base_runs)
                st.markdown(f"""
                **Recommendation:** To achieve desired power of {desired_power:.2f}, consider:
                - Adding approximately {int(additional_runs)} additional runs (replicates or center points)
                - Reducing experimental variability to increase effect size
                - Using a more efficient design if appropriate
                """)
        
        with st.expander("### Randomization and Blocking Strategies"):
            st.markdown("""
            **Concept Anchor**: Randomization distributes uncontrolled variability randomly across conditions, while blocking isolates known sources of nuisance variation.

            **Practical Lens**: In bioassay development, day-to-day variability often exceeds within-day variability. Using a randomized complete block design with days as blocks allows focus on treatment effects while accounting for inter-day variation, improving assay robustness characterization.

            **Implementation Strategies**:
            1. **Complete Randomization**: All runs randomized without constraints
               - Simplest approach
               - Provides maximum protection against bias
               - May be impractical with hard-to-change factors

            2. **Blocking**: Groups experiments into homogeneous blocks
               - Reduces variance from known nuisance factors
               - Common blocks in biotech: equipment units, raw material lots, days/shifts
               - Must maintain balance and orthogonality within blocks

            3. **Split-Plot Designs**: Accommodates hard-to-change factors
               - Whole plots: Hard-to-change factors (e.g., bioreactor temperature)
               - Sub-plots: Easy-to-change factors (e.g., sampling time, analytical conditions)
               - Requires special analysis accounting for different error structures
            """)
            
            # Common blocking factors in biotechnology
            st.markdown("#### Common Blocking Factors in Biotechnology")
            
            blocking_examples = pd.DataFrame({
                "Blocking Factor": [
                    "Time-based Blocks", 
                    "Equipment-based Blocks", 
                    "Material-based Blocks", 
                    "Operator-based Blocks", 
                    "Location-based Blocks"
                ],
                "Examples": [
                    "Days, shifts, weeks, cell passages",
                    "Bioreactor units, chromatography skids, incubators",
                    "Cell banks, media lots, resin lots, buffer preparations",
                    "Technicians, analysts, shift teams",
                    "Laboratory sites, manufacturing facilities, incubator positions"
                ],
                "Application": [
                    "Control for time-dependent drift or changes",
                    "Control for performance differences between equipment units",
                    "Control for batch-to-batch variability in materials",
                    "Control for technique or execution differences",
                    "Control for environmental or location-specific variations"
                ]
            })
            
            st.table(blocking_examples)
            
            # Randomization visualization
            st.markdown("#### Randomization Strategies Comparison")
            
            # Generate visualization of different randomization strategies
            # Simplified example with 8 runs, 2 blocks, 2 whole plots
            fig = go.Figure()
            
            # Data for visualization
            strategies = ["Complete Random", "Blocked", "Split-Plot"]
            run_orders = [
                [3, 7, 1, 5, 8, 6, 2, 4],
                [[5, 2, 7, 3], [8, 1, 6, 4]],
                [[1, 3, 4, 2], [7, 5, 8, 6]]
            ]
            
            # Offset for vertical positioning of strategies
            offsets = [0, 10, 20]
            colors = ['blue', 'green', 'orange']
            
            # Add strategy labels
            for i, strategy in enumerate(strategies):
                fig.add_annotation(
                    x=-1,
                    y=offsets[i] + 1.5,
                    text=strategy,
                    showarrow=False,
                    font=dict(size=14)
                )
            
            # Add complete random strategy
            for j, run in enumerate(run_orders[0]):
                fig.add_trace(go.Scatter(
                    x=[j],
                    y=[offsets[0]],
                    mode='markers',
                    marker=dict(size=30, color=colors[0]),
                    text=f"Run {run}",
                    name=f"Run {run}",
                    showlegend=False,
                    hoverinfo="text"
                ))
            
            # Add blocked strategy
            for block in range(2):
                fig.add_shape(
                    type="rect",
                    x0=-0.5,
                    y0=offsets[1] - 1.5,
                    x1=3.5,
                    y1=offsets[1] + 1.5,
                    line=dict(color="gray", width=1),
                    fillcolor="gray",
                    opacity=0.1
                )
                fig.add_annotation(
                    x=1.5,
                    y=offsets[1] + 2,
                    text=f"Block {block+1}",
                    showarrow=False
                )
                for j, run in enumerate(run_orders[1][block]):
                    fig.add_trace(go.Scatter(
                        x=[j + (block * 4)],
                        y=[offsets[1]],
                        mode='markers',
                        marker=dict(size=30, color=colors[1]),
                        text=f"Run {run}",
                        name=f"Run {run}",
                        showlegend=False,
                        hoverinfo="text"
                    ))
            
            # Add split-plot strategy
            for wp in range(2):
                fig.add_shape(
                    type="rect",
                    x0=-0.5 + (wp * 4),
                    y0=offsets[2] - 1.5,
                    x1=3.5 + (wp * 4),
                    y1=offsets[2] + 1.5,
                    line=dict(color="purple", width=2),
                    fillcolor="purple",
                    opacity=0.1
                )
                fig.add_annotation(
                    x=1.5 + (wp * 4),
                    y=offsets[2] + 2,
                    text=f"Whole Plot {wp+1}",
                    showarrow=False
                )
                for j, run in enumerate(run_orders[2][wp]):
                    fig.add_trace(go.Scatter(
                        x=[j + (wp * 4)],
                        y=[offsets[2]],
                        mode='markers',
                        marker=dict(size=30, color=colors[2]),
                        text=f"Run {run}",
                        name=f"Run {run}",
                        showlegend=False,
                        hoverinfo="text"
                    ))
            
            fig.update_layout(
                title="Comparison of Randomization Strategies",
                height=400,
                showlegend=False,
                xaxis=dict(
                    showticklabels=False,
                    range=[-1, 8]
                ),
                yaxis=dict(
                    showticklabels=False,
                    range=[-2, 25]
                )
            )
            
            st.plotly_chart(fig)
    
    # Tab 3: Execution & Analysis
    with tab3:
        st.markdown("""
        ## Stage 3: Execution and Analysis
        
        Proper execution of the experimental design and systematic analysis of results are critical to extracting valid insights.
        """)
        
        with st.expander("### Experimental Execution", expanded=True):
            st.markdown("""
            **Concept Anchor**: Proper execution maintains design integrity while documenting critical metadata needed for subsequent analysis and interpretation.

            **Practical Lens**: During biomanufacturing process characterization, careful documentation of actual factor levels (vs. target levels), unexpected events, and environmental conditions provides context for outlier investigation and supports regulatory filings demonstrating process understanding.

            **Best Practices**:
            1. **Design Adherence**: Follow the randomization schedule precisely
            2. **Factor Level Verification**: Record actual (not just target) factor levels
            3. **Execution Documentation**: Track important metadata and environmental conditions
            4. **Quality Control**: Implement in-process checks to identify execution problems
            5. **Contingency Planning**: Establish protocols for handling deviations and missing data
            """)
            
            # Execution checklist
            st.markdown("#### Experimental Execution Checklist")
            
            execution_tasks = [
                "Prepare detailed experimental protocol with run order",
                "Perform equipment calibration and system suitability",
                "Prepare materials and reagents with proper quality checks",
                "Train personnel on execution procedures",
                "Implement appropriate blinding procedures if needed",
                "Execute runs according to randomized schedule",
                "Document actual factor settings for each run",
                "Record all metadata and environmental conditions",
                "Implement in-process quality checks",
                "Document any deviations or unexpected events",
                "Collect and verify response measurements"
            ]
            
            for i, task in enumerate(execution_tasks):
                st.checkbox(task, key=f"exec_task_{i}")
            
            # Reset checklist button
            if st.button("Reset Checklist"):
                for i in range(len(execution_tasks)):
                    st.session_state[f"exec_task_{i}"] = False
        
        with st.expander("### Data Validation and Preprocessing"):
            st.markdown("""
            **Concept Anchor**: Data validation ensures quality and integrity before analysis, while preprocessing transforms raw data into a form suitable for statistical modeling.

            **Practical Lens**: In bioanalytical datasets, preprocessing might include normalizing fluorescence readings to internal standards, applying appropriate transformations to achieve normality, and flagging potential outliers for investigation while ensuring regulatory compliance.

            **Key Steps**:
            1. **Data Inspection**: Review for completeness, accuracy, and adherence to design
            2. **Outlier Detection**: Identify potential outliers using:
               - Graphical methods (box plots, control charts)
               - Statistical tests (Grubbs' test, Dixon's Q test)
               - Process knowledge (deviation reports, execution notes)

            3. **Transformation Selection**: Apply appropriate transformations when needed:
               - Log transformation for multiplicative effects or positively skewed data
               - Square root for count data with Poisson-like variation
               - Box-Cox for identifying optimal transformation family
            """)
            
            # Common transformations in biotechnology
            st.markdown("#### Common Transformations in Biotechnology")
            
            transformations = pd.DataFrame({
                "Transformation": ["Log (natural)", "Log10", "Square Root", "Arcsin", "Box-Cox", "Logit"],
                "Formula": ["ln(y)", "log₁₀(y)", "√y", "sin⁻¹(√y)", "(yᵏ-1)/k", "ln(y/(1-y))"],
                "When to Use": [
                    "Multiplicative effects, right-skewed data",
                    "Order of magnitude changes, right-skewed data",
                    "Count data, Poisson-distributed responses",
                    "Proportion/percentage data (0-1 or 0-100%)",
                    "When optimal transformation is unknown",
                    "Proportion data with logistic relationship"
                ],
                "Biotech Example": [
                    "Cell growth rates, enzyme activity",
                    "Microbial counts, viral titers",
                    "Colony counts, particulate matter",
                    "Viability percentages, conversion rates",
                    "General response optimization",
                    "Binding assays, dose-response curves"
                ]
            })
            
            st.table(transformations)
        
        with st.expander("### Statistical Analysis Workflow"):
            st.markdown("""
            **Concept Anchor**: Statistical analysis extracts signal from noise, quantifying factor effects, interaction patterns, and model adequacy to support reliable conclusions.

            **Practical Lens**: In protein formulation studies, analysis might progress from ANOVA to identify significant stabilizing excipients, to response surface modeling to optimize concentration ranges, to model validation using confirmation runs at predicted optimal conditions.

            **Analysis Sequence**:
            1. **Effect Estimation**: Calculate main effects and interactions
            2. **Significance Testing**: Identify statistically significant effects
            3. **Model Building**: Construct predictive models of response variables
            4. **Model Validation**: Assess adequacy through diagnostic checks
            5. **Optimization**: Identify optimal factor settings (when applicable)
            6. **Confirmation**: Verify predictions with confirmation runs
            """)
            
            # Statistical analysis workflow diagram
            st.markdown("#### Statistical Analysis Workflow")
            
            # Create a flowchart-like visualization
            analysis_steps = [
                "Data Preparation & Validation",
                "Effect Estimation (ANOVA/Regression)",
                "Significance Testing (p-values, F-tests)",
                "Model Building & Selection",
                "Diagnostic Validation",
                "Response Surface Analysis",
                "Optimization & Confirmation"
            ]
            
            analysis_descriptions = [
                "Clean, validate, and structure data for analysis",
                "Calculate effect sizes and direction for factors and interactions",
                "Determine which effects are statistically significant",
                "Build predictive models, potentially with transformations",
                "Check assumptions, identify outliers, validate model fit",
                "Map relationship between factors and responses",
                "Find optimal settings and verify with confirmation runs"
            ]
            
            # Create a simple flow diagram
            fig = go.Figure()
            
            # Add nodes for each step
            for i, (step, desc) in enumerate(zip(analysis_steps, analysis_descriptions)):
                # Node position
                y_pos = 10 - i * 1.5
                
                # Add node
                fig.add_trace(go.Scatter(
                    x=[0],
                    y=[y_pos],
                    mode='markers+text',
                    marker=dict(size=30, color='lightblue', line=dict(color='darkblue', width=2)),
                    text=[str(i+1)],
                    showlegend=False
                ))
                
                # Add step text
                fig.add_annotation(
                    x=2,
                    y=y_pos,
                    text=step,
                    showarrow=False,
                    font=dict(size=14, color='darkblue'),
                    align="left",
                    xanchor="left"
                )
                
                # Add description
                fig.add_annotation(
                    x=2,
                    y=y_pos - 0.5,
                    text=desc,
                    showarrow=False,
                    font=dict(size=12),
                    align="left",
                    xanchor="left"
                )
                
                # Add arrow to next step
                if i < len(analysis_steps) - 1:
                    fig.add_shape(
                        type="line",
                        x0=0,
                        y0=y_pos - 0.5,
                        x1=0,
                        y1=y_pos - 1,
                        line=dict(color="darkblue", width=2, dash="solid"),
                        layer="below"
                    )
            
            fig.update_layout(
                height=600,
                showlegend=False,
                plot_bgcolor='white',
                xaxis=dict(
                    showticklabels=False,
                    range=[-1, 10]
                ),
                yaxis=dict(
                    showticklabels=False,
                    range=[-1, 11]
                )
            )
            
            st.plotly_chart(fig)
    
    # Tab 4: Interpretation & Decision Making
    with tab4:
        st.markdown("""
        ## Stage 4: Interpretation and Decision Making
        
        Translating statistical results into scientific insights and actionable decisions is the ultimate goal of DOE.
        """)
        
        with st.expander("### Model Interpretation", expanded=True):
            st.markdown("""
            **Concept Anchor**: Interpretation translates statistical results into scientific insights, connecting statistical significance with practical importance.

            **Practical Lens**: In cell culture optimization, effect interpretation might reveal that temperature effects on protein quality are twice as large as medium composition effects, but with important temperature-by-pH interactions that necessitate simultaneous optimization of both factors.

            **Interpretation Framework**:
            1. **Effect Magnitude**: Quantify the practical importance of effects
            2. **Effect Direction**: Identify whether effects increase or decrease responses
            3. **Interaction Patterns**: Understand how factors work together
            4. **Mechanistic Insights**: Connect statistical findings to biological mechanisms
            5. **Practical Significance**: Differentiate statistical from practical significance
            """)
            
            # Interpretation guidance visualization
            st.markdown("#### Effect Interpretation Guidelines")
            
            interpretation_table = pd.DataFrame({
                "Finding": [
                    "Large positive main effect",
                    "Large negative main effect",
                    "Small but significant effect",
                    "Significant positive interaction",
                    "Significant negative interaction",
                    "Significant quadratic effect (negative)",
                    "Significant quadratic effect (positive)"
                ],
                "Interpretation": [
                    "Increasing this factor increases the response substantially",
                    "Decreasing this factor increases the response substantially",
                    "Factor has consistent but modest impact on response",
                    "Combined effect of factors is greater than the sum of individual effects",
                    "Combined effect of factors is less than the sum of individual effects",
                    "Response has a maximum within the experimental range",
                    "Response has a minimum within the experimental range"
                ],
                "Typical Action": [
                    "Consider setting at high level or explore higher levels",
                    "Consider setting at low level or explore lower levels",
                    "May be important for fine-tuning or cumulative effects",
                    "Optimize these factors simultaneously, considering synergies",
                    "Avoid certain combinations, may indicate competing mechanisms",
                    "Find peak and optimize around it (response surface designs)",
                    "Move away from minimum or determine if minimum is acceptable"
                ]
            })
            
            st.table(interpretation_table)
        
        with st.expander("### Design Space Characterization"):
            st.markdown("""
            **Concept Anchor**: Design space defines the multidimensional combination of factors where quality is assured, providing operational flexibility while maintaining product quality.

            **Practical Lens**: For a biopharmaceutical product, the design space might specify ranges for pH (6.8-7.2), temperature (30-34°C), and dissolved oxygen (40-60%) where critical quality attributes meet specifications with appropriate confidence.

            **Mathematical Foundation**:
            The probability that a response $Y$ meets specifications within a region $R$ is:

            $$P(L \\leq Y \\leq U | \\mathbf{x} \\in R) \\geq \\pi$$

            Where:
            - $L$ and $U$ are lower and upper specification limits
            - $\\mathbf{x}$ is the vector of process parameters
            - $R$ is the design space region
            - $\\pi$ is the required confidence level (typically 0.90 or 0.95)
            """)
            
            # Design space visualization example
            st.markdown("#### Design Space Visualization Example")
            
            # Simple two-factor design space visualization
            # Generate grid data
            x = np.linspace(-1, 1, 50)
            y = np.linspace(-1, 1, 50)
            X, Y = np.meshgrid(x, y)
            
            # Create a design space boundary (ellipsoid shape)
            Z = 0.9 - (X**2 + Y**2 + 0.5*X*Y)
            
            # Create figure
            fig = go.Figure()
            
            # Add contour for design space
            fig.add_trace(go.Contour(
                z=Z,
                x=x,
                y=y,
                contours=dict(
                    start=0,
                    end=1,
                    size=0.1,
                    showlabels=True
                ),
                colorscale='Viridis',
                colorbar=dict(title="Probability of Meeting Specs")
            ))
            
            # Add specification boundary
            fig.add_trace(go.Contour(
                z=Z,
                x=x,
                y=y,
                contours=dict(
                    start=0,
                    end=0,
                    coloring='lines',
                    showlabels=True,
                    labelfont=dict(color='white')
                ),
                line=dict(color='red', width=2),
                showscale=False
            ))
            
            # Update layout
            fig.update_layout(
                title="Example Process Design Space (Two Factors)",
                xaxis_title="Factor 1 (e.g., pH)",
                yaxis_title="Factor 2 (e.g., Temperature)",
                height=500
            )
            
            st.plotly_chart(fig)
            
            st.markdown("""
            **Design Space Interpretation:**
            - Region inside red boundary: Process parameters with ≥ 95% probability of meeting all specifications
            - Color gradient: Probability of meeting specifications (darker = higher probability)
            - Center region: Most robust operating parameters (maximum confidence)
            - This visualization supports regulatory filings and defines operational flexibility
            """)
        
        with st.expander("### Decision Making and Next Steps"):
            st.markdown("""
            **Concept Anchor**: DOE insights drive development decisions, including process changes, additional experimentation, or advancement to the next development phase.

            **Practical Lens**: Following process characterization studies, decisions might include setting manufacturing control strategies, defining in-process controls and specifications, or planning additional studies to address knowledge gaps.

            **Decision Framework**:
            1. **Conclusion Validation**: Assess reliability and limitations of findings
            2. **Risk Assessment**: Evaluate residual uncertainties and their impacts
            3. **Knowledge Integration**: Combine new findings with prior knowledge
            4. **Action Planning**: Determine specific actions based on findings
            5. **Iteration Planning**: Define follow-up experimentation when needed
            """)
            
            # Decision tree for next steps
            st.markdown("#### Decision Framework for Next Steps")
            
            decision_steps = {
                "Outcome Assessment": [
                    "Were experimental objectives met?",
                    "Are results statistically and practically significant?",
                    "Are there unexpected findings requiring further investigation?"
                ],
                "Knowledge Gaps": [
                    "Are there remaining knowledge gaps requiring additional experiments?",
                    "Is the model predictive across the entire region of interest?",
                    "Have all critical interactions been characterized?"
                ],
                "Implementation Planning": [
                    "What are the optimal factor settings for implementation?",
                    "What control strategy is needed for critical parameters?",
                    "How should specification ranges be set for process parameters?"
                ],
                "Risk Management": [
                    "What residual risks remain after the study?",
                    "How robust is the process to uncontrolled variations?",
                    "What monitoring strategy is needed during implementation?"
                ]
            }
            
            for category, questions in decision_steps.items():
                st.markdown(f"**{category}**")
                for question in questions:
                    st.markdown(f"- {question}")
    
    # Tab 5: Interactive Planning Tool
    with tab5:
        # Call the interactive function for DOE planning
        design_planning_tool()

def design_planning_tool():
    st.header("Experimental Design Planning Tool")
    
    st.markdown("""
    This interactive tool will guide you through the DOE planning process, step by step,
    helping you make informed decisions about your experimental design in biotechnology applications.
    """)
    
    # Use tabs for the different stages of DOE planning
    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Problem Definition", 
        "2. Design Selection", 
        "3. Resource Planning",
        "4. Design Summary"
    ])
    
    # Initialize session state for persistent data across interactions
    if 'factors' not in st.session_state:
        st.session_state.factors = []
        st.session_state.responses = []
        st.session_state.design_type = None
        st.session_state.design_resolution = None
        st.session_state.center_points = 0
        st.session_state.replicates = 1
        st.session_state.blocking_factors = []
        st.session_state.design_name = "My DOE"
        st.session_state.objective = ""
        st.session_state.min_effect_size = 0.0
        
    # Tab 1: Problem Definition
    with tab1:
        st.subheader("Define Your Experimental Objectives")
        
        st.session_state.design_name = st.text_input(
            "Design Name", 
            value=st.session_state.design_name,
            help="A descriptive name for your experiment"
        )
        
        st.session_state.objective = st.text_area(
            "Experimental Objective", 
            value=st.session_state.objective,
            help="What scientific question are you trying to answer?"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Define Factors")
            
            # Biotechnology-specific factor categories
            factor_categories = [
                "Process Parameters",
                "Media Components",
                "Physical Conditions",
                "Equipment Settings",
                "Reagent Properties",
                "Other"
            ]
            
            # Add a new factor
            with st.expander("Add Factor", expanded=len(st.session_state.factors) == 0):
                new_factor_name = st.text_input("Factor Name", key="new_factor_name")
                new_factor_category = st.selectbox("Category", factor_categories, key="new_factor_category")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    new_factor_low = st.text_input("Low Level", key="new_factor_low")
                with col_b:
                    new_factor_high = st.text_input("High Level", key="new_factor_high")
                    
                new_factor_units = st.text_input("Units", key="new_factor_units")
                new_factor_hard_to_change = st.checkbox("Hard to change?", key="new_factor_hard", 
                                                      help="Factors that are difficult or time-consuming to adjust between runs")
                
                if st.button("Add Factor"):
                    if new_factor_name and new_factor_low and new_factor_high:
                        st.session_state.factors.append({
                            "name": new_factor_name,
                            "category": new_factor_category,
                            "low": new_factor_low,
                            "high": new_factor_high,
                            "units": new_factor_units,
                            "hard_to_change": new_factor_hard_to_change
                        })
                        st.success(f"Added factor: {new_factor_name}")
                        st.experimental_rerun()
            
            # Display existing factors
            if st.session_state.factors:
                st.subheader("Current Factors")
                for i, factor in enumerate(st.session_state.factors):
                    with st.expander(f"{factor['name']} ({factor['low']} to {factor['high']} {factor['units']})"):
                        st.write(f"**Category:** {factor['category']}")
                        st.write(f"**Range:** {factor['low']} to {factor['high']} {factor['units']}")
                        st.write(f"**Hard to change:** {'Yes' if factor['hard_to_change'] else 'No'}")
                        
                        if st.button(f"Remove {factor['name']}", key=f"remove_factor_{i}"):
                            st.session_state.factors.pop(i)
                            st.experimental_rerun()
        
        with col2:
            st.subheader("Define Responses")
            
            # Biotechnology-specific response categories
            response_categories = [
                "Product Yield",
                "Product Quality",
                "Process Efficiency",
                "Biological Activity",
                "Impurity Profile",
                "Physical Property",
                "Other"
            ]
            
            # Add a new response
            with st.expander("Add Response Variable", expanded=len(st.session_state.responses) == 0):
                new_response_name = st.text_input("Response Name", key="new_response_name")
                new_response_category = st.selectbox("Category", response_categories, key="new_response_category")
                new_response_units = st.text_input("Units", key="new_response_units")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    new_response_lower_spec = st.text_input("Lower Specification (if applicable)", key="new_response_lower")
                with col_b:
                    new_response_upper_spec = st.text_input("Upper Specification (if applicable)", key="new_response_upper")
                
                new_response_priority = st.slider("Priority", 1, 5, 3, 
                                               help="1 = Lowest priority, 5 = Highest priority")
                
                if st.button("Add Response"):
                    if new_response_name:
                        st.session_state.responses.append({
                            "name": new_response_name,
                            "category": new_response_category,
                            "units": new_response_units,
                            "lower_spec": new_response_lower_spec,
                            "upper_spec": new_response_upper_spec,
                            "priority": new_response_priority
                        })
                        st.success(f"Added response: {new_response_name}")
                        st.experimental_rerun()
            
            # Display existing responses
            if st.session_state.responses:
                st.subheader("Current Responses")
                for i, response in enumerate(st.session_state.responses):
                    with st.expander(f"{response['name']} ({response['units']})"):
                        st.write(f"**Category:** {response['category']}")
                        st.write(f"**Units:** {response['units']}")
                        
                        specs = []
                        if response['lower_spec']:
                            specs.append(f"Lower: {response['lower_spec']}")
                        if response['upper_spec']:
                            specs.append(f"Upper: {response['upper_spec']}")
                            
                        if specs:
                            st.write(f"**Specifications:** {', '.join(specs)}")
                            
                        st.write(f"**Priority:** {response['priority']}/5")
                        
                        if st.button(f"Remove {response['name']}", key=f"remove_response_{i}"):
                            st.session_state.responses.pop(i)
                            st.experimental_rerun()
        
        # Effect size estimation (for power calculations)
        st.subheader("Effect Size Estimation")
        
        st.markdown("""
        The minimum effect size is the smallest change in your response that you consider 
        practically significant. This helps determine the required number of experimental runs.
        """)
        
        if st.session_state.responses:
            response_options = [r["name"] for r in st.session_state.responses]
            primary_response = st.selectbox("Primary Response for Power Calculation", response_options)
            
            # Find the selected response
            selected_response = next((r for r in st.session_state.responses if r["name"] == primary_response), None)
            
            if selected_response:
                response_units = selected_response["units"]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.session_state.min_effect_size = st.number_input(
                        f"Minimum Important Effect Size ({response_units})",
                        min_value=0.0,
                        step=0.1,
                        value=st.session_state.min_effect_size,
                        help="The smallest effect that you want to be able to detect"
                    )
                
                with col2:
                    historical_std_dev = st.number_input(
                        f"Estimated Standard Deviation ({response_units})",
                        min_value=0.01,
                        step=0.1,
                        value=1.0,
                        help="Based on historical data or preliminary studies"
                    )
                
                # Calculate standardized effect size
                if st.session_state.min_effect_size > 0 and historical_std_dev > 0:
                    standardized_effect = st.session_state.min_effect_size / historical_std_dev
                    
                    st.write(f"**Standardized Effect Size:** {standardized_effect:.2f}")
                    
                    if standardized_effect < 0.5:
                        st.warning("Small effect size. You may need many replicates to detect this effect.")
                    elif standardized_effect > 2.0:
                        st.success("Large effect size. You should be able to detect this with fewer runs.")
    
    # Tab 2: Design Selection
    with tab2:
        st.subheader("Select Experimental Design")
        
        # Only proceed if we have factors and responses
        if not st.session_state.factors:
            st.warning("Please define at least one factor in the Problem Definition tab.")
        elif not st.session_state.responses:
            st.warning("Please define at least one response in the Problem Definition tab.")
        else:
            num_factors = len(st.session_state.factors)
            
            # Design type selection
            design_types = [
                "Full Factorial",
                "Fractional Factorial",
                "Plackett-Burman",
                "Response Surface (CCD)",
                "Box-Behnken"
            ]
            
            # Filter available designs based on number of factors
            available_designs = design_types.copy()
            if num_factors < 3:
                if "Box-Behnken" in available_designs:
                    available_designs.remove("Box-Behnken")
            if num_factors < 2:
                if "Response Surface (CCD)" in available_designs:
                    available_designs.remove("Response Surface (CCD)")
                
            col1, col2 = st.columns(2)
            
            with col1:
                st.session_state.design_type = st.selectbox(
                    "Design Type",
                    available_designs,
                    index=min(available_designs.index(st.session_state.design_type) 
                            if st.session_state.design_type in available_designs else 0,
                            len(available_designs)-1)
                )
                
                # Design-specific options
                if st.session_state.design_type == "Fractional Factorial":
                    resolution_options = ["III", "IV", "V"]
                    st.session_state.design_resolution = st.selectbox(
                        "Design Resolution",
                        resolution_options,
                        index=resolution_options.index(st.session_state.design_resolution) 
                        if st.session_state.design_resolution in resolution_options else 1
                    )
                
                if st.session_state.design_type in ["Full Factorial", "Fractional Factorial"]:
                    st.session_state.center_points = st.number_input(
                        "Number of Center Points",
                        min_value=0,
                        max_value=10,
                        value=st.session_state.center_points,
                        help="Center points help detect curvature and provide an estimate of pure error"
                    )
                
                st.session_state.replicates = st.number_input(
                    "Number of Replicates",
                    min_value=1,
                    max_value=10,
                    value=st.session_state.replicates,
                    help="Complete replication of the entire design"
                )
            
            with col2:
                # Power and sample size calculation
                st.subheader("Statistical Power")
                
                alpha = st.slider(
                    "Significance Level (α)",
                    min_value=0.01,
                    max_value=0.10,
                    value=0.05,
                    step=0.01,
                    help="Probability of Type I error (false positive)"
                )
                
                desired_power = st.slider(
                    "Desired Power (1-β)",
                    min_value=0.70,
                    max_value=0.99,
                    value=0.80,
                    step=0.05,
                    help="Probability of detecting a true effect (1 minus Type II error)"
                )
                
                # Calculate number of runs required based on design type
                if st.session_state.min_effect_size > 0:
                    # Simplified power calculation for demonstration
                    # In a real application, this would be more sophisticated
                    standardized_effect = st.session_state.min_effect_size
                    
                    # Calculate base runs based on design type
                    if st.session_state.design_type == "Full Factorial":
                        base_runs = 2**num_factors
                    elif st.session_state.design_type == "Fractional Factorial":
                        # Simplified calculation
                        if st.session_state.design_resolution == "III":
                            base_runs = max(2**(num_factors - max(1, num_factors-4)), 8)
                        elif st.session_state.design_resolution == "IV":
                            base_runs = max(2**(num_factors - max(1, num_factors-5)), 16)
                        else:  # Resolution V
                            base_runs = max(2**(num_factors - max(1, num_factors-6)), 16)
                    elif st.session_state.design_type == "Plackett-Burman":
                        # Next multiple of 4 that's ≥ num_factors+1
                        base_runs = 4 * math.ceil((num_factors + 1) / 4)
                    elif st.session_state.design_type == "Response Surface (CCD)":
                        base_runs = 2**num_factors + 2*num_factors + 1
                    elif st.session_state.design_type == "Box-Behnken":
                        # Approximation
                        base_runs = 2*num_factors*(num_factors-1) + 1
                    else:
                        base_runs = 2**num_factors
                    
                    # Add center points
                    base_runs += st.session_state.center_points
                    
                    # Calculate total runs with replication
                    total_runs = base_runs * st.session_state.replicates
                    
                    # Calculate achieved power (simplified)
                    # This is a very simplified calculation for demonstration
                    df_error = total_runs - num_factors - 1
                    if df_error > 0:
                        # Using a simplified approximation
                        f_critical = 4.0  # Approximation of F critical value
                        non_centrality = (standardized_effect**2 * total_runs) / (2**num_factors * 4)
                        achieved_power = min(0.99, max(0.10, 0.5 + 0.3 * non_centrality))
                        
                        power_color = "red" if achieved_power < 0.7 else "orange" if achieved_power < 0.8 else "green"
                        st.markdown(f"**Achieved Power:** <span style='color:{power_color}'>{achieved_power:.2f}</span>", unsafe_allow_html=True)
                        
                        if achieved_power < desired_power:
                            st.warning(f"The current design may not have sufficient power to detect your minimum effect size. Consider increasing replicates or adjusting your design.")
                        else:
                            st.success(f"The current design should have sufficient power to detect your minimum effect size.")
                    else:
                        st.error("Not enough degrees of freedom for error estimation. Increase the number of runs.")
                else:
                    st.info("Please specify a minimum effect size in the Problem Definition tab to calculate power.")
            
            # Blocking strategy
            st.subheader("Blocking Strategy")
            
            st.markdown("""
            Blocking helps control for known sources of variation that are not of primary interest.
            Common blocking factors in biotechnology include:
            - Equipment units (different bioreactors, chromatography skids)
            - Material lots (media batches, resin lots)
            - Personnel (different operators or analysts)
            - Time periods (days, weeks, shifts)
            """)
            
            use_blocking = st.checkbox("Use Blocking in Design", value=len(st.session_state.blocking_factors) > 0)
            
            if use_blocking:
                with st.expander("Add Blocking Factor"):
                    block_name = st.text_input("Blocking Factor Name", key="new_block_name")
                    block_levels = st.number_input("Number of Levels", min_value=2, max_value=10, value=2, key="new_block_levels")
                    
                    if st.button("Add Blocking Factor"):
                        if block_name:
                            st.session_state.blocking_factors.append({
                                "name": block_name,
                                "levels": block_levels
                            })
                            st.success(f"Added blocking factor: {block_name}")
                            st.experimental_rerun()
                
                # Display existing blocking factors
                if st.session_state.blocking_factors:
                    for i, block in enumerate(st.session_state.blocking_factors):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{block['name']}** ({block['levels']} levels)")
                        with col3:
                            if st.button(f"Remove", key=f"remove_block_{i}"):
                                st.session_state.blocking_factors.pop(i)
                                st.experimental_rerun()
            else:
                st.session_state.blocking_factors = []
                
            # Handling hard-to-change factors
            hard_to_change_factors = [f for f in st.session_state.factors if f["hard_to_change"]]
            
            if hard_to_change_factors:
                st.subheader("Hard-to-Change Factors Strategy")
                
                st.markdown("""
                Your design includes hard-to-change factors, which may benefit from a split-plot design approach.
                In split-plot designs:
                - Hard-to-change factors are assigned to whole plots
                - Easy-to-change factors are randomized within each whole plot
                """)
                
                use_split_plot = st.checkbox("Use Split-Plot Design", value=True)
                
                if use_split_plot:
                    st.info(f"The design will treat these factors as whole-plot factors: {', '.join([f['name'] for f in hard_to_change_factors])}")
    
    # Tab 3: Resource Planning
    with tab3:
        st.subheader("Resource Planning")
        
        # Only proceed if we have factors and responses
        if not st.session_state.factors or not st.session_state.responses:
            st.warning("Please complete the Problem Definition tab first.")
        else:
            # Calculate number of runs
            num_factors = len(st.session_state.factors)
            
            if st.session_state.design_type == "Full Factorial":
                base_runs = 2**num_factors
            elif st.session_state.design_type == "Fractional Factorial":
                if st.session_state.design_resolution == "III":
                    base_runs = max(2**(num_factors - max(1, num_factors-4)), 8)
                elif st.session_state.design_resolution == "IV":
                    base_runs = max(2**(num_factors - max(1, num_factors-5)), 16)
                else:  # Resolution V
                    base_runs = max(2**(num_factors - max(1, num_factors-6)), 16)
            elif st.session_state.design_type == "Plackett-Burman":
                base_runs = 4 * math.ceil((num_factors + 1) / 4)
            elif st.session_state.design_type == "Response Surface (CCD)":
                base_runs = 2**num_factors + 2*num_factors + 1
            elif st.session_state.design_type == "Box-Behnken":
                base_runs = 2*num_factors*(num_factors-1) + 1
            else:
                base_runs = 2**num_factors
            
            # Add center points
            if hasattr(st.session_state, 'center_points'):
                base_runs += st.session_state.center_points
            
            # Account for blocking
            blocking_multiplier = 1
            for block in st.session_state.blocking_factors:
                blocking_multiplier *= block["levels"]
            
            # Calculate total runs
            total_runs = base_runs * st.session_state.replicates * blocking_multiplier
            
            st.write(f"**Total Experimental Runs Required:** {total_runs}")
            
            # Resource estimation
            st.subheader("Resource Estimation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                time_per_run = st.number_input("Estimated Time per Run (hours)", 
                                             min_value=0.1, 
                                             max_value=168.0, 
                                             value=1.0,
                                             step=0.5)
                
                setup_time = st.number_input("Setup/Preparation Time (hours)",
                                           min_value=0.0,
                                           max_value=100.0,
                                           value=2.0,
                                           step=0.5)
                
                analysis_time = st.number_input("Analysis Time per Run (hours)",
                                              min_value=0.0,
                                              max_value=100.0,
                                              value=0.5,
                                              step=0.1)
            
            with col2:
                cost_per_run = st.number_input("Estimated Cost per Run ($)",
                                             min_value=0,
                                             max_value=10000,
                                             value=100,
                                             step=10)
                
                fixed_costs = st.number_input("Fixed Costs ($)",
                                            min_value=0,
                                            max_value=50000,
                                            value=500,
                                            step=100)
            
            # Calculate totals
            total_time = setup_time + (time_per_run + analysis_time) * total_runs
            total_cost = fixed_costs + cost_per_run * total_runs
            
            st.subheader("Total Estimates")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Time", f"{total_time:.1f} hours")
                if total_time > 40:
                    st.write(f"({total_time/40:.1f} work weeks)")
            
            with col2:
                st.metric("Total Cost", f"${total_cost:,.2f}")
            
            # Timeline visualization
            st.subheader("Estimated Timeline")
            
            # Simplified Gantt chart
            tasks = [
                {"Task": "Setup & Preparation", "Start": 0, "Duration": setup_time},
                {"Task": "Experimental Runs", "Start": setup_time, "Duration": time_per_run * total_runs},
                {"Task": "Analysis", "Start": setup_time + time_per_run * total_runs, "Duration": analysis_time * total_runs}
            ]
            
            # Add tasks for each factor
            for i, block in enumerate(st.session_state.blocking_factors):
                block_duration = total_time / len(st.session_state.blocking_factors)
                tasks.append({
                    "Task": f"Block: {block['name']}", 
                    "Start": i * block_duration, 
                    "Duration": block_duration
                })
            
            # Create DataFrame for Gantt chart
            gantt_df = pd.DataFrame(tasks)
            gantt_df["End"] = gantt_df["Start"] + gantt_df["Duration"]
            
            # Create Gantt chart with Plotly
            fig = px.timeline(gantt_df, x_start="Start", x_end="End", y="Task",
                            color="Task", title="Experimental Timeline (hours)")
            fig.update_layout(xaxis_title="Time (hours)")
            
            st.plotly_chart(fig)
    
    # Tab 4: Design Summary
    with tab4:
        st.subheader("Experimental Design Summary")
        
        # Only proceed if we have factors and responses
        if not st.session_state.factors or not st.session_state.responses:
            st.warning("Please complete the Problem Definition tab first.")
        else:
            # Create summary card
            st.markdown(f"""
            ### {st.session_state.design_name}
            
            **Objective:** {st.session_state.objective}
            
            **Design Type:** {st.session_state.design_type}
            """)
            
            if st.session_state.design_type == "Fractional Factorial":
                st.markdown(f"**Resolution:** {st.session_state.design_resolution}")
            
            # Factors summary
            st.subheader("Factors")
            
            factor_df = pd.DataFrame([
                {
                    "Factor": f["name"],
                    "Category": f["category"],
                    "Low Level": f"{f['low']} {f['units']}",
                    "High Level": f"{f['high']} {f['units']}",
                    "Hard to Change": "Yes" if f["hard_to_change"] else "No"
                }
                for f in st.session_state.factors
            ])
            
            st.dataframe(factor_df)
            
            # Responses summary
            st.subheader("Responses")
            
            response_df = pd.DataFrame([
                {
                    "Response": r["name"],
                    "Category": r["category"],
                    "Units": r["units"],
                    "Specifications": f"{r['lower_spec'] if r['lower_spec'] else '-'} to {r['upper_spec'] if r['upper_spec'] else '-'}",
                    "Priority": r["priority"]
                }
                for r in st.session_state.responses
            ])
            
            st.dataframe(response_df)
            
            # Design details
            st.subheader("Design Details")
            
            # Calculate runs
            num_factors = len(st.session_state.factors)
            
            if st.session_state.design_type == "Full Factorial":
                base_runs = 2**num_factors
                design_desc = f"2^{num_factors} full factorial"
            elif st.session_state.design_type == "Fractional Factorial":
                if st.session_state.design_resolution == "III":
                    fraction = max(1, num_factors-4)
                elif st.session_state.design_resolution == "IV":
                    fraction = max(1, num_factors-5)
                else:  # Resolution V
                    fraction = max(1, num_factors-6)
                    
                fraction = min(fraction, num_factors-1)
                base_runs = 2**(num_factors-fraction)
                design_desc = f"2^({num_factors}-{fraction}) fractional factorial, Resolution {st.session_state.design_resolution}"
            elif st.session_state.design_type == "Plackett-Burman":
                base_runs = 4 * math.ceil((num_factors + 1) / 4)
                design_desc = f"Plackett-Burman design with {base_runs} runs"
            elif st.session_state.design_type == "Response Surface (CCD)":
                base_runs = 2**num_factors + 2*num_factors + 1
                design_desc = f"Central Composite Design with {base_runs} runs"
            elif st.session_state.design_type == "Box-Behnken":
                base_runs = 2*num_factors*(num_factors-1) + 1
                design_desc = f"Box-Behnken Design with {base_runs} runs"
            else:
                base_runs = 2**num_factors
                design_desc = f"Custom design with {base_runs} runs"
            
            # Add center points
            if hasattr(st.session_state, 'center_points') and st.session_state.center_points > 0:
                base_runs += st.session_state.center_points
                design_desc += f" plus {st.session_state.center_points} center points"
            
            # Account for blocking
            blocking_multiplier = 1
            block_desc = ""
            for i, block in enumerate(st.session_state.blocking_factors):
                blocking_multiplier *= block["levels"]
                if i == 0:
                    block_desc = f"blocked by {block['name']} ({block['levels']} levels)"
                else:
                    block_desc += f" and {block['name']} ({block['levels']} levels)"
            
            # Calculate total runs
            total_runs = base_runs * st.session_state.replicates * blocking_multiplier
            
            if st.session_state.replicates > 1:
                design_desc += f", replicated {st.session_state.replicates} times"
            
            if block_desc:
                design_desc += f", {block_desc}"
            
            st.markdown(f"""
            **Design Description:** {design_desc}
            
            **Base Design Runs:** {base_runs}
            
            **Total Experimental Runs:** {total_runs}
            """)
            
            # Power summary
            if st.session_state.min_effect_size > 0:
                st.subheader("Statistical Power")
                
                # Very simplified power calculation
                standardized_effect = st.session_state.min_effect_size
                df_error = total_runs - num_factors - 1
                
                if df_error > 0:
                    # Using a simplified approximation
                    non_centrality = (standardized_effect**2 * total_runs) / (2**num_factors * 4)
                    achieved_power = min(0.99, max(0.10, 0.5 + 0.3 * non_centrality))
                    
                    st.markdown(f"""
                    **Minimum Detectable Effect:** {st.session_state.min_effect_size}
                    
                    **Estimated Power:** {achieved_power:.2f}
                    
                    **Interpretation:** This design has a {achieved_power:.0%} chance of detecting an effect of size {st.session_state.min_effect_size} or larger.
                    """)
            
            # Export options
            st.subheader("Export Design")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Export Design Summary (CSV)"):
                    # Create summary dataframe
                    summary_data = {
                        "Design Name": [st.session_state.design_name],
                        "Objective": [st.session_state.objective],
                        "Design Type": [st.session_state.design_type],
                        "Total Runs": [total_runs],
                        "Number of Factors": [num_factors],
                        "Number of Responses": [len(st.session_state.responses)]
                    }
                    
                    if st.session_state.design_type == "Fractional Factorial":
                        summary_data["Resolution"] = [st.session_state.design_resolution]
                    
                    summary_df = pd.DataFrame(summary_data)
                    
                    # Convert to CSV
                    csv = summary_df.to_csv(index=False)
                    
                    # Create download button
                    st.download_button(
                        label="Download Summary CSV",
                        data=csv,
                        file_name=f"{st.session_state.design_name.replace(' ', '_')}_summary.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("Generate Design Matrix"):
                    # For demonstration purposes, we'll show a success message
                    # In a full application, this would generate and download the design matrix
                    st.success("Design matrix would be generated in the full application.")
            
            # Next steps
            st.subheader("Next Steps")
            
            st.markdown("""
            1. **Finalize Design**: Review all parameters and make any final adjustments.
            2. **Run Simulation**: Test the design with simulated data to verify its properties.
            3. **Prepare Experimental Protocol**: Document detailed run procedures.
            4. **Execute Experiment**: Follow the randomized run order and document all results.
            5. **Analyze Results**: Import data into the Analysis module for statistical evaluation.
            """)

if __name__ == "__main__":
    show()