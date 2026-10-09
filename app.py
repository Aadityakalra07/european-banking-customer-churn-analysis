import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="European Banking | Customer Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATA LOADING
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "processed_data"


@st.cache_data
def load_data():
    data = pd.read_csv(
        DATA_DIR / "customers_cleaned.csv"
    )

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "Dataset not found. Make sure "
        "'customers_cleaned.csv' exists inside "
        "the processed_data folder."
    )
    st.stop()


# =========================================================
# VALIDATE REQUIRED COLUMNS
# =========================================================

required_columns = [
    "CustomerId",
    "Geography",
    "Gender",
    "Age",
    "AgeGroup",
    "TenureGroup",
    "CreditScoreBand",
    "BalanceSegment",
    "IsActiveMember",
    "EstimatedSalary",
    "Balance",
    "Exited"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Required columns are missing: {missing_columns}"
    )
    st.stop()


# =========================================================
# SIDEBAR — PROJECT INFORMATION
# =========================================================

st.sidebar.title("🏦 Banking Analytics")

st.sidebar.caption(
    "Customer Segmentation & Churn Pattern Analytics"
)

st.sidebar.divider()

st.sidebar.subheader("Customer Filters")


# Geography filter

geographies = sorted(
    df["Geography"].dropna().unique().tolist()
)

selected_geographies = st.sidebar.multiselect(
    "Geography",
    options=geographies,
    default=geographies
)


# Age group filter

age_order = [
    "<30",
    "30–45",
    "46–60",
    "60+"
]

available_age_groups = [
    age
    for age in age_order
    if age in df["AgeGroup"].unique()
]

selected_age_groups = st.sidebar.multiselect(
    "Age Group",
    options=available_age_groups,
    default=available_age_groups
)


# Tenure filter

tenure_order = [
    "New",
    "Mid-term",
    "Long-term"
]

available_tenure_groups = [
    tenure
    for tenure in tenure_order
    if tenure in df["TenureGroup"].unique()
]

selected_tenure_groups = st.sidebar.multiselect(
    "Tenure Group",
    options=available_tenure_groups,
    default=available_tenure_groups
)


# Gender filter

genders = sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_genders = st.sidebar.multiselect(
    "Gender",
    options=genders,
    default=genders
)


# Credit score filter

credit_order = [
    "Low",
    "Medium",
    "High"
]

available_credit_bands = [
    band
    for band in credit_order
    if band in df["CreditScoreBand"].unique()
]

selected_credit_bands = st.sidebar.multiselect(
    "Credit Score Band",
    options=available_credit_bands,
    default=available_credit_bands
)


# Balance filter

balance_order = [
    "Zero-balance",
    "Low-balance",
    "High-balance"
]

available_balance_segments = [
    segment
    for segment in balance_order
    if segment in df["BalanceSegment"].unique()
]

selected_balance_segments = st.sidebar.multiselect(
    "Balance Segment",
    options=available_balance_segments,
    default=available_balance_segments
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["Geography"].isin(selected_geographies)
    & df["AgeGroup"].isin(selected_age_groups)
    & df["TenureGroup"].isin(selected_tenure_groups)
    & df["Gender"].isin(selected_genders)
    & df["CreditScoreBand"].isin(selected_credit_bands)
    & df["BalanceSegment"].isin(selected_balance_segments)
].copy()


# =========================================================
# DASHBOARD HEADER
# =========================================================

st.title(
    "Customer Segmentation & Churn Analytics"
)

st.markdown(
    """
    Analyze customer churn patterns across European banking
    markets, demographic groups, customer tenure, and
    financial segments.
    """
)

st.divider()


# =========================================================
# OVERALL CHURN SUMMARY
# =========================================================

st.subheader("Overall Churn Summary")

total_customers = len(filtered_df)

churned_customers = int(
    filtered_df["Exited"].sum()
)

retained_customers = (
    total_customers - churned_customers
)

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0
    else 0
)

retention_rate = (
    retained_customers / total_customers * 100
    if total_customers > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churned Customers",
    f"{churned_customers:,}"
)

col3.metric(
    "Retained Customers",
    f"{retained_customers:,}"
)

col4.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)


st.caption(
    "KPIs update dynamically according to the selected "
    "customer segment filters."
)


