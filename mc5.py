import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import math 
import plotly.graph_objs as go

from helpers.linear_indicator import create_linear_indicator
from helpers.balance_display import display_balances
from helpers.inputs_to_df import create_parameters_dataframe

from helpers.styling import tab_style_css
from helpers.styling import button_style_css
from helpers.styling import download_button_style_css

from simulations.simulation_mc import monte_carlo_simulation

# Set Streamlit to use full-width layout
st.set_page_config(layout="wide")

# set button styles 
st.markdown(button_style_css, unsafe_allow_html=True)
st.markdown(download_button_style_css, unsafe_allow_html=True)

current_year = datetime.now().year

# Streamlit Display
st.write("# Retirement Analysis with Monte Carlo Simulation")

# Function to load parameters from a CSV file
def load_parameters_from_csv(uploaded_file):
    try:
        # Read the CSV file into a DataFrame
        params_df = pd.read_csv(uploaded_file)

        # Validate the DataFrame (check if all required columns are present)
        required_columns = [
            "current_age", "partner_current_age", "life_expectancy", "retirement_age",
            "partner_retirement_age", "initial_savings", "stock_percentage", "bond_percentage",
            "annual_earnings", "self_yearly_increase", "tax_rate", "partner_earnings",
            "partner_yearly_increase", "annual_expense", "mortgage_payment", "inflation_mean",
            "annual_expense_decrease", "mortgage_years_remaining", "inflation_std",
            "annual_social_security", "withdrawal_start_age", "cola_rate",
            "partner_social_security", "partner_withdrawal_start_age",
            "self_healthcare_cost", "self_healthcare_start_age",
            "partner_healthcare_cost", "partner_healthcare_start_age",
            "stock_return_mean", "bond_return_mean", "simulations",
            "stock_return_std", "bond_return_std", "years_until_downsize",
            "residual_amount", "adjust_expense_year_1", "adjust_expense_amount_1",
            "adjust_expense_year_2", "adjust_expense_amount_2",
            "adjust_expense_year_3", "adjust_expense_amount_3",
            "one_time_year_1", "one_time_amount_1",
            "one_time_year_2", "one_time_amount_2",
            "one_time_year_3", "one_time_amount_3",
            "windfall_year_1", "windfall_amount_1",
            "windfall_year_2", "windfall_amount_2",
            "windfall_year_3", "windfall_amount_3"
        ]

        # Check if all required columns are present
        if not all(col in params_df.columns for col in required_columns):
            st.error("Uploaded file is missing one or more required columns.")
            return

        # Set the values in the form fields directly
        current_age = params_df["current_age"].iloc[0]
        partner_current_age = params_df["partner_current_age"].iloc[0]
        life_expectancy = params_df["life_expectancy"].iloc[0]
        retirement_age = params_df["retirement_age"].iloc[0]
        partner_retirement_age = params_df["partner_retirement_age"].iloc[0]
        initial_savings = params_df["initial_savings"].iloc[0]
        stock_percentage = params_df["stock_percentage"].iloc[0]
        bond_percentage = params_df["bond_percentage"].iloc[0]
        annual_earnings = params_df["annual_earnings"].iloc[0]
        self_yearly_increase = params_df["self_yearly_increase"].iloc[0]
        tax_rate = params_df["tax_rate"].iloc[0]
        partner_earnings = params_df["partner_earnings"].iloc[0]
        partner_yearly_increase = params_df["partner_yearly_increase"].iloc[0]
        annual_expense = params_df["annual_expense"].iloc[0]
        mortgage_payment = params_df["mortgage_payment"].iloc[0]
        inflation_mean = params_df["inflation_mean"].iloc[0]
        annual_expense_decrease = params_df["annual_expense_decrease"].iloc[0]
        mortgage_years_remaining = params_df["mortgage_years_remaining"].iloc[0]
        inflation_std = params_df["inflation_std"].iloc[0]
        annual_social_security = params_df["annual_social_security"].iloc[0]
        withdrawal_start_age = params_df["withdrawal_start_age"].iloc[0]
        cola_rate = params_df["cola_rate"].iloc[0]
        partner_social_security = params_df["partner_social_security"].iloc[0]
        partner_withdrawal_start_age = params_df["partner_withdrawal_start_age"].iloc[0]
        self_healthcare_cost = params_df["self_healthcare_cost"].iloc[0]
        self_healthcare_start_age = params_df["self_healthcare_start_age"].iloc[0]
        partner_healthcare_cost = params_df["partner_healthcare_cost"].iloc[0]
        partner_healthcare_start_age = params_df["partner_healthcare_start_age"].iloc[0]
        stock_return_mean = params_df["stock_return_mean"].iloc[0]
        bond_return_mean = params_df["bond_return_mean"].iloc[0]
        simulations = params_df["simulations"].iloc[0]
        stock_return_std = params_df["stock_return_std"].iloc[0]
        bond_return_std = params_df["bond_return_std"].iloc[0]
        years_until_downsize = params_df["years_until_downsize"].iloc[0]
        residual_amount = params_df["residual_amount"].iloc[0]
        adjust_expense_year_1 = params_df["adjust_expense_year_1"].iloc[0]
        adjust_expense_amount_1 = params_df["adjust_expense_amount_1"].iloc[0]
        adjust_expense_year_2 = params_df["adjust_expense_year_2"].iloc[0]
        adjust_expense_amount_2 = params_df["adjust_expense_amount_2"].iloc[0]
        adjust_expense_year_3 = params_df["adjust_expense_year_3"].iloc[0]
        adjust_expense_amount_3 = params_df["adjust_expense_amount_3"].iloc[0]
        one_time_year_1 = params_df["one_time_year_1"].iloc[0]
        one_time_amount_1 = params_df["one_time_amount_1"].iloc[0]
        one_time_year_2 = params_df["one_time_year_2"].iloc[0]
        one_time_amount_2 = params_df["one_time_amount_2"].iloc[0]
        one_time_year_3 = params_df["one_time_year_3"].iloc[0]
        one_time_amount_3 = params_df["one_time_amount_3"].iloc[0]
        windfall_year_1 = params_df["windfall_year_1"].iloc[0]
        windfall_amount_1 = params_df["windfall_amount_1"].iloc[0]
        windfall_year_2 = params_df["windfall_year_2"].iloc[0]
        windfall_amount_2 = params_df["windfall_amount_2"].iloc[0]
        windfall_year_3 = params_df["windfall_year_3"].iloc[0]
        windfall_amount_3 = params_df["windfall_amount_3"].iloc[0]

        # Set the values in the form fields directly
        return {
            "current_age": current_age,
            "partner_current_age": partner_current_age,
            "life_expectancy": life_expectancy,
            "retirement_age": retirement_age,
            "partner_retirement_age": partner_retirement_age,
            "initial_savings": initial_savings,
            "stock_percentage": stock_percentage,
            "bond_percentage": bond_percentage,
            "annual_earnings": annual_earnings,
            "self_yearly_increase": self_yearly_increase,
            "tax_rate": tax_rate,
            "partner_earnings": partner_earnings,
            "partner_yearly_increase": partner_yearly_increase,
            "annual_expense": annual_expense,
            "mortgage_payment": mortgage_payment,
            "inflation_mean": inflation_mean,
            "annual_expense_decrease": annual_expense_decrease,
            "mortgage_years_remaining": mortgage_years_remaining,
            "inflation_std": inflation_std,
            "annual_social_security": annual_social_security,
            "withdrawal_start_age": withdrawal_start_age,
            "cola_rate": cola_rate,
            "partner_social_security": partner_social_security,
            "partner_withdrawal_start_age": partner_withdrawal_start_age,
            "self_healthcare_cost": self_healthcare_cost,
            "self_healthcare_start_age": self_healthcare_start_age,
            "partner_healthcare_cost": partner_healthcare_cost,
            "partner_healthcare_start_age": partner_healthcare_start_age,
            "stock_return_mean": stock_return_mean,
            "bond_return_mean": bond_return_mean,
            "simulations": simulations,
            "stock_return_std": stock_return_std,
            "bond_return_std": bond_return_std,
            "years_until_downsize": years_until_downsize,
            "residual_amount": residual_amount,
            "adjust_expense_year_1": adjust_expense_year_1,
            "adjust_expense_amount_1": adjust_expense_amount_1,
            "adjust_expense_year_2": adjust_expense_year_2,
            "adjust_expense_amount_2": adjust_expense_amount_2,
            "adjust_expense_year_3": adjust_expense_year_3,
            "adjust_expense_amount_3": adjust_expense_amount_3,
            "one_time_year_1": one_time_year_1,
            "one_time_amount_1": one_time_amount_1,
            "one_time_year_2": one_time_year_2,
            "one_time_amount_2": one_time_amount_2,
            "one_time_year_3": one_time_year_3,
            "one_time_amount_3": one_time_amount_3,
            "windfall_year_1": windfall_year_1,
            "windfall_amount_1": windfall_amount_1,
            "windfall_year_2": windfall_year_2,
            "windfall_amount_2": windfall_amount_2,
            "windfall_year_3": windfall_year_3,
            "windfall_amount_3": windfall_amount_3,
        }

    except Exception as e:
        st.error(f"Error loading parameters: {e}")


