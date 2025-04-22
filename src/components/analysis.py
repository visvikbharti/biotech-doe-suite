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

# Helper function for standardized effect calculation (difference of averages)
def calculate_main_effect(data, factor_col, response_col):
    """Calculates the main effect of a factor based on difference of averages."""
    mean_high = data.loc[data[factor_col] == 1, response_col].mean()
    mean_low = data.loc[data[factor_col] == -1, response_col].mean()
    return mean_high - mean_low

def calculate_interaction_effect(data, factor1_col, factor2_col, response_col):
    """Calculates the two-factor interaction effect."""
    # Effect of factor1 when factor2 is high
    mean_1p_2p = data.loc[(data[factor1_col] == 1) & (data[factor2_col] == 1), response_col].mean()
    mean_1m_2p = data.loc[(data[factor1_col] == -1) & (data[factor2_col] == 1), response_col].mean()
    effect1_at_2p = mean_1p_2p - mean_1m_2p

    # Effect of factor1 when factor2 is low
    mean_1p_2m = data.loc[(data[factor1_col] == 1) & (data[factor2_col] == -1), response_col].mean()
    mean_1m_2m = data.loc[(data[factor1_col] == -1) & (data[factor2_col] == -1), response_col].mean()
    effect1_at_2m = mean_1p_2m - mean_1m_2m

    # Interaction is half the difference of these effects
    interaction_effect = (effect1_at_2p - effect1_at_2m) / 2.0
    return interaction_effect

def show():
    st.header("Analysis and Interpretation")

    st.markdown("""
    ## Statistical Analysis Framework

    The statistical analysis of experimental designs in biotechnology translates raw data into actionable insights through a structured
    framework that ensures reliability, validity, and interpretability. This section presents the analytical methods, diagnostic approaches,
    and interpretation strategies essential for extracting maximum value from DOE studies.
    """)

    # Create tabs for different analysis sections
    tabs = st.tabs([
        "Effect Estimation",
        "Significance Testing",
        "Model Diagnostics",
        "Response Surface Methods",
        "Design Space Characterization",
        "Analysis Workflow"
    ])

    # Tab 1: Effect Estimation
    with tabs[0]:
        st.subheader("Effect Estimation")

        st.markdown("""
        ### Main Effect Calculation
        **Concept Anchor**: A main effect quantifies the average impact of changing a factor from its low to high level, providing a direct measure of that factor's influence on the response.

        **Practical Lens**: In bioprocess development, main effect estimates for critical process parameters like temperature, pH, and dissolved oxygen directly inform process control strategies. For example, a main effect of +15% for temperature on enzyme activity indicates the criticality of temperature control in process design.

        **Mathematical Foundation**:
        The main effect of factor A is the difference between the average response when A is at its high level and the average response when A is at its low level:

        $$E_A = \\bar{y}_{A+} - \\bar{y}_{A-}$$

        Where:
        - $E_A$ is the effect of factor A
        - $\\bar{y}_{A+}$ is the average response when A is at its high level (+1)
        - $\\bar{y}_{A-}$ is the average response when A is at its low level (-1)

        Alternatively, using coded levels ($x_{iA} = \\pm 1$) and $n$ runs:

        $$E_A = \\frac{\\sum_{i=1}^{n} x_{iA}y_i}{n/2}$$

        *Note: Both formulas yield the same result for orthogonal two-level designs.*
        """)

        # Interactive demo for main effect calculation
        st.markdown("#### Interactive Main Effect Calculation")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Experiment Setup**")
            n_runs_main = st.slider("Number of Runs", min_value=4, max_value=16, value=8, step=4, key="main_effect_runs")
            true_effect_size = st.slider("True Effect Size (Difference in Averages)", min_value=0.0, max_value=20.0, value=10.0, step=0.5, key="main_effect_size")
            noise_level_main = st.slider("Noise Level (σ)", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key="main_effect_noise")

        # Generate experimental data
        np.random.seed(42)  # For reproducibility
        factor_A_main = np.array([-1] * (n_runs_main//2) + [1] * (n_runs_main//2))
        np.random.shuffle(factor_A_main)  # Randomize run order

        # Generate response based on the definition E_A = y_high_avg - y_low_avg
        # The coefficient (beta) is E_A / 2. So, y = base + beta * factor_A + noise
        base_response_main = 50
        response_main = base_response_main + (true_effect_size / 2.0) * factor_A_main + np.random.normal(0, noise_level_main, n_runs_main)

        # Create a dataframe for display and calculation
        exp_data_main = pd.DataFrame({
            "Run": range(1, n_runs_main + 1),
            "Factor_A": factor_A_main, # Use consistent column name
            "Response": response_main.round(2)
        })

        # Calculate effect using the helper function (difference of averages)
        calculated_effect_main = calculate_main_effect(exp_data_main, "Factor_A", "Response")
        mean_plus_main = exp_data_main.loc[exp_data_main["Factor_A"] == 1, "Response"].mean()
        mean_minus_main = exp_data_main.loc[exp_data_main["Factor_A"] == -1, "Response"].mean()

        with col2:
            st.markdown("**Experiment Data**")
            st.dataframe(exp_data_main[["Run", "Factor_A", "Response"]])

        # Display calculated effects
        st.markdown("**Calculated Effect**")
        st.markdown(f"""
        - Average response at high level (A+): {mean_plus_main:.2f}
        - Average response at low level (A-): {mean_minus_main:.2f}
        - **Main effect of Factor A (Difference): {calculated_effect_main:.2f}**
        """)

        # Visualization of main effect
        fig_main = go.Figure()

        # Add data points
        fig_main.add_trace(go.Scatter(
            x=exp_data_main["Factor_A"],
            y=exp_data_main["Response"],
            mode='markers',
            marker=dict(size=10, color='blue'),
            name='Experimental Results'
        ))

        # Add effect visualization (line connecting averages)
        fig_main.add_trace(go.Scatter(
            x=[-1, 1],
            y=[mean_minus_main, mean_plus_main],
            mode='lines+markers',
            marker=dict(size=12, color='red'),
            line=dict(width=3, color='red', dash='dash'),
            name='Main Effect'
        ))

        fig_main.update_layout(
            title="Visualization of Main Effect",
            xaxis=dict(
                title="Factor A Level",
                tickvals=[-1, 1],
                ticktext=["Low (-1)", "High (+1)"]
            ),
            yaxis=dict(title="Response"),
            height=400
        )

        st.plotly_chart(fig_main)

        st.markdown("---") # Separator

        st.markdown("### Interaction Effect Calculation")
        st.markdown("""
        **Concept Anchor**: Interaction effects measure how the impact of one factor on the response depends on the level of another factor, revealing synergistic or antagonistic relationships common in biological systems.

        **Practical Lens**: In cell culture optimization, significant temperature-by-pH interactions inform operating parameters, as the optimal pH may vary with culture temperature. This interaction insight enables targeted optimization rather than independent factor adjustment.

        **Mathematical Foundation**:
        The two-factor interaction effect for factors A and B ($E_{AB}$) is half the difference between the effect of A when B is high and the effect of A when B is low:

        $$E_{AB} = \\frac{1}{2} [ (\\bar{y}_{A+B+} - \\bar{y}_{A-B+}) - (\\bar{y}_{A+B-} - \\bar{y}_{A-B-}) ]$$

        Where terms like $\\bar{y}_{A+B+}$ represent the average response when both factors are at their high levels.

        Alternatively, using coded levels ($x_{iA}, x_{iB} = \\pm 1$) and $n$ runs:

        $$E_{AB} = \\frac{\\sum_{i=1}^{n} (x_{iA}x_{iB})y_i}{n/2}$$

        *Note: Both formulas yield the same result for orthogonal two-level designs.*
        """)

        st.markdown("#### Interactive Interaction Effect Visualization")

        # Setup for interaction effect demo
        interaction_magnitude = st.slider("True Interaction Magnitude (E_AB)", min_value=-10.0, max_value=10.0, value=5.0, step=0.5, key="interaction_mag")
        n_runs_interaction = st.slider("Number of Runs (e.g., 2² design)", min_value=4, max_value=16, value=8, step=4, key="interaction_runs")
        noise_level_interaction = st.slider("Noise Level (σ)", min_value=0.1, max_value=5.0, value=1.0, step=0.1, key="interaction_noise")

        # Generate 2-factor experiment data
        np.random.seed(42)
        # Ensure we have enough points for the design (e.g., 2^2 = 4, replicated if n_runs > 4)
        replicates = n_runs_interaction // 4
        if replicates < 1: replicates = 1
        n_actual_runs = replicates * 4

        factor_A_int = np.tile([-1, 1, -1, 1], replicates)
        factor_B_int = np.tile([-1, -1, 1, 1], replicates)

        # Shuffle if needed, but keep A and B paired correctly for calculation
        shuffle_idx = np.random.permutation(n_actual_runs)
        factor_A_int = factor_A_int[shuffle_idx]
        factor_B_int = factor_B_int[shuffle_idx]

        # Generate response based on the model y = base + beta_A*A + beta_B*B + beta_AB*A*B + noise
        # Where beta = Effect / 2
        effect_A_int = 8.0  # Fixed main effect of A for demo
        effect_B_int = 4.0  # Fixed main effect of B for demo
        base_response_int = 50.0

        response_int = (base_response_int +
                        (effect_A_int / 2.0) * factor_A_int +
                        (effect_B_int / 2.0) * factor_B_int +
                        (interaction_magnitude / 2.0) * factor_A_int * factor_B_int +
                        np.random.normal(0, noise_level_interaction, n_actual_runs))

        # Create dataframe for calculation and display
        exp_data_int = pd.DataFrame({
            "Run": range(1, n_actual_runs + 1),
            "Factor_A": factor_A_int,
            "Factor_B": factor_B_int,
            "Response": response_int.round(2)
        })

        # Calculate interaction effect using the helper function
        calc_interaction_effect = calculate_interaction_effect(exp_data_int, "Factor_A", "Factor_B", "Response")

        # Calculate average responses for each factor combination for plotting
        y_Aplus_Bplus = exp_data_int.loc[(exp_data_int["Factor_A"] == 1) & (exp_data_int["Factor_B"] == 1), "Response"].mean()
        y_Aplus_Bminus = exp_data_int.loc[(exp_data_int["Factor_A"] == 1) & (exp_data_int["Factor_B"] == -1), "Response"].mean()
        y_Aminus_Bplus = exp_data_int.loc[(exp_data_int["Factor_A"] == -1) & (exp_data_int["Factor_B"] == 1), "Response"].mean()
        y_Aminus_Bminus = exp_data_int.loc[(exp_data_int["Factor_A"] == -1) & (exp_data_int["Factor_B"] == -1), "Response"].mean()

        # Display data
        st.dataframe(exp_data_int)

        # Create interaction plot
        fig_int = go.Figure()

        # B at low level
        fig_int.add_trace(go.Scatter(
            x=[-1, 1],
            y=[y_Aminus_Bminus, y_Aplus_Bminus],
            mode='lines+markers',
            marker=dict(size=10, color='blue'),
            line=dict(width=2, color='blue'),
            name='B at Low Level (-1)'
        ))

        # B at high level
        fig_int.add_trace(go.Scatter(
            x=[-1, 1],
            y=[y_Aminus_Bplus, y_Aplus_Bplus],
            mode='lines+markers',
            marker=dict(size=10, color='red'),
            line=dict(width=2, color='red'),
            name='B at High Level (+1)'
        ))

        fig_int.update_layout(
            title=f"Interaction Plot (Calculated E_AB: {calc_interaction_effect:.2f})",
            xaxis=dict(
                title="Factor A Level",
                tickvals=[-1, 1],
                ticktext=["Low (-1)", "High (+1)"]
            ),
            yaxis=dict(title="Response"),
            height=400
        )

        st.plotly_chart(fig_int)

        st.markdown(f"""
        **Interpretation:**

        The calculated interaction effect is {calc_interaction_effect:.2f}.
        - A value far from zero suggests a strong interaction (non-parallel lines).
        - A value close to zero suggests little to no interaction (lines are nearly parallel).

        In biological systems, interactions like this are common. For example, in fermentation processes, the effect of temperature on product yield often depends on the pH level, requiring simultaneous optimization of both factors.
        """)

        st.markdown("---") # Separator

        st.markdown("### Regression Coefficient Estimation")
        st.markdown("""
        **Concept Anchor**: Regression coefficients translate experimental effects into predictive models, allowing interpolation, extrapolation, and optimization across the design space.

        **Practical Lens**: In protein expression optimization, a regression model with significant coefficients for temperature, inducer concentration, and their interaction enables prediction of protein yield across the entire design space, guiding process development and scale-up decisions.

        **Mathematical Foundation**:
        For a model $y = X\\beta + \\varepsilon$, the least squares estimator is:

        $$\\hat{\\beta} = (X^TX)^{-1}X^Ty$$

        Where:
        - $X$ is the design matrix (including intercept and effect terms)
        - $y$ is the vector of response values
        - $\\hat{\\beta}$ is the vector of estimated coefficients

        For orthogonal designs, this simplifies to:

        $$\\hat{\\beta}_j = \\frac{X_j^Ty}{X_j^TX_j}$$

        **Relationship between Effects and Coefficients (for coded -1/+1 factors):**

        $$\\hat{\\beta}_0 = \\bar{y} \\quad \\text{(Intercept is the overall average response)}$$
        $$\\hat{\\beta}_j = \\frac{E_j}{2} \\quad \\text{(for main effects and interactions)}$$

        *This means the coefficient represents half the change in response when moving from the center (0) to the high level (+1) of the corresponding coded factor/interaction.*
        """)

    # Tab 2: Significance Testing
    with tabs[1]:
        st.subheader("Significance Testing")

        st.markdown("""
        ### Analysis of Variance (ANOVA)
        **Concept Anchor**: ANOVA partitions total variation into components attributable to different factors and error, enabling statistical significance testing of effects.

        **Practical Lens**: In bioanalytical method validation, ANOVA determines whether observed differences across pH levels represent real effects or random variation, supporting robust method development and regulatory compliance.

        **Mathematical Foundation**:
        The total sum of squares is partitioned as:

        $$SS_{Total} = SS_{Model} + SS_{Error}$$

        Where:
        - $SS_{Total} = \\sum_{i=1}^{n} (y_i - \\bar{y})^2$
        - $SS_{Model} = \\sum_{i=1}^{n} (\\hat{y}_i - \\bar{y})^2$
        - $SS_{Error} = \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2$

        The model sum of squares can be further partitioned by effects:

        $$SS_{Model} = SS_A + SS_B + SS_{AB} + ...$$

        The F-statistic for testing factor A's significance is:

        $$F_A = \\frac{MS_A}{MS_{Error}} = \\frac{SS_A/df_A}{SS_{Error}/df_{Error}}$$

        Where $MS$ represents Mean Squares and $df$ represents degrees of freedom.
        """)

        # Interactive ANOVA example
        st.markdown("#### Interactive ANOVA Example")

        # Setup for ANOVA demo
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Experiment Parameters**")
            # Use effect sizes directly
            effect_A_anova = st.slider("Effect of Factor A (E_A)", min_value=0.0, max_value=15.0, value=8.0, step=0.5, key="anova_effect_A")
            effect_B_anova = st.slider("Effect of Factor B (E_B)", min_value=0.0, max_value=15.0, value=4.0, step=0.5, key="anova_effect_B")
            effect_AB_anova = st.slider("A×B Interaction Effect (E_AB)", min_value=0.0, max_value=10.0, value=3.0, step=0.5, key="anova_effect_AB")
            error_std_anova = st.slider("Error Standard Deviation (σ)", min_value=0.5, max_value=10.0, value=2.0, step=0.5, key="anova_error")

        # Generate 2-factor factorial data
        np.random.seed(42)
        runs_anova = 16  # 2^2 with 4 replicates
        factor_A_anova = np.repeat([-1, 1, -1, 1], runs_anova//4) # Balanced design
        factor_B_anova = np.repeat([-1, -1, 1, 1], runs_anova//4) # Balanced design

        # Generate response with specified effects (using Effect/2 for coefficients)
        response_anova = 50.0 + (effect_A_anova/2.0) * factor_A_anova + (effect_B_anova/2.0) * factor_B_anova + (effect_AB_anova/2.0) * factor_A_anova * factor_B_anova
        response_anova += np.random.normal(0, error_std_anova, runs_anova)

        # Create dataframe for analysis
        anova_data = pd.DataFrame({
            'A': factor_A_anova,
            'B': factor_B_anova,
            'Response': response_anova
        })
        anova_data['AB'] = anova_data['A'] * anova_data['B'] # Calculate interaction term

        # Fit model using statsmodels
        model_anova = ols('Response ~ A + B + AB', data=anova_data).fit()
        anova_table = sm.stats.anova_lm(model_anova, typ=2) # Type 2 SS is generally preferred

        # Calculate Sums of Squares manually for educational purposes
        SS_Total_anova = np.sum((response_anova - np.mean(response_anova))**2)
        SS_Model_anova = np.sum((model_anova.fittedvalues - np.mean(response_anova))**2)
        SS_Error_anova = np.sum((response_anova - model_anova.fittedvalues)**2)

        # Calculate R-squared
        r_squared_anova = SS_Model_anova / SS_Total_anova

        with col2:
            st.markdown("**ANOVA Table**")

            # Format the ANOVA table for display
            formatted_anova = anova_table.copy()
            formatted_anova['F'] = formatted_anova['F'].round(3)
            formatted_anova['PR(>F)'] = formatted_anova['PR(>F)'].round(4)
            formatted_anova.columns = ['Sum Sq', 'DF', 'F-value', 'p-value'] # Reorder slightly
            formatted_anova = formatted_anova[['DF', 'Sum Sq', 'F-value', 'p-value']] # Select columns
            formatted_anova['Mean Sq'] = formatted_anova['Sum Sq'] / formatted_anova['DF'] # Calculate Mean Square
            formatted_anova = formatted_anova[['DF', 'Sum Sq', 'Mean Sq', 'F-value', 'p-value']] # Final order

            st.dataframe(formatted_anova.style.format({
                'Sum Sq': '{:.2f}',
                'Mean Sq': '{:.2f}',
                'F-value': '{:.3f}',
                'p-value': '{:.4g}'
            }).background_gradient(subset=['p-value'], cmap='Reds_r'))

            st.markdown(f"""
            **Model Statistics**:
            - R² = {r_squared_anova:.4f}
            - $SS_{Total}$ = {SS_Total_anova:.2f}
            - $SS_{Model}$ = {SS_Model_anova:.2f}
            - $SS_{Error}$ = {SS_Error_anova:.2f}
            """)

        # Create effect visualization
        st.markdown("**Visualizing ANOVA Components**")

        # Create bar chart of effects and their significance
        effect_names_anova = ['A', 'B', 'AB']
        effect_values_anova = [effect_A_anova, effect_B_anova, effect_AB_anova] # Use the input effect sizes
        p_values_anova = anova_table['PR(>F)'].values[:-1] # Exclude residual p-value

        # Create DataFrame for Plotly Express
        plot_df_anova = pd.DataFrame({
            'Effect Term': effect_names_anova,
            'Effect Size': effect_values_anova,
            'p-value': p_values_anova
        })

        fig_anova = px.bar(
            plot_df_anova,
            x='Effect Term',
            y='Effect Size',
            color='p-value',
            color_continuous_scale='RdYlGn_r', # Red = significant (low p), Green = insignificant (high p)
            color_continuous_midpoint=0.05, # Set midpoint for color scale
            labels={'Effect Term': 'Effect Term', 'Effect Size': 'Effect Size (E)', 'color': 'p-value'},
            title="Effects and Their Statistical Significance"
        )

        st.plotly_chart(fig_anova)

        st.markdown(f"""
        **Interpretation:**

        The ANOVA table shows how the total variation in the response is partitioned into components due to factors A, B, their interaction, and random error.

        - Factor A has {"a significant" if p_values_anova[0] < 0.05 else "an insignificant"} effect (p = {p_values_anova[0]:.4f})
        - Factor B has {"a significant" if p_values_anova[1] < 0.05 else "an insignificant"} effect (p = {p_values_anova[1]:.4f})
        - The A×B interaction is {"significant" if p_values_anova[2] < 0.05 else "insignificant"} (p = {p_values_anova[2]:.4f})

        In biotechnology applications, significant effects identify critical process parameters that require careful control during manufacturing.
        """)

        st.markdown("---") # Separator

        st.markdown("### Effect Plots and Half-Normal Plots")
        st.markdown("""
        **Concept Anchor**: Effect plots and half-normal plots provide visual methods for identifying significant effects, particularly useful in screening experiments with many factors.

        **Practical Lens**: In upstream process screening, half-normal plots rapidly identify the vital few parameters from the trivial many, revealing that dissolved oxygen and feed rate significantly impact product titer while several other parameters show negligible effects.

        **Mathematical Approach**:
        1. **Pareto Plot of Effects**:
           - Plot absolute effect size vs. factors
           - Include significance threshold
           - Sort effects in descending order

        2. **Half-Normal Plot**:
           - Plot absolute effect size vs. theoretical half-normal quantiles
           - Effects that deviate from the straight line are potentially significant
           - For ordered absolute effects $|E_{(1)}| \\leq |E_{(2)}| \\leq ... \\leq |E_{(m)}|$, plot points:
             $$\\left(z_{(i)}, |E_{(i)}|\\right)$$
             Where $z_{(i)} = \\Phi^{-1}\\left(\\frac{i+m-0.5}{2m}\\right)$ and $\\Phi^{-1}$ is the inverse standard normal CDF. *Note: Formula adjusted slightly for standard half-normal plotting.*
        """)

        # Demo of half-normal plot
        st.markdown("#### Interactive Half-Normal Plot Example")

        # Generate effect data for half-normal plot
        np.random.seed(23)

        # Number of effects to simulate
        n_effects_hnp = st.slider("Number of Effects", min_value=5, max_value=15, value=7, step=1, key="hnp_effects")

        # Generate effects: a few significant, most are noise
        true_effects_hnp = np.zeros(n_effects_hnp)

        # Set 2-3 effects to be significant
        num_sig_hnp = 3 if n_effects_hnp >= 7 else min(2, n_effects_hnp)
        sig_indices_hnp = np.random.choice(n_effects_hnp, num_sig_hnp, replace=False)
        true_effects_hnp[sig_indices_hnp] = np.random.uniform(5, 15, num_sig_hnp) * np.random.choice([-1, 1], num_sig_hnp) # Add sign

        # Add noise to all effects
        observed_effects_hnp = true_effects_hnp + np.random.normal(0, 1.5, n_effects_hnp)

        # Effect names (A, B, C, AB, AC, etc.) - Simplified for demo
        effect_names_hnp = [f"Effect_{chr(65+i)}" for i in range(n_effects_hnp)]

        # Create half-normal plot
        abs_effects_hnp = np.abs(observed_effects_hnp)
        sorted_indices_hnp = np.argsort(abs_effects_hnp)
        sorted_abs_effects_hnp = abs_effects_hnp[sorted_indices_hnp]
        sorted_names_hnp = [effect_names_hnp[i] for i in sorted_indices_hnp]

        # Calculate half-normal quantiles
        p_points_hnp = (np.arange(1, n_effects_hnp + 1) - 0.5) / n_effects_hnp # Standard formula
        z_points_hnp = stats.norm.ppf((1 + p_points_hnp) / 2)

        # Create dataframe for plotting
        hnp_data = pd.DataFrame({
            'Effect': sorted_names_hnp,
            'AbsoluteEffect': sorted_abs_effects_hnp,
            'HalfNormalQuantile': z_points_hnp,
            'IsSignificant': np.isin(sorted_indices_hnp, sig_indices_hnp) # Mark the truly significant ones
        })

        # Create half-normal plot using Plotly Express
        fig_hnp = px.scatter(
            hnp_data,
            x='HalfNormalQuantile',
            y='AbsoluteEffect',
            text='Effect',
            color='IsSignificant', # Color based on whether it was truly significant
            color_discrete_map={True: 'red', False: 'blue'},
            labels={'HalfNormalQuantile': 'Half-Normal Quantile (z)', 'AbsoluteEffect': 'Absolute Effect |E|', 'IsSignificant': 'Truly Significant'},
            title="Half-Normal Plot of Effects"
        )

        # Add line representing noise (using robust estimate - Lenth's PSE)
        # Lenth's method is common for analyzing unreplicated factorials
        try:
            s0 = 1.5 * np.median(abs_effects_hnp)
            pseudo_std_err = 1.5 * np.median(abs_effects_hnp[abs_effects_hnp < 2.5 * s0])
            # Add a line based on this pseudo standard error
            x_trend_hnp = np.linspace(0, max(z_points_hnp), 100)
            y_trend_hnp = pseudo_std_err * x_trend_hnp # Line through origin with slope = PSE

            fig_hnp.add_trace(go.Scatter(
                x=x_trend_hnp,
                y=y_trend_hnp,
                mode='lines',
                line=dict(color='gray', dash='dash'),
                name='Noise Trend (Lenth PSE)'
            ))
        except:
            st.warning("Could not calculate Lenth's PSE for noise trend line.")


        fig_hnp.update_traces(textposition='top right')
        st.plotly_chart(fig_hnp)

        # Show Pareto chart of effects
        pareto_data_hnp = pd.DataFrame({
            'Effect': effect_names_hnp,
            'AbsoluteEffect': abs_effects_hnp,
            'IsSignificant': np.isin(np.arange(n_effects_hnp), sig_indices_hnp)
        }).sort_values('AbsoluteEffect', ascending=False)

        fig_pareto_hnp = px.bar(
            pareto_data_hnp,
            x='Effect',
            y='AbsoluteEffect',
            color='IsSignificant',
            color_discrete_map={True: 'red', False: 'blue'},
            title="Pareto Chart of Effects"
        )

        # Add reference line for significance threshold (e.g., Lenth's ME)
        try:
            margin_error = stats.t.ppf(1 - 0.05 / 2, df=n_effects_hnp // 3) * pseudo_std_err # Approximate df
            fig_pareto_hnp.add_shape(
                type="line",
                x0=-0.5, x1=n_effects_hnp-0.5,
                y0=margin_error, y1=margin_error,
                line=dict(color="red", width=2, dash="dash"),
                name="Significance Threshold (Lenth ME)"
            )
        except:
            pass # Skip if PSE calculation failed

        st.plotly_chart(fig_pareto_hnp)

        st.markdown("""
        **Interpretation:**

        - **Half-Normal Plot**: Effects falling along the dashed line are consistent with noise, while effects deviating significantly (often colored red if truly significant in this demo) are likely real effects.
        - **Pareto Chart**: Displays the absolute effect sizes in descending order. Effects exceeding the significance threshold (red dashed line) are typically considered statistically significant.

        In biotechnology applications, these plots help researchers quickly identify the vital few parameters that most strongly influence a bioprocess or analytical method, directing focus to the critical factors.
        """)

        st.markdown("---") # Separator

        st.markdown("### Effect Sparsity and Model Reduction")
        st.markdown("""
        **Concept Anchor**: Effect sparsity principle posits that most systems are driven by a relatively small number of main effects and low-order interactions, enabling model simplification without sacrificing predictive power.

        **Practical Lens**: In a 32-run vaccine formulation study with 5 factors, applying effect sparsity principles reveals that only 3 main effects and 2 two-factor interactions significantly affect stability, allowing focused optimization on these critical parameters.

        **Methodological Approach**:
        1. **Backward Elimination**: Start with full model, sequentially remove least significant terms (highest p-value > threshold).
        2. **Forward Selection**: Start with intercept, add most significant terms one by one (lowest p-value < threshold).
        3. **Stepwise Regression**: Combination of forward and backward steps.
        4. **Information Criteria**: Select model minimizing AIC (Akaike Information Criterion) or BIC (Bayesian Information Criterion).
           - $AIC = 2k - 2\\ln(L)$
           - $BIC = k\\ln(n) - 2\\ln(L)$
           - Where $k$ is number of parameters, $L$ is likelihood, $n$ is sample size. Lower values are better.
        """)

        # Model reduction demo
        st.markdown("#### Interactive Model Reduction Example")

        # Generate data for model reduction example
        np.random.seed(42)
        n_runs_mr = 32
        n_factors_mr = 5

        # Create factor columns (A-E) using standard order generation
        factor_names_mr = list("ABCDE")
        factor_data_mr = {}

        for i, name in enumerate(factor_names_mr):
            # Pattern length doubles for each factor
            pattern_length = 2**(n_factors_mr - 1 - i)
            # Create the repeating pattern of -1s and 1s
            pattern = np.repeat([-1, 1], pattern_length)
            # Tile the pattern to fill the column
            repeats = n_runs_mr // (2 * pattern_length)
            factor_data_mr[name] = np.tile(pattern, repeats)

        # Add 2-factor interactions
        interaction_terms_mr = []
        for i, j in combinations(range(n_factors_mr), 2):
            name_i = factor_names_mr[i]
            name_j = factor_names_mr[j]
            interaction_name = f"{name_i}{name_j}"
            interaction_terms_mr.append(interaction_name)
            factor_data_mr[interaction_name] = factor_data_mr[name_i] * factor_data_mr[name_j]

        # Define active effects (using sparsity principle)
        # In this case: A, C, E, AC, and AE are active
        active_effects_mr = ['A', 'C', 'E', 'AC', 'AE']
        effect_sizes_mr = {
            'A': 10.0,
            'C': 7.5,
            'E': 5.0,
            'AC': 4.0,
            'AE': 3.0
        }

        # Generate response (using Effect/2 for coefficients)
        response_mr = np.ones(n_runs_mr) * 50.0  # Base response
        for effect, size in effect_sizes_mr.items():
            response_mr += (size / 2.0) * factor_data_mr[effect]

        # Add noise
        noise_level_mr = st.slider("Noise Level (σ)", min_value=0.5, max_value=5.0, value=2.0, step=0.5, key="model_reduction_noise")
        response_mr += np.random.normal(0, noise_level_mr, n_runs_mr)

        # Create full dataframe for analysis
        model_data_mr = pd.DataFrame(factor_data_mr)
        model_data_mr['Response'] = response_mr

        # Fit full model
        all_terms_mr = factor_names_mr + interaction_terms_mr
        formula_full_mr = "Response ~ " + " + ".join(all_terms_mr)
        full_model_mr = ols(formula_full_mr, data=model_data_mr).fit()

        # Display full model summary
        # Calculate Effect = 2 * Coefficient
        full_summary_mr_df = pd.DataFrame({
            'Coefficient': full_model_mr.params,
            'Std Error': full_model_mr.bse,
            't-value': full_model_mr.tvalues,
            'p-value': full_model_mr.pvalues
        })
        full_summary_mr_df['Effect'] = full_summary_mr_df['Coefficient'] * 2
        full_summary_mr_df.loc['Intercept', 'Effect'] = full_summary_mr_df.loc['Intercept', 'Coefficient'] # Intercept is not doubled
        full_summary_mr_df = full_summary_mr_df[['Effect', 'Coefficient', 'Std Error', 't-value', 'p-value']] # Reorder


        st.markdown("**Full Model Summary**")
        st.dataframe(full_summary_mr_df.style.format({
            'Effect': '{:.4f}',
            'Coefficient': '{:.4f}',
            'Std Error': '{:.4f}',
            't-value': '{:.3f}',
            'p-value': '{:.4f}'
        }).background_gradient(subset=['p-value'], cmap='Reds_r'))

        # Perform model reduction via backward elimination
        p_threshold_mr = st.slider("p-value Threshold for Term Inclusion", min_value=0.01, max_value=0.2, value=0.05, step=0.01, key="mr_p_thresh")

        # Manually perform backward elimination based on p-value
        significant_terms_mr = full_summary_mr_df[full_summary_mr_df['p-value'] <= p_threshold_mr].index.tolist()

        # Remove Intercept from list for formula building, if present
        if 'Intercept' in significant_terms_mr:
            significant_terms_mr.remove('Intercept')

        # Check if any terms remain significant
        if significant_terms_mr:
            reduced_formula_mr = "Response ~ " + " + ".join(significant_terms_mr)
            reduced_model_mr = ols(reduced_formula_mr, data=model_data_mr).fit()

            # Display reduced model summary
            # Calculate Effect = 2 * Coefficient
            reduced_summary_mr_df = pd.DataFrame({
                'Coefficient': reduced_model_mr.params,
                'Std Error': reduced_model_mr.bse,
                't-value': reduced_model_mr.tvalues,
                'p-value': reduced_model_mr.pvalues
            })
            reduced_summary_mr_df['Effect'] = reduced_summary_mr_df['Coefficient'] * 2
            reduced_summary_mr_df.loc['Intercept', 'Effect'] = reduced_summary_mr_df.loc['Intercept', 'Coefficient'] # Intercept is not doubled
            reduced_summary_mr_df = reduced_summary_mr_df[['Effect', 'Coefficient', 'Std Error', 't-value', 'p-value']] # Reorder

            st.markdown(f"**Reduced Model (p ≤ {p_threshold_mr})**")
            st.dataframe(reduced_summary_mr_df.style.format({
                'Effect': '{:.4f}',
                'Coefficient': '{:.4f}',
                'Std Error': '{:.4f}',
                't-value': '{:.3f}',
                'p-value': '{:.4f}'
            }).background_gradient(subset=['p-value'], cmap='Reds_r'))

            # Compare models
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Full Model**")
                st.metric("R²", f"{full_model_mr.rsquared:.4f}")
                st.metric("Adjusted R²", f"{full_model_mr.rsquared_adj:.4f}")
                st.metric("AIC", f"{full_model_mr.aic:.2f}")
                st.metric("BIC", f"{full_model_mr.bic:.2f}")
                st.metric("Parameters", f"{len(full_model_mr.params)}")

            with col2:
                st.markdown("**Reduced Model**")
                st.metric("R²", f"{reduced_model_mr.rsquared:.4f}")
                st.metric("Adjusted R²", f"{reduced_model_mr.rsquared_adj:.4f}")
                st.metric("AIC", f"{reduced_model_mr.aic:.2f}")
                st.metric("BIC", f"{reduced_model_mr.bic:.2f}")
                st.metric("Parameters", f"{len(reduced_model_mr.params)}")

            # Model comparison test (only if models are different)
            if len(reduced_model_mr.params) < len(full_model_mr.params):
                try:
                    # Use compare_f_test for nested models
                    f_stat_comp, p_value_comp, _ = full_model_mr.compare_f_test(reduced_model_mr)

                    st.markdown("**Model Comparison Test (Full vs. Reduced)**")
                    st.markdown(f"""
                    - F-statistic: {f_stat_comp:.4f}
                    - p-value: {p_value_comp:.4g}

                    Interpretation: A low p-value (< 0.05) suggests the full model provides a significantly better fit than the reduced model (i.e., removing terms significantly worsened the fit). A high p-value suggests the reduced model is adequate.
                    """)
                except Exception as e:
                    st.warning(f"Could not perform model comparison test: {e}")


            # Compare with active effects
            correct_identifications_mr = sum(1 for term in significant_terms_mr if term in active_effects_mr)
            false_positives_mr = sum(1 for term in significant_terms_mr if term not in active_effects_mr)
            false_negatives_mr = sum(1 for term in active_effects_mr if term not in significant_terms_mr)

            st.markdown("**Model Reduction Effectiveness**")
            st.markdown(f"""
            - Correctly identified active effects: {correct_identifications_mr}/{len(active_effects_mr)}
            - False positives (inactive effects included): {false_positives_mr}
            - False negatives (active effects missed): {false_negatives_mr}
            """)

        else:
            st.warning("No terms met the significance threshold. The reduced model is just the intercept. Consider increasing the p-value threshold or re-evaluating the experiment.")

    # Tab 3: Model Diagnostics
    with tabs[2]:
        st.subheader("Model Diagnostics")
        
        st.markdown("### Residual Analysis")
        st.markdown("""
        **Concept Anchor**: Residual analysis examines differences between observed and predicted values to validate model assumptions and identify potential issues in experimental data.

        **Practical Lens**: In bioreactor scale-up studies, residual analysis reveals heteroscedasticity at higher cell densities, indicating that a log transformation of the response improves model validity and prediction accuracy across the scale-up range.

        **Diagnostic Approaches**:
        1. **Residual vs. Predicted Plot**:
           - Detect non-linearity and heteroscedasticity
           - Look for even scatter around zero line
           - Test randomness with runs test: $Z = \\frac{R - E(R)}{\\sigma_R}$
             Where $R$ is the number of runs, $E(R) = \\frac{2n_1n_2}{n_1+n_2}+1$, and $\\sigma_R = \\sqrt{\\frac{2n_1n_2(2n_1n_2-n_1-n_2)}{(n_1+n_2)^2(n_1+n_2-1)}}$

        2. **Residual Normality**:
           - Normal probability plot of residuals
           - Shapiro-Wilk test: $W = \\frac{(\\sum_{i=1}^n a_i x_{(i)})^2}{\\sum_{i=1}^n (x_i - \\bar{x})^2}$
             Where $x_{(i)}$ are ordered observations and $a_i$ are constants

        3. **Residual vs. Run Order Plot**:
           - Detect time-dependent effects
           - Look for random pattern (no trends)
           - Test for autocorrelation: $r = \\frac{\\sum_{i=1}^{n-1} (e_i - \\bar{e})(e_{i+1} - \\bar{e})}{\\sum_{i=1}^n (e_i - \\bar{e})^2}$
        """)
        
        # Interactive residual analysis demo
        st.markdown("#### Interactive Residual Analysis")
        
        # Model parameters for simulation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Simulation Parameters**")
            diagnostics_issue = st.selectbox(
                "Select Issue to Demonstrate",
                ["No Issues (Good Model)", "Non-Linearity", "Heteroscedasticity", "Time-Dependent Effect", "Outliers"]
            )
            
            n_runs = st.slider("Number of Runs", min_value=10, max_value=40, value=20, step=5, key="diag_runs")
        
        # Generate data with selected issue
        np.random.seed(42)
        
        # Create simple linear model data
        x1 = np.random.uniform(-1, 1, n_runs)
        x2 = np.random.uniform(-1, 1, n_runs)
        
        # Create run order
        run_order = np.arange(1, n_runs + 1)
        
        # Base model
        y_true = 50 + 5 * x1 + 3 * x2
        
        # Add selected issue
        if diagnostics_issue == "No Issues (Good Model)":
            # Just add constant noise
            y = y_true + np.random.normal(0, 1, n_runs)
            issue_description = "This model shows well-behaved residuals with no pattern, consistent variance, and normal distribution."
            
        elif diagnostics_issue == "Non-Linearity":
            # Add quadratic term not included in model
            y = y_true + 4 * x1**2 + np.random.normal(0, 1, n_runs)
            issue_description = "Non-linearity appears as a curved pattern in residuals vs. predicted plot, indicating that the linear model is missing higher-order terms."
            
        elif diagnostics_issue == "Heteroscedasticity":
            # Variance increases with predicted value
            base_noise = np.random.normal(0, 1, n_runs)
            variable_noise = base_noise * (1 + 2 * abs(x1))
            y = y_true + variable_noise
            issue_description = "Heteroscedasticity appears as a fan or cone shape in the residuals, with variance increasing or decreasing with the predicted value."
            
        elif diagnostics_issue == "Time-Dependent Effect":
            # Add time trend to residuals
            time_effect = 0.1 * run_order
            y = y_true + time_effect + np.random.normal(0, 1, n_runs)
            issue_description = "Time-dependent effects appear as trends in the residuals vs. run order plot, indicating potential drift in the system over time."
            
        elif diagnostics_issue == "Outliers":
            # Add a few outliers
            y = y_true + np.random.normal(0, 1, n_runs)
            outlier_indices = np.random.choice(n_runs, 2, replace=False)
            y[outlier_indices] += np.array([6, -6])  # Add large deviations
            issue_description = "Outliers appear as points with unusually large residuals that don't follow the pattern of the rest of the data."
        
        # Create dataframe for analysis
        diag_data = pd.DataFrame({
            'RunOrder': run_order,
            'x1': x1,
            'x2': x2,
            'Response': y
        })
        
        # Fit linear model
        diag_model = ols('Response ~ x1 + x2', data=diag_data).fit()
        
        # Calculate fitted values and residuals
        diag_data['Fitted'] = diag_model.fittedvalues
        diag_data['Residual'] = diag_model.resid
        diag_data['Std_Residual'] = diag_model.get_influence().resid_studentized_internal
        
        # Diagnostic plots
        with col2:
            st.markdown("**Model Summary**")
            st.markdown(f"""
            - R² = {diag_model.rsquared:.4f}
            - Adjusted R² = {diag_model.rsquared_adj:.4f}
            - F-statistic p-value = {diag_model.f_pvalue:.4g}
            - Shapiro-Wilk test for normality: p = {stats.shapiro(diag_data['Residual'])[1]:.4f}
            """)
        
        st.markdown(f"**Issue Being Demonstrated**: {diagnostics_issue}")
        st.markdown(issue_description)
        
        # Create diagnostic plots
        fig = make_subplots(rows=2, cols=2, 
                           subplot_titles=["Residuals vs. Fitted Values", "Normal Q-Q Plot", 
                                         "Residuals vs. Run Order", "Residual Histogram"])
        
        # 1. Residuals vs. Fitted
        fig.add_trace(
            go.Scatter(
                x=diag_data['Fitted'], 
                y=diag_data['Std_Residual'],
                mode='markers',
                marker=dict(size=10, color=diag_data['Std_Residual'], colorscale='RdBu_r', showscale=False),
                name='Residuals'
            ),
            row=1, col=1
        )
        
        # Add a smoothed trend line
        try:
            from statsmodels.nonparametric.smoothers_lowess import lowess
            smoothed = lowess(diag_data['Std_Residual'], diag_data['Fitted'], frac=0.6)
            
            fig.add_trace(
                go.Scatter(
                    x=smoothed[:, 0],
                    y=smoothed[:, 1],
                    mode='lines',
                    line=dict(color='black', width=2),
                    name='Trend'
                ),
                row=1, col=1
            )
        except:
            pass
        
        # Add reference line at y=0
        fig.add_shape(
            type="line", x0=min(diag_data['Fitted']), x1=max(diag_data['Fitted']), 
            y0=0, y1=0, line=dict(color="red", dash="dash"),
            row=1, col=1
        )
        
        # 2. Normal Q-Q Plot
        fig.add_trace(
            go.Scatter(
                x=np.sort(stats.norm.ppf(np.arange(1, n_runs + 1) / (n_runs + 1))),
                y=np.sort(diag_data['Std_Residual']),
                mode='markers',
                marker=dict(size=10),
                name='QQ Plot'
            ),
            row=1, col=2
        )
        
        # Add reference line
        qq_x = np.linspace(min(diag_data['Std_Residual']), max(diag_data['Std_Residual']), 100)
        fig.add_trace(
            go.Scatter(
                x=qq_x,
                y=qq_x,
                mode='lines',
                line=dict(color="red", dash="dash"),
                name='Normal Reference'
            ),
            row=1, col=2
        )
        
        # 3. Residuals vs. Run Order
        fig.add_trace(
            go.Scatter(
                x=diag_data['RunOrder'],
                y=diag_data['Std_Residual'],
                mode='markers+lines',
                marker=dict(size=10),
                name='Time Series'
            ),
            row=2, col=1
        )
        
        # Add reference line at y=0
        fig.add_shape(
            type="line", x0=min(diag_data['RunOrder']), x1=max(diag_data['RunOrder']), 
            y0=0, y1=0, line=dict(color="red", dash="dash"),
            row=2, col=1
        )
        
        # 4. Residual Histogram
        fig.add_trace(
            go.Histogram(
                x=diag_data['Std_Residual'],
                nbinsx=10,
                name='Histogram'
            ),
            row=2, col=2
        )
        
        # Add normal distribution curve
        x_norm = np.linspace(min(diag_data['Std_Residual']), max(diag_data['Std_Residual']), 100)
        y_norm = stats.norm.pdf(x_norm, np.mean(diag_data['Std_Residual']), np.std(diag_data['Std_Residual']))
        y_norm = y_norm * (n_runs / max(y_norm) * 0.3)  # Scale to match histogram
        
        fig.add_trace(
            go.Scatter(
                x=x_norm,
                y=y_norm,
                mode='lines',
                line=dict(color="red", width=2),
                name='Normal Curve'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            width=800,
            showlegend=False,
            title_text="Model Diagnostic Plots"
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Fitted Values", row=1, col=1)
        fig.update_yaxes(title_text="Standardized Residuals", row=1, col=1)
        
        fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=2)
        fig.update_yaxes(title_text="Sample Quantiles", row=1, col=2)
        
        fig.update_xaxes(title_text="Run Order", row=2, col=1)
        fig.update_yaxes(title_text="Standardized Residuals", row=2, col=1)
        
        fig.update_xaxes(title_text="Residuals", row=2, col=2)
        fig.update_yaxes(title_text="Frequency", row=2, col=2)
        
        st.plotly_chart(fig)
        
        st.markdown("### Outlier Detection and Treatment")
        st.markdown("""
        **Concept Anchor**: Outliers are observations that deviate significantly from model predictions, potentially indicating experimental issues, transcription errors, or interesting phenomena requiring investigation.

        **Practical Lens**: In fermentation optimization, an outlier detection algorithm flags an observation with high residual, leading to discovery of a contamination event. This finding prompts improved sterility protocols rather than data exclusion, enhancing process robustness.

        **Mathematical Approach**:
        1. **Standardized Residuals**:
           - $r_i = \\frac{e_i}{\\sqrt{MSE}}$
           - Flag if $|r_i| > 3$

        2. **Studentized Residuals**:
           - $t_i = \\frac{e_i}{\\sqrt{MSE(1-h_{ii})}}$
           - Where $h_{ii}$ is the leverage (diagonal of hat matrix $H = X(X^TX)^{-1}X^T$)
           - Flag if $|t_i| > t_{\\alpha/2, n-p-1}$
           - Use Bonferroni correction for multiple testing

        3. **Cook's Distance**:
           - $D_i = \\frac{r_i^2}{p} \\cdot \\frac{h_{ii}}{1-h_{ii}}$
           - Flag if $D_i > F_{0.5, p, n-p}$ or $D_i > 4/n$

        4. **DFFITS**:
           - $DFFITS_i = t_i \\sqrt{\\frac{h_{ii}}{1-h_{ii}}}$
           - Flag if $|DFFITS_i| > 2\\sqrt{\\frac{p}{n}}$
        """)
        
        st.markdown("### Transformation Selection")
        st.markdown("""
        **Concept Anchor**: Response transformations modify the scale of analysis to better meet statistical assumptions, stabilize variance, and improve model fit in nonlinear biological systems.

        **Practical Lens**: In enzyme kinetics studies, a log transformation of product formation rate linearizes the relationship with substrate concentration at low levels, enabling more accurate parameter estimation and mechanistic understanding across concentration ranges.

        **Methodological Approach**:
        1. **Box-Cox Transformation**:
           - $y(\\lambda) = \\begin{cases} 
              \\frac{y^\\lambda - 1}{\\lambda} & \\text{if } \\lambda \\neq 0 \\\\
              \\ln(y) & \\text{if } \\lambda = 0
              \\end{cases}$
           - Maximum likelihood estimation of $\\lambda$
           - Common values: $\\lambda = 1$ (no transformation), $\\lambda = 0.5$ (square root), $\\lambda = 0$ (log), $\\lambda = -1$ (reciprocal)

        2. **Variance-Stabilizing Transformations**:
           - Count data: Square root transformation
           - Proportion data: Arcsine transformation $\\sin^{-1}(\\sqrt{p})$
           - Right-skewed data: Log transformation

        3. **Empirical Approach**:
           - Plot log(standard deviation) vs. log(mean) for groups
           - Slope ≈ 0: No transformation needed
           - Slope ≈ 0.5: Square root transformation
           - Slope ≈ 1: Log transformation
           - Slope ≈ 2: Reciprocal transformation
        """)
        
        # Interactive transformation demo
        st.markdown("#### Interactive Transformation Demo")
        
        # Setup for transformation demo
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Generation Parameters**")
            
            data_pattern = st.selectbox(
                "Data Pattern",
                ["Right-Skewed (Concentration)", "Count Data (Cell Counts)", "Proportion Data (Viability)"]
            )
            
            noise_level = st.slider("Noise Level", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
        
        # Generate data based on selection
        np.random.seed(42)
        n_points = 30
        x = np.linspace(0, 10, n_points)
        
        if data_pattern == "Right-Skewed (Concentration)":
            # Generate exponentially increasing data (e.g., concentration vs. response)
            base_y = np.exp(0.3 * x)
            noise = np.random.lognormal(0, noise_level, n_points)
            y = base_y * noise
            
            suggested_transform = "Log Transformation"
            transform_formula = r"y' = \ln(y)"
            transform_function = np.log
            
        elif data_pattern == "Count Data (Cell Counts)":
            # Generate count data with variance proportional to mean
            base_y = 5 * x + 10
            noise = np.random.poisson(base_y) / base_y
            y = base_y * noise
            
            suggested_transform = "Square Root Transformation"
            transform_formula = r"y' = \sqrt{y}"
            transform_function = np.sqrt
            
        elif data_pattern == "Proportion Data (Viability)":
            # Generate proportion data (bounded between 0 and 1)
            base_y = 1 / (1 + np.exp(-0.5 * (x - 5)))  # Logistic function
            noise = np.random.normal(1, noise_level, n_points)
            y = np.clip(base_y * noise, 0.01, 0.99)  # Ensure within (0,1)
            
            suggested_transform = "Arcsin-Square-Root Transformation"
            transform_formula = r"y' = \sin^{-1}(\sqrt{y})"
            transform_function = lambda y: np.arcsin(np.sqrt(y))
        
        # Apply transformation
        y_transformed = transform_function(y)
        
        # Fit models to original and transformed data
        model_orig = ols('y ~ x', data=pd.DataFrame({'x': x, 'y': y})).fit()
        model_trans = ols('y ~ x', data=pd.DataFrame({'x': x, 'y': y_transformed})).fit()
        
        # Calculate residuals
        residuals_orig = model_orig.resid
        residuals_trans = model_trans.resid
        
        # Check normality
        shapiro_orig = stats.shapiro(residuals_orig)
        shapiro_trans = stats.shapiro(residuals_trans)
        
        # Check homoscedasticity (simple test using correlation between abs residuals and fitted)
        homo_test_orig = stats.pearsonr(np.abs(residuals_orig), model_orig.fittedvalues)[0]
        homo_test_trans = stats.pearsonr(np.abs(residuals_trans), model_trans.fittedvalues)[0]
        
        with col2:
            st.markdown("**Transformation Diagnostics**")
            
            st.markdown(f"""
            **Suggested Transformation**: {suggested_transform}
            
            **Formula**: ${transform_formula}$
            
            **Normality Test (Shapiro-Wilk):**
            - Original data: p = {shapiro_orig[1]:.4f} {"✓" if shapiro_orig[1] > 0.05 else "✗"}
            - Transformed data: p = {shapiro_trans[1]:.4f} {"✓" if shapiro_trans[1] > 0.05 else "✗"}
            
            **Homoscedasticity (Residual-Fitted Correlation):**
            - Original data: r = {homo_test_orig:.4f} {"✓" if abs(homo_test_orig) < 0.3 else "✗"}
            - Transformed data: r = {homo_test_trans:.4f} {"✓" if abs(homo_test_trans) < 0.3 else "✗"}
            """)
        
        # Create visualization of transformation
        fig = make_subplots(rows=2, cols=2, 
                           subplot_titles=["Original Data", "Transformed Data", 
                                         "Original Residuals", "Transformed Residuals"])
        
        # Original data plot
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='markers',
                marker=dict(size=8, color='blue'),
                name='Original Data'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=x,
                y=model_orig.fittedvalues,
                mode='lines',
                line=dict(color='red', width=2),
                name='Model Fit'
            ),
            row=1, col=1
        )
        
        # Transformed data plot
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y_transformed,
                mode='markers',
                marker=dict(size=8, color='green'),
                name='Transformed Data'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=x,
                y=model_trans.fittedvalues,
                mode='lines',
                line=dict(color='red', width=2),
                name='Model Fit'
            ),
            row=1, col=2
        )
        
        # Original residuals plot
        fig.add_trace(
            go.Scatter(
                x=model_orig.fittedvalues,
                y=residuals_orig,
                mode='markers',
                marker=dict(size=8, color='blue'),
                name='Original Residuals'
            ),
            row=2, col=1
        )
        
        # Add reference line at y=0
        fig.add_shape(
            type="line", x0=min(model_orig.fittedvalues), x1=max(model_orig.fittedvalues), 
            y0=0, y1=0, line=dict(color="red", dash="dash"),
            row=2, col=1
        )
        
        # Transformed residuals plot
        fig.add_trace(
            go.Scatter(
                x=model_trans.fittedvalues,
                y=residuals_trans,
                mode='markers',
                marker=dict(size=8, color='green'),
                name='Transformed Residuals'
            ),
            row=2, col=2
        )
        
        # Add reference line at y=0
        fig.add_shape(
            type="line", x0=min(model_trans.fittedvalues), x1=max(model_trans.fittedvalues), 
            y0=0, y1=0, line=dict(color="red", dash="dash"),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            width=800,
            showlegend=False,
            title_text=f"Effect of {suggested_transform}"
        )
        
        st.plotly_chart(fig)
        
        st.markdown(f"""
        **Interpretation:**
        
        The {suggested_transform.lower()} is {"effective" if shapiro_trans[1] > shapiro_orig[1] and abs(homo_test_trans) < abs(homo_test_orig) else "partly effective" if shapiro_trans[1] > shapiro_orig[1] or abs(homo_test_trans) < abs(homo_test_orig) else "not effective"} for this data:
        
        - **Normality**: The transformation {"improves" if shapiro_trans[1] > shapiro_orig[1] else "does not improve"} the normality of residuals.
        - **Homoscedasticity**: The transformation {"improves" if abs(homo_test_trans) < abs(homo_test_orig) else "does not improve"} the variance stability.
        
        In biotechnology applications, appropriate transformations can significantly improve model validity and predictive power, especially with biological data that often exhibit non-normal distributions and heterogeneous variance.
        """)
    
    # Tab 4: Response Surface Methods
    with tabs[3]:
        st.subheader("Response Surface Methods")
        
        st.markdown("""
        ### Quadratic Model Fitting
        **Concept Anchor**: Quadratic models extend linear models by incorporating squared terms, enabling the detection of curvature and optimal regions in the experimental space.

        **Practical Lens**: In chromatography optimization, a quadratic model of protein binding capacity as a function of pH and salt concentration reveals a clear optimum at pH 7.2 and 150 mM NaCl, with significant curvature that would be missed by linear models.

        **Mathematical Foundation**:
        The full quadratic model for k factors is:

        $y = \\beta_0 + \\sum_{i=1}^{k} \\beta_i x_i + \\sum_{i=1}^{k} \\beta_{ii} x_i^2 + \\sum_{i<j}^{k} \\beta_{ij} x_i x_j + \\varepsilon$

        The fitted model provides predictions:

        $\\hat{y} = \\hat{\\beta}_0 + \\sum_{i=1}^{k} \\hat{\\beta}_i x_i + \\sum_{i=1}^{k} \\hat{\\beta}_{ii} x_i^2 + \\sum_{i<j}^{k} \\hat{\\beta}_{ij} x_i x_j$

        Model quality is assessed via:
        - $R^2 = 1 - \\frac{SS_{Error}}{SS_{Total}}$
        - Adjusted $R^2 = 1 - \\frac{SS_{Error}/df_{Error}}{SS_{Total}/df_{Total}}$
        - Predicted $R^2 = 1 - \\frac{PRESS}{SS_{Total}}$ where $PRESS = \\sum_{i=1}^{n} \\left(\\frac{e_i}{1-h_{ii}}\\right)^2$
        """)
        
        st.markdown("### Response Surface Visualization")
        st.markdown("""
        **Concept Anchor**: Surface plots, contour plots, and interaction plots visually communicate complex relationships between factors and responses, making statistical findings accessible and actionable.

        **Practical Lens**: In vaccine formulation studies, contour plots of antigen stability across temperature and pH reveal a stability window between pH 6.5-7.2 and 2-8°C, providing clear parameters for formulation development and storage conditions.

        **Visualization Approaches**:
        1. **Contour Plots**:
           - Display lines of constant response across two factors
           - Enable identification of optimal regions
           - Mathematical representation: Lines where $\\hat{y}(x_1, x_2) = c$ for various values of $c$

        2. **Surface Plots**:
           - 3D representation of predicted response across two factors
           - Provide intuitive visualization of response curvature
           - Mathematical representation: Surface defined by $z = \\hat{y}(x_1, x_2)$

        3. **Interaction Plots**:
           - Display predicted response for one factor at different levels of another
           - Reveal presence and nature of interactions
           - Non-parallel lines indicate interaction

        4. **Sweet Spot Plots**:
           - Overlay multiple contour plots for different responses
           - Identify regions satisfying multiple criteria
           - Define operability region where all responses meet specifications
        """)
        
        # Interactive response surface demo
        st.markdown("#### Interactive Response Surface Visualization")
        
        # Setup for response surface demo
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Response Surface Parameters**")
            
            # Model coefficients
            b0 = st.slider("Intercept (β₀)", min_value=40.0, max_value=60.0, value=50.0, step=1.0)
            b1 = st.slider("Linear x₁ (β₁)", min_value=-10.0, max_value=10.0, value=5.0, step=0.5)
            b2 = st.slider("Linear x₂ (β₂)", min_value=-10.0, max_value=10.0, value=-3.0, step=0.5)
            b11 = st.slider("Quadratic x₁² (β₁₁)", min_value=-10.0, max_value=10.0, value=-4.0, step=0.5)
            b22 = st.slider("Quadratic x₂² (β₂₂)", min_value=-10.0, max_value=10.0, value=-6.0, step=0.5)
            b12 = st.slider("Interaction x₁x₂ (β₁₂)", min_value=-10.0, max_value=10.0, value=2.0, step=0.5)
            
            plot_type = st.radio("Plot Type", ["Contour Plot", "3D Surface Plot", "Both"])
        
        # Generate grid for response surface
        x1 = np.linspace(-1, 1, 30)
        x2 = np.linspace(-1, 1, 30)
        x1_grid, x2_grid = np.meshgrid(x1, x2)
        
        # Calculate response using quadratic model
        z_grid = b0 + b1*x1_grid + b2*x2_grid + b11*(x1_grid**2) + b22*(x2_grid**2) + b12*x1_grid*x2_grid
        
        # Calculate stationary point
        # For a quadratic model, the stationary point is where the partial derivatives are zero
        # ∂y/∂x₁ = β₁ + 2β₁₁x₁ + β₁₂x₂ = 0
        # ∂y/∂x₂ = β₂ + 2β₂₂x₂ + β₁₂x₁ = 0
        
        # Set up system of equations
        B = np.array([[2*b11, b12], [b12, 2*b22]])
        b = np.array([-b1, -b2])
        
        try:
            # Solve for stationary point
            xs = np.linalg.solve(B, b)
            x1s, x2s = xs[0], xs[1]
            
            # Check if stationary point is within region
            stationary_in_region = (abs(x1s) <= 1.0) and (abs(x2s) <= 1.0)
            
            # Calculate response at stationary point
            ys = b0 + b1*x1s + b2*x2s + b11*(x1s**2) + b22*(x2s**2) + b12*x1s*x2s
            
            # Determine nature of stationary point from eigenvalues
            eigenvalues = np.linalg.eigvals(B)
            
            if all(eigenvalues > 0):
                point_type = "Minimum"
            elif all(eigenvalues < 0):
                point_type = "Maximum"
            else:
                point_type = "Saddle Point"
        
        except np.linalg.LinAlgError:
            # Handle case where B is singular
            stationary_in_region = False
            point_type = "Ridge System"
            x1s, x2s, ys = 0, 0, 0
        
        with col2:
            st.markdown("**Response Surface Visualization**")
            
            if plot_type in ["Contour Plot", "Both"]:
                # Create contour plot
                fig_contour = go.Figure(data=
                    go.Contour(
                        z=z_grid,
                        x=x1, 
                        y=x2,
                        colorscale='Viridis',
                        contours=dict(
                            showlabels=True,
                            labelfont=dict(size=12, color='white')
                        )
                    )
                )
                
                # Add stationary point if in region
                if stationary_in_region:
                    fig_contour.add_trace(
                        go.Scatter(
                            x=[x1s],
                            y=[x2s],
                            mode='markers',
                            marker=dict(size=12, color='red', symbol='star'),
                            name=f'{point_type} ({x1s:.2f}, {x2s:.2f})'
                        )
                    )
                
                # Update layout
                fig_contour.update_layout(
                    title=f"Contour Plot",
                    xaxis_title="Factor x₁",
                    yaxis_title="Factor x₂",
                    height=400
                )
                
                st.plotly_chart(fig_contour)
            
            if plot_type in ["3D Surface Plot", "Both"]:
                # Create 3D surface plot
                fig_surface = go.Figure(data=
                    go.Surface(
                        z=z_grid,
                        x=x1,
                        y=x2,
                        colorscale='Viridis'
                    )
                )
                
                # Add stationary point if in region
                if stationary_in_region:
                    fig_surface.add_trace(
                        go.Scatter3d(
                            x=[x1s],
                            y=[x2s],
                            z=[ys],
                            mode='markers',
                            marker=dict(size=6, color='red', symbol='circle'),
                            name=f'{point_type} ({x1s:.2f}, {x2s:.2f}, {ys:.2f})'
                        )
                    )
                
                # Update layout
                fig_surface.update_layout(
                    title=f"3D Surface Plot",
                    scene=dict(
                        xaxis_title="Factor x₁",
                        yaxis_title="Factor x₂",
                        zaxis_title="Response"
                    ),
                    height=500,
                    width=600
                )
                
                st.plotly_chart(fig_surface)
            
            # Show canonical analysis results
            st.markdown("**Canonical Analysis**")
            
            if point_type != "Ridge System":
                st.markdown(f"""
                **Stationary Point:** ({x1s:.4f}, {x2s:.4f})
                
                **Response at Stationary Point:** {ys:.4f}
                
                **Point Type:** {point_type}
                
                **Eigenvalues:** {eigenvalues[0]:.4f}, {eigenvalues[1]:.4f}
                
                **Location:** {"Within experimental region" if stationary_in_region else "Outside experimental region"}
                """)
            else:
                st.markdown("""
                **Ridge System Detected**
                
                The quadratic surface has a ridge or valley rather than a distinct optimum.
                This occurs when at least one eigenvalue is near zero, indicating that the 
                response changes very little in certain directions.
                """)
        
        st.markdown("""
        **Interpretation:**
        
        The response surface visualizations help identify optimal operating conditions and understand how factors interact to affect the response. In biotechnology, these tools are invaluable for process optimization, such as:
        
        - Finding optimal culture conditions for cell growth or protein expression
        - Identifying robust operating windows for bioreactor parameters
        - Determining optimal buffer compositions for protein purification
        - Characterizing the design space for regulatory submissions
        """)
        
        st.markdown("### Canonical Analysis")
        st.markdown("""
        **Concept Anchor**: Canonical analysis identifies the stationary point and nature of the response surface through eigenvalue analysis, providing a mathematical characterization of optimal regions.

        **Practical Lens**: In biocatalytic reaction optimization, canonical analysis reveals a saddle point at medium temperature and pH, indicating that optimization should proceed by moving away from this point along the principal axes toward the true maximum.

        **Mathematical Foundation**:
        For a quadratic model in k factors, the canonical form is:

        $y = \\hat{\\beta}_0 + \\sum_{i=1}^{k} \\lambda_i w_i^2$

        Where:
        - $w_i$ are the canonical variables (linear combinations of original factors)
        - $\\lambda_i$ are eigenvalues of the matrix $\\mathbf{B}$ of quadratic coefficients

        The stationary point $\\mathbf{x_s}$ is calculated as:

        $\\mathbf{x_s} = -\\frac{1}{2}\\mathbf{B}^{-1}\\mathbf{b}$

        Where:
        - $\\mathbf{B}$ is the matrix of second-order coefficients $\\beta_{ij}$
        - $\\mathbf{b}$ is the vector of first-order coefficients $\\beta_i$

        The nature of the stationary point depends on eigenvalues:
        - All $\\lambda_i < 0$: Maximum
        - All $\\lambda_i > 0$: Minimum
        - Mixed signs: Saddle point
        - Some $\\lambda_i = 0$: Ridge system
        """)
        
        st.markdown("### Optimization Methods")
        st.markdown("""
        **Concept Anchor**: Numerical optimization methods identify factor settings that maximize, minimize, or target specific response values, potentially with multiple constraints representing process requirements.

        **Practical Lens**: In cell culture media optimization, numerical methods identify the combination of 15 amino acids and vitamins that maximizes cell density and protein titer while maintaining acceptable osmolarity and cost constraints, directly informing manufacturing formulations.

        **Methodological Approaches**:
        1. **Desirability Functions**:
           - Individual desirability functions $d_i(y_i)$ for each response
           - Overall desirability $D = (d_1 \\times d_2 \\times ... \\times d_m)^{1/m}$
           - Maximize $D$ across factor space
           - Functional forms:
             * Target: $d_i(y_i) = \\begin{cases} 
               \\left(\\frac{y_i-L}{T-L}\\right)^s & L \\leq y_i \\leq T \\\\
               \\left(\\frac{U-y_i}{U-T}\\right)^t & T \\leq y_i \\leq U \\\\
               0 & \\text{otherwise}
               \\end{cases}$
             * Maximize: $d_i(y_i) = \\begin{cases} 
               0 & y_i < L \\\\
               \\left(\\frac{y_i-L}{T-L}\\right)^s & L \\leq y_i \\leq T \\\\
               1 & y_i > T
               \\end{cases}$
             * Minimize: $d_i(y_i) = \\begin{cases} 
               1 & y_i < T \\\\
               \\left(\\frac{U-y_i}{U-T}\\right)^t & T \\leq y_i \\leq U \\\\
               0 & y_i > U
               \\end{cases}$

        2. **Direct Search Methods**:
           - Simplex methods for constrained optimization
           - Gradient-based methods (steepest ascent/descent)
           - Grid search for complex response surfaces
           - Genetic algorithms for multi-modal surfaces

        3. **Multiple Response Optimization**:
           - Overlay plots for visual optimization
           - Constrained optimization with primary and secondary responses
           - Pareto-optimal solutions for competing objectives
        """)
        
        # Interactive optimization demo
        st.markdown("#### Interactive Multi-Response Optimization")
        
        # Setup for optimization demo
        st.markdown("""
        This demo simulates optimizing a bioprocess with two responses: Protein Yield and Purity.
        The goal is to maximize both responses while staying within operating constraints.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Response Models & Constraints**")
            
            # Optimization objectives
            st.markdown("**Optimization Objectives:**")
            yield_importance = st.slider("Protein Yield Importance", min_value=1, max_value=5, value=3, step=1)
            purity_importance = st.slider("Purity Importance", min_value=1, max_value=5, value=3, step=1)
            
            # Constraints
            st.markdown("**Factor Constraints:**")
            temp_range = st.slider("Temperature Range (°C)", min_value=25.0, max_value=40.0, value=(28.0, 37.0), step=0.5)
            ph_range = st.slider("pH Range", min_value=5.0, max_value=8.0, value=(6.0, 7.5), step=0.1)
            
            # Response constraints
            st.markdown("**Response Constraints:**")
            min_yield = st.slider("Minimum Yield (g/L)", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
            min_purity = st.slider("Minimum Purity (%)", min_value=75.0, max_value=99.0, value=90.0, step=0.5)
        
        # Define response models (simulated quadratic models)
        def yield_model(temp, ph):
            # Simulated model for protein yield
            # Maximum around temp=32, pH=6.8
            return 3.5 - 0.25*(temp-32)**2 - 0.5*(ph-6.8)**2 + 0.1*(temp-32)*(ph-6.8)
        
        def purity_model(temp, ph):
            # Simulated model for protein purity
            # Maximum around temp=30, pH=7.2
            return 95 - 0.2*(temp-30)**2 - 0.3*(ph-7.2)**2 - 0.1*(temp-30)*(ph-7.2)
        
        # Generate grid for surface
        temps = np.linspace(temp_range[0], temp_range[1], 50)
        phs = np.linspace(ph_range[0], ph_range[1], 50)
        temp_grid, ph_grid = np.meshgrid(temps, phs)
        
        # Calculate responses over grid
        yield_grid = np.zeros_like(temp_grid)
        purity_grid = np.zeros_like(temp_grid)
        desirability_grid = np.zeros_like(temp_grid)
        
        for i in range(temp_grid.shape[0]):
            for j in range(temp_grid.shape[1]):
                temp = temp_grid[i, j]
                ph = ph_grid[i, j]
                
                # Calculate model predictions
                yield_pred = yield_model(temp, ph)
                purity_pred = purity_model(temp, ph)
                
                yield_grid[i, j] = yield_pred
                purity_grid[i, j] = purity_pred
                
                # Calculate individual desirabilities
                # Yield desirability (maximize)
                if yield_pred < min_yield:
                    d_yield = 0
                else:
                    d_yield = min(1, (yield_pred - min_yield) / (5.0 - min_yield))
                
                # Purity desirability (maximize)
                if purity_pred < min_purity:
                    d_purity = 0
                else:
                    d_purity = min(1, (purity_pred - min_purity) / (100.0 - min_purity))
                
                # Overall desirability with importance weights
                weight_sum = yield_importance + purity_importance
                if d_yield > 0 and d_purity > 0:
                    desirability_grid[i, j] = (d_yield**(yield_importance/weight_sum)) * (d_purity**(purity_importance/weight_sum))
                else:
                    desirability_grid[i, j] = 0
        
        # Find optimal point
        optimal_idx = np.unravel_index(np.argmax(desirability_grid), desirability_grid.shape)
        optimal_temp = temp_grid[optimal_idx]
        optimal_ph = ph_grid[optimal_idx]
        optimal_yield = yield_grid[optimal_idx]
        optimal_purity = purity_grid[optimal_idx]
        optimal_desirability = desirability_grid[optimal_idx]
        
        with col2:
            st.markdown("**Optimization Results**")
            
            # Create contour plot showing desirability
            fig = go.Figure()
            
            # Add desirability contour
            fig.add_trace(
                go.Contour(
                    z=desirability_grid,
                    x=temps,
                    y=phs,
                    colorscale='Viridis',
                    contours=dict(
                        showlabels=True,
                        labelfont=dict(size=12, color='white')
                    ),
                    colorbar=dict(title="Desirability"),
                    name="Desirability"
                )
            )
            
            # Add constraint boundaries for yield
            yield_contour_levels = [min_yield]
            fig.add_trace(
                go.Contour(
                    z=yield_grid,
                    x=temps,
                    y=phs,
                    contours=dict(
                        coloring='lines',
                        showlabels=False,
                        start=min_yield,
                        end=min_yield,
                        size=0
                    ),
                    line=dict(color='red', width=2),
                    showscale=False,
                    name=f"Min Yield ({min_yield} g/L)"
                )
            )
            
            # Add constraint boundaries for purity
            purity_contour_levels = [min_purity]
            fig.add_trace(
                go.Contour(
                    z=purity_grid,
                    x=temps,
                    y=phs,
                    contours=dict(
                        coloring='lines',
                        showlabels=False,
                        start=min_purity,
                        end=min_purity,
                        size=0
                    ),
                    line=dict(color='blue', width=2),
                    showscale=False,
                    name=f"Min Purity ({min_purity}%)"
                )
            )
            
            # Add optimal point
            fig.add_trace(
                go.Scatter(
                    x=[optimal_temp],
                    y=[optimal_ph],
                    mode='markers',
                    marker=dict(size=12, color='red', symbol='star'),
                    name='Optimal Point'
                )
            )
            
            # Update layout
            fig.update_layout(
                title="Multi-Response Optimization",
                xaxis_title="Temperature (°C)",
                yaxis_title="pH",
                height=450
            )
            
            st.plotly_chart(fig)
            
            st.markdown(f"""
            **Optimal Conditions:**
            - Temperature: {optimal_temp:.2f}°C
            - pH: {optimal_ph:.2f}
            
            **Predicted Responses:**
            - Protein Yield: {optimal_yield:.2f} g/L
            - Purity: {optimal_purity:.2f}%
            - Overall Desirability: {optimal_desirability:.4f}
            
            **Interpretation:**
            The contour plot shows the desirability function across the experimental space. The red and blue lines represent the minimum yield and purity constraints, respectively. The optimal point (red star) represents the best compromise between the two responses based on their relative importance.
            """)
        
        st.markdown("""
        In biotechnology, multi-response optimization is essential for processes with multiple quality attributes. For example:
        
        - Cell culture optimization balancing cell density, viability, and product titer
        - Purification processes maximizing yield while ensuring high purity
        - Formulation development optimizing stability, viscosity, and osmolality
        
        The desirability approach provides a systematic way to balance competing objectives and identify operating conditions that satisfy all critical requirements.
        """)
    
    # Tab 5: Design Space Characterization
    with tabs[4]:
        st.subheader("Design Space Characterization")
        
        st.markdown("""
        ### Prediction Uncertainty
        **Concept Anchor**: Prediction uncertainty quantifies variability in model predictions across the design space, enabling risk-based decisions and identifying regions of high confidence.

        **Practical Lens**: In bioprocess characterization, prediction variance maps highlight increased uncertainty at extreme temperature conditions, guiding more conservative operating limits in these regions to ensure consistent product quality.

        **Mathematical Foundation**:
        For a linear model, the variance of prediction at a point $\\mathbf{x_0}$ is:

        $\\text{Var}(\\hat{y}(\\mathbf{x_0})) = \\sigma^2 \\mathbf{x_0^T}(\\mathbf{X^TX})^{-1}\\mathbf{x_0}$

        The prediction interval at confidence level $1-\\alpha$ is:

        $\\hat{y}(\\mathbf{x_0}) \\pm t_{\\alpha/2, n-p} \\sqrt{\\text{Var}(\\hat{y}(\\mathbf{x_0}))}$

        For multivariate prediction, the confidence region is an ellipsoid:

        $(\\mathbf{X\\hat{\\beta}} - \\mathbf{X\\beta})^T(\\mathbf{X^TX})(\\mathbf{X\\hat{\\beta}} - \\mathbf{X\\beta}) \\leq ps^2F_{\\alpha, p, n-p}$

        Where:
        - $s^2$ is the estimate of $\\sigma^2$
        - $p$ is the number of parameters
        - $n$ is the number of observations
        """)
        
        # Interactive prediction uncertainty demo
        st.markdown("#### Interactive Prediction Uncertainty Visualization")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Experiment Design Parameters**")
            
            design_type = st.selectbox(
                "Design Type",
                ["Factorial (2²)", "Central Composite", "D-Optimal"]
            )
            
            noise_level = st.slider("Error Standard Deviation", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
            
            confidence_level = st.slider("Confidence Level (%)", min_value=90, max_value=99, value=95, step=1)
        
        # Generate design points based on selection
        if design_type == "Factorial (2²)":
            # 2² factorial with center point
            design_points = np.array([
                [-1, -1], [-1, 1], [1, -1], [1, 1], [0, 0]
            ])
            design_name = "2² Factorial with Center Point"
            
        elif design_type == "Central Composite":
            # Central composite design
            alpha = 1.414  # Rotatable design
            design_points = np.array([
                [-1, -1], [-1, 1], [1, -1], [1, 1],  # Factorial points
                [-alpha, 0], [alpha, 0], [0, -alpha], [0, alpha],  # Axial points
                [0, 0], [0, 0]  # Center points (replicated)
            ])
            design_name = "Central Composite Design"
            
        else:  # D-Optimal
            # Simulated D-optimal design for constrained space
            design_points = np.array([
                [-1, -0.8], [-0.6, 0.9], [0.2, 1], [1, 0.5], [1, -0.6],
                [0.6, -1], [-0.3, -1], [-0.7, 0.2], [0.5, 0.1], [0, 0]
            ])
            design_name = "D-Optimal Design"
        
        # True model for simulation
        def true_model(x1, x2):
            return 50 + 5*x1 - 3*x2 + 2*x1*x2 - 2*x1**2 - 1*x2**2
        
        # Generate response data
        np.random.seed(42)
        y = np.array([true_model(x[0], x[1]) for x in design_points]) + np.random.normal(0, noise_level, len(design_points))
        
        # Create dataframe for modeling
        design_df = pd.DataFrame({
            'x1': design_points[:, 0],
            'x2': design_points[:, 1],
            'y': y
        })
        
        # Fit quadratic model
        model_formula = "y ~ x1 + x2 + I(x1**2) + I(x2**2) + x1:x2"
        uncertainty_model = ols(model_formula, data=design_df).fit()
        
        # Create grid for prediction
        x1_grid = np.linspace(-1.5, 1.5, 50)
        x2_grid = np.linspace(-1.5, 1.5, 50)
        xx1, xx2 = np.meshgrid(x1_grid, x2_grid)
        
        # Create prediction data
        grid_points = np.column_stack([xx1.ravel(), xx2.ravel()])
        pred_df = pd.DataFrame({
            'x1': grid_points[:, 0],
            'x2': grid_points[:, 1]
        })
        
        # Add model terms
        pred_df['x1:x2'] = pred_df['x1'] * pred_df['x2']
        pred_df['I(x1**2)'] = pred_df['x1']**2
        pred_df['I(x2**2)'] = pred_df['x2']**2
        
        # Make predictions
        X_pred = sm.add_constant(pred_df)
        predictions = uncertainty_model.predict(X_pred)
        
        # Calculate prediction variance
        X_design = sm.add_constant(design_df[['x1', 'x2', 'x1:x2', 'I(x1**2)', 'I(x2**2)']])
        MSE = np.sum(uncertainty_model.resid**2) / (len(y) - len(uncertainty_model.params))
        
        # Calculate prediction variance for each point
        prediction_var = np.zeros(len(pred_df))
        
        for i in range(len(pred_df)):
            x_i = X_pred.iloc[i].values.reshape(-1, 1)
            prediction_var[i] = MSE * np.sum((x_i.T @ np.linalg.pinv(X_design.T @ X_design) @ x_i))
        
        # Calculate margin of error for prediction intervals
        alpha = 1 - confidence_level/100
        t_crit = stats.t.ppf(1-alpha/2, df=len(y)-len(uncertainty_model.params))
        margin_of_error = t_crit * np.sqrt(prediction_var)
        
        # Reshape for plotting
        z_pred = predictions.values.reshape(xx1.shape)
        z_var = prediction_var.reshape(xx1.shape)
        z_margin = margin_of_error.reshape(xx1.shape)
        
        with col2:
            st.markdown("**Prediction Uncertainty Map**")
            
            # Create visualization
            fig = make_subplots(rows=1, cols=2, 
                              subplot_titles=["Predicted Response", "Prediction Standard Error"])
            
            # Predicted response contour
            fig.add_trace(
                go.Contour(
                    z=z_pred,
                    x=x1_grid,
                    y=x2_grid,
                    colorscale='Viridis',
                    contours=dict(showlabels=True),
                    colorbar=dict(title="Response", x=0.46),
                    showscale=True
                ),
                row=1, col=1
            )
            
            # Add design points
            fig.add_trace(
                go.Scatter(
                    x=design_points[:, 0],
                    y=design_points[:, 1],
                    mode='markers',
                    marker=dict(size=10, color='red', line=dict(width=1, color='black')),
                    name='Design Points'
                ),
                row=1, col=1
            )
            
            # Prediction standard error contour
            fig.add_trace(
                go.Contour(
                    z=np.sqrt(z_var),
                    x=x1_grid,
                    y=x2_grid,
                    colorscale='Reds',
                    contours=dict(showlabels=True),
                    colorbar=dict(title="Std Error", x=1.0),
                    showscale=True
                ),
                row=1, col=2
            )
            
            # Add design points to second plot
            fig.add_trace(
                go.Scatter(
                    x=design_points[:, 0],
                    y=design_points[:, 1],
                    mode='markers',
                    marker=dict(size=10, color='blue', line=dict(width=1, color='black')),
                    name='Design Points',
                    showlegend=False
                ),
                row=1, col=2
            )
            
            # Update layout
            fig.update_layout(
                height=450,
                title_text=f"Prediction Maps for {design_name}",
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Factor x₁", row=1, col=1)
            fig.update_yaxes(title_text="Factor x₂", row=1, col=1)
            
            fig.update_xaxes(title_text="Factor x₁", row=1, col=2)
            fig.update_yaxes(title_text="Factor x₂", row=1, col=2)
            
            st.plotly_chart(fig)
            
            # Create a plot showing prediction intervals at a slice
            x1_slice = 0  # Slice at x1 = 0
            slice_indices = np.where(np.isclose(xx1, x1_slice, atol=x1_grid[1]-x1_grid[0]))[0]
            
            if len(slice_indices) > 0:
                # Extract slice data
                x2_slice = xx2[0, slice_indices]
                y_pred_slice = z_pred[0, slice_indices]
                margin_slice = z_margin[0, slice_indices]
                
                # Create prediction interval plot
                fig_interval = go.Figure()
                
                # Add predicted line
                fig_interval.add_trace(
                    go.Scatter(
                        x=x2_slice,
                        y=y_pred_slice,
                        mode='lines',
                        line=dict(color='blue', width=2),
                        name='Predicted Response'
                    )
                )
                
                # Add upper prediction interval
                fig_interval.add_trace(
                    go.Scatter(
                        x=x2_slice,
                        y=y_pred_slice + margin_slice,
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False
                    )
                )
                
                # Add lower prediction interval with fill between
                fig_interval.add_trace(
                    go.Scatter(
                        x=x2_slice,
                        y=y_pred_slice - margin_slice,
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(0, 0, 255, 0.2)',
                        name=f'{confidence_level}% Prediction Interval'
                    )
                )
                
                # Update layout
                fig_interval.update_layout(
                    title=f"Prediction Interval at x₁ = {x1_slice}",
                    xaxis_title="Factor x₂",
                    yaxis_title="Predicted Response",
                    height=300
                )
                
                st.plotly_chart(fig_interval)
            
            st.markdown(f"""
            **Interpretation:**
            
            - The left plot shows the predicted response across the factor space.
            - The right plot shows the standard error of prediction, which increases with distance from design points.
            - The prediction interval plot shows the uncertainty in predictions at x₁ = 0 across different values of x₂.
            
            In bioprocess development, understanding prediction uncertainty is crucial for defining robust operating ranges. Regions with high uncertainty may require additional experimentation or more conservative control strategies to ensure consistent product quality.
            """)
        
        st.markdown("### Design Space Mapping")
        st.markdown("""
        **Concept Anchor**: Design space mapping integrates model predictions, uncertainty, and process requirements to define the multidimensional combination of variables that ensures quality, supporting regulatory submissions and operational flexibility.

        **Practical Lens**: For a monoclonal antibody process, design space mapping defines the acceptable ranges of pH (6.8-7.2), temperature (33-37°C), and dissolved oxygen (30-60%) where glycosylation patterns meet specifications with 95% confidence, supporting a successful regulatory filing.

        **Methodological Approach**:
        1. **Probability-Based Approach**:
           - For a specification $L \\leq y \\leq U$, calculate:
             $P(L \\leq y \\leq U|\\mathbf{x}) = \\Phi\\left(\\frac{U-\\hat{y}(\\mathbf{x})}{\\hat{\\sigma}_y(\\mathbf{x})}\\right) - \\Phi\\left(\\frac{L-\\hat{y}(\\mathbf{x})}{\\hat{\\sigma}_y(\\mathbf{x})}\\right)$
           - Define design space where $P(L \\leq y \\leq U|\\mathbf{x}) \\geq \\pi$ (e.g., $\\pi = 0.95$)

        2. **Bayesian Credible Regions**:
           - Incorporate prior knowledge about parameters
           - Posterior predictive distribution:
             $p(y|\\mathbf{x}, \\text{data}) = \\int p(y|\\mathbf{x}, \\boldsymbol{\\theta})p(\\boldsymbol{\\theta}|\\text{data})d\\boldsymbol{\\theta}$
           - Credible regions account for parameter uncertainty

        3. **Bootstrap Approach**:
           - Resample residuals to generate multiple response surfaces
           - Calculate probability empirically from bootstrap distribution
           - No distributional assumptions required
        """)
        
        # Interactive design space demo
        st.markdown("#### Interactive Design Space Mapping")
        
        st.markdown("""
        This demo shows how to map the design space for a bioprocess with two quality attributes:
        - Product Titer (yield)
        - Product Quality (measured as % main variant)
        
        The design space is the region where both attributes meet their specifications with the required confidence.
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Design Space Parameters**")
            
            # Quality attribute specifications
            st.markdown("**Quality Attribute Specifications:**")
            titer_spec = st.slider("Minimum Titer (g/L)", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
            quality_spec = st.slider("Minimum Quality (%)", min_value=80.0, max_value=99.0, value=90.0, step=1.0)
            
            # Confidence level
            ds_confidence = st.slider("Required Confidence (%)", min_value=70, max_value=99, value=90, step=1, key="ds_confidence")
            
            # Model uncertainty
            model_uncertainty = st.slider("Model Uncertainty", min_value=1, max_value=10, value=5, step=1)
        
        # Define simulated response models
        def titer_mean_model(temp, ph):
            # Simulated model for product titer
            return 5.0 - 0.3*(temp-33)**2 - 0.2*(ph-7.0)**2 + 0.1*(temp-33)*(ph-7.0)
        
        def quality_mean_model(temp, ph):
            # Simulated model for product quality
            return 95.0 - 0.15*(temp-31)**2 - 0.25*(ph-6.8)**2 - 0.05*(temp-31)*(ph-6.8)
        
        # Define model standard errors
        def titer_se_model(temp, ph, base_se=0.2):
            # Standard error increases with distance from center
            distance = np.sqrt((temp-32)**2 + (ph-7.0)**2)
            return base_se * (1 + 0.1*model_uncertainty*distance)
        
        def quality_se_model(temp, ph, base_se=0.5):
            # Standard error increases with distance from center
            distance = np.sqrt((temp-32)**2 + (ph-7.0)**2)
            return base_se * (1 + 0.1*model_uncertainty*distance)
        
        # Generate grid for visualization
        temps = np.linspace(25, 40, 50)
        phs = np.linspace(6.0, 8.0, 50)
        temp_grid, ph_grid = np.meshgrid(temps, phs)
        
        # Calculate probability of meeting specifications
        titer_prob_grid = np.zeros_like(temp_grid)
        quality_prob_grid = np.zeros_like(temp_grid)
        combined_prob_grid = np.zeros_like(temp_grid)
        
        for i in range(temp_grid.shape[0]):
            for j in range(temp_grid.shape[1]):
                temp = temp_grid[i, j]
                ph = ph_grid[i, j]
                
                # Calculate mean and standard error for each response
                titer_mean = titer_mean_model(temp, ph)
                titer_se = titer_se_model(temp, ph)
                
                quality_mean = quality_mean_model(temp, ph)
                quality_se = quality_se_model(temp, ph)
                
                # Calculate probability of meeting titer spec
                titer_z = (titer_mean - titer_spec) / titer_se
                titer_prob = stats.norm.cdf(titer_z)
                titer_prob_grid[i, j] = titer_prob
                
                # Calculate probability of meeting quality spec
                quality_z = (quality_mean - quality_spec) / quality_se
                quality_prob = stats.norm.cdf(quality_z)
                quality_prob_grid[i, j] = quality_prob
                
                # Combined probability (assuming independence)
                combined_prob_grid[i, j] = titer_prob * quality_prob
        
        # Create binary design space mask
        required_prob = ds_confidence / 100
        design_space_mask = combined_prob_grid >= required_prob
        
        with col2:
            st.markdown("**Design Space Visualization**")
            
            # Create visualization
            fig = make_subplots(rows=1, cols=2, subplot_titles=["Individual Probabilities", "Design Space"])
            
            # Create contour for titer probability
            fig.add_trace(
                go.Contour(
                    z=titer_prob_grid,
                    x=temps,
                    y=phs,
                    colorscale='Blues',
                    contours=dict(
                        start=0.5,
                        end=1,
                        size=0.1,
                        showlabels=True,
                        labelfont=dict(size=10, color='white')
                    ),
                    line=dict(width=0.5),
                    showscale=False,
                    name="Titer Probability"
                ),
                row=1, col=1
            )
            
            # Create contour for quality probability
            fig.add_trace(
                go.Contour(
                    z=quality_prob_grid,
                    x=temps,
                    y=phs,
                    colorscale='Greens',
                    contours=dict(
                        start=0.5,
                        end=1,
                        size=0.1,
                        showlabels=True,
                        labelfont=dict(size=10, color='white')
                    ),
                    line=dict(width=0.5),
                    showscale=False,
                    name="Quality Probability",
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            # Add contour line for required probability (design space boundary)
            fig.add_trace(
                go.Contour(
                    z=combined_prob_grid,
                    x=temps,
                    y=phs,
                    contours=dict(
                        start=required_prob,
                        end=required_prob,
                        coloring='lines',
                        showlabels=False
                    ),
                    line=dict(color='red', width=2),
                    showscale=False,
                    name=f"{ds_confidence}% Confidence Contour"
                ),
                row=1, col=1
            )
            
            # Design space plot (filled contour)
            fig.add_trace(
                go.Contour(
                    z=combined_prob_grid,
                    x=temps,
                    y=phs,
                    contours=dict(
                        start=required_prob,
                        end=1,
                        coloring='fill',
                        showlabels=False
                    ),
                    colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,200,0,0.4)']],
                    showscale=False,
                    name="Design Space"
                ),
                row=1, col=2
            )
            
            # Add contour showing combined probability
            fig.add_trace(
                go.Contour(
                    z=combined_prob_grid,
                    x=temps,
                    y=phs,
                    colorscale='Viridis',
                    contours=dict(
                        start=0.5,
                        end=1,
                        size=0.1,
                        showlabels=True,
                        labelfont=dict(size=10, color='white')
                    ),
                    colorbar=dict(title="Probability"),
                    name="Combined Probability"
                ),
                row=1, col=2
            )
            
            # Add contour line for required probability (design space boundary)
            fig.add_trace(
                go.Contour(
                    z=combined_prob_grid,
                    x=temps,
                    y=phs,
                    contours=dict(
                        start=required_prob,
                        end=required_prob,
                        coloring='lines',
                        showlabels=False
                    ),
                    line=dict(color='red', width=2),
                    showscale=False,
                    name=f"{ds_confidence}% Confidence Boundary"
                ),
                row=1, col=2
            )
            
            # Update layout
            fig.update_layout(
                height=450,
                title_text="Design Space Mapping with Uncertainty",
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1)
            fig.update_yaxes(title_text="pH", row=1, col=1)
            
            fig.update_xaxes(title_text="Temperature (°C)", row=1, col=2)
            fig.update_yaxes(title_text="pH", row=1, col=2)
            
            st.plotly_chart(fig)
            
            # Calculate design space size and characteristics
            if np.any(design_space_mask):
                # Calculate design space area as percentage of total space
                total_area = temp_grid.shape[0] * temp_grid.shape[1]
                design_space_area = np.sum(design_space_mask)
                ds_percentage = (design_space_area / total_area) * 100
                
                # Find design space boundaries
                temp_in_ds = temp_grid[design_space_mask]
                ph_in_ds = ph_grid[design_space_mask]
                
                temp_min, temp_max = np.min(temp_in_ds), np.max(temp_in_ds)
                ph_min, ph_max = np.min(ph_in_ds), np.max(ph_in_ds)
                
                # Calculate robustness as distance from optimal to edge
                combined_prob_in_ds = combined_prob_grid[design_space_mask]
                optimal_idx = np.unravel_index(np.argmax(combined_prob_grid), combined_prob_grid.shape)
                optimal_temp = temp_grid[optimal_idx]
                optimal_ph = ph_grid[optimal_idx]
                
                st.markdown(f"""
                **Design Space Characteristics**:
                
                - **Size**: {ds_percentage:.1f}% of experimental region
                - **Temperature Range**: {temp_min:.1f} to {temp_max:.1f}°C
                - **pH Range**: {ph_min:.1f} to {ph_max:.1f}
                - **Optimal Point**: Temperature = {optimal_temp:.1f}°C, pH = {optimal_ph:.1f}
                - **Confidence Level**: {ds_confidence}%
                
                This design space represents the operating region where there is at least a {ds_confidence}% probability of meeting both the titer specification ({titer_spec} g/L) and the quality specification ({quality_spec}%).
                """)
            else:
                st.warning("""
                No valid design space found with the current specifications and confidence level.
                Consider:
                - Relaxing the specifications
                - Lowering the required confidence level
                - Improving the models to reduce uncertainty
                """)
        
        st.markdown("""
        **Applications in Biotech Regulatory Context:**
        
        Design space mapping is a key element of Quality by Design (QbD) submissions to regulatory agencies. It demonstrates:
        
        1. **Process Understanding**: The relationship between process parameters and quality attributes
        2. **Risk Assessment**: The impact of parameter variability on product quality
        3. **Control Strategy**: The rationale for parameter ranges and control points
        4. **Operational Flexibility**: The ability to operate within a validated space rather than at fixed setpoints
        
        For biopharmaceutical products, well-defined design spaces enable:
        - Faster approval of manufacturing changes
        - Reduced post-approval variation filings
        - More robust manufacturing with consistent product quality
        """)
        
        st.markdown("### Robustness Analysis")
        st.markdown("""
        **Concept Anchor**: Robustness analysis assesses process sensitivity to uncontrolled variations, quantifying the impact of factor perturbations on critical quality attributes and process performance.

        **Practical Lens**: In biopharmaceutical lyophilization, robustness analysis reveals that shelf temperature variations of ±2°C significantly impact product moisture content, leading to tighter equipment qualification requirements and more stringent in-process controls.

        **Methodological Approaches**:
        1. **Sensitivity Analysis**:
           - Partial derivatives: $\\frac{\\partial \\hat{y}}{\\partial x_i}$
           - Normalized sensitivity: $\\frac{x_i}{\\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial x_i}$
           - Tolerance analysis: Impact of factor variation $\\Delta x_i$ on response
             $\\Delta \\hat{y} \\approx \\sum_{i=1}^{k} \\frac{\\partial \\hat{y}}{\\partial x_i} \\Delta x_i$

        2. **Monte Carlo Simulation**:
           - Define probability distributions for factor variations
           - Generate random samples from these distributions
           - Predict responses for each sample
           - Characterize output distribution and failure probability

        3. **Edge of Failure Analysis**:
           - Identify combinations of factors at boundary of acceptable performance
           - Calculate distance to failure from nominal operating point
           - Establish safety margins based on process variability
        """)
    
    # Tab 6: Analysis Workflow
    with tabs[5]:
        doe_analysis_workflow()

def doe_analysis_workflow():
    st.header("DOE Analysis Workflow")
    
    st.markdown("""
    This interactive analysis tool demonstrates the complete workflow for analyzing DOE results
    in biotechnology applications. Work through each step to understand how to extract maximum
    value from your experimental data.
    """)
    
    # Create tabs for different analysis steps
    tabs = st.tabs([
        "1. Data Import & Preparation", 
        "2. Effect Estimation", 
        "3. Significance Testing",
        "4. Model Diagnostics",
        "5. Response Surface Analysis",
        "6. Design Space Mapping"
    ])
    
    # Sample dataset options
    datasets = {
        "Protein Expression Optimization": {
            "description": "A 2³ factorial design studying the effects of Temperature (30°C, 37°C), pH (6.5, 7.5), and Inducer Concentration (0.1, 1.0 mM) on protein expression yield in E. coli.",
            "factors": ["Temperature", "pH", "Inducer"],
            "responses": ["Protein_Yield", "Cell_Density", "Purity"],
            "units": {"Protein_Yield": "mg/L", "Cell_Density": "OD600", "Purity": "%"},
            "design_type": "Full Factorial"
        },
        "Chromatography Optimization": {
            "description": "A central composite design studying the effects of Buffer pH (6.0-8.0), Salt Concentration (0-500 mM), and Load Capacity (5-20 mg/mL) on protein binding and recovery.",
            "factors": ["pH", "Salt", "Load_Capacity"],
            "responses": ["Binding", "Recovery", "Purity"],
            "units": {"Binding": "%", "Recovery": "%", "Purity": "%"},
            "design_type": "Response Surface"
        },
        "Cell Culture Media Optimization": {
            "description": "A fractional factorial design studying the effects of 5 media components on cell growth and protein production in CHO cells.",
            "factors": ["Glucose", "Glutamine", "Serum", "Growth_Factor", "Buffer"],
            "responses": ["Cell_Density", "Viability", "Productivity"],
            "units": {"Cell_Density": "million cells/mL", "Viability": "%", "Productivity": "pg/cell/day"},
            "design_type": "Fractional Factorial"
        }
    }
    
    # Session state to store data and models
    if 'data' not in st.session_state:
        st.session_state.data = None
        st.session_state.selected_dataset = None
        st.session_state.selected_response = None
        st.session_state.model = None
        st.session_state.model_summary = None
        st.session_state.significant_effects = None
    
    # 1. Data Import & Preparation
    with tabs[0]:
        st.subheader("Data Import & Preparation")
        
        st.markdown("""
        Start by importing your experimental data. The data should include columns for:
        - Run order
        - Factor settings (coded or actual)
        - Response measurements
        """)
        
        data_source = st.radio(
            "Select Data Source",
            ["Use Sample Dataset", "Upload Your Own Data"],
            index=0
        )
        
        if data_source == "Use Sample Dataset":
            selected_dataset = st.selectbox(
                "Select Sample Dataset",
                list(datasets.keys()),
                index=0
            )
            
            st.info(datasets[selected_dataset]["description"])
            
            if st.button("Load Sample Dataset") or st.session_state.selected_dataset == selected_dataset:
                st.session_state.selected_dataset = selected_dataset
                
                # Generate data based on selected dataset
                if selected_dataset == "Protein Expression Optimization":
                    # Create 2³ factorial design
                    factors = datasets[selected_dataset]["factors"]
                    runs = 2**len(factors)
                    
                    # Create design matrix in standard order
                    design_matrix = np.zeros((runs, len(factors)))
                    for i in range(runs):
                        for j in range(len(factors)):
                            design_matrix[i, j] = 1 if (i // 2**(len(factors)-j-1)) % 2 else -1
                    
                    # Set up the data
                    data = pd.DataFrame(design_matrix, columns=factors)
                    
                    # Convert coded values to actual
                    data["Temperature"] = data["Temperature"].map({-1: 30, 1: 37})
                    data["pH"] = data["pH"].map({-1: 6.5, 1: 7.5})
                    data["Inducer"] = data["Inducer"].map({-1: 0.1, 1: 1.0})
                    
                    # Generate response data with known effects and some noise
                    # Protein Yield: Positive effects for Temperature, Inducer, and Temp*Inducer interaction
                    base_yield = 500
                    temp_effect = 150
                    ph_effect = -30
                    inducer_effect = 200
                    temp_inducer_effect = 100
                    
                    data["Protein_Yield"] = (base_yield + 
                                           temp_effect * (data["Temperature"] - 33.5) / 3.5 + 
                                           ph_effect * (data["pH"] - 7) / 0.5 + 
                                           inducer_effect * (data["Inducer"] - 0.55) / 0.45 + 
                                           temp_inducer_effect * (data["Temperature"] - 33.5) / 3.5 * (data["Inducer"] - 0.55) / 0.45 + 
                                           np.random.normal(0, 25, runs))
                    
                    # Cell Density: Negative effect of Inducer, Positive effect of pH
                    data["Cell_Density"] = 5.0 + 0.8 * (data["pH"] - 7) / 0.5 - 1.2 * (data["Inducer"] - 0.55) / 0.45 + np.random.normal(0, 0.2, runs)
                    
                    # Purity: Mild effects
                    data["Purity"] = 90 + 3 * (data["Temperature"] - 33.5) / 3.5 + 2 * (data["pH"] - 7) / 0.5 + np.random.normal(0, 1, runs)
                    
                    # Add run order
                    run_order = np.random.permutation(runs) + 1
                    data.insert(0, "RunOrder", run_order)
                    data.insert(1, "StdOrder", range(1, runs + 1))
                    
                    # Add center points
                    center_points = pd.DataFrame({
                        "RunOrder": [runs + i + 1 for i in range(3)],
                        "StdOrder": [runs + i + 1 for i in range(3)],
                        "Temperature": [33.5] * 3,
                        "pH": [7.0] * 3,
                        "Inducer": [0.55] * 3,
                        "Protein_Yield": [base_yield + np.random.normal(0, 20) for _ in range(3)],
                        "Cell_Density": [5.0 + np.random.normal(0, 0.15) for _ in range(3)],
                        "Purity": [90 + np.random.normal(0, 0.8) for _ in range(3)]
                    })
                    
                    data = pd.concat([data, center_points], ignore_index=True)
                    
                elif selected_dataset == "Chromatography Optimization":
                    # Create central composite design
                    # Factorial points
                    factors = ["pH", "Salt", "Load_Capacity"]
                    factorial_points = np.array([
                        [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
                        [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]
                    ])
                    
                    # Axial points
                    alpha = 1.682  # Rotatable design
                    axial_points = np.array([
                        [-alpha, 0, 0], [alpha, 0, 0],
                        [0, -alpha, 0], [0, alpha, 0],
                        [0, 0, -alpha], [0, 0, alpha]
                    ])
                    
                    # Center points
                    center_points = np.array([[0, 0, 0]] * 6)
                    
                    # Combine all points
                    design_matrix = np.vstack([factorial_points, axial_points, center_points])
                    
                    # Create dataframe
                    data = pd.DataFrame(design_matrix, columns=factors)
                    
                    # Convert coded values to actual
                    data["pH"] = 7.0 + data["pH"] * 1.0
                    data["Salt"] = 250 + data["Salt"] * 250
                    data["Load_Capacity"] = 12.5 + data["Load_Capacity"] * 7.5
                    
                    # Generate response data with quadratic effects
                    # Binding: Quadratic effect of pH, negative effect of Salt
                    runs = data.shape[0]
                    
                    # Define coded variables for response generation
                    x1 = (data["pH"] - 7.0) / 1.0
                    x2 = (data["Salt"] - 250) / 250
                    x3 = (data["Load_Capacity"] - 12.5) / 7.5
                    
                    # Binding: Optimal at pH 7.0, decreases with Salt
                    data["Binding"] = 85 - 5 * x2 - 12 * x1**2 - 5 * x2**2 - 3 * x3**2 - 7 * x1 * x2 + np.random.normal(0, 2, runs)
                    
                    # Recovery: Interaction between pH and Load Capacity
                    data["Recovery"] = 90 - 8 * x3 - 4 * x1**2 - 4 * x3**2 + 6 * x1 * x3 + np.random.normal(0, 3, runs)
                    
                    # Purity: Linear effect of Salt, quadratic effect of Load Capacity
                    data["Purity"] = 95 + 3 * x2 - 1.5 * x1 - 5 * x3**2 + np.random.normal(0, 1, runs)
                    
                    # Add run order
                    run_order = np.random.permutation(runs) + 1
                    data.insert(0, "RunOrder", run_order)
                    data.insert(1, "StdOrder", range(1, runs + 1))
                    
                elif selected_dataset == "Cell Culture Media Optimization":
                    # Create fractional factorial design (2^5-1)
                    factors = ["Glucose", "Glutamine", "Serum", "Growth_Factor", "Buffer"]
                    runs = 16  # 2^(5-1)
                    
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
                    
                    # Create dataframe
                    data = pd.DataFrame(design_matrix, columns=factors)
                    
                    # Convert coded values to actual
                    data["Glucose"] = 4.0 + data["Glucose"] * 2.0  # 2.0 to 6.0 g/L
                    data["Glutamine"] = 4.0 + data["Glutamine"] * 2.0  # 2.0 to 6.0 mM
                    data["Serum"] = 5.0 + data["Serum"] * 5.0  # 0 to 10%
                    data["Growth_Factor"] = 5.0 + data["Growth_Factor"] * 5.0  # 0 to 10 ng/mL
                    data["Buffer"] = 20.0 + data["Buffer"] * 10.0  # 10 to 30 mM
                    
                    # Generate response data
                    # Cell Density: Positive effects for Glucose, Glutamine, Serum
                    data["Cell_Density"] = (10.0 + 
                                          2.0 * (data["Glucose"] - 4.0) / 2.0 + 
                                          1.5 * (data["Glutamine"] - 4.0) / 2.0 + 
                                          3.0 * (data["Serum"] - 5.0) / 5.0 +
                                          0.5 * (data["Growth_Factor"] - 5.0) / 5.0 +
                                          1.2 * (data["Glucose"] - 4.0) / 2.0 * (data["Glutamine"] - 4.0) / 2.0 +
                                          np.random.normal(0, 0.5, runs))
                    
                    # Viability: Effects from Serum and Buffer
                    data["Viability"] = (95.0 + 
                                       3.0 * (data["Serum"] - 5.0) / 5.0 - 
                                       1.0 * (data["Buffer"] - 20.0) / 10.0 +
                                       np.random.normal(0, 1.0, runs))
                    
                    # Productivity: Complex interactions
                    data["Productivity"] = (25.0 + 
                                         5.0 * (data["Glucose"] - 4.0) / 2.0 + 
                                         3.0 * (data["Glutamine"] - 4.0) / 2.0 + 
                                         2.0 * (data["Growth_Factor"] - 5.0) / 5.0 -
                                         1.0 * (data["Serum"] - 5.0) / 5.0 * (data["Growth_Factor"] - 5.0) / 5.0 +
                                         np.random.normal(0, 2.0, runs))
                    
                    # Add center points
                    center_points = pd.DataFrame({
                        "RunOrder": [runs + i + 1 for i in range(4)],
                        "StdOrder": [runs + i + 1 for i in range(4)],
                        "Glucose": [4.0] * 4,
                        "Glutamine": [4.0] * 4,
                        "Serum": [5.0] * 4,
                        "Growth_Factor": [5.0] * 4,
                        "Buffer": [20.0] * 4,
                        "Cell_Density": [10.0 + np.random.normal(0, 0.3) for _ in range(4)],
                        "Viability": [95.0 + np.random.normal(0, 0.8) for _ in range(4)],
                        "Productivity": [25.0 + np.random.normal(0, 1.5) for _ in range(4)]
                    })
                    
                    # Add run order
                    run_order = np.random.permutation(runs) + 1
                    data.insert(0, "RunOrder", run_order)
                    data.insert(1, "StdOrder", range(1, runs + 1))
                    
                    data = pd.concat([data, center_points], ignore_index=True)
                
                # Store the generated data
                st.session_state.data = data
                st.success(f"Successfully loaded {selected_dataset} dataset with {len(data)} runs.")
        
        else:
            # File uploader for custom data
            uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
            
            if uploaded_file is not None:
                try:
                    data = pd.read_csv(uploaded_file)
                    st.session_state.data = data
                    st.success(f"Successfully loaded data with {len(data)} rows and {len(data.columns)} columns.")
                except Exception as e:
                    st.error(f"Error loading file: {e}")
        
        # Display the data if available
        if st.session_state.data is not None:
            st.subheader("Experimental Data")
            
            # Allow selecting columns to display
            all_columns = list(st.session_state.data.columns)
            cols_to_display = st.multiselect(
                "Select Columns to Display",
                all_columns,
                default=all_columns[:min(10, len(all_columns))]
            )
            
            if cols_to_display:
                st.dataframe(st.session_state.data[cols_to_display])
            else:
                st.dataframe(st.session_state.data)
            
            # Data summary statistics
            st.subheader("Data Summary")
            
            # Identify factor and response columns
            if st.session_state.selected_dataset:
                factor_cols = datasets[st.session_state.selected_dataset]["factors"]
                response_cols = datasets[st.session_state.selected_dataset]["responses"]
            else:
                # For uploaded data, make a best guess based on column names
                factor_cols = [col for col in all_columns if col not in ["RunOrder", "StdOrder"] 
                              and not any(resp in col.lower() for resp in ["yield", "response", "output", "result"])]
                response_cols = [col for col in all_columns if col not in factor_cols + ["RunOrder", "StdOrder"]]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Factor Summary:**")
                if factor_cols:
                    factor_summary = st.session_state.data[factor_cols].describe().T
                    factor_summary = factor_summary[["count", "mean", "min", "max"]]
                    st.dataframe(factor_summary)
                else:
                    st.info("No factor columns identified.")
            
            with col2:
                st.markdown("**Response Summary:**")
                if response_cols:
                    response_summary = st.session_state.data[response_cols].describe().T
                    response_summary = response_summary[["count", "mean", "std", "min", "max"]]
                    st.dataframe(response_summary)
                else:
                    st.info("No response columns identified.")
            
            # Select primary response for analysis
            st.subheader("Select Primary Response")
            if response_cols:
                selected_response = st.selectbox(
                    "Choose the primary response variable for analysis",
                    response_cols
                )
                st.session_state.selected_response = selected_response
                
                if st.session_state.selected_dataset:
                    response_unit = datasets[st.session_state.selected_dataset]["units"].get(selected_response, "")
                    if response_unit:
                        st.markdown(f"Response unit: **{response_unit}**")
                
                # Basic distribution of the selected response
                fig = px.histogram(
                    st.session_state.data, 
                    x=selected_response,
                    title=f"Distribution of {selected_response}",
                    nbins=12
                )
                st.plotly_chart(fig)
            else:
                st.warning("No response variables identified for analysis.")
    
    # 2. Effect Estimation
    with tabs[1]:
        st.subheader("Effect Estimation")
        
        if st.session_state.data is None or st.session_state.selected_response is None:
            st.warning("Please complete the data import step first.")
        else:
            st.markdown("""
            In this step, we'll estimate the effects of each factor and their interactions
            on the selected response variable.
            """)
            
            # Get data and selected response
            data = st.session_state.data
            response = st.session_state.selected_response
            
            # Determine factors based on dataset or guess from columns
            if st.session_state.selected_dataset:
                factor_cols = datasets[st.session_state.selected_dataset]["factors"]
            else:
                # For uploaded data, make a best guess
                all_columns = list(data.columns)
                factor_cols = [col for col in all_columns if col not in ["RunOrder", "StdOrder"] 
                              and not any(resp in col.lower() for resp in ["yield", "response", "output", "result"])
                              and col != response]
            
            # Create coded variables for analysis
            st.markdown("### Creating Coded Variables")
            st.markdown("""
            For effect estimation, we convert actual factor values to coded levels (-1, 0, +1).
            This makes effects directly comparable across factors with different scales.
            """)
            
            # Function to code a variable to [-1, 1] range
            def code_variable(x):
                x_min, x_max = x.min(), x.max()
                # Check if the variable has only two unique values
                if len(x.unique()) <= 2:
                    return pd.Series(np.where(x == x_min, -1, 1), index=x.index)
                else:
                    # More than two levels - assume continuous
                    return pd.Series(2 * (x - x_min) / (x_max - x_min) - 1, index=x.index)
            
            # Create coded dataframe
            coded_data = data.copy()
            for factor in factor_cols:
                coded_data[f"{factor}_coded"] = code_variable(coded_data[factor])
            
            # Display coded data
            st.markdown("**Sample of Coded Data:**")
            display_cols = ["RunOrder", "StdOrder"] + \
                          [f"{factor}" for factor in factor_cols] + \
                          [f"{factor}_coded" for factor in factor_cols] + \
                          [response]
            st.dataframe(coded_data[display_cols].head(5))
            
            # Create model matrix with main effects and interactions
            st.markdown("### Model Matrix Construction")
            
            # Let user choose which interactions to include
            st.markdown("""
            Select which interaction terms to include in the model.
            For screening designs, main effects might be sufficient.
            For characterization, include two-factor interactions.
            """)
            
            include_2fi = st.checkbox("Include Two-Factor Interactions", value=True)
            include_3fi = st.checkbox("Include Three-Factor Interactions", value=False)
            
            # Create model formula
            coded_factors = [f"{factor}_coded" for factor in factor_cols]
            model_terms = coded_factors.copy()
            
            # Add interaction terms
            if include_2fi:
                for i, j in combinations(range(len(coded_factors)), 2):
                    interaction_term = f"{coded_factors[i]}:{coded_factors[j]}"
                    model_terms.append(interaction_term)
            
            if include_3fi and len(coded_factors) >= 3:
                for i, j, k in combinations(range(len(coded_factors)), 3):
                    interaction_term = f"{coded_factors[i]}:{coded_factors[j]}:{coded_factors[k]}"
                    model_terms.append(interaction_term)
            
            # For RSM designs, add squared terms
            if st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] == "Response Surface":
                include_squared = st.checkbox("Include Squared Terms (for RSM)", value=True)
                if include_squared:
                    for factor in coded_factors:
                        model_terms.append(f"I({factor}**2)")
            else:
                include_squared = False
            
            # Build model formula
            formula = f"{response} ~ {' + '.join(model_terms)}"
            st.code(formula, language="python")
            
            # Fit the model
            try:
                model = ols(formula, data=coded_data).fit()
                st.session_state.model = model
                
                # Display model summary
                st.markdown("### Model Summary")
                
                # Create custom summary table
                summary_df = pd.DataFrame({
                    'Coefficient': model.params,
                    'Std Error': model.bse,
                    't-value': model.tvalues,
                    'p-value': model.pvalues
                })
                
                # Calculate effects from coefficients (effect = 2 * coefficient)
                effects = summary_df['Coefficient'] * 2
                effects.iloc[0] = summary_df['Coefficient'].iloc[0]  # Intercept is not multiplied
                summary_df['Effect'] = effects
                
                # Reorder columns
                summary_df = summary_df[['Effect', 'Coefficient', 'Std Error', 't-value', 'p-value']]
                
                # Store in session state
                st.session_state.model_summary = summary_df
                
                # Display summary
                st.dataframe(summary_df.style.format({
                    'Effect': '{:.4f}',
                    'Coefficient': '{:.4f}',
                    'Std Error': '{:.4f}',
                    't-value': '{:.3f}',
                    'p-value': '{:.4f}'
                }).background_gradient(subset=['p-value'], cmap='Reds_r'))
                
                # Model fit statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("R² Value", f"{model.rsquared:.4f}")
                with col2:
                    st.metric("Adjusted R²", f"{model.rsquared_adj:.4f}")
                with col3:
                    st.metric("F-statistic p-value", f"{model.f_pvalue:.4g}")
                
                # Effect visualization
                st.markdown("### Effect Visualization")
                
                # Pareto chart of absolute effects (excluding intercept)
                effect_df = summary_df.iloc[1:].copy()  # Skip intercept
                effect_df['Absolute Effect'] = effect_df['Effect'].abs()
                effect_df = effect_df.sort_values('Absolute Effect', ascending=False)
                
                fig = px.bar(
                    effect_df,
                    y=effect_df.index,
                    x='Absolute Effect',
                    orientation='h',
                    title="Pareto Chart of Standardized Effects",
                    color='p-value',
                    color_continuous_scale='Viridis_r',
                )
                
                # Add significance line
                alpha = 0.05
                t_crit = stats.t.ppf(1-alpha/2, model.df_resid)
                se = summary_df['Std Error'].iloc[1]  # Standard error for effects
                sig_line = t_crit * se * 2  # Convert to effect scale
                
                fig.add_vline(x=sig_line, line_dash="dash", line_color="red")
                fig.add_annotation(x=sig_line, y=0, text=f"Significance Line (α={alpha})", 
                                 showarrow=True, arrowhead=1, ax=40, ay=40)
                
                fig.update_layout(height=500)
                st.plotly_chart(fig)
                
                # Half-normal plot of effects
                st.markdown("### Half-Normal Plot of Effects")
                
                # Prepare data for half-normal plot
                effects_for_plot = summary_df.iloc[1:]['Effect'].abs().sort_values().reset_index(drop=True)
                n = len(effects_for_plot)
                
                # Calculate half-normal quantiles
                p = (np.arange(1, n + 1) - 0.5) / (2 * n)
                z = stats.norm.ppf((1 + p) / 2)
                
                # Create dataframe for plotting
                hnp_df = pd.DataFrame({
                    'Half-Normal Quantile': z,
                    'Absolute Effect': effects_for_plot,
                    'Effect Name': summary_df.iloc[1:].index[effects_for_plot.index]
                })
                
                # Create half-normal plot
                fig = px.scatter(
                    hnp_df,
                    x='Half-Normal Quantile',
                    y='Absolute Effect',
                    title="Half-Normal Plot of Effects",
                    text='Effect Name',
                    color=np.log1p(hnp_df['Absolute Effect']),
                    color_continuous_scale='Viridis'
                )
                
                # Add trend line for the smaller effects (assumed to be noise)
                # Use the first half of sorted effects to establish the noise trend
                noise_cutoff = n // 2
                slope, _, _, _, _ = stats.linregress(z[:noise_cutoff], effects_for_plot[:noise_cutoff])
                
                x_range = np.linspace(0, max(z), 100)
                y_range = slope * x_range
                
                fig.add_trace(go.Scatter(
                    x=x_range,
                    y=y_range,
                    mode='lines',
                    line=dict(dash='dash', color='red'),
                    name='Noise Trend'
                ))
                
                fig.update_traces(textposition='top right')
                fig.update_layout(height=500)
                st.plotly_chart(fig)
                
                # Identify significant effects
                alpha = 0.05
                significant_effects = summary_df[summary_df['p-value'] < alpha].index.tolist()
                if 'Intercept' in significant_effects:
                    significant_effects.remove('Intercept')
                
                st.session_state.significant_effects = significant_effects
                
                if significant_effects:
                    st.markdown("### Significant Effects Identified")
                    st.markdown(f"At α = {alpha}, the following effects are statistically significant:")
                    for effect in significant_effects:
                        effect_value = summary_df.loc[effect, 'Effect']
                        p_value = summary_df.loc[effect, 'p-value']
                        st.markdown(f"- **{effect}**: Effect = {effect_value:.4f}, p-value = {p_value:.4g}")
                else:
                    st.warning("No statistically significant effects detected at α = 0.05.")
                
                # Main effects plots
                st.markdown("### Main Effects Plots")
                
                main_effects = [f for f in coded_factors if f in model.params.index]
                
                if main_effects:
                    # Create a subplot for each main effect
                    fig = make_subplots(rows=1, cols=len(main_effects), 
                                       subplot_titles=[f.replace('_coded', '') for f in main_effects])
                    
                    for i, factor in enumerate(main_effects):
                        # Create prediction data
                        pred_data = pd.DataFrame({
                            factor: [-1, 1]
                        })
                        
                        # Set other factors to 0 (center point)
                        for other_factor in main_effects:
                            if other_factor != factor:
                                pred_data[other_factor] = 0
                        
                        # Predict response
                        X_pred = sm.add_constant(pred_data)
                        y_pred = np.dot(X_pred, model.params.loc[['Intercept', factor]])
                        
                        # Add to subplot
                        fig.add_trace(
                            go.Scatter(
                                x=[-1, 1],
                                y=y_pred,
                                mode='lines+markers',
                                name=factor.replace('_coded', ''),
                                line=dict(width=3),
                                showlegend=False
                            ),
                            row=1, col=i+1
                        )
                        
                        # Set factor name as x-axis title
                        fig.update_xaxes(title_text="Low (-1) to High (+1)", row=1, col=i+1)
                        
                        # Set y-axis title for first subplot only
                        if i == 0:
                            fig.update_yaxes(title_text=response, row=1, col=i+1)
                    
                    fig.update_layout(height=400, title="Main Effects Plots")
                    st.plotly_chart(fig)
                
                # Interaction plots (if applicable)
                if include_2fi and len(coded_factors) >= 2:
                    st.markdown("### Interaction Plots")
                    
                    # Find significant interactions
                    interaction_terms = [term for term in model.params.index if ':' in term and '::' not in term]
                    
                    if interaction_terms:
                        # Calculate significance of interactions
                        sig_interactions = [term for term in interaction_terms if term in significant_effects]
                        
                        # If there are significant interactions, plot them
                        if sig_interactions:
                            selected_interactions = sig_interactions
                            st.markdown("Showing significant interactions:")
                        else:
                            # Otherwise, show the top few by effect size
                            interaction_effects = {term: abs(summary_df.loc[term, 'Effect']) for term in interaction_terms}
                            top_interactions = sorted(interaction_effects.items(), key=lambda x: x[1], reverse=True)[:3]
                            selected_interactions = [term for term, _ in top_interactions]
                            st.markdown("No significant interactions found. Showing top interactions by effect size:")
                        
                        # Create a subplot for each selected interaction
                        fig = make_subplots(rows=1, cols=len(selected_interactions), 
                                          subplot_titles=[term.replace('_coded', '') for term in selected_interactions])
                        
                        for i, term in enumerate(selected_interactions):
                            # Extract factor names
                            factors = term.split(':')
                            
                            # Create prediction data
                            factor_values = [-1, 1]
                            pred_data = pd.DataFrame({
                                factors[0]: np.repeat(factor_values, 2),
                                factors[1]: np.tile(factor_values, 2)
                            })
                            
                            # Set other factors to 0 (center point)
                            for other_factor in coded_factors:
                                if other_factor not in factors:
                                    pred_data[other_factor] = 0
                            
                            # Add interaction term
                            pred_data[term] = pred_data[factors[0]] * pred_data[factors[1]]
                            
                            # Prepare prediction matrix
                            X_pred = sm.add_constant(pred_data)
                            X_pred = X_pred[['Intercept', factors[0], factors[1], term]]
                            
                            # Predict response
                            y_pred = np.dot(X_pred, model.params.loc[['Intercept', factors[0], factors[1], term]])
                            
                            # Reshape for plotting
                            y_matrix = y_pred.values.reshape(2, 2)
                            
                            # Add traces for each level of the second factor
                            for j, level in enumerate([-1, 1]):
                                name = f"{factors[1].split('_')[0]} = {level}"
                                fig.add_trace(
                                    go.Scatter(
                                        x=[-1, 1],
                                        y=y_matrix[:, j],
                                        mode='lines+markers',
                                        name=name,
                                        showlegend=(i == 0)
                                    ),
                                    row=1, col=i+1
                                )
                            
                            # Set factor name as x-axis title
                            factor_name = factors[0].replace('_coded', '')
                            fig.update_xaxes(title_text=factor_name, row=1, col=i+1)
                            
                            # Set y-axis title for first subplot only
                            if i == 0:
                                fig.update_yaxes(title_text=response, row=1, col=i+1)
                        
                        fig.update_layout(height=400, title="Interaction Plots")
                        st.plotly_chart(fig)
                    else:
                        st.info("No interaction terms in the model.")
                
            except Exception as e:
                st.error(f"Error fitting model: {e}")
                st.exception(e)
    
    # 3. Significance Testing
    with tabs[2]:
        st.subheader("Significance Testing")
        
        if st.session_state.model is None:
            st.warning("Please complete the effect estimation step first.")
        else:
            st.markdown("""
            This step evaluates the statistical significance of effects and the overall model.
            We use t-tests for individual terms and F-test for the overall model.
            """)
            
            # Get model from session state
            model = st.session_state.model
            summary_df = st.session_state.model_summary
            
            # ANOVA table
            st.markdown("### Analysis of Variance (ANOVA)")
            
            # Create ANOVA table
            anova_table = sm.stats.anova_lm(model, typ=2)
            
            # Add mean square column
            anova_table['MS'] = anova_table['sum_sq'] / anova_table['df']
            
            # Reorder columns
            anova_table = anova_table[['df', 'sum_sq', 'MS', 'F', 'PR(>F)']]
            
            # Rename columns for clarity
            anova_table.columns = ['DF', 'Sum of Squares', 'Mean Square', 'F-value', 'p-value']
            
            # Format the table
            st.dataframe(anova_table.style.format({
                'Sum of Squares': '{:.4f}',
                'Mean Square': '{:.4f}',
                'F-value': '{:.3f}',
                'p-value': '{:.4g}'
            }).background_gradient(subset=['p-value'], cmap='Reds_r'))
            
            # Overall model statistics
            st.markdown("### Model Fit Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("R²", f"{model.rsquared:.4f}")
                st.markdown("""
                *Proportion of variance explained by the model.*  
                Higher is better, but can be inflated by adding terms.
                """)
            
            with col2:
                st.metric("Adjusted R²", f"{model.rsquared_adj:.4f}")
                st.markdown("""
                *R² adjusted for the number of terms.*  
                Penalizes unnecessary model complexity.
                """)
            
            with col3:
                st.metric("Model p-value", f"{model.f_pvalue:.4g}")
                st.markdown("""
                *Tests overall significance of the model.*  
                Values < 0.05 indicate a significant model.
                """)
            
            # Model error metrics
            st.markdown("### Prediction Error Metrics")
            
            # Calculate various error metrics
            n = len(model.resid)
            p = len(model.params)
            
            rmse = np.sqrt(np.mean(model.resid**2))
            
            # Calculate PRESS (Prediction Error Sum of Squares)
            h_diag = np.diag(model.get_influence().hat_matrix_diag)
            press_resid = model.resid / (1 - h_diag)
            press = np.sum(press_resid**2)
            
            # Calculate PRESS RMSE
            press_rmse = np.sqrt(press / n)
            
            # Calculate predicted R-squared
            tss = np.sum((model.model.endog - np.mean(model.model.endog))**2)
            pred_r_squared = 1 - (press / tss)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("RMSE", f"{rmse:.4f}")
                st.markdown("""
                *Root Mean Square Error.*  
                Average prediction error in the original units.
                """)
            
            with col2:
                st.metric("PRESS RMSE", f"{press_rmse:.4f}")
                st.markdown("""
                *Prediction RMSE from leave-one-out cross-validation.*  
                Measures model's predictive performance.
                """)
            
            with col3:
                st.metric("Predicted R²", f"{pred_r_squared:.4f}")
                st.markdown("""
                *R² calculated using PRESS.*  
                Measures predictive power of the model.
                """)
            
            # Lack of fit test (if center points or pure replicates are available)
            if st.session_state.selected_dataset:
                # Check if there are center points
                if datasets[st.session_state.selected_dataset]["design_type"] in ["Full Factorial", "Fractional Factorial", "Response Surface"]:
                    st.markdown("### Lack of Fit Test")
                    
                    data = st.session_state.data
                    response = st.session_state.selected_response
                    
                    # Identify unique design points and replicates
                    factor_cols = datasets[st.session_state.selected_dataset]["factors"]
                    
                    # Create a unique identifier for each design point
                    data['point_id'] = data[factor_cols].astype(str).sum(axis=1)
                    
                    # Calculate pure error
                    pure_error_df = data.groupby('point_id')[response].agg(['count', 'mean', 'var'])
                    pure_error_df = pure_error_df[pure_error_df['count'] > 1]  # Only points with replicates
                    
                    if not pure_error_df.empty:
                        # Degrees of freedom for pure error
                        df_pure_error = sum(pure_error_df['count'] - 1)
                        
                        # Sum of squares for pure error
                        ss_pure_error = sum((pure_error_df['count'] - 1) * pure_error_df['var'])
                        
                        # Lack of fit statistics
                        df_lack_of_fit = model.df_resid - df_pure_error
                        ss_lack_of_fit = model.ssr - ss_pure_error
                        
                        if df_lack_of_fit > 0:
                            ms_lack_of_fit = ss_lack_of_fit / df_lack_of_fit
                            ms_pure_error = ss_pure_error / df_pure_error
                            
                            f_lack_of_fit = ms_lack_of_fit / ms_pure_error
                            p_lack_of_fit = 1 - stats.f.cdf(f_lack_of_fit, df_lack_of_fit, df_pure_error)
                            
                            # Create lack of fit table
                            lack_of_fit_table = pd.DataFrame({
                                'Source': ['Lack of Fit', 'Pure Error', 'Total Error'],
                                'DF': [df_lack_of_fit, df_pure_error, model.df_resid],
                                'Sum of Squares': [ss_lack_of_fit, ss_pure_error, model.ssr],
                                'Mean Square': [ms_lack_of_fit, ms_pure_error, model.ssr/model.df_resid],
                                'F-value': [f_lack_of_fit, np.nan, np.nan],
                                'p-value': [p_lack_of_fit, np.nan, np.nan]
                            })
                            
                            st.dataframe(lack_of_fit_table.style.format({
                                'Sum of Squares': '{:.4f}',
                                'Mean Square': '{:.4f}',
                                'F-value': '{:.3f}',
                                'p-value': '{:.4g}'
                            }))
                            
                            # Interpretation
                            if p_lack_of_fit < 0.05:
                                st.warning(f"Significant lack of fit detected (p = {p_lack_of_fit:.4g})")
                                st.markdown("""
                                The model doesn't adequately fit the data. Consider:
                                - Adding higher-order terms
                                - Adding interaction terms
                                - Transforming the response variable
                                """)
                            else:
                                st.success(f"No significant lack of fit (p = {p_lack_of_fit:.4g})")
                                st.markdown("""
                                The model adequately fits the data. Any deviations from the model
                                can be explained by random error.
                                """)
                        else:
                            st.info("Cannot calculate lack of fit (insufficient degrees of freedom)")
                    else:
                        st.info("Cannot perform lack of fit test (no replicated points found)")
            
            # Effect significance visualization
            st.markdown("### Effect Significance Visualization")
            
            # Create bar chart of effect significance
            effect_p_values = summary_df.iloc[1:].copy()  # Skip intercept
            effect_p_values = effect_p_values.sort_values('p-value')
            
            fig = px.bar(
                effect_p_values,
                y=effect_p_values.index,
                x='-log10(p-value)',
                orientation='h',
                title="-log₁₀(p-value) for Model Terms",
                color='-log10(p-value)',
                color_continuous_scale='Viridis',
                hover_data=['Effect', 'p-value']
            )
            
            # Add significance line at alpha = 0.05
            sig_line = -np.log10(0.05)
            fig.add_vline(x=sig_line, line_dash="dash", line_color="red")
            fig.add_annotation(x=sig_line, y=0, text="Significance (α=0.05)", 
                             showarrow=True, arrowhead=1, ax=40, ay=40)
            
            # Compute x values (as -log10(p-value))
            effect_p_values['-log10(p-value)'] = -np.log10(effect_p_values['p-value'])
            
            fig.update_layout(height=500)
            st.plotly_chart(fig)
            
            # Reduced model if many insignificant terms
            if effect_p_values['p-value'].max() > 0.2 and len(effect_p_values) > 5:
                st.markdown("### Model Reduction")
                st.markdown("""
                Several terms appear insignificant. Consider a reduced model
                with only the significant terms for improved prediction.
                """)
                
                # Allow user to select p-value threshold
                p_threshold = st.slider(
                    "p-value Threshold for Term Inclusion",
                    min_value=0.01,
                    max_value=0.20,
                    value=0.10,
                    step=0.01
                )
                
                # Get significant terms
                significant_terms = effect_p_values[effect_p_values['p-value'] <= p_threshold].index.tolist()
                
                if significant_terms:
                    # Create reduced model formula
                    reduced_formula = f"{st.session_state.selected_response} ~ {' + '.join(significant_terms)}"
                    
                    st.code(reduced_formula, language="python")
                    
                    # Fit reduced model
                    try:
                        data = st.session_state.data
                        coded_factors = [f"{factor}_coded" for factor in factor_cols]
                        
                        # Ensure all required coded variables are in the data
                        for term in significant_terms:
                            if ':' in term:
                                # Handle interaction terms
                                factors = term.split(':')
                                data[term] = data[factors[0]] * data[factors[1]]
                            elif '**2' in term:
                                # Handle squared terms
                                factor = term.split('(')[1].split(')')[0].replace('**2', '')
                                data[term] = data[factor]**2
                        
                        reduced_model = ols(reduced_formula, data=data).fit()
                        
                        # Compare models
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Full Model:**")
                            st.metric("R²", f"{model.rsquared:.4f}")
                            st.metric("Adjusted R²", f"{model.rsquared_adj:.4f}")
                            st.metric("RMSE", f"{rmse:.4f}")
                            st.metric("Terms", f"{len(model.params)}")
                        
                        with col2:
                            st.markdown("**Reduced Model:**")
                            reduced_rmse = np.sqrt(np.mean(reduced_model.resid**2))
                            st.metric("R²", f"{reduced_model.rsquared:.4f}")
                            st.metric("Adjusted R²", f"{reduced_model.rsquared_adj:.4f}")
                            st.metric("RMSE", f"{reduced_rmse:.4f}")
                            st.metric("Terms", f"{len(reduced_model.params)}")
                        
                        # Model comparison test
                        if len(reduced_model.params) < len(model.params):
                            f_stat, p_value = model.compare_f_test(reduced_model)
                            
                            st.markdown("### Model Comparison Test")
                            st.markdown(f"""
                            **F-statistic:** {f_stat:.3f}  
                            **p-value:** {p_value:.4g}
                            """)
                            
                            if p_value < 0.05:
                                st.warning("The reduced model is significantly worse than the full model.")
                                st.markdown("Consider keeping additional terms for better fit.")
                            else:
                                st.success("The reduced model is not significantly different from the full model.")
                                st.markdown("The reduced model provides similar fit with fewer terms. Consider using it for simplicity.")
                        
                    except Exception as e:
                        st.error(f"Error fitting reduced model: {e}")
                else:
                    st.warning(f"No terms were significant at p ≤ {p_threshold}")
    
    # 4. Model Diagnostics
    with tabs[3]:
        st.subheader("Model Diagnostics")
        
        if st.session_state.model is None:
            st.warning("Please complete the effect estimation step first.")
        else:
            st.markdown("""
            Model diagnostics check the validity of model assumptions and identify potential issues
            that might affect the reliability of your conclusions.
            """)
            
            # Get model and data
            model = st.session_state.model
            
            # Calculate fitted values and residuals
            fitted = model.fittedvalues
            residuals = model.resid
            std_residuals = model.get_influence().resid_studentized_internal
            
            # Prepare diagnostic data
            diag_data = pd.DataFrame({
                'Fitted': fitted,
                'Residual': residuals,
                'Standardized Residual': std_residuals,
                'Run Order': st.session_state.data['RunOrder']
            })
            
            # Add actual response values
            diag_data['Actual'] = fitted + residuals
            
            # 1. Residuals vs. Fitted Values
            st.markdown("### Residuals vs. Fitted Values")
            st.markdown("""
            This plot checks for non-linearity, heteroscedasticity, and outliers. Ideally, 
            residuals should be randomly scattered around zero with no pattern.
            """)
            
            fig = px.scatter(
                diag_data,
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
            
            # Add smoother to check for patterns
            x_range = np.linspace(min(fitted), max(fitted), 100)
            from scipy.stats import gaussian_kde
            try:
                # Only add smoother if there are enough points
                if len(fitted) > 5:
                    # Use LOWESS smoother
                    from statsmodels.nonparametric.smoothers_lowess import lowess
                    z = lowess(residuals, fitted, frac=0.6, it=1, return_sorted=False)
                    
                    fig.add_trace(go.Scatter(
                        x=fitted,
                        y=z,
                        mode='lines',
                        line=dict(color='black', width=2),
                        name='Trend'
                    ))
            except Exception as e:
                pass  # Skip smoother if it fails
            
            st.plotly_chart(fig)
            
            # Interpretation of residual vs. fitted plot
            if np.std(z) > 0.2 * np.std(residuals):
                st.warning("Potential non-linearity detected. Consider adding higher-order terms or transforming the response.")
            elif np.max(np.abs(std_residuals)) > 3:
                st.warning("Potential outliers detected. Check runs with standardized residuals beyond ±3.")
            else:
                st.success("No obvious patterns or issues detected in residuals vs. fitted values.")
            
            # 2. Normal Probability Plot of Residuals
            st.markdown("### Normal Probability Plot of Residuals")
            st.markdown("""
            This plot checks if residuals follow a normal distribution. Points should follow
            the diagonal line closely if the normality assumption is satisfied.
            """)
            
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
                title="Normal Probability Plot of Residuals",
                xaxis_title="Theoretical Quantiles",
                yaxis_title="Standardized Residuals",
                height=500
            )
            
            st.plotly_chart(fig)
            
            # Test for normality
            stat, p_value = stats.shapiro(residuals)
            
            st.markdown(f"""
            **Shapiro-Wilk Normality Test:**  
            Test Statistic: {stat:.4f}  
            p-value: {p_value:.4g}
            """)
            
            if p_value < 0.05:
                st.warning(f"Residuals may not be normally distributed (p = {p_value:.4g}).")
                st.markdown("""
                Consider:
                - Transforming the response variable
                - Checking for outliers
                - Using non-parametric methods if appropriate
                """)
            else:
                st.success(f"Residuals appear to be normally distributed (p = {p_value:.4g}).")
            
            # 3. Residuals vs. Run Order
            st.markdown("### Residuals vs. Run Order")
            st.markdown("""
            This plot checks for time-dependent effects or drift in your experiment.
            Residuals should show no trend or pattern over run order.
            """)
            
            fig = px.scatter(
                diag_data.sort_values('Run Order'),
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
            
            # Add smoother trend line
            if len(diag_data) > 5:
                try:
                    from statsmodels.nonparametric.smoothers_lowess import lowess
                    sorted_data = diag_data.sort_values('Run Order')
                    z = lowess(sorted_data['Residual'], sorted_data['Run Order'], frac=0.6, it=1, return_sorted=False)
                    
                    fig.add_trace(go.Scatter(
                        x=sorted_data['Run Order'],
                        y=z,
                        mode='lines',
                        line=dict(color='black', width=2),
                        name='Trend'
                    ))
                except Exception as e:
                    pass  # Skip smoother if it fails
            
            st.plotly_chart(fig)
            
            # Test for autocorrelation
            try:
                from statsmodels.stats.stattools import durbin_watson
                dw_stat = durbin_watson(diag_data.sort_values('Run Order')['Residual'])
                
                st.markdown(f"""
                **Durbin-Watson Statistic: {dw_stat:.4f}**  
                - Values near 2 indicate no autocorrelation
                - Values < 1.5 suggest positive autocorrelation
                - Values > 2.5 suggest negative autocorrelation
                """)
                
                if dw_stat < 1.5 or dw_stat > 2.5:
                    st.warning(f"Potential autocorrelation detected (DW = {dw_stat:.4f}).")
                    st.markdown("""
                    This may indicate time-dependent effects in your experiment such as:
                    - Equipment drift
                    - Environmental changes
                    - Learning effects
                    - Reagent degradation
                    """)
                else:
                    st.success(f"No significant autocorrelation detected (DW = {dw_stat:.4f}).")
            except Exception as e:
                st.info("Couldn't calculate autocorrelation statistic")
            
            # 4. Influence Diagnostics
            st.markdown("### Influence Diagnostics")
            st.markdown("""
            These diagnostics identify influential observations that might have a 
            disproportionate effect on your model and conclusions.
            """)
            
            # Calculate influence measures
            influence = model.get_influence()
            leverage = influence.hat_matrix_diag
            cooks_d = influence.cooks_distance[0]
            dffits = influence.dffits[0]
            
            # Add to diagnostic data
            diag_data['Leverage'] = leverage
            diag_data['Cook\'s Distance'] = cooks_d
            diag_data['DFFITS'] = dffits
            
            # Plot leverage vs. standardized residuals (bubble size = Cook's distance)
            fig = px.scatter(
                diag_data,
                x='Leverage',
                y='Standardized Residual',
                size='Cook\'s Distance',
                hover_data=['Run Order', 'DFFITS'],
                title="Influence Plot",
                labels={
                    "Leverage": "Leverage",
                    "Standardized Residual": "Studentized Residuals",
                    "Cook\'s Distance": "Cook's Distance"
                }
            )
            
            # Add threshold lines
            k = len(model.params)
            n = len(residuals)
            leverage_threshold = 2 * (k + 1) / n
            fig.add_vline(x=leverage_threshold, line_dash="dash", line_color="red")
            fig.add_hline(y=3, line_dash="dash", line_color="red")
            fig.add_hline(y=-3, line_dash="dash", line_color="red")
            
            st.plotly_chart(fig)
            
            # Identify influential observations
            influential_points = diag_data[
                (np.abs(diag_data['Standardized Residual']) > 3) |
                (diag_data['Leverage'] > leverage_threshold) |
                (diag_data['Cook\'s Distance'] > 4/n)
            ]
            
            if not influential_points.empty:
                st.warning("Potentially influential observations detected:")
                st.dataframe(influential_points)
                
                st.markdown("""
                **Interpretation:**
                - **High Leverage:** Points with unusual factor combinations that could influence the model
                - **High Residual:** Points poorly predicted by the model
                - **High Cook's Distance:** Points that significantly change the model if removed
                
                Consider:
                - Checking these runs for experimental errors
                - Rerunning the analysis without these points to see how the conclusions change
                - Investigating process conditions that might explain these unusual results
                """)
            else:
                st.success("No highly influential observations detected.")
            
            # 5. Transformation suggestion
            st.markdown("### Transformation Analysis")
            st.markdown("""
            If residuals show non-normality or heteroscedasticity, a transformation
            of the response variable might improve the model.
            """)
            
            # Box-Cox transformation analysis
            y = st.session_state.data[st.session_state.selected_response]
            
            # Only proceed if all values are positive
            if np.all(y > 0):
                try:
                    from scipy.stats import boxcox
                    from scipy import optimize
                    
                    # Function to optimize for Box-Cox transformation
                    def box_cox_normality(lambda_val):
                        if lambda_val == 0:
                            transformed = np.log(y)
                        else:
                            transformed = (y**lambda_val - 1) / lambda_val
                        _, p_val = stats.shapiro(transformed)
                        return -p_val  # Negative because we want to maximize p-value
                    
                    # Find optimal lambda
                    result = optimize.minimize_scalar(box_cox_normality, bounds=(-2, 2), method='bounded')
                    optimal_lambda = result.x
                    
                    # Calculate transformed values
                    if abs(optimal_lambda) < 0.01:  # Close to zero
                        transformed = np.log(y)
                        transform_name = "Natural logarithm (log)"
                    elif abs(optimal_lambda - 0.5) < 0.05:  # Close to 0.5
                        transformed = np.sqrt(y)
                        transform_name = "Square root"
                    elif abs(optimal_lambda - 1.0) < 0.05:  # Close to 1
                        transformed = y
                        transform_name = "No transformation (identity)"
                    elif abs(optimal_lambda + 1.0) < 0.05:  # Close to -1
                        transformed = 1/y
                        transform_name = "Reciprocal (1/y)"
                    else:
                        transformed = (y**optimal_lambda - 1) / optimal_lambda
                        transform_name = f"Box-Cox (λ = {optimal_lambda:.3f})"
                    
                    # Compare distributions
                    fig = make_subplots(rows=1, cols=2, 
                                       subplot_titles=["Original Response", "Transformed Response"])
                    
                    # Original distribution
                    fig.add_trace(
                        go.Histogram(x=y, nbinsx=10, name="Original"),
                        row=1, col=1
                    )
                    
                    # Transformed distribution
                    fig.add_trace(
                        go.Histogram(x=transformed, nbinsx=10, name="Transformed"),
                        row=1, col=2
                    )
                    
                    fig.update_layout(title=f"Suggested Transformation: {transform_name}")
                    st.plotly_chart(fig)
                    
                    # Test normality of original and transformed data
                    _, p_original = stats.shapiro(y)
                    _, p_transformed = stats.shapiro(transformed)
                    
                    st.markdown(f"""
                    **Normality Test p-values:**
                    - Original data: {p_original:.4g}
                    - Transformed data: {p_transformed:.4g}
                    
                    **Recommended transformation: {transform_name}**
                    """)
                    
                    if p_transformed > p_original and p_transformed > 0.05:
                        st.success(f"The {transform_name} transformation improves normality.")
                    elif p_transformed > p_original:
                        st.info(f"The {transform_name} transformation helps, but residuals may still not be perfectly normal.")
                    else:
                        st.info("No transformation significantly improves normality.")
                    
                except Exception as e:
                    st.info("Could not perform transformation analysis.")
            else:
                st.info("Box-Cox transformation requires all response values to be positive.")
                
                # Suggest other transformations
                if np.min(y) <= 0:
                    st.markdown("""
                    For data with zero or negative values, consider these transformations:
                    - Add a constant: y' = y + |min(y)| + 1
                    - Arcsinh transformation: y' = sinh⁻¹(y) = ln(y + √(y² + 1))
                    """)
    
    # 5. Response Surface Analysis
    with tabs[4]:
        st.subheader("Response Surface Analysis")
        
        if st.session_state.model is None:
            st.warning("Please complete the effect estimation step first.")
        elif st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] != "Response Surface":
            st.info("""
            Response surface analysis is most appropriate for response surface designs
            (Central Composite, Box-Behnken, etc.) that include center points and axial points.
            
            For factorial designs, we can still explore the predicted response across the design space,
            but true optimization requires a design that can estimate curvature.
            """)
        
        if st.session_state.model is not None:
            st.markdown("""
            Response surface analysis visualizes how factors affect the response across the
            design space, helping to identify optimal operating conditions.
            """)
            
            # Get data and model
            model = st.session_state.model
            data = st.session_state.data
            response = st.session_state.selected_response
            
            # Get factor information
            if st.session_state.selected_dataset:
                factor_cols = datasets[st.session_state.selected_dataset]["factors"]
            else:
                # For uploaded data, make a best guess
                all_columns = list(data.columns)
                factor_cols = [col for col in all_columns if col not in ["RunOrder", "StdOrder"] 
                              and not any(resp in col.lower() for resp in ["yield", "response", "output", "result"])
                              and col != response]
            
            # Create coded variables if they don't exist
            coded_factors = [f"{factor}_coded" for factor in factor_cols]
            
            for factor in factor_cols:
                if f"{factor}_coded" not in data.columns:
                    # Function to code a variable to [-1, 1] range
                    def code_variable(x):
                        x_min, x_max = x.min(), x.max()
                        # Check if the variable has only two unique values
                        if len(x.unique()) <= 2:
                            return pd.Series(np.where(x == x_min, -1, 1), index=x.index)
                        else:
                            # More than two levels - assume continuous
                            return pd.Series(2 * (x - x_min) / (x_max - x_min) - 1, index=x.index)
                    
                    data[f"{factor}_coded"] = code_variable(data[factor])
            
            # Allow user to select factors for visualization
            if len(factor_cols) > 2:
                selected_factors = st.multiselect(
                    "Select factors to visualize (max 2)",
                    factor_cols,
                    default=factor_cols[:2],
                    max_selections=2
                )
                
                if len(selected_factors) == 0:
                    selected_factors = factor_cols[:min(2, len(factor_cols))]
            else:
                selected_factors = factor_cols
            
            if len(selected_factors) == 1:
                # For one factor, create line plot
                st.markdown(f"### Response vs. {selected_factors[0]}")
                
                # Create range of values for the factor
                factor = selected_factors[0]
                x_min, x_max = data[factor].min(), data[factor].max()
                x_range = np.linspace(x_min, x_max, 100)
                
                # Create prediction data
                pred_data = pd.DataFrame({
                    factor: x_range
                })
                
                # Code the variable
                x_min_data, x_max_data = data[factor].min(), data[factor].max()
                pred_data[f"{factor}_coded"] = 2 * (pred_data[factor] - x_min_data) / (x_max_data - x_min_data) - 1
                
                # For other factors, set to center (0)
                for f in factor_cols:
                    if f != factor:
                        pred_data[f"{f}_coded"] = 0
                
                # Create interaction terms if needed
                if include_2fi:
                    for i, j in combinations(range(len(factor_cols)), 2):
                        f1 = f"{factor_cols[i]}_coded"
                        f2 = f"{factor_cols[j]}_coded"
                        if f1 in pred_data.columns and f2 in pred_data.columns:
                            pred_data[f"{f1}:{f2}"] = pred_data[f1] * pred_data[f2]
                
                # Create squared terms if needed
                if st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] == "Response Surface":
                    for f in factor_cols:
                        f_coded = f"{f}_coded"
                        if f_coded in pred_data.columns:
                            pred_data[f"I({f_coded}**2)"] = pred_data[f_coded]**2
                
                # Predict response
                try:
                    import patsy
                    X_pred = patsy.dmatrix(model.model.formula, pred_data, return_type='dataframe')
                    y_pred = model.predict(X_pred)
                    
                    # Get confidence intervals
                    from statsmodels.sandbox.regression.predstd import wls_prediction_std
                    _, lower, upper = wls_prediction_std(model, X_pred)
                    
                    # Create plot
                    fig = go.Figure()
                    
                    # Add prediction line
                    fig.add_trace(go.Scatter(
                        x=pred_data[factor],
                        y=y_pred,
                        mode='lines',
                        line=dict(color='blue', width=3),
                        name='Predicted Response'
                    ))
                    
                    # Add confidence intervals
                    fig.add_trace(go.Scatter(
                        x=pred_data[factor],
                        y=upper,
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=pred_data[factor],
                        y=lower,
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(0, 0, 255, 0.2)',
                        name='95% Confidence Interval'
                    ))
                    
                    # Add actual data points
                    fig.add_trace(go.Scatter(
                        x=data[factor],
                        y=data[response],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name='Actual Data'
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title=f"{response} vs. {factor}",
                        xaxis_title=factor,
                        yaxis_title=response,
                        height=500
                    )
                    
                    st.plotly_chart(fig)
                    
                    # Find optimal point
                    optimal_idx = np.argmax(y_pred)
                    optimal_x = pred_data[factor].iloc[optimal_idx]
                    optimal_y = y_pred[optimal_idx]
                    
                    st.markdown(f"""
                    **Optimal Value:**
                    - {factor}: {optimal_x:.4g}
                    - Predicted {response}: {optimal_y:.4g}
                    """)
                    
                except Exception as e:
                    st.error(f"Error generating prediction: {e}")
                    st.exception(e)
            
            elif len(selected_factors) == 2:
                # For two factors, create contour or surface plot
                st.markdown(f"### Response Surface for {selected_factors[0]} and {selected_factors[1]}")
                
                # Create grid of values for selected factors
                factor1, factor2 = selected_factors
                x1_min, x1_max = data[factor1].min(), data[factor1].max()
                x2_min, x2_max = data[factor2].min(), data[factor2].max()
                
                x1_grid = np.linspace(x1_min, x1_max, 30)
                x2_grid = np.linspace(x2_min, x2_max, 30)
                x1_mesh, x2_mesh = np.meshgrid(x1_grid, x2_grid)
                
                # Create prediction data
                pred_df = pd.DataFrame({
                    factor1: x1_mesh.flatten(),
                    factor2: x2_mesh.flatten()
                })
                
                # Code the variables
                for factor in [factor1, factor2]:
                    x_min_data, x_max_data = data[factor].min(), data[factor].max()
                    pred_df[f"{factor}_coded"] = 2 * (pred_df[factor] - x_min_data) / (x_max_data - x_min_data) - 1
                
                # For other factors, set to center (0)
                for f in factor_cols:
                    if f not in [factor1, factor2]:
                        pred_df[f"{f}_coded"] = 0
                
                # Create interaction terms if needed
                for i, j in combinations(range(len(factor_cols)), 2):
                    f1 = f"{factor_cols[i]}_coded"
                    f2 = f"{factor_cols[j]}_coded"
                    if f1 in pred_df.columns and f2 in pred_df.columns:
                        pred_df[f"{f1}:{f2}"] = pred_df[f1] * pred_df[f2]
                
                # Create squared terms if needed
                if st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] == "Response Surface":
                    for f in factor_cols:
                        f_coded = f"{f}_coded"
                        if f_coded in pred_df.columns:
                            pred_df[f"I({f_coded}**2)"] = pred_df[f_coded]**2
                
                # Predict response
                try:
                    import patsy
                    X_pred = patsy.dmatrix(model.model.formula, pred_df, return_type='dataframe')
                    y_pred = model.predict(X_pred)
                    
                    # Reshape for contour plot
                    z_mesh = y_pred.values.reshape(x2_grid.shape)
                    
                    # Create visualization
                    plot_type = st.radio(
                        "Select plot type",
                        ["Contour Plot", "3D Surface Plot"],
                        index=0
                    )
                    
                    if plot_type == "Contour Plot":
                        fig = go.Figure(data=go.Contour(
                            z=z_mesh,
                            x=x1_grid,
                            y=x2_grid,
                            colorscale='Viridis',
                            contours=dict(showlabels=True),
                            colorbar=dict(title=response)
                        ))
                        
                        # Add data points
                        fig.add_trace(go.Scatter(
                            x=data[factor1],
                            y=data[factor2],
                            mode='markers',
                            marker=dict(
                                color='red',
                                size=10,
                                line=dict(color='black', width=1)
                            ),
                            name='Experimental Points'
                        ))
                        
                        # Find maximum point
                        max_idx = np.argmax(y_pred)
                        max_x1 = pred_df[factor1].iloc[max_idx]
                        max_x2 = pred_df[factor2].iloc[max_idx]
                        
                        # Add marker for maximum
                        fig.add_trace(go.Scatter(
                            x=[max_x1],
                            y=[max_x2],
                            mode='markers',
                            marker=dict(
                                color='gold',
                                size=15,
                                symbol='star',
                                line=dict(color='black', width=1)
                            ),
                            name='Predicted Optimum'
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
                            x=data[factor1],
                            y=data[factor2],
                            z=data[response],
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
                    
                    max_x1 = pred_df[factor1].iloc[max_idx]
                    max_x2 = pred_df[factor2].iloc[max_idx]
                    max_y = y_pred[max_idx]
                    
                    min_x1 = pred_df[factor1].iloc[min_idx]
                    min_x2 = pred_df[factor2].iloc[min_idx]
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
                    
                    # Add canonical analysis if it's a response surface model
                    if st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] == "Response Surface":
                        st.markdown("### Canonical Analysis")
                        st.markdown("""
                        Canonical analysis characterizes the response surface by finding 
                        the stationary point and determining if it's a maximum, minimum, or saddle point.
                        """)
                        
                        try:
                            # Extract quadratic coefficients
                            quad_terms = [term for term in model.params.index if '**2' in term]
                            interact_terms = [term for term in model.params.index if ':' in term]
                            linear_terms = [term for term in model.params.index if term != 'Intercept'
                                          and term not in quad_terms and term not in interact_terms]
                            
                            if quad_terms:
                                # Construct B matrix (quadratic terms)
                                B = np.zeros((len(linear_terms), len(linear_terms)))
                                
                                # Fill diagonal with quadratic coefficients
                                for i, term in enumerate(linear_terms):
                                    factor = term.replace('_coded', '')
                                    quad_term = f"I({term}**2)"
                                    if quad_term in model.params.index:
                                        B[i, i] = model.params[quad_term]
                                
                                # Fill off-diagonal with interaction coefficients (divide by 2)
                                for term in interact_terms:
                                    f1, f2 = term.split(':')
                                    i = linear_terms.index(f1)
                                    j = linear_terms.index(f2)
                                    B[i, j] = model.params[term] / 2
                                    B[j, i] = model.params[term] / 2
                                
                                # Construct b vector (linear terms)
                                b = np.array([model.params[term] for term in linear_terms])
                                
                                # Calculate stationary point
                                try:
                                    xs = -np.linalg.solve(B, b/2)
                                    
                                    # Calculate predicted response at stationary point
                                    ys = model.params['Intercept'] + np.dot(b, xs) + np.dot(xs, np.dot(B, xs))
                                    
                                    # Calculate eigenvalues to determine nature of stationary point
                                    eigenvalues = np.linalg.eigvals(B)
                                    
                                    # Determine type of stationary point
                                    if np.all(eigenvalues < 0):
                                        point_type = "Maximum"
                                    elif np.all(eigenvalues > 0):
                                        point_type = "Minimum"
                                    else:
                                        point_type = "Saddle Point"
                                    
                                    # Display results
                                    st.markdown(f"**Stationary Point Type: {point_type}**")
                                    
                                    # Convert coded values back to actual
                                    stationary_actual = {}
                                    for i, term in enumerate(linear_terms):
                                        factor = term.replace('_coded', '')
                                        x_min_data, x_max_data = data[factor].min(), data[factor].max()
                                        actual_value = x_min_data + (xs[i] + 1) * (x_max_data - x_min_data) / 2
                                        stationary_actual[factor] = actual_value
                                    
                                    # Check if stationary point is within experimental region
                                    within_region = True
                                    for val in xs:
                                        if val < -1 or val > 1:
                                            within_region = False
                                            break
                                    
                                    status = "within" if within_region else "outside"
                                    
                                    st.markdown(f"""
                                    **Stationary Point (Coded Coordinates):**
                                    {", ".join([f"{term} = {xs[i]:.4g}" for i, term in enumerate(linear_terms)])}
                                    
                                    **Stationary Point (Actual Values):**
                                    {", ".join([f"{k} = {v:.4g}" for k, v in stationary_actual.items()])}
                                    
                                    **Predicted Response at Stationary Point:**
                                    {response} = {ys:.4g}
                                    
                                    **Eigenvalues of B Matrix:**
                                    {", ".join([f"{e:.4g}" for e in eigenvalues])}
                                    
                                    The stationary point is {status} the experimental region.
                                    """)
                                    
                                    if not within_region and point_type == "Maximum":
                                        st.info("""
                                        The maximum is outside the experimental region. 
                                        Consider running additional experiments in the direction of the stationary point.
                                        """)
                                    elif not within_region and point_type == "Minimum":
                                        st.info("""
                                        The minimum is outside the experimental region.
                                        The optimum may be at one of the boundaries of your experimental space.
                                        """)
                                    elif point_type == "Saddle Point":
                                        st.info("""
                                        The surface has a saddle point. The optimum will be found by moving
                                        along the eigenvector corresponding to the negative eigenvalue.
                                        """)
                                
                                except np.linalg.LinAlgError:
                                    st.warning("Could not calculate stationary point (singular matrix).")
                                    st.info("""
                                    This typically occurs when the response surface is nearly flat in some directions.
                                    The system may have a ridge or valley rather than a clear optimum.
                                    """)
                            else:
                                st.info("Canonical analysis requires quadratic terms in the model.")
                        
                        except Exception as e:
                            st.error(f"Error in canonical analysis: {e}")
                
                except Exception as e:
                    st.error(f"Error generating prediction: {e}")
                    st.exception(e)
            
            else:
                st.info("Please select at least one factor for visualization.")
            
            # Response optimizer (if applicable)
            if len(factor_cols) >= 1:
                st.markdown("### Response Optimizer")
                st.markdown("""
                Use this tool to find optimal factor settings for your desired response value.
                You can maximize, minimize, or target a specific value.
                """)
                
                # Optimization objective
                optimization_goal = st.radio(
                    "Optimization Goal",
                    ["Maximize Response", "Minimize Response", "Target Specific Value"],
                    index=0
                )
                
                if optimization_goal == "Target Specific Value":
                    target_value = st.number_input(
                        f"Target Value for {response}",
                        value=float(data[response].mean())
                    )
                
                # Constraints on factors
                st.markdown("### Factor Constraints")
                st.markdown("Specify the allowed range for each factor (defaults to experimental range).")
                
                factor_constraints = {}
                for factor in factor_cols:
                    col1, col2 = st.columns(2)
                    with col1:
                        min_val = st.number_input(
                            f"Minimum {factor}",
                            value=float(data[factor].min()),
                            key=f"min_{factor}"
                        )
                    with col2:
                        max_val = st.number_input(
                            f"Maximum {factor}",
                            value=float(data[factor].max()),
                            key=f"max_{factor}"
                        )
                    factor_constraints[factor] = (min_val, max_val)
                
                # Run optimization
                if st.button("Find Optimal Settings"):
                    try:
                        # Prepare optimization function
                        def objective_function(x):
                            # Create dataframe with factor values
                            pred_data = pd.DataFrame({factor: [val] for factor, val in zip(factor_cols, x)})
                            
                            # Code variables
                            for i, factor in enumerate(factor_cols):
                                x_min_data, x_max_data = data[factor].min(), data[factor].max()
                                pred_data[f"{factor}_coded"] = 2 * (pred_data[factor] - x_min_data) / (x_max_data - x_min_data) - 1
                            
                            # Create interaction terms
                            for i, j in combinations(range(len(factor_cols)), 2):
                                f1 = f"{factor_cols[i]}_coded"
                                f2 = f"{factor_cols[j]}_coded"
                                pred_data[f"{f1}:{f2}"] = pred_data[f1] * pred_data[f2]
                            
                            # Create squared terms
                            if st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] == "Response Surface":
                                for f in factor_cols:
                                    f_coded = f"{f}_coded"
                                    pred_data[f"I({f_coded}**2)"] = pred_data[f_coded]**2
                            
                            # Predict response
                            X_pred = patsy.dmatrix(model.model.formula, pred_data, return_type='dataframe')
                            y_pred = model.predict(X_pred)[0]
                            
                            # Return based on optimization goal
                            if optimization_goal == "Maximize Response":
                                return -y_pred  # Negative because we're minimizing
                            elif optimization_goal == "Minimize Response":
                                return y_pred
                            else:  # Target value
                                return (y_pred - target_value)**2
                        
                        # Initial guess (center of experimental region)
                        x0 = [(factor_constraints[factor][0] + factor_constraints[factor][1])/2 for factor in factor_cols]
                        
                        # Bounds for optimization
                        bounds = [(factor_constraints[factor][0], factor_constraints[factor][1]) for factor in factor_cols]
                        
                        # Run optimization
                        from scipy.optimize import minimize
                        
                        result = minimize(
                            objective_function,
                            x0=x0,
                            bounds=bounds,
                            method='L-BFGS-B'
                        )
                        
                        if result.success:
                            # Create prediction at optimal point
                            optimal_settings = {factor: val for factor, val in zip(factor_cols, result.x)}
                            
                            # Create dataframe for prediction
                            pred_data = pd.DataFrame({factor: [val] for factor, val in optimal_settings.items()})
                            
                            # Code variables
                            for factor in factor_cols:
                                x_min_data, x_max_data = data[factor].min(), data[factor].max()
                                pred_data[f"{factor}_coded"] = 2 * (pred_data[factor] - x_min_data) / (x_max_data - x_min_data) - 1
                            
                            # Create interaction terms
                            for i, j in combinations(range(len(factor_cols)), 2):
                                f1 = f"{factor_cols[i]}_coded"
                                f2 = f"{factor_cols[j]}_coded"
                                pred_data[f"{f1}:{f2}"] = pred_data[f1] * pred_data[f2]
                            
                            # Create squared terms
                            if st.session_state.selected_dataset and datasets[st.session_state.selected_dataset]["design_type"] == "Response Surface":
                                for f in factor_cols:
                                    f_coded = f"{f}_coded"
                                    pred_data[f"I({f_coded}**2)"] = pred_data[f_coded]**2
                            
                            # Predict response
                            X_pred = patsy.dmatrix(model.model.formula, pred_data, return_type='dataframe')
                            optimal_response = model.predict(X_pred)[0]
                            
                            # Display results
                            st.markdown("### Optimal Settings")
                            
                            # Format as a DataFrame for display
                            optimal_df = pd.DataFrame({
                                "Factor": factor_cols,
                                "Optimal Setting": [optimal_settings[factor] for factor in factor_cols]
                            })
                            
                            st.dataframe(optimal_df.style.format({"Optimal Setting": "{:.4g}"}))
                            
                            st.markdown(f"""
                            **Predicted Response at Optimal Settings:**
                            {response} = {optimal_response:.4g}
                            """)
                            
                            # Check if any factors are at their bounds
                            at_bounds = []
                            for factor in factor_cols:
                                min_bound, max_bound = factor_constraints[factor]
                                value = optimal_settings[factor]
                                if np.isclose(value, min_bound, rtol=1e-4) or np.isclose(value, max_bound, rtol=1e-4):
                                    at_bounds.append(factor)
                            
                            if at_bounds:
                                st.warning(f"The following factors are at their constraints: {', '.join(at_bounds)}")
                                st.markdown("""
                                This suggests the true optimum may be outside your experimental region.
                                Consider expanding the range for these factors in future experiments.
                                """)
                            
                            # Prediction interval at optimal point
                            try:
                                from statsmodels.sandbox.regression.predstd import wls_prediction_std
                                _, lower, upper = wls_prediction_std(model, X_pred)
                                
                                st.markdown(f"""
                                **95% Prediction Interval:**
                                {lower[0]:.4g} to {upper[0]:.4g}
                                """)
                            except:
                                pass
                        else:
                            st.error(f"Optimization failed: {result.message}")
                    
                    except Exception as e:
                        st.error(f"Error in optimization: {e}")
                        st.exception(e)
    
    # 6. Design Space Mapping
    with tabs[5]:
        st.subheader("Design Space Mapping")
        
        if st.session_state.model is None:
            st.warning("Please complete the effect estimation step first.")
        else:
            st.markdown("""
            Design space mapping identifies regions where all responses meet specifications
            with high confidence, supporting Quality by Design (QbD) approaches.
            """)
            
            # Get data and model
            model = st.session_state.model
            data = st.session_state.data
            selected_response = st.session_state.selected_response
            
            # Get factor information
            if st.session_state.selected_dataset:
                factor_cols = datasets[st.session_state.selected_dataset]["factors"]
                response_cols = datasets[st.session_state.selected_dataset]["responses"]
            else:
                # For uploaded data, make a best guess
                all_columns = list(data.columns)
                factor_cols = [col for col in all_columns if col not in ["RunOrder", "StdOrder"] 
                              and not any(resp in col.lower() for resp in ["yield", "response", "output", "result"])
                              and col != selected_response]
                response_cols = [col for col in all_columns if col not in factor_cols + ["RunOrder", "StdOrder"]]
            
            # Let user select responses for multi-response optimization
            if len(response_cols) > 1:
                st.markdown("### Select Responses for Design Space")
                
                selected_responses = st.multiselect(
                    "Responses to include in design space",
                    response_cols,
                    default=[selected_response]
                )
                
                if not selected_responses:
                    selected_responses = [selected_response]
            else:
                selected_responses = [selected_response]
            
            # Define specifications for each response
            st.markdown("### Response Specifications")
            st.markdown("""
            Define the acceptable range for each response. The design space will show
            regions where all responses meet these specifications.
            """)
            
            response_specs = {}
            for response in selected_responses:
                st.markdown(f"**{response}**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    spec_type = st.selectbox(
                        "Specification Type",
                        ["Range", "Minimum", "Maximum"],
                        key=f"spec_type_{response}"
                    )
                
                with col2:
                    if spec_type in ["Range", "Minimum"]:
                        lower = st.number_input(
                            "Lower Limit",
                            value=float(data[response].mean() - data[response].std()),
                            key=f"lower_{response}"
                        )
                    else:
                        lower = None
                
                with col3:
                    if spec_type in ["Range", "Maximum"]:
                        upper = st.number_input(
                            "Upper Limit",
                            value=float(data[response].mean() + data[response].std()),
                            key=f"upper_{response}"
                        )
                    else:
                        upper = None
                
                response_specs[response] = {
                    "lower": lower,
                    "upper": upper
                }
            
            # Select factors for visualization
            if len(factor_cols) > 2:
                selected_factors = st.multiselect(
                    "Select factors for design space visualization (max 2)",
                    factor_cols,
                    default=factor_cols[:2],
                    max_selections=2
                )
                
                if len(selected_factors) == 0:
                    selected_factors = factor_cols[:min(2, len(factor_cols))]
            else:
                selected_factors = factor_cols
            
            # Set values for non-visualized factors
            if len(factor_cols) > len(selected_factors):
                st.markdown("### Settings for Other Factors")
                st.markdown("""
                Set values for factors not included in the visualization.
                The design space will be calculated with these factors fixed at the specified values.
                """)
                
                other_factor_settings = {}
                for factor in factor_cols:
                    if factor not in selected_factors:
                        other_factor_settings[factor] = st.slider(
                            factor,
                            min_value=float(data[factor].min()),
                            max_value=float(data[factor].max()),
                            value=float(data[factor].mean()),
                            key=f"other_{factor}"
                        )
            else:
                other_factor_settings = {}
            
            # Confidence level for design space
            confidence_level = st.slider(
                "Confidence Level (%)",
                min_value=80,
                max_value=99,
                value=95,
                step=1
            )
            
            # Generate design space
            if len(selected_factors) >= 1 and st.button("Generate Design Space"):
                try:
                    # Create grid of values for selected factors
                    if len(selected_factors) == 1:
                        factor = selected_factors[0]
                        x_min, x_max = data[factor].min(), data[factor].max()
                        x_grid = np.linspace(x_min, x_max, 100)
                        
                        # Create prediction data
                        pred_df = pd.DataFrame({
                            factor: x_grid
                        })
                        
                        # Set other factors
                        for other_factor, value in other_factor_settings.items():
                            pred_df[other_factor] = value
                        
                        # Create coded variables
                        for f in factor_cols:
                            if f in pred_df.columns:
                                x_min_data, x_max_data = data[f].min(), data[f].max()
                                pred_df[f"{f}_coded"] = 2 * (pred_df[f] - x_min_data) / (x_max_data - x_min_data) - 1
                        
                    else:  # 2 factors
                        factor1, factor2 = selected_factors
                        x1_min, x1_max = data[factor1].min(), data[factor1].max()
                        x2_min, x2_max = data[factor2].min(), data[factor2].max()
                        
                        x1_grid = np.linspace(x1_min, x1_max, 50)
                        x2_grid = np.linspace(x2_min, x2_max, 50)
                        x1_mesh, x2_mesh = np.meshgrid(x1_grid, x2_grid)
                        
                        # Create prediction data
                        pred_df = pd.DataFrame({
                            factor1: x1_mesh.flatten(),
                            factor2: x2_mesh.flatten()
                        })
                        
                        # Set other factors
                        for other_factor, value in other_factor_settings.items():
                            pred_df[other_factor] = value
                        
                        # Create coded variables
                        for f in factor_cols:
                            if f in pred_df.columns:
                                x_min_data, x_max_data = data[f].min(), data[f].max()
                                pred_df[f"{f}_coded"] = 2 * (pred_df[f] - x_min_data) / (x_max_data - x_min_data) - 1
                    
                    # Fit models for all responses if needed
                    response_models = {}
                    
                    for response in selected_responses:
                        if response == selected_response:
                            response_models[response] = model
                        else:
                            # Need to fit a new model for this response
                            # Use the same model structure as the primary response
                            formula = model.model.formula.replace(selected_response, response)
                            response_models[response] = ols(formula, data=data).fit()
                    
                    # Calculate predictions and confidence intervals for each response
                    import patsy
                    
                    # Create coordinate grid for visualization
                    if len(selected_factors) == 1:
                        x_coords = pred_df[selected_factors[0]].values
                        
                        # Create output grid
                        in_space = np.ones(len(x_coords), dtype=bool)
                        
                        # Check each response against specifications
                        for response, resp_model in response_models.items():
                            # Get specifications
                            specs = response_specs[response]
                            
                            # Create model matrix
                            X_pred = patsy.dmatrix(resp_model.model.formula, pred_df, return_type='dataframe')
                            
                            # Predict response
                            y_pred = resp_model.predict(X_pred)
                            
                            # Get prediction intervals
                            from statsmodels.sandbox.regression.predstd import wls_prediction_std
                            _, lower, upper = wls_prediction_std(resp_model, X_pred)
                            
                            # Adjust intervals based on confidence level
                            z_ratio = stats.norm.ppf(0.5 + confidence_level/200) / stats.norm.ppf(0.975)
                            margin = (upper - y_pred) * z_ratio
                            lower_ci = y_pred - margin
                            upper_ci = y_pred + margin
                            
                            # Check against specifications
                            if specs["lower"] is not None:
                                in_space &= (lower_ci >= specs["lower"])
                            
                            if specs["upper"] is not None:
                                in_space &= (upper_ci <= specs["upper"])
                        
                        # Create plot
                        fig = go.Figure()
                        
                        # Add design space region
                        fig.add_trace(go.Scatter(
                            x=x_coords[in_space],
                            y=[0] * np.sum(in_space),
                            mode='markers',
                            marker=dict(
                                color='green',
                                size=10,
                                symbol='line-ns',
                                line=dict(width=2, color='black')
                            ),
                            name='Design Space'
                        ))
                        
                        # Add axes and update layout
                        fig.update_layout(
                            title=f"Design Space for {selected_factors[0]}",
                            xaxis_title=selected_factors[0],
                            yaxis_title="",
                            yaxis=dict(
                                showticklabels=False,
                                range=[-1, 1],
                                zeroline=True,
                                zerolinewidth=2
                            ),
                            height=400
                        )
                        
                        st.plotly_chart(fig)
                        
                        # Display design space limits
                        if np.any(in_space):
                            valid_x = x_coords[in_space]
                            st.markdown(f"""
                            **Design Space Limits for {selected_factors[0]}:**
                            {selected_factors[0]}: {np.min(valid_x):.4g} to {np.max(valid_x):.4g}
                            """)
                        else:
                            st.warning("No valid design space found with the current specifications.")
                    
                    else:  # 2 factors
                        factor1, factor2 = selected_factors
                        x1_coords = pred_df[factor1].values
                        x2_coords = pred_df[factor2].values
                        
                        # Create output grid
                        in_space = np.ones(len(x1_coords), dtype=bool)
                        
                        # Track predictions for each response
                        predictions = {}
                        
                        # Check each response against specifications
                        for response, resp_model in response_models.items():
                            # Get specifications
                            specs = response_specs[response]
                            
                            # Create model matrix
                            X_pred = patsy.dmatrix(resp_model.model.formula, pred_df, return_type='dataframe')
                            
                            # Predict response
                            y_pred = resp_model.predict(X_pred)
                            predictions[response] = y_pred
                            
                            # Get prediction intervals
                            from statsmodels.sandbox.regression.predstd import wls_prediction_std
                            _, lower, upper = wls_prediction_std(resp_model, X_pred)
                            
                            # Adjust intervals based on confidence level
                            z_ratio = stats.norm.ppf(0.5 + confidence_level/200) / stats.norm.ppf(0.975)
                            margin = (upper - y_pred) * z_ratio
                            lower_ci = y_pred - margin
                            upper_ci = y_pred + margin
                            
                            # Check against specifications
                            if specs["lower"] is not None:
                                in_space &= (lower_ci >= specs["lower"])
                            
                            if specs["upper"] is not None:
                                in_space &= (upper_ci <= specs["upper"])
                        
                        # Reshape for contour plot
                        grid_shape = (len(x2_grid), len(x1_grid))
                        in_space_grid = in_space.reshape(grid_shape)
                        
                        # Create design space plot
                        fig = go.Figure()
                        
                        # Add design space region
                        fig.add_trace(go.Contour(
                            z=in_space_grid.astype(int),
                            x=x1_grid,
                            y=x2_grid,
                            contours=dict(
                                start=0,
                                end=1,
                                coloring='fill',
                                showlabels=True
                            ),
                            colorscale=['white', 'green'],
                            showscale=False,
                            name='Design Space'
                        ))
                        
                        # Add experimental points
                        fig.add_trace(go.Scatter(
                            x=data[factor1],
                            y=data[factor2],
                            mode='markers',
                            marker=dict(
                                color='black',
                                size=8,
                                symbol='circle',
                                line=dict(width=1, color='black')
                            ),
                            name='Experimental Points'
                        ))
                        
                        # Update layout
                        fig.update_layout(
                            title=f"Design Space at {confidence_level}% Confidence",
                            xaxis_title=factor1,
                            yaxis_title=factor2,
                            height=600
                        )
                        
                        st.plotly_chart(fig)
                        
                        # Option to show individual response contours
                        if st.checkbox("Show Individual Response Contours"):
                            for response in selected_responses:
                                st.markdown(f"### {response} Contour Plot")
                                
                                # Get predictions for this response
                                z_grid = predictions[response].reshape(grid_shape)
                                
                                # Get specifications
                                specs = response_specs[response]
                                
                                # Create contour plot
                                fig = go.Figure()
                                
                                # Add contour
                                fig.add_trace(go.Contour(
                                    z=z_grid,
                                    x=x1_grid,
                                    y=x2_grid,
                                    colorscale='Viridis',
                                    contours=dict(
                                        showlabels=True,
                                        labelfont=dict(size=12, color='white')
                                    ),
                                    colorbar=dict(title=response)
                                ))
                                
                                # Add specification lines
                                if specs["lower"] is not None:
                                    fig.add_trace(go.Contour(
                                        z=z_grid,
                                        x=x1_grid,
                                        y=x2_grid,
                                        contours=dict(
                                            start=specs["lower"],
                                            end=specs["lower"],
                                            coloring='lines',
                                            showlabels=True,
                                            labelfont=dict(color='red')
                                        ),
                                        line=dict(color='red', width=2),
                                        showscale=False,
                                        name=f"Lower Spec: {specs['lower']}"
                                    ))
                                
                                if specs["upper"] is not None:
                                    fig.add_trace(go.Contour(
                                        z=z_grid,
                                        x=x1_grid,
                                        y=x2_grid,
                                        contours=dict(
                                            start=specs["upper"],
                                            end=specs["upper"],
                                            coloring='lines',
                                            showlabels=True,
                                            labelfont=dict(color='red')
                                        ),
                                        line=dict(color='red', width=2),
                                        showscale=False,
                                        name=f"Upper Spec: {specs['upper']}"
                                    ))
                                
                                # Add experimental points
                                fig.add_trace(go.Scatter(
                                    x=data[factor1],
                                    y=data[factor2],
                                    mode='markers',
                                    marker=dict(
                                        color='black',
                                        size=8,
                                        symbol='circle',
                                        line=dict(width=1, color='black')
                                    ),
                                    name='Experimental Points'
                                ))
                                
                                # Update layout
                                fig.update_layout(
                                    title=f"{response} Contour Plot",
                                    xaxis_title=factor1,
                                    yaxis_title=factor2,
                                    height=500
                                )
                                
                                st.plotly_chart(fig)
                        
                        # Calculate design space area
                        factor1_range = x1_max - x1_min
                        factor2_range = x2_max - x2_min
                        total_area = factor1_range * factor2_range
                        design_space_area = np.sum(in_space) / len(in_space) * total_area
                        percent_area = (design_space_area / total_area) * 100
                        
                        st.markdown(f"""
                        **Design Space Summary:**
                        - Coverage: {percent_area:.1f}% of experimental region
                        - Confidence Level: {confidence_level}%
                        """)
                        
                        # Check if design space exists
                        if np.any(in_space):
                            # Find a representative point in the design space
                            # (approximating the centroid)
                            def distance_to_center(coords):
                                x1, x2 = coords
                                x1_center = (x1_min + x1_max) / 2
                                x2_center = (x2_min + x2_max) / 2
                                return ((x1 - x1_center) / factor1_range)**2 + ((x2 - x2_center) / factor2_range)**2
                            
                            valid_points = np.column_stack((x1_coords[in_space], x2_coords[in_space]))
                            
                            if len(valid_points) > 0:
                                distances = [distance_to_center(point) for point in valid_points]
                                center_idx = np.argmin(distances)
                                center_point = valid_points[center_idx]
                                
                                st.markdown(f"""
                                **Suggested Operating Point:**
                                - {factor1}: {center_point[0]:.4g}
                                - {factor2}: {center_point[1]:.4g}
                                """)
                                
                                # Predict responses at this point
                                center_df = pd.DataFrame({
                                    factor1: [center_point[0]],
                                    factor2: [center_point[1]]
                                })
                                
                                # Set other factors
                                for other_factor, value in other_factor_settings.items():
                                    center_df[other_factor] = value
                                
                                # Create coded variables
                                for f in factor_cols:
                                    if f in center_df.columns:
                                        x_min_data, x_max_data = data[f].min(), data[f].max()
                                        center_df[f"{f}_coded"] = 2 * (center_df[f] - x_min_data) / (x_max_data - x_min_data) - 1
                                
                                # Predict all responses
                                st.markdown("**Predicted Responses at Suggested Point:**")
                                
                                for response, resp_model in response_models.items():
                                    X_pred = patsy.dmatrix(resp_model.model.formula, center_df, return_type='dataframe')
                                    y_pred = resp_model.predict(X_pred)[0]
                                    
                                    # Get prediction interval
                                    _, lower, upper = wls_prediction_std(resp_model, X_pred)
                                    
                                    # Adjust for confidence level
                                    z_ratio = stats.norm.ppf(0.5 + confidence_level/200) / stats.norm.ppf(0.975)
                                    margin = (upper[0] - y_pred) * z_ratio
                                    
                                    st.markdown(f"""
                                    - {response}: {y_pred:.4g} ({y_pred - margin:.4g} to {y_pred + margin:.4g})
                                    """)
                        else:
                            st.warning("No valid design space found with the current specifications.")
                            st.markdown("""
                            Consider:
                            - Relaxing the response specifications
                            - Lowering the confidence level
                            - Adjusting settings for fixed factors
                            """)
                
                except Exception as e:
                    st.error(f"Error generating design space: {e}")
                    st.exception(e)

                st.markdown("""
                **Applications in Biotech Regulatory Context:**
                
                Design space mapping is a key element of Quality by Design (QbD) submissions to regulatory agencies. It demonstrates:
                
                1. **Process Understanding**: The relationship between process parameters and quality attributes
                2. **Risk Assessment**: The impact of parameter variability on product quality
                3. **Control Strategy**: The rationale for parameter ranges and control points
                4. **Operational Flexibility**: The ability to operate within a validated space rather than at fixed setpoints
                
                For biopharmaceutical products, well-defined design spaces enable:
                - Faster approval of manufacturing changes
                - Reduced post-approval variation filings
                - More robust manufacturing with consistent product quality
                """)
                
                st.markdown("### Robustness Analysis")
                st.markdown("""
                **Concept Anchor**: Robustness analysis assesses process sensitivity to uncontrolled variations, quantifying the impact of factor perturbations on critical quality attributes and process performance.

                **Practical Lens**: In biopharmaceutical lyophilization, robustness analysis reveals that shelf temperature variations of ±2°C significantly impact product moisture content, leading to tighter equipment qualification requirements and more stringent in-process controls.

                **Methodological Approaches**:
                1. **Sensitivity Analysis**:
                   - Partial derivatives: $\\frac{\\partial \\hat{y}}{\\partial x_i}$
                   - Normalized sensitivity: $\\frac{x_i}{\\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial x_i}$
                   - Tolerance analysis: Impact of factor variation $\\Delta x_i$ on response
                     $\\Delta \\hat{y} \\approx \\sum_{i=1}^{k} \\frac{\\partial \\hat{y}}{\\partial x_i} \\Delta x_i$

                2. **Monte Carlo Simulation**:
                   - Define probability distributions for factor variations
                   - Generate random samples from these distributions
                   - Predict responses for each sample
                   - Characterize output distribution and failure probability

                3. **Edge of Failure Analysis**:
                   - Identify combinations of factors at boundary of acceptable performance
                   - Calculate distance to failure from nominal operating point
                   - Establish safety margins based on process variability
                """)

# Main function to run when imported
if __name__ == "__main__":
    show()