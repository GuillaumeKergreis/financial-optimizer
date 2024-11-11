import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown('''
    # Financial Optimizer
    
    The goal of this application is to lead your choice into which investment account and supports 
    are the best for you in term of net financial return.
    
    This application is designed for the French market, 
    and we will compare here the different types of saving accounts available on the market.
    
    Here are the analysis hypothesis :
    - We want to invest money on the financial market on the very long run (20 years +)
    - We will take the MSCI World Index as a reference investment support for each account
    - We use a free management mode (Mode de gestion libre), no managed mode (Mode de gestion pilotée)
    - We will focus only on the lowest fee taking investment platforms (Implying online providers only)
    - At the investment maturity, we want to withdraw the entire investment (capital + profit/loss)
    - We invest the money in one shot at the beginning of the period
    - We consider no transactions or arbitrage fees as insignificant over the performance result
    - We consider the 
    
    We will consider these types of French Accounts :
    - AV : Assurance-vie (French Life insurance with tax advantage), the most popular type of account 
    - PEA : Plan d'Epargne en Actions (Limited Stock account with tax advantage)
    - PER : Plan d'Epargne Retraite (Retirement account with tax advantage), funds only available at retirement age (currently around 62 years old)
    - CTO : Compte Titre Ordinaire (Basic stock account, no tax advantage)
    
    And here are the brokers chosen for each account type :
    - AV : BoursoBank
    - PEA : BoursoBank
    - PER : BoursoBank
    - CTO : Interactive Brokers
    
    Note : This is a V1 of this tool, and I'm planning to implement more in the next iterations.
    
    Resources :
    - https://www.lopinion.fr/economie/trop-cher-la-cour-des-comptes-epingle-le-plan-epargne-retraite
    - PER BoursoBank : https://s.brsimg.com/content/pdf/matla/boursorama-an-financiere.pdf
        - https://www.blackrock.com/fr/particuliers/products/307527/ishares-msci-usa-esg-enhanced-ucits-etf-fund
        - https://www.blackrock.com/fr/intermediaries/products/307564/ishares-msci-europe-esg-enhanced-ucits-etf-eur-acc-fund
    - AV BoursoBank : https://api.boursobank.com/services/api/files/public/lifeinsurance-document.phtml?docType=annexe-financiere-libre
        - https://www.blackrock.com/fr/intermediaries/products/290846/ishares-msci-world-sri-ucits-etf
    - PEA BoursoBank :
        - https://www.blackrock.com/fr/particuliers/products/335178/ishares-msci-world-swap-pea-ucits-etf
    - CTO :
        - https://www.amundietf.fr/fr/professionnels/produits/equity/amundi-prime-global-ucits-etf-dr-c/lu2089238203
    
    ''')

social_security_tax = st.sidebar.number_input('Social Security Tax (%)', value=17.2)
flat_tax = st.sidebar.number_input('Flat Tax (PFU) (%)', value=12.8 + social_security_tax,
                                   help='By default Social security tax (17.2%) + 12.8%')
life_insurance_withdraw_tax = st.sidebar.number_input('AV withdraw tax (%)', value=7.5 + social_security_tax,
                                                      help='By default Social security tax (17.2%) + 7.5%')

col1, col2 = st.columns(2)
current_age = col1.number_input('Current age (years)', value=26, min_value=0)
retirement_age = col2.number_input('Retirement age (years)', value=64, min_value=0)
investment_duration = retirement_age - current_age

st.divider()

col1, col2 = st.columns(2)
current_marginal_income_tax_layer = col1.selectbox('Current marginal income tax layer (%)', options=[0, 11, 30, 41, 45],
                                                   index=2)
retirement_marginal_income_tax_layer = col2.selectbox('Retirement (Hypothetical) marginal income tax layer (%)',
                                                      options=[0, 11, 30, 41, 45],
                                                      index=2)
st.markdown(
    '[Just a reminder regarding French Income Tax brackets](https://www.service-public.fr/particuliers/vosdroits/F1419?lang=en)')

st.divider()

col1, col2, col3 = st.columns(3)
initial_investment = col1.number_input('Initial investment (€)', value=10000, min_value=100)
investment_duration = col2.number_input('Investment duration (years)', value=investment_duration, disabled=True,
                                        help='Investment duration = Retirement age - Current age')
annual_investment_performance = col3.number_input('Annual expected investment return (%)', value=8)

st.divider()