# Add upload button for the CSV file
uploaded_file = st.file_uploader("Upload your parameters CSV file", type=["csv"])
if uploaded_file is not None:
    parameters = load_parameters_from_csv(uploaded_file)

    # Set the form fields using the loaded parameters
    if parameters:
        current_age = parameters["current_age"]
        partner_current_age = parameters["partner_current_age"]
        life_expectancy = parameters["life_expectancy"]
        retirement_age = parameters["retirement_age"]
        partner_retirement_age = parameters["partner_retirement_age"]
        initial_savings = parameters["initial_savings"]
        stock_percentage = parameters["stock_percentage"]
        bond_percentage = parameters["bond_percentage"]
        annual_earnings = parameters["annual_earnings"]
        self_yearly_increase = parameters["self_yearly_increase"]
        tax_rate = parameters["tax_rate"]
        partner_earnings = parameters["partner_earnings"]
        partner_yearly_increase = parameters["partner_yearly_increase"]
        annual_expense = parameters["annual_expense"]
        mortgage_payment = parameters["mortgage_payment"]
        inflation_mean = parameters["inflation_mean"]
        annual_expense_decrease = parameters["annual_expense_decrease"]
        mortgage_years_remaining = parameters["mortgage_years_remaining"]
        inflation_std = parameters["inflation_std"]
        annual_social_security = parameters["annual_social_security"]
        withdrawal_start_age = parameters["withdrawal_start_age"]
        cola_rate = parameters["cola_rate"]
        partner_social_security = parameters["partner_social_security"]
        partner_withdrawal_start_age = parameters["partner_withdrawal_start_age"]
        self_healthcare_cost = parameters["self_healthcare_cost"]
        self_healthcare_start_age = parameters["self_healthcare_start_age"]
        partner_healthcare_cost = parameters["partner_healthcare_cost"]
        partner_healthcare_start_age = parameters["partner_healthcare_start_age"]
        stock_return_mean = parameters["stock_return_mean"]
        bond_return_mean = parameters["bond_return_mean"]
        simulations = parameters["simulations"]
        stock_return_std = parameters["stock_return_std"]
        bond_return_std = parameters["bond_return_std"]
        years_until_downsize = parameters["years_until_downsize"]
        residual_amount = parameters["residual_amount"]
        adjust_expense_year_1 = parameters["adjust_expense_year_1"]
        adjust_expense_amount_1 = parameters["adjust_expense_amount_1"]
        adjust_expense_year_2 = parameters["adjust_expense_year_2"]
        adjust_expense_amount_2 = parameters["adjust_expense_amount_2"]
        adjust_expense_year_3 = parameters["adjust_expense_year_3"]
        adjust_expense_amount_3 = parameters["adjust_expense_amount_3"]
        one_time_year_1 = parameters["one_time_year_1"]
        one_time_amount_1 = parameters["one_time_amount_1"]
        one_time_year_2 = parameters["one_time_year_2"]
        one_time_amount_2 = parameters["one_time_amount_2"]
        one_time_year_3 = parameters["one_time_year_3"]
        one_time_amount_3 = parameters["one_time_amount_3"]
        windfall_year_1 = parameters["windfall_year_1"]
        windfall_amount_1 = parameters["windfall_amount_1"]
        windfall_year_2 = parameters["windfall_year_2"]
        windfall_amount_2 = parameters["windfall_amount_2"]
        windfall_year_3 = parameters["windfall_year_3"]
        windfall_amount_3 = parameters["windfall_amount_3"]