# =========================================================
# CHURN DISTRIBUTION
# =========================================================

st.divider()

st.subheader("Customer Churn Distribution")


if total_customers > 0:

    churn_distribution = pd.DataFrame({
        "Customer Status": [
            "Retained",
            "Churned"
        ],
        "Customers": [
            retained_customers,
            churned_customers
        ]
    })

    fig = px.pie(
        churn_distribution,
        names="Customer Status",
        values="Customers",
        hole=0.55,
        title="Retained vs Churned Customers"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent"
    )

    fig.update_layout(
        legend_title_text="Customer Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "No customers match the selected filters. "
        "Adjust the filters to view the dashboard."
    )


# =========================================================
# CUSTOMER DATA PREVIEW
# =========================================================

st.divider()

st.subheader("Customer Segment Explorer")

st.write(
    "Explore customer records matching the selected filters."
)

display_columns = [
    "CustomerId",
    "Geography",
    "Gender",
    "AgeGroup",
    "TenureGroup",
    "CreditScoreBand",
    "BalanceSegment",
    "IsActiveMember",
    "Balance",
    "EstimatedSalary",
    "Exited"
]

if total_customers > 0:

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Showing {total_customers:,} matching customer records."
    )

else:

    st.info(
        "No customer records are available for the "
        "current filter selection."
    )
# =========================================================
# MODULE 2 — GEOGRAPHY-WISE CHURN ANALYSIS
# =========================================================

st.divider()

st.header("Geography-Wise Churn Analysis")

st.markdown(
    """
    Compare customer churn across France, Germany, and Spain
    to identify regional differences in customer retention.
    """
)

if not filtered_df.empty:

    # Calculate country-level metrics using the active filters
    geography_analysis = (
        filtered_df.groupby("Geography")
        .agg(
            Customer_Count=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum")
        )
        .reset_index()
    )

    geography_analysis["Retained_Customers"] = (
        geography_analysis["Customer_Count"]
        - geography_analysis["Churned_Customers"]
    )

    geography_analysis["Churn_Rate_%"] = (
        geography_analysis["Churned_Customers"]
        / geography_analysis["Customer_Count"]
        * 100
    ).round(2)

    # Overall churn rate for the currently filtered population
    filtered_overall_churn = (
        filtered_df["Exited"].mean() * 100
    )

    # Geographic Risk Index:
    # Country churn rate / overall filtered churn rate
    if filtered_overall_churn > 0:

        geography_analysis["Geographic_Risk_Index"] = (
            geography_analysis["Churn_Rate_%"]
            / filtered_overall_churn
        ).round(2)

    else:

        geography_analysis["Geographic_Risk_Index"] = np.nan

    # Sort by the official country order
    country_order = ["France", "Germany", "Spain"]

    geography_analysis["Country_Order"] = (
        geography_analysis["Geography"]
        .map({
            country: index
            for index, country in enumerate(country_order)
        })
    )

    geography_analysis = (
        geography_analysis
        .sort_values("Country_Order")
        .drop(columns="Country_Order")
    )

    # -----------------------------------------------------
    # COUNTRY SUMMARY
    # -----------------------------------------------------

    st.subheader("Regional Churn Summary")

    geo_col1, geo_col2, geo_col3 = st.columns(3)

    for column, country in zip(
        [geo_col1, geo_col2, geo_col3],
        country_order
    ):

        country_data = geography_analysis[
            geography_analysis["Geography"] == country
        ]

        if not country_data.empty:

            row = country_data.iloc[0]

            column.metric(
                label=f"{country} Churn Rate",
                value=f"{row['Churn_Rate_%']:.2f}%",
                help=(
                    f"Customers: {int(row['Customer_Count']):,} | "
                    f"Churned: {int(row['Churned_Customers']):,}"
                )
            )

        else:

            column.metric(
                label=f"{country} Churn Rate",
                value="N/A"
            )

    # -----------------------------------------------------
    # CHURN RATE CHART
    # -----------------------------------------------------

    st.subheader("Churn Rate by Country")

    geography_chart = px.bar(
        geography_analysis,
        x="Geography",
        y="Churn_Rate_%",
        text="Churn_Rate_%",
        hover_data=[
            "Customer_Count",
            "Churned_Customers",
            "Retained_Customers"
        ],
        labels={
            "Geography": "Country",
            "Churn_Rate_%": "Churn Rate (%)",
            "Customer_Count": "Total Customers",
            "Churned_Customers": "Churned Customers",
            "Retained_Customers": "Retained Customers"
        },
        title="Customer Churn Rate Across European Countries"
    )

    geography_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    geography_chart.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Country",
        yaxis_range=[
            0,
            max(
                5,
                geography_analysis["Churn_Rate_%"].max() * 1.2
            )
        ]
    )

    st.plotly_chart(
        geography_chart,
        use_container_width=True
    )

    # -----------------------------------------------------
    # GEOGRAPHIC RISK INDEX
    # -----------------------------------------------------

    st.subheader("Geographic Risk Index")

    st.caption(
        "Index = Country churn rate ÷ overall churn rate "
        "for the currently filtered population. "
        "Values above 1 indicate above-average churn."
    )

    risk_chart = px.bar(
        geography_analysis,
        x="Geography",
        y="Geographic_Risk_Index",
        text="Geographic_Risk_Index",
        labels={
            "Geography": "Country",
            "Geographic_Risk_Index": "Geographic Risk Index"
        },
        title="Regional Churn Risk Relative to the Overall Rate"
    )

    risk_chart.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    risk_chart.add_hline(
        y=1,
        line_dash="dash",
        annotation_text="Overall churn benchmark"
    )

    risk_chart.update_layout(
        yaxis_title="Geographic Risk Index",
        xaxis_title="Country"
    )

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

    # -----------------------------------------------------
    # DETAILED TABLE
    # -----------------------------------------------------

    st.subheader("Regional Performance Details")

    display_geography = geography_analysis.copy()

    display_geography["Geographic_Risk_Index"] = (
        display_geography["Geographic_Risk_Index"]
        .round(2)
    )

    st.dataframe(
        display_geography,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # AUTOMATIC OBSERVATION
    # -----------------------------------------------------

    if not geography_analysis.empty:

        highest_risk_country = geography_analysis.loc[
            geography_analysis["Churn_Rate_%"].idxmax()
        ]

        st.info(
            f"**Highest churn rate:** "
            f"{highest_risk_country['Geography']} "
            f"({highest_risk_country['Churn_Rate_%']:.2f}%). "
            f"This result reflects the currently selected filters."
        )

else:

    st.warning(
        "No customers match the current filters. "
        "Adjust the sidebar selections to view geographic analysis."
    )
# =========================================================
# MODULE 3 — AGE & TENURE CHURN COMPARISON
# =========================================================

st.divider()

st.header("Age & Tenure Churn Comparison")

st.markdown(
    """
    Compare churn across customer age groups and banking
    tenure to identify segments with different retention patterns.
    """
)

if not filtered_df.empty:

    # -----------------------------------------------------
    # AGE-WISE CHURN ANALYSIS
    # -----------------------------------------------------

    st.subheader("Age-Wise Churn Analysis")

    age_order = ["<30", "30–45", "46–60", "60+"]

    age_analysis = (
        filtered_df.groupby("AgeGroup", observed=False)
        .agg(
            Customer_Count=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum")
        )
        .reset_index()
    )

    age_analysis["Retained_Customers"] = (
        age_analysis["Customer_Count"]
        - age_analysis["Churned_Customers"]
    )

    age_analysis["Churn_Rate_%"] = (
        age_analysis["Churned_Customers"]
        / age_analysis["Customer_Count"]
        .replace(0, np.nan)
        * 100
    ).round(2)

    age_analysis["Age_Order"] = (
        age_analysis["AgeGroup"]
        .map({
            group: index
            for index, group in enumerate(age_order)
        })
    )

    age_analysis = (
        age_analysis
        .sort_values("Age_Order")
        .drop(columns="Age_Order")
    )

    age_chart = px.bar(
        age_analysis,
        x="AgeGroup",
        y="Churn_Rate_%",
        text="Churn_Rate_%",
        hover_data=[
            "Customer_Count",
            "Churned_Customers",
            "Retained_Customers"
        ],
        labels={
            "AgeGroup": "Age Group",
            "Churn_Rate_%": "Churn Rate (%)",
            "Customer_Count": "Total Customers",
            "Churned_Customers": "Churned Customers",
            "Retained_Customers": "Retained Customers"
        },
        title="Churn Rate Across Customer Age Groups"
    )

    age_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    age_chart.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Churn Rate (%)"
    )

    st.plotly_chart(
        age_chart,
        use_container_width=True
    )

    st.dataframe(
        age_analysis,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # TENURE-WISE CHURN ANALYSIS
    # -----------------------------------------------------

    st.divider()

    st.subheader("Tenure-Wise Churn Analysis")

    tenure_order = [
        "New",
        "Mid-term",
        "Long-term"
    ]

    tenure_analysis = (
        filtered_df.groupby("TenureGroup", observed=False)
        .agg(
            Customer_Count=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum")
        )
        .reset_index()
    )

    tenure_analysis["Retained_Customers"] = (
        tenure_analysis["Customer_Count"]
        - tenure_analysis["Churned_Customers"]
    )

    tenure_analysis["Churn_Rate_%"] = (
        tenure_analysis["Churned_Customers"]
        / tenure_analysis["Customer_Count"]
        .replace(0, np.nan)
        * 100
    ).round(2)

    tenure_analysis["Tenure_Order"] = (
        tenure_analysis["TenureGroup"]
        .map({
            group: index
            for index, group in enumerate(tenure_order)
        })
    )

    tenure_analysis = (
        tenure_analysis
        .sort_values("Tenure_Order")
        .drop(columns="Tenure_Order")
    )

    tenure_chart = px.bar(
        tenure_analysis,
        x="TenureGroup",
        y="Churn_Rate_%",
        text="Churn_Rate_%",
        hover_data=[
            "Customer_Count",
            "Churned_Customers",
            "Retained_Customers"
        ],
        labels={
            "TenureGroup": "Tenure Group",
            "Churn_Rate_%": "Churn Rate (%)",
            "Customer_Count": "Total Customers",
            "Churned_Customers": "Churned Customers",
            "Retained_Customers": "Retained Customers"
        },
        title="Churn Rate Across Customer Tenure Groups"
    )

    tenure_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    tenure_chart.update_layout(
        xaxis_title="Tenure Group",
        yaxis_title="Churn Rate (%)"
    )

    st.plotly_chart(
        tenure_chart,
        use_container_width=True
    )

    st.dataframe(
        tenure_analysis,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # CUSTOMER DISTRIBUTION BY AGE AND TENURE
    # -----------------------------------------------------

    st.divider()

    st.subheader("Customer Distribution by Age & Tenure")

    age_tenure_analysis = (
        filtered_df
        .groupby(
            ["AgeGroup", "TenureGroup"],
            observed=False
        )
        .agg(
            Customer_Count=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum")
        )
        .reset_index()
    )

    age_tenure_analysis["Churn_Rate_%"] = (
        age_tenure_analysis["Churned_Customers"]
        / age_tenure_analysis["Customer_Count"]
        .replace(0, np.nan)
        * 100
    ).round(2)

    age_tenure_chart = px.density_heatmap(
        age_tenure_analysis,
        x="TenureGroup",
        y="AgeGroup",
        z="Churn_Rate_%",
        category_orders={
            "AgeGroup": age_order,
            "TenureGroup": tenure_order
        },
        text_auto=".2f",
        labels={
            "AgeGroup": "Age Group",
            "TenureGroup": "Tenure Group",
            "Churn_Rate_%": "Churn Rate (%)"
        },
        title="Churn Rate by Age and Tenure"
    )

    st.plotly_chart(
        age_tenure_chart,
        use_container_width=True
    )

    st.caption(
        "The heatmap shows churn rates for each age and tenure "
        "combination. Hover over a cell to inspect its value."
    )

    # -----------------------------------------------------
    # KEY OBSERVATIONS
    # -----------------------------------------------------

    st.divider()

    st.subheader("Age & Tenure Observations")

    valid_age = age_analysis.dropna(
        subset=["Churn_Rate_%"]
    )

    valid_tenure = tenure_analysis.dropna(
        subset=["Churn_Rate_%"]
    )

    observation_col1, observation_col2 = st.columns(2)

    with observation_col1:

        if not valid_age.empty:

            highest_age = valid_age.loc[
                valid_age["Churn_Rate_%"].idxmax()
            ]

            st.info(
                f"**Highest-churn age group:** "
                f"{highest_age['AgeGroup']} "
                f"({highest_age['Churn_Rate_%']:.2f}%)."
            )

    with observation_col2:

        if not valid_tenure.empty:

            highest_tenure = valid_tenure.loc[
                valid_tenure["Churn_Rate_%"].idxmax()
            ]

            st.info(
                f"**Highest-churn tenure group:** "
                f"{highest_tenure['TenureGroup']} "
                f"({highest_tenure['Churn_Rate_%']:.2f}%)."
            )

else:

    st.warning(
        "No customers match the current filters. "
        "Adjust the sidebar selections to view age and tenure analysis."
    )

    # =========================================================
# MODULE 4 — HIGH-VALUE CUSTOMER CHURN EXPLORER
# =========================================================

st.divider()

st.header("High-Value Customer Churn Explorer")

st.markdown(
    """
    Explore churn among high-balance customers, compare financial
    profiles, and examine the account balance exposure associated
    with churn.
    """
)

if not filtered_df.empty:

    # -----------------------------------------------------
    # 1. IDENTIFY HIGH-VALUE CUSTOMERS
    # -----------------------------------------------------

    # High-balance customers are used as the project's
    # operational proxy for high-value customers.

    high_value_df = filtered_df[
        filtered_df["BalanceSegment"] == "High-balance"
    ].copy()

    high_value_total = len(high_value_df)

    high_value_churners = high_value_df[
        high_value_df["Exited"] == 1
    ].copy()

    high_value_retained = high_value_df[
        high_value_df["Exited"] == 0
    ].copy()

    high_value_churned_count = len(high_value_churners)

    high_value_retained_count = len(high_value_retained)

    high_value_churn_rate = (
        high_value_churned_count / high_value_total * 100
        if high_value_total > 0
        else 0
    )

    # -----------------------------------------------------
    # 2. HIGH-VALUE CUSTOMER KPI CARDS
    # -----------------------------------------------------

    st.subheader("High-Value Customer Overview")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "High-Balance Customers",
        f"{high_value_total:,}"
    )

    kpi2.metric(
        "High-Balance Churners",
        f"{high_value_churned_count:,}"
    )

    kpi3.metric(
        "High-Value Churn Rate",
        f"{high_value_churn_rate:.2f}%"
    )

    kpi4.metric(
        "High-Value Retained",
        f"{high_value_retained_count:,}"
    )

    # High-value churn ratio:
    # High-value churners / all churners in filtered population.

    total_filtered_churners = int(filtered_df["Exited"].sum())

    high_value_churn_ratio = (
        high_value_churned_count / total_filtered_churners * 100
        if total_filtered_churners > 0
        else 0
    )

    st.metric(
        "High-Value Churn Ratio",
        f"{high_value_churn_ratio:.2f}%",
        help=(
            "Percentage of all churned customers in the currently "
            "filtered population who belong to the high-balance segment."
        )
    )

    # -----------------------------------------------------
    # 3. CHURN RATE BY BALANCE SEGMENT
    # -----------------------------------------------------

    st.divider()

    st.subheader("Churn Across Balance Segments")

    balance_order = [
        "Zero-balance",
        "Low-balance",
        "High-balance"
    ]

    balance_analysis = (
        filtered_df.groupby("BalanceSegment")
        .agg(
            Customer_Count=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum")
        )
        .reset_index()
    )

    balance_analysis["Churn_Rate_%"] = (
        balance_analysis["Churned_Customers"]
        / balance_analysis["Customer_Count"].replace(0, np.nan)
        * 100
    ).round(2)

    balance_analysis["Balance_Order"] = (
        balance_analysis["BalanceSegment"]
        .map({
            segment: index
            for index, segment in enumerate(balance_order)
        })
    )

    balance_analysis = (
        balance_analysis
        .sort_values("Balance_Order")
        .drop(columns="Balance_Order")
    )

    balance_chart = px.bar(
        balance_analysis,
        x="BalanceSegment",
        y="Churn_Rate_%",
        text="Churn_Rate_%",
        hover_data=[
            "Customer_Count",
            "Churned_Customers"
        ],
        title="Churn Rate by Balance Segment",
        labels={
            "BalanceSegment": "Balance Segment",
            "Churn_Rate_%": "Churn Rate (%)",
            "Customer_Count": "Total Customers",
            "Churned_Customers": "Churned Customers"
        }
    )

    balance_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    balance_chart.update_layout(
        xaxis_title="Balance Segment",
        yaxis_title="Churn Rate (%)"
    )

    st.plotly_chart(
        balance_chart,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 4. SALARY VS BALANCE COMPARISON
    # -----------------------------------------------------

    st.divider()

    st.subheader("Estimated Salary vs Account Balance")

    st.caption(
        "Compare the financial profiles of churned and retained "
        "customers. Estimated salary is not actual bank revenue."
    )

    salary_balance_df = filtered_df.copy()

    salary_balance_df["Customer Status"] = (
        salary_balance_df["Exited"]
        .map({
            0: "Retained",
            1: "Churned"
        })
    )

    salary_balance_chart = px.scatter(
        salary_balance_df,
        x="EstimatedSalary",
        y="Balance",
        color="Customer Status",
        opacity=0.65,
        hover_data=[
            "CustomerId",
            "Geography",
            "AgeGroup",
            "BalanceSegment"
        ],
        labels={
            "EstimatedSalary": "Estimated Salary",
            "Balance": "Account Balance"
        },
        title="Salary and Account Balance by Customer Status"
    )

    salary_balance_chart.update_layout(
        xaxis_title="Estimated Salary",
        yaxis_title="Account Balance"
    )

    st.plotly_chart(
        salary_balance_chart,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 5. FINANCIAL PROFILE COMPARISON
    # -----------------------------------------------------

    st.subheader("Churned vs Retained Financial Profiles")

    financial_profile = (
        filtered_df.groupby("Exited")
        .agg(
            Customer_Count=("CustomerId", "count"),
            Average_Balance=("Balance", "mean"),
            Median_Balance=("Balance", "median"),
            Average_Salary=("EstimatedSalary", "mean"),
            Median_Salary=("EstimatedSalary", "median")
        )
        .reset_index()
    )

    financial_profile["Customer_Status"] = (
        financial_profile["Exited"]
        .map({
            0: "Retained",
            1: "Churned"
        })
    )

    financial_profile = financial_profile[
        [
            "Customer_Status",
            "Customer_Count",
            "Average_Balance",
            "Median_Balance",
            "Average_Salary",
            "Median_Salary"
        ]
    ].round(2)

    st.dataframe(
        financial_profile,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # 6. BALANCE EXPOSURE ASSOCIATED WITH CHURN
    # -----------------------------------------------------

    st.divider()

    st.subheader("Balance Exposure Associated with Churn")

    total_churned_balance = filtered_df.loc[
        filtered_df["Exited"] == 1,
        "Balance"
    ].sum()

    high_value_churned_balance = high_value_churners[
        "Balance"
    ].sum()

    high_value_balance_share = (
        high_value_churned_balance / total_churned_balance * 100
        if total_churned_balance > 0
        else 0
    )

    exposure_col1, exposure_col2, exposure_col3 = st.columns(3)

    exposure_col1.metric(
        "Total Churned-Customer Balance",
        f"{total_churned_balance:,.2f}"
    )

    exposure_col2.metric(
        "High-Value Churner Balance",
        f"{high_value_churned_balance:,.2f}"
    )

    exposure_col3.metric(
        "Share of Churned Balance",
        f"{high_value_balance_share:.2f}%"
    )

    st.caption(
        "These figures represent account balance exposure associated "
        "with churn, not actual revenue or profit loss. The dataset "
        "does not provide actual revenue or customer lifetime value."
    )

    # -----------------------------------------------------
    # 7. HIGH-VALUE CHURN BY GEOGRAPHY
    # -----------------------------------------------------

    st.divider()

    st.subheader("High-Value Churn by Geography")

    if not high_value_df.empty:

        high_value_geo = (
            high_value_df.groupby("Geography")
            .agg(
                High_Value_Customers=("CustomerId", "count"),
                Churned_Customers=("Exited", "sum")
            )
            .reset_index()
        )

        high_value_geo["Churn_Rate_%"] = (
            high_value_geo["Churned_Customers"]
            / high_value_geo["High_Value_Customers"]
            * 100
        ).round(2)

        geo_chart = px.bar(
            high_value_geo,
            x="Geography",
            y="Churn_Rate_%",
            text="Churn_Rate_%",
            hover_data=[
                "High_Value_Customers",
                "Churned_Customers"
            ],
            title="High-Value Customer Churn Rate by Country",
            labels={
                "Geography": "Country",
                "Churn_Rate_%": "Churn Rate (%)"
            }
        )

        geo_chart.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        st.plotly_chart(
            geo_chart,
            use_container_width=True
        )

    else:

        st.info(
            "No high-balance customers match the current filters."
        )

    # -----------------------------------------------------
    # 8. HIGH-VALUE CHURN BY AGE GROUP
    # -----------------------------------------------------

    st.subheader("High-Value Churn by Age Group")

    if not high_value_df.empty:

        age_order = ["<30", "30–45", "46–60", "60+"]

        high_value_age = (
            high_value_df.groupby("AgeGroup")
            .agg(
                High_Value_Customers=("CustomerId", "count"),
                Churned_Customers=("Exited", "sum")
            )
            .reset_index()
        )

        high_value_age["Churn_Rate_%"] = (
            high_value_age["Churned_Customers"]
            / high_value_age["High_Value_Customers"]
            * 100
        ).round(2)

        high_value_age["Age_Order"] = (
            high_value_age["AgeGroup"]
            .map({
                group: index
                for index, group in enumerate(age_order)
            })
        )

        high_value_age = (
            high_value_age
            .sort_values("Age_Order")
            .drop(columns="Age_Order")
        )

        age_chart = px.bar(
            high_value_age,
            x="AgeGroup",
            y="Churn_Rate_%",
            text="Churn_Rate_%",
            hover_data=[
                "High_Value_Customers",
                "Churned_Customers"
            ],
            title="High-Value Customer Churn Rate by Age",
            labels={
                "AgeGroup": "Age Group",
                "Churn_Rate_%": "Churn Rate (%)"
            }
        )

        age_chart.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        st.plotly_chart(
            age_chart,
            use_container_width=True
        )

    # -----------------------------------------------------
    # 9. HIGH-VALUE CUSTOMER TABLE
    # -----------------------------------------------------

    st.divider()

    st.subheader("High-Value Customer Explorer")

    st.caption(
        "Inspect high-balance customer records matching the "
        "selected sidebar filters."
    )

    status_selection = st.selectbox(
        "Customer Status",
        options=[
            "All",
            "Churned",
            "Retained"
        ],
        key="high_value_status_filter"
    )

    explorer_df = high_value_df.copy()

    if status_selection == "Churned":

        explorer_df = explorer_df[
            explorer_df["Exited"] == 1
        ]

    elif status_selection == "Retained":

        explorer_df = explorer_df[
            explorer_df["Exited"] == 0
        ]

    explorer_columns = [
        "CustomerId",
        "Geography",
        "Gender",
        "Age",
        "AgeGroup",
        "TenureGroup",
        "CreditScoreBand",
        "Balance",
        "EstimatedSalary",
        "IsActiveMember",
        "Exited"
    ]

    st.dataframe(
        explorer_df[explorer_columns].sort_values(
            "Balance",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Showing {len(explorer_df):,} high-balance customer records."
    )

    # -----------------------------------------------------
    # 10. DOWNLOAD FILTERED HIGH-VALUE DATA
    # -----------------------------------------------------

    csv_data = explorer_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download High-Value Customer Data",
        data=csv_data,
        file_name="high_value_customer_analysis.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "No customers match the current sidebar filters. "
        "Adjust the filters to explore high-value churn."
    )

# =========================================================
# REQUIRED KPI: ENGAGEMENT DROP + GENDER CHURN ANALYSIS
# =========================================================

st.divider()

st.header("Engagement & Gender-Based Churn Analysis")

if not filtered_df.empty:

    # -----------------------------------------------------
    # 1. ENGAGEMENT DROP INDICATOR
    # -----------------------------------------------------

    st.subheader("Engagement Drop Indicator")

    active_customers = filtered_df[
        filtered_df["IsActiveMember"] == 1
    ]

    inactive_customers = filtered_df[
        filtered_df["IsActiveMember"] == 0
    ]

    active_churn_rate = (
        active_customers["Exited"].mean() * 100
        if not active_customers.empty else 0
    )

    inactive_churn_rate = (
        inactive_customers["Exited"].mean() * 100
        if not inactive_customers.empty else 0
    )

    engagement_drop = inactive_churn_rate - active_churn_rate

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Active Customer Churn Rate",
        f"{active_churn_rate:.2f}%"
    )

    col2.metric(
        "Inactive Customer Churn Rate",
        f"{inactive_churn_rate:.2f}%"
    )

    col3.metric(
        "Engagement Drop Indicator",
        f"{engagement_drop:.2f} percentage points"
    )

    engagement_df = pd.DataFrame({
        "Customer Engagement": ["Active", "Inactive"],
        "Churn Rate (%)": [
            active_churn_rate,
            inactive_churn_rate
        ]
    })

    engagement_chart = px.bar(
        engagement_df,
        x="Customer Engagement",
        y="Churn Rate (%)",
        color="Customer Engagement",
        text="Churn Rate (%)",
        title="Churn Rate by Customer Engagement"
    )

    engagement_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    engagement_chart.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Customer Engagement",
        showlegend=False
    )

    st.plotly_chart(
        engagement_chart,
        use_container_width=True
    )

    st.caption(
        "Engagement Drop Indicator = inactive customer churn rate "
        "minus active customer churn rate. A positive value indicates "
        "higher churn among inactive customers."
    )

    # -----------------------------------------------------
    # 2. GENDER-BASED CHURN ANALYSIS
    # -----------------------------------------------------

    st.subheader("Gender-Based Churn Comparison")

    gender_summary = (
        filtered_df.groupby("Gender")
        .agg(
            Total_Customers=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum"),
            Average_Balance=("Balance", "mean"),
            Average_Salary=("EstimatedSalary", "mean")
        )
        .reset_index()
    )

    gender_summary["Churn_Rate"] = (
        gender_summary["Churned_Customers"]
        / gender_summary["Total_Customers"]
        * 100
    )

    col1, col2 = st.columns(2)

    with col1:
        gender_chart = px.bar(
            gender_summary,
            x="Gender",
            y="Churn_Rate",
            color="Gender",
            text="Churn_Rate",
            title="Churn Rate by Gender"
        )

        gender_chart.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        gender_chart.update_layout(
            xaxis_title="Gender",
            yaxis_title="Churn Rate (%)",
            showlegend=False
        )

        st.plotly_chart(
            gender_chart,
            use_container_width=True
        )

    with col2:
        gender_count_chart = px.bar(
            gender_summary,
            x="Gender",
            y="Churned_Customers",
            color="Gender",
            text="Churned_Customers",
            title="Number of Churned Customers by Gender"
        )

        gender_count_chart.update_layout(
            xaxis_title="Gender",
            yaxis_title="Churned Customers",
            showlegend=False
        )

        st.plotly_chart(
            gender_count_chart,
            use_container_width=True
        )

    st.dataframe(
        gender_summary.rename(columns={
            "Gender": "Gender",
            "Total_Customers": "Total Customers",
            "Churned_Customers": "Churned Customers",
            "Average_Balance": "Average Balance",
            "Average_Salary": "Average Estimated Salary",
            "Churn_Rate": "Churn Rate (%)"
        }).round(2),
        use_container_width=True,
        hide_index=True
    )

    highest_gender_churn = gender_summary.loc[
        gender_summary["Churn_Rate"].idxmax()
    ]

    st.info(
        f"{highest_gender_churn['Gender']} customers have the higher "
        f"churn rate in the currently selected data: "
        f"{highest_gender_churn['Churn_Rate']:.2f}%."
    )

else:
    st.warning(
        "No customers match the selected filters. "
        "Please adjust the filters to view this analysis."
    )
# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "European Banking | Customer Segmentation & "
    "Churn Pattern Analytics"
)