compensatory_per_amount = initial_investment * (current_marginal_income_tax_layer / 100)
compensatory_per_pea_net_performance = annual_investment_performance - 0.25
compensatory_per_pea_return_invested_before_tax = compensatory_per_amount * (
        (1 + compensatory_per_pea_net_performance / 100) ** investment_duration)
compensatory_per_pea_return_tax = social_security_tax / 100 * (
        compensatory_per_pea_return_invested_before_tax - compensatory_per_amount)
compensatory_per_pea_value_after_tax = compensatory_per_pea_return_invested_before_tax - compensatory_per_pea_return_tax

data = [
    {
        'Account type': 'AV : Assurance-vie',
        'Platform': 'BoursoBank',
        'Platform account management fees (%)': 0.75,
        'Investment support': 'ISHARES MSCI WORLD SRI-EUR-A IE00BYX2JD69',
        'Investment support fees (%)': 0.20,
        'Capital gain tax (%)': life_insurance_withdraw_tax,
        'Income tax (€)': 0,
        'PER tax rebate invested net value (€)': 0
    },
    {
        'Account type': 'PER : Plan Epargne Retraite',
        'Platform': 'BoursoBank',
        'Platform account management fees (%)': 0.50,
        'Investment support': '70% ISHARES MSCI USA ESG ENHANCED UCITS ETF USD (ACC) + 30% ISHARES MSCI EUROPE ESG ENHANCED UCITS ETF EUR (ACC)',
        'Investment support fees (%)': 0.085,
        'Capital gain tax (%)': flat_tax,
        'Income tax (€)': retirement_marginal_income_tax_layer / 100 * initial_investment,
        'PER tax rebate invested net value (€)': compensatory_per_pea_value_after_tax
    },
    {
        'Account type': 'PEA : Plan Epargne Actions',
        'Platform': 'BoursoBank',
        'Platform account management fees (%)': 0,
        'Investment support': 'iShares MSCI World Swap PEA UCITS ETF',
        'Investment support fees (%)': 0.25,
        'Capital gain tax (%)': social_security_tax,
        'Income tax (€)': 0,
        'PER tax rebate invested net value (€)': 0
    },
    {
        'Account type': 'CTO : Compte Titre Ordinaire',
        'Platform': 'Interactive Brokers',
        'Platform account management fees (%)': 0,
        'Investment support': 'Amundi Prime Global UCITS ETF DR (C)',
        'Investment support fees (%)': 0.05,
        'Capital gain tax (%)': flat_tax,
        'Income tax (€)': 0,
        'PER tax rebate invested net value (€)': 0
    }
]

compensatory_per_investment = st.selectbox('Selection of compensation investment for PER',
                                           ['PEA : Plan Epargne Actions'])

# st.data_editor(data)

df = pd.DataFrame(data)
df['Total annual fees (%)'] = df['Platform account management fees (%)'] + df['Investment support fees (%)']
df['Annual return (after fees) (%)'] = annual_investment_performance - df['Total annual fees (%)']
df[f'Account value after {investment_duration} years (€)'] = df['Annual return (after fees) (%)'].apply(
    lambda x: initial_investment * ((1 + x / 100) ** investment_duration))
df['Capital gain tax (€)'] = df['Capital gain tax (%)'] / 100 * (
        df[f'Account value after {investment_duration} years (€)'] - initial_investment)
df['Value after taxes (€)'] = df[f'Account value after {investment_duration} years (€)'] - df['Capital gain tax (€)'] - \
                              df['Income tax (€)']
df['Total final net value (€)'] = df['Value after taxes (€)'] + df['PER tax rebate invested net value (€)']
df['Total final net ROE (%)'] = (df['Total final net value (€)'] - initial_investment) / initial_investment * 100

df = df.pivot_table(columns='Account type', aggfunc='first')

df = df.reindex(labels=[
    # 'Account type',
    'Platform',

    'Platform account management fees (%)',
    'Investment support',
    'Investment support fees (%)',
    'Total annual fees (%)',

    'Annual return (after fees) (%)',
    f'Account value after {investment_duration} years (€)',

    'Capital gain tax (%)',
    'Capital gain tax (€)',
    'Income tax (€)',
    'Value after taxes (€)',

    'PER tax rebate invested net value (€)',
    'Total final net value (€)',
    'Total final net ROE (%)'

])

st.table(df)

st.dataframe(df, use_container_width=True)