# Add upload button for the CSV file
uploaded_file = st.file_uploader("Upload your parameters CSV file", type=["csv"])
print(uploaded_file) 
parameters = None
if uploaded_file is not None:
    parameters = load_parameters_from_csv(uploaded_file)

print(parameters)

# Put the tabs inside a container with fixed height
with st.container(height=420, border=None):

    # Set the tab styles 
    st.markdown(tab_style_css, unsafe_allow_html=True)

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([" Personal Details ", " Investments and Savings ", " Income & Taxes", "Expense", "Social Security", "Healthcare Costs", "Market Returns", "Downsize", "Adjust Yearly Expense", "One Time Expense", "Windfall"])

    # Tab 1: Personal Details
    with tab1:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            current_age = st.number_input("Current Age", value=parameters["current_age"] if parameters else 55)
            partner_current_age = st.number_input("Partner's Current Age", value=parameters["partner_current_age"] if parameters else 50)
            st.markdown("<br>", unsafe_allow_html=True)
            life_expectancy = st.number_input("Life Expectancy", value=parameters["life_expectancy"] if parameters else 92)
        with col2:
            retirement_age = st.number_input("Retirement Age", value=parameters["retirement_age"] if parameters else 60)
            partner_retirement_age = st.number_input("Partner's Retirement Age", value=parameters["partner_retirement_age"] if parameters else 58)

        # Calculate the range of valid years based on current age and life expectancy
        start_year = current_year 
        end_year = current_year + (life_expectancy - current_age)
        # Create a list of years for drops downs 
        years = list(range(start_year, end_year + 1))

    # Tab 2: Investment and Savings
    with tab2:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            initial_savings = st.number_input("Current Total Portfolio", value=parameters["initial_savings"] if parameters else 2000000, step=100000)
            st.markdown("<br>", unsafe_allow_html=True)
            stock_percentage = st.slider("Percentage of Stock Investment (%)", min_value=0, max_value=100, value=parameters["stock_percentage"] if parameters else 60)
            bond_percentage = 100 - stock_percentage  # Calculate bond percentage

    # Tab 3: Income
    with tab3:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            annual_earnings = st.number_input("Annual Earnings", value=parameters["annual_earnings"] if parameters else 200000, step=5000)
            self_yearly_increase = st.number_input("Self Yearly Increase (%)", value=parameters["self_yearly_increase"] * 100 if parameters else 5.0, step=0.5) / 100  # Convert to decimal

            st.markdown("<br>", unsafe_allow_html=True)
            tax_rate = st.number_input("Tax Rate (%)", value=parameters["tax_rate"] * 100 if parameters else 10.0, step=1.0) / 100  # Convert to decimal
        with col2:
            partner_earnings = st.number_input("Partner's Annual Earnings", value=parameters["partner_earnings"] if parameters else 200000, step=5000)
            partner_yearly_increase = st.number_input("Partner Yearly Increase (%)", value=parameters["partner_yearly_increase"] * 100 if parameters else 5.0, step=0.5) / 100  # Convert to decimal

    # Tab 4: Expense
    with tab4:
        col1, col2 , col3 = st.columns([1,1,2])
        with col1:
            annual_expense = st.number_input("Annual Expense", value=parameters["annual_expense"] if parameters else 10000 * 12, step=2000)
            mortgage_payment = st.number_input("Yearly Mortgage", value=parameters["mortgage_payment"] if parameters else 36000, step=2000)
            inflation_mean = st.number_input("Inflation Mean (%)", value=parameters["inflation_mean"] * 100 if parameters else 2.5) / 100  # Convert to decimal

        with col2:
            annual_expense_decrease = st.number_input("Annual Decrease post Retirement (Smile *) (%)", value=parameters["annual_expense_decrease"] * 100 if parameters else 0.5, step=0.05) / 100  # Convert to decimal
            mortgage_years_remaining = st.number_input("Mortgage Years Remaining", value=parameters["mortgage_years_remaining"] if parameters else 25)
            inflation_std = st.number_input("Inflation Std Dev (%)", value=parameters["inflation_std"] * 100 if parameters else 1.0) / 100  # Convert to decimal
        st.markdown("<br>", unsafe_allow_html=True)
        st.write ('###### * Smile : Research shows household expenses decrease about 1% year over year in retirement and then can increase towards end of life due to healthcare cost')

    # Tab 5: Social Security 
    with tab5:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            annual_social_security = st.number_input("Social Security", value=parameters["annual_social_security"] if parameters else 3000 * 12, step=1000)
            withdrawal_start_age = st.number_input("Withdrawal Start Age (Self)", value=parameters["withdrawal_start_age"] if parameters else 67)
            cola_rate = st.number_input("COLA Rate (%)", value=parameters["cola_rate"] * 100 if parameters else 1.50) / 100  # Convert to decimal
        with col2:
            partner_social_security = st.number_input("Partner's Social Security", value=parameters["partner_social_security"] if parameters else 1500 * 12, step=1000)
            partner_withdrawal_start_age = st.number_input("Partner's Withdrawal Start Age", value=parameters["partner_withdrawal_start_age"] if parameters else 65)

    # Tab 6: Healthcare Costs
    with tab6:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            self_healthcare_cost = st.number_input("Self Bridge Healthcare Cost (Annual)", value=parameters["self_healthcare_cost"] if parameters else 5000, step=1000)
            self_healthcare_start_age = st.number_input("Self Healthcare Bridge Start Age", value=parameters["self_healthcare_start_age"] if parameters else retirement_age)
        with col2:
            partner_healthcare_cost = st.number_input("Partner Bridge Healthcare Cost (Annual)", value=parameters["partner_healthcare_cost"] if parameters else 5000, step=1000)
            partner_healthcare_start_age = st.number_input("Partner Healthcare Bridge Start Age", value=parameters["partner_healthcare_start_age"] if parameters else partner_retirement_age)
        st.markdown("<br>", unsafe_allow_html=True)
        st.write ('###### Bridge cost is amount needed to self fund medical insurance after retirement before Medicare starts at 65')

    # Tab 7: Market Returns
    with tab7:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            stock_return_mean = st.number_input("Stock Return Mean (%)", value=parameters["stock_return_mean"] * 100 if parameters else 10.00, step=0.25) / 100  # Convert to decimal
            bond_return_mean = st.number_input("Bond Return Mean (%)", value=parameters["bond_return_mean"] * 100 if parameters else 3.75, step=0.25) / 100  # Convert to decimal
            st.markdown("<br>", unsafe_allow_html=True)
            simulations = st.number_input("Number of Simulations", value=parameters["simulations"] if parameters else 1000, step=1000)
        with col2:
            stock_return_std = st.number_input("Stock Return Std Dev (%)", value=parameters["stock_return_std"] * 100 if parameters else 19.00, step=0.25) / 100  # Convert to decimal
            bond_return_std = st.number_input("Bond Return Std Dev (%)", value=parameters["bond_return_std"] * 100 if parameters else 1.2, step=0.05) / 100  # Convert to decimal
        st.markdown("<br>", unsafe_allow_html=True)
        st.write ('###### Market Return Parameters are based on actual values of US equity (S&P 500) and Bond markets (Bloomberg) for last 100 years - similar to what Fiedilty uses')
 
    # Tab 8: Downsize
    with tab8:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            years_until_downsize = st.number_input("After how many years?", value=parameters["years_until_downsize"] if parameters else 0)
            residual_amount = st.number_input("Net Addition to Retirement Savings", value=parameters["residual_amount"] if parameters else 0, step=100000)

    # Tab 9: Adjust Recurring Expenses
    with tab9:
        st.write("##### Yearly Expense Adjustments")
        
        # Entry 1
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            adjust_expense_year_1 = st.selectbox("Year of Adjustment 1", years, index=0 if parameters is None else years.index(parameters["adjust_expense_year_1"]))
        with col2:
            adjust_expense_amount_1 = st.number_input("Adjustment Amount 1 ", value=parameters["adjust_expense_amount_1"] if parameters else 0, step=2000)
        
        # Entry 2
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            adjust_expense_year_2 = st.selectbox("Year of Adjustment 2", years, index=0 if parameters is None else years.index(parameters["adjust_expense_year_2"]))
        with col2:
            adjust_expense_amount_2 = st.number_input("Adjustment Amount 2 ", value=parameters["adjust_expense_amount_2"] if parameters else 0, step=2000)
        
        # Entry 3
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            adjust_expense_year_3 = st.selectbox("Year of Adjustment 3", years, index=0 if parameters is None else years.index(parameters["adjust_expense_year_3"]))
        with col2:
            adjust_expense_amount_3 = st.number_input("Adjustment Amount 3 ", value=parameters["adjust_expense_amount_3"] if parameters else 0, step=2000)

    # Tab 10: One-Time Expenses
    with tab10:
        st.write("##### One-Time Expenses")
        
        # Entry 1
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            one_time_year_1 = st.selectbox("Year of One-Time Expense 1", years, index=0 if parameters is None else years.index(parameters["one_time_year_1"]))
        with col2:
            one_time_amount_1 = st.number_input("One-Time Expense Amount 1 ", value=parameters["one_time_amount_1"] if parameters else 0, step=5000)
        
        # Entry 2
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            one_time_year_2 = st.selectbox("Year of One-Time Expense 2", years, index=0 if parameters is None else years.index(parameters["one_time_year_2"]))
        with col2:
            one_time_amount_2 = st.number_input("One-Time Expense Amount 2 ", value=parameters["one_time_amount_2"] if parameters else 0, step=5000)
        
        # Entry 3
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            one_time_year_3 = st.selectbox("Year of One-Time Expense 3", years, index=0 if parameters is None else years.index(parameters["one_time_year_3"]))
        with col2:
            one_time_amount_3 = st.number_input("One-Time Expense Amount 3 ", value=parameters["one_time_amount_3"] if parameters else 0, step=5000)

    # Tab 11: Windfalls
    with tab11:
        st.write("##### Windfalls")
        
        # Entry 1
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            windfall_year_1 = st.selectbox("Year of Windfall 1", years, index=0 if parameters is None else years.index(parameters["windfall_year_1"]))
        with col2:
            windfall_amount_1 = st.number_input("Windfall Amount 1 ", value=parameters["windfall_amount_1"] if parameters else 0, step=5000)
        
        # Entry 2
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            windfall_year_2 = st.selectbox("Year of Windfall 2", years, index=0 if parameters is None else years.index(parameters["windfall_year_2"]))
        with col2:
            windfall_amount_2 = st.number_input("Windfall Amount 2 ", value=parameters["windfall_amount_2"] if parameters else 0, step=5000)
        
        # Entry 3
        col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
        with col1:
            windfall_year_3 = st.selectbox("Year of Windfall 3", years, index=0 if parameters is None else years.index(parameters["windfall_year_3"]))
        with col2:
            windfall_amount_3 = st.number_input("Windfall Amount 3 ", value=parameters["windfall_amount_3"] if parameters else 0, step=5000)


# # Put the tabs inside a container with fixed height
# with st.container(height=420, border=None):

#     # set the tab styles 
#     st.markdown(tab_style_css, unsafe_allow_html=True)

#     # Create tabs for different sections
#     tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([" Personal Details ", " Investments and Savings ", " Income & Taxes", "Expense", "Social Security", "Healthcare Costs", "Market Returns", "Downsize", "Adjust Yearly Expense", "One Time Expense", "Windfall"])

#     # Tab 1: Personal Details
#     with tab1:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             current_age = st.number_input("Current Age", value=55)
#             partner_current_age = st.number_input("Partner's Current Age", value=50)
#             st.markdown("<br>", unsafe_allow_html=True)
#             life_expectancy = st.number_input("Life Expectancy", value=92)
#         with col2:
#             retirement_age = st.number_input("Retirement Age", value=60)
#             partner_retirement_age = st.number_input("Partner's Retirement Age", value=58)

#         # Calculate the range of valid years based on current age and life expectancy
#         start_year = current_year 
#         end_year = current_year + (life_expectancy - current_age)
#         # Create a list of years for drops downs 
#         years = list(range(start_year, end_year + 1))


#     # Tab 2: Investment and Savings
#     with tab2:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             initial_savings = st.number_input("Current Total Portfolio", value=2000000, step=100000)
#             st.markdown("<br>", unsafe_allow_html=True)
#             stock_percentage = st.slider("Percentage of Stock Investment (%)", min_value=0, max_value=100, value=60)
#             bond_percentage = 100 - stock_percentage  # Calculate bond percentage

#     # Tab 3: Income
#     with tab3:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             annual_earnings = st.number_input("Annual Earnings", value=200000, step=5000)
#             self_yearly_increase = st.number_input("Self Yearly Increase (%)", value=5.0, step=0.5) / 100  # Convert to decimal

#             st.markdown("<br>", unsafe_allow_html=True)
#             tax_rate = st.number_input("Tax Rate (%)", value=10.0, step=1.0) / 100  # Convert to decimal
#         with col2:
#             partner_earnings = st.number_input("Partner's Annual Earnings", value=200000, step=5000)
#             partner_yearly_increase = st.number_input("Partner Yearly Increase (%)", value=5.0, step=0.5) / 100  # Convert to decimal

#     # Tab 4: Expense
#     with tab4:
#         col1, col2 , col3 = st.columns([1,1,2])
#         with col1:
#             annual_expense = st.number_input("Annual Expense", value=10000 * 12, step=2000)
#             mortgage_payment = st.number_input("Yearly Mortgage", value=36000, step=2000)
#             inflation_mean = st.number_input("Inflation Mean (%)", value=2.5) / 100  # Convert to decimal

#         with col2:
#             annual_expense_decrease = st.number_input("Annual Decrease post Retirement (Smile *) (%)", value=0.5, step=0.05) / 100  # Convert to decimal
#             mortgage_years_remaining = st.number_input("Mortgage Years Remaining", value=25)
#             inflation_std = st.number_input("Inflation Std Dev (%)", value=1.0) / 100  # Convert to decimal
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.write ('###### * Smile : Research shows household expenses decrease about 1% year over year in retirement and then can increase towards end of life due to healthcare cost')

#     # Tab 5: Social Security 
#     with tab5:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             annual_social_security = st.number_input("Social Security", value=3000 * 12, step=1000)
#             withdrawal_start_age = st.number_input("Withdrawal Start Age (Self)", value=67)
#             cola_rate = st.number_input("COLA Rate (%)", value=1.50) / 100  # Convert to decimal
#         with col2:
#             partner_social_security = st.number_input("Partner's Social Security", value=1500 * 12, step=1000)
#             partner_withdrawal_start_age = st.number_input("Partner's Withdrawal Start Age", value=65)

#     # Tab 6: Healthcare Costs
#     with tab6:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             self_healthcare_cost = st.number_input("Self Bridge Healthcare Cost (Annual)", value=5000, step=1000)
#             self_healthcare_start_age = st.number_input("Self Healthcare Bridge Start Age", value=retirement_age)
#         with col2:
#             partner_healthcare_cost = st.number_input("Partner Bridge Healthcare Cost (Annual)", value=5000, step=1000)
#             partner_healthcare_start_age = st.number_input("Partner Healthcare Bridge Start Age", value=partner_retirement_age)
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.write ('###### Bridge cost is amount needed to self fund medical insurance after retirement before Medicare starts at 65')

#     # Tab 7: Market Returns
#     with tab7:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             stock_return_mean = st.number_input("Stock Return Mean (%)", value=10.00, step=0.25) / 100  # Convert to decimal
#             bond_return_mean = st.number_input("Bond Return Mean (%)", value=3.75, step=0.25) / 100  # Convert to decimal
#             st.markdown("<br>", unsafe_allow_html=True)
#             simulations = st.number_input("Number of Simulations", value=1000, step=1000)
#         with col2:
#             stock_return_std = st.number_input("Stock Return Std Dev (%)", value=19.00, step=0.25) / 100  # Convert to decimal
#             bond_return_std = st.number_input("Bond Return Std Dev (%)", value=1.2, step=0.05) / 100  # Convert to decimal
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.write ('###### Market Return Parameters are based on actual values of US equity (S&P 500) and Bond markets (Bloomberg) for last 100 years - similar to what Fiedilty uses')
 
#     # Tab 8: Downsize
#     with tab8:
#         col1, col2, col3 = st.columns([1,1,2])
#         with col1:
#             years_until_downsize = st.number_input("After how many years?", value=0)
#             residual_amount = st.number_input("Net Addition to Retirement Savings", value=0, step=100000)

#     # Tab 9: Adjust Recurring Expenses
#     with tab9:
#         st.write("##### Yearly Expense Adjustments")
        
#         # Entry 1
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             adjust_expense_year_1 = st.selectbox("Year of Adjustment 1", years, key="year_adjustment_1")
#         with col2:
#             adjust_expense_amount_1 = st.number_input("Adjustment Amount 1 ", value=0, step=2000, key="amount_adjustment_1")
        
#         # Entry 2
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             adjust_expense_year_2 = st.selectbox("Year of Adjustment 2", years, key="year_adjustment_2")
#         with col2:
#             adjust_expense_amount_2 = st.number_input("Adjustment Amount 2 ", value=0, step=2000, key="amount_adjustment_2")
        
#         # Entry 3
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             adjust_expense_year_3 = st.selectbox("Year of Adjustment 3", years, key="year_adjustment_3")
#         with col2:
#             adjust_expense_amount_3 = st.number_input("Adjustment Amount 3 ", value=0, step=2000, key="amount_adjustment_3")


#     # Tab 10: One-Time Expenses
#     with tab10:
#         st.write("##### One-Time Expenses")
        
#         # Entry 1
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             one_time_year_1 = st.selectbox("Year of One-Time Expense 1", years, key="one_time_year_1")
#         with col2:
#             one_time_amount_1 = st.number_input("One-Time Expense Amount 1 ", value=0, step=5000, key="one_time_amount_1")
        
#         # Entry 2
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             one_time_year_2 = st.selectbox("Year of One-Time Expense 2", years, key="one_time_year_2")
#         with col2:
#             one_time_amount_2 = st.number_input("One-Time Expense Amount 2 ", value=0, step=5000, key="one_time_amount_2")
        
#         # Entry 3
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             one_time_year_3 = st.selectbox("Year of One-Time Expense 3", years, key="one_time_year_3")
#         with col2:
#             one_time_amount_3 = st.number_input("One-Time Expense Amount 3 ", value=0, step=5000, key="one_time_amount_3")

#     # Tab 11: Windfalls
#     with tab11:
#         st.write("##### Windfalls")
        
#         # Entry 1
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             windfall_year_1 = st.selectbox("Year of Windfall 1", years, key="windfall_year_1")
#         with col2:
#             windfall_amount_1 = st.number_input("Windfall Amount 1 ", value=0, step=5000, key="windfall_amount_1")
        
#         # Entry 2
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             windfall_year_2 = st.selectbox("Year of Windfall 2", years, key="windfall_year_2")
#         with col2:
#             windfall_amount_2 = st.number_input("Windfall Amount 2 ", value=0, step=5000, key="windfall_amount_2")
        
#         # Entry 3
#         col1, col2, col3 = st.columns([1, 1, 2])  # Adjust column widths as needed
#         with col1:
#             windfall_year_3 = st.selectbox("Year of Windfall 3", years, key="windfall_year_3")
#         with col2:
#             windfall_amount_3 = st.number_input("Windfall Amount 3 ", value=0, step=5000, key="windfall_amount_3")


# Create download parameters feature 
params_df = create_parameters_dataframe(
    current_age, partner_current_age, life_expectancy, retirement_age,
    partner_retirement_age, initial_savings, stock_percentage, bond_percentage,
    annual_earnings, self_yearly_increase, tax_rate, partner_earnings,
    partner_yearly_increase, annual_expense, mortgage_payment, inflation_mean,
    annual_expense_decrease, mortgage_years_remaining, inflation_std,
    annual_social_security, withdrawal_start_age, cola_rate,
    partner_social_security, partner_withdrawal_start_age,
    self_healthcare_cost, self_healthcare_start_age,
    partner_healthcare_cost, partner_healthcare_start_age,
    stock_return_mean, bond_return_mean, simulations,
    stock_return_std, bond_return_std, years_until_downsize,
    residual_amount, adjust_expense_year_1, adjust_expense_amount_1,
    adjust_expense_year_2, adjust_expense_amount_2,
    adjust_expense_year_3, adjust_expense_amount_3,
    one_time_year_1, one_time_amount_1,
    one_time_year_2, one_time_amount_2,
    one_time_year_3, one_time_amount_3,
    windfall_year_1, windfall_amount_1,
    windfall_year_2, windfall_amount_2,
    windfall_year_3, windfall_amount_3
)

# Convert DataFrame to CSV format
csv = params_df.to_csv(index=False)  # Convert DataFrame to CSV format

# Add download button for the CSV file
st.download_button(
    label="Download Simulation Parameters",
    data=csv,
    type='primary',
    file_name='retirement_parameters.csv',
    mime='text/csv',
    icon=":material/download:",
)


# Calculate earning years
earning_years = retirement_age - current_age
partner_earning_years = partner_retirement_age - partner_current_age

# packe Adjustments
adjust_expense_years = [adjust_expense_year_1, adjust_expense_year_2, adjust_expense_year_3]
adjust_expense_amounts = [adjust_expense_amount_1, adjust_expense_amount_2, adjust_expense_amount_3]

# Pack One-Time Expenses
one_time_years = [one_time_year_1, one_time_year_2, one_time_year_3]
one_time_amounts = [one_time_amount_1, one_time_amount_2, one_time_amount_3]

# Pack Windfalls
windfall_years = [windfall_year_1, windfall_year_2, windfall_year_3]
windfall_amounts = [windfall_amount_1, windfall_amount_2, windfall_amount_3]



# Run the simulation
success_count, failure_count, cash_flow_10th, cash_flow_50th, cash_flow_90th = monte_carlo_simulation(
    current_age, partner_current_age, life_expectancy, initial_savings, 
    annual_earnings, partner_earnings, self_yearly_increase, partner_yearly_increase,
    annual_expense, mortgage_payment,
    mortgage_years_remaining, retirement_age, partner_retirement_age, 
    annual_social_security, withdrawal_start_age, partner_social_security, 
    partner_withdrawal_start_age, self_healthcare_cost, self_healthcare_start_age, partner_healthcare_start_age,
    partner_healthcare_cost, stock_percentage, bond_percentage, 
    stock_return_mean, bond_return_mean, stock_return_std, bond_return_std, 
    simulations, tax_rate, cola_rate, inflation_mean, inflation_std, annual_expense_decrease, 
    years_until_downsize, residual_amount, 
    adjust_expense_years, adjust_expense_amounts,  
    one_time_years, one_time_amounts,             
    windfall_years, windfall_amounts        
)

# Prepare data for display for each percentile
df_cashflow_10th = pd.DataFrame(cash_flow_10th)
df_cashflow_50th = pd.DataFrame(cash_flow_50th)
df_cashflow_90th = pd.DataFrame(cash_flow_90th)

# Function to format the DataFrame
def format_cashflow_dataframe(df):
    if df.empty:
        return df

    # Format Amount Columns
    numeric_columns = [
        'Beginning Portfolio Value', 'Self Gross Earning', 'Partner Gross Earning',
        'Self Social Security', 'Partner Social Security', 'Gross Earnings', 'Combined Social Security',
        'Investment Return', 'Downsize Proceeds', 'Mortgage', 'Healthcare Expense', 'Self Health Expense',  'Partner Health Expense',
        'Total Expense', 'Tax', 'Portfolio Draw', 'Ending Portfolio Value', 'Yearly Expense Adj', 'One Time Expense', 'Windfall Amt'
    ]

    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: f"{x:,.0f}")

    # Format % Columns 
    percent_columns = [
        'Investment Return %', 
        'Drawdown %' 
    ]
    for col in percent_columns:
        df[col] = df[col].apply(lambda x: f"{x * 100:.2f}%")  # Multiply by 100 and format to 2 decimal places


    return df

# Format the DataFrames
df_cashflow_10th = format_cashflow_dataframe(df_cashflow_10th)
df_cashflow_50th = format_cashflow_dataframe(df_cashflow_50th)
df_cashflow_90th = format_cashflow_dataframe(df_cashflow_90th)

# Display success and failure rates
total_simulations = success_count + failure_count
success_rate = (success_count / total_simulations) * 100 if total_simulations > 0 else 0
failure_rate = (failure_count / total_simulations) * 100 if total_simulations > 0 else 0


st.write("## Simulation Results")

st.markdown(create_linear_indicator(math.floor(success_rate), "Success Probablity: "), unsafe_allow_html=True)

# Extract the end-of-period balances for the 10th, 50th, and 90th percentiles
end_balance_10th = df_cashflow_10th['Ending Portfolio Value'].iloc[-1]  # Last entry for 10th percentile
end_balance_50th = df_cashflow_50th['Ending Portfolio Value'].iloc[-1]  # Last entry for 50th percentile
end_balance_90th = df_cashflow_90th['Ending Portfolio Value'].iloc[-1]  # Last entry for 90th percentile


# Convert balances to millions and format to 2 decimal places
end_balance_10th_millions = float(end_balance_10th.replace(',', '')) / 1_000_000
end_balance_50th_millions = float(end_balance_50th.replace(',', '')) / 1_000_000
end_balance_90th_millions = float(end_balance_90th.replace(',', '')) / 1_000_000

# Display the end-of-period balances
st.markdown(display_balances(end_balance_10th_millions, end_balance_50th_millions, end_balance_90th_millions), unsafe_allow_html=True)


# Function to convert formatted string to numerical value
def convert_to_numeric(value):
    return float(value.replace('$', '').replace(',', ''))

# Function to apply conditional styling
def highlight_columns(s):
    styles = []
    for value in s:
        numeric_value = convert_to_numeric(value)
        if numeric_value > 0:
            styles.append('background-color: #ECFBEC; font-weight: bold;')  # Green background for positive values
        else:
            styles.append('background-color: #F9DFDF; font-weight: bold;')    # Red background for negative values
    return styles


st.markdown("<br>", unsafe_allow_html=True)
st.write("### Yearly Cash Flow Summary ")
st.markdown("<br>", unsafe_allow_html=True)
# Create tabs for the cash flow summaries
tab_50th, tab_10th, tab_90th = st.tabs(["Most Likely", "Worst Case", "Best Case"])

# Tab for 50th Percentile
with tab_50th:
    # Apply the styling to specific columns
    styled_df_50th = df_cashflow_50th.style.apply(highlight_columns, subset=['Beginning Portfolio Value', 'Ending Portfolio Value'])
    
    # Display the content
    st.write("##### 50th Percentile Simulation")
    st.dataframe(styled_df_50th, hide_index=True, use_container_width=True)

    # Create a container for the charts
    st.subheader("Portfolio Balance Over Time")
    # Plotting the results using Streamlit's line chart for the 50th percentile
    st.line_chart(df_cashflow_50th.set_index('Year')['Ending Portfolio Value'].str.replace(',', '').astype(float))

# Tab for 10th Percentile
with tab_10th:
    # Apply the styling to specific columns
    styled_df_10th = df_cashflow_10th.style.apply(highlight_columns, subset=['Beginning Portfolio Value', 'Ending Portfolio Value'])
    
    # Display the content
    st.write("##### 10th Percentile Simulation")
    st.dataframe(styled_df_10th, hide_index=True, use_container_width=True)
    st.subheader("Portfolio Balance Over Time")
    # Plotting the results using Streamlit's line chart for the 50th percentile
    st.line_chart(df_cashflow_10th.set_index('Year')['Ending Portfolio Value'].str.replace(',', '').astype(float))


# Tab for 90th Percentile
with tab_90th:
    # Apply the styling to specific columns
    styled_df_90th = df_cashflow_90th.style.apply(highlight_columns, subset=['Beginning Portfolio Value', 'Ending Portfolio Value'])
    
    # Display the content
    st.write("##### 90th Percentile Simulation")
    st.dataframe(styled_df_90th, hide_index=True, use_container_width=True)
    st.subheader("Portfolio Balance Over Time")
    # Plotting the results using Streamlit's line chart for the 50th percentile
    st.line_chart(df_cashflow_90th.set_index('Year')['Ending Portfolio Value'].str.replace(',', '').astype(float))