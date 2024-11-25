import streamlit as st
import pandas as pd

st.set_page_config(page_title='Financial Optimizer tool', layout="wide")

st.markdown('''
    # Financial Optimizer
    
    The goal of this application is to lead your choice into which investment account and supports 
    are the best for you in term of net financial return.
    
    This application is designed for the French market and compare the different investment Tax wrapper account type (aka "Envoloppe fiscale" in french).
    
    ''')

st.divider()
st.subheader('Documentation')

with st.container():
    with st.expander('Considered types of tax wrapper ("Enveloppe Fiscale") accounts', expanded=True):
        account_types = [
            {
                'Name': 'Assurance Vie',
                'Symbol': 'AV',
                'Description': 'French Life Insurance tax wrapper',
                'Limitations': 'None',
                'Tax advantage': True,
                'Link': 'https://www.service-public.fr/particuliers/vosdroits/F15268'
            },
            {
                'Name': 'Plan d\'Epargne Retraite',
                'Symbol': 'PER',
                'Description': 'Retirement saving plan : Limited Stock account with tax advantages',
                'Limitations': 'Maximum tax deduction equivalent to 10% of your salary (minimum of 4 399 € and maximum of 35 194 €)',
                'Tax advantage': True,
                'Link': 'https://www.service-public.fr/particuliers/vosdroits/F36526/0?idFicheParent=F34982'
            },
            {
                'Name': 'Plan d\'Epargne en Actions',
                'Symbol': 'PEA',
                'Description': 'Stock Saving Plan : Limited Stock account with tax advantages',
                'Limitations': '150 000 € maximum deposit',
                'Tax advantage': True,
                'Link': 'https://www.economie.gouv.fr/particuliers/plan-epargne-actions-pea'
            },
            {
                'Name': 'Compte Titre Ordinaire',
                'Symbol': 'CTO',
                'Description': 'Basic stock account : Unlimited Stock account with no tax advantage',
                'Limitations': 'None',
                'Tax advantage': False,
                'Link': 'https://www.amf-france.org/fr/espace-epargnants/comprendre-les-produits-financiers/supports-dinvestissement/compte-titres'
            }
        ]
        account_types_df = pd.DataFrame(account_types)
        account_types_df.set_index('Name', inplace=True)
        account_types_df = account_types_df.pivot_table(columns='Name', aggfunc='first')
        account_types_df = account_types_df.reindex(
            labels=['Symbol', 'Description', 'Limitations', 'Tax advantage', 'Link'], fill_value=0)

        st.markdown(account_types_df.to_markdown())
        # st.table(account_types_df)

    with st.expander('Analysis hypothesis'):
        st.markdown('''
        - We want to invest money on the financial market on the very long run (20 years +)
        - We will take the MSCI World Index as a reference investment support for each account
        - We use a free management mode (Mode de gestion libre), no managed mode (Mode de gestion pilotée)
        - We will focus only on the lowest fee taking investment platforms (Implying online providers only)
        - At the investment maturity, we want to withdraw the entire investment (capital + profit/loss)
        - We invest the money in one shot (lump sum) at the beginning of the period, and withdraw the money in one shot at the end of the period
        - We consider no transactions or arbitrage fees as insignificant over the performance result
        ''')

    with st.expander("Resources related to investment supports"):
        st.markdown('''
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

# Sidebar configuration : 
st.sidebar.text('Tax configuration :')
social_security_tax = st.sidebar.number_input('Social Security Tax (%)', value=17.2)
flat_tax = st.sidebar.number_input('Flat Tax (PFU) (%)', value=12.8 + social_security_tax,
                                   help='By default Social security tax (17.2%) + 12.8%')
life_insurance_capital_gain_tax_rate = st.sidebar.number_input('AV withdraw tax (%)', value=7.5 + social_security_tax,
                                                               help='By default Social security tax (17.2%) + 7.5%')

st.divider()
st.subheader('Configuration')

with st.expander('Calculation parameters', expanded=True):
    col1, col2 = st.columns(2)
    current_age = col1.number_input('Current age (years)', value=26, min_value=0)
    retirement_age = col2.number_input('Retirement age (years)', value=64, min_value=0)
    investment_duration = retirement_age - current_age

    st.divider()
    col1, col2 = st.columns(2)
    current_marginal_income_tax_layer = col1.selectbox('Current marginal income tax layer (%)',
                                                       options=[0, 11, 30, 41, 45],
                                                       index=2)
    retirement_marginal_income_tax_layer = col2.selectbox('Retirement (Hypothetical) marginal income tax layer (%)',
                                                          options=[0, 11, 30, 41, 45],
                                                          index=2)
    st.markdown(
        '[Just a reminder regarding French Income Tax brackets](https://www.service-public.fr/particuliers/vosdroits/F1419?lang=en)')

    # TODO : calculate automatically the marginal tranches according to the person's revenues

    st.divider()
    col1, col2, col3 = st.columns(3)
    initial_investment = col1.number_input('Initial investment (€)', value=10000, min_value=100)
    investment_duration = col2.number_input('Investment duration (years)', value=investment_duration, disabled=True,
                                            help='Investment duration = Retirement age - Current age')
    annual_investment_performance = col3.number_input('Annual expected investment return (%)', value=8)

with st.expander('PER Calculation details', expanded=False):
    # Calculation for the net performance of the invested PER tax rebate
    # TODO : Allow allocation of the tax rebate in another account type that the PEA
    compensatory_per_investment = st.selectbox('Selection of compensation investment for PER',
                                               ['PEA : Plan Epargne Actions'])
    compensatory_per_amount = initial_investment * (current_marginal_income_tax_layer / 100)
    compensatory_per_pea_net_performance = annual_investment_performance - 0.25
    compensatory_per_pea_return_invested_before_tax = compensatory_per_amount * (
            (1 + compensatory_per_pea_net_performance / 100) ** investment_duration)
    compensatory_per_pea_return_tax = social_security_tax / 100 * (
            compensatory_per_pea_return_invested_before_tax - compensatory_per_amount)
    compensatory_per_pea_value_after_tax = compensatory_per_pea_return_invested_before_tax - compensatory_per_pea_return_tax

    st.markdown(f'''
        When you invest in a PER, the government will give you a tax rebate equivalent to your current marginal tax income bracket.
        If you invest `{initial_investment}` € in a PER, and your marginal income tax bracket is `{current_marginal_income_tax_layer}` %,
        you'll get `{compensatory_per_amount}` € as tax rebate.
        
        You'll then have to pay back this tax rebate according to your marginal income tax bracket at retirement.
        So if your marginal income tax bracket at retirement is `{retirement_marginal_income_tax_layer}` %,
        you'll have to give back `{initial_investment * retirement_marginal_income_tax_layer / 100}` € to the government at `{retirement_age}` years old.
        
        As we want to compare the different investment plans from a pure saving effort, we have ton invest these `{compensatory_per_amount}` €.
        
        Lets say we invest these `{compensatory_per_amount}` € in a PEA, after management fees and capital gain taxes, you'll end up having `{compensatory_per_pea_value_after_tax}` €.
        This net amount have then to be re-integrated to the PER net performance (`PER tax rebate invested net value (€)` column in the result table).
    ''')

data = [
    {
        'Account type': 'AV : Assurance-vie',
        'Platform': 'BoursoBank',
        'Platform account management fees (%)': 0.75,
        # 'Platform investment transaction fees (%)': 0,
        # 'Platform divestment transaction fees (%)': 0,
        'Investment support': 'ISHARES MSCI WORLD SRI-EUR-A IE00BYX2JD69',
        'Investment support annual fees (%)': 0.20,
        'Capital gain tax (%)': life_insurance_capital_gain_tax_rate,
        'Income tax (€)': 0,
        'PER tax rebate invested net value (€)': 0
    },
    {
        'Account type': 'PER : Plan Epargne Retraite',
        'Platform': 'BoursoBank',
        'Platform account management fees (%)': 0.50,
        # 'Platform investment transaction fees (%)': 0,
        # 'Platform divestment transaction fees (%)': 0,
        'Investment support': '70% ISHARES MSCI USA ESG ENHANCED UCITS ETF USD (ACC) + 30% ISHARES MSCI EUROPE ESG ENHANCED UCITS ETF EUR (ACC)',
        'Investment support annual fees (%)': 0.085,
        'Capital gain tax (%)': flat_tax,
        'Income tax (€)': retirement_marginal_income_tax_layer / 100 * initial_investment,
        'PER tax rebate invested net value (€)': compensatory_per_pea_value_after_tax
    },
    {
        'Account type': 'PEA : Plan Epargne Actions',
        'Platform': 'BoursoBank',
        'Platform account management fees (%)': 0,
        # 'Platform investment transaction fees (%)': 0.5,
        # 'Platform divestment transaction fees (%)': 0.5,
        'Investment support': 'iShares MSCI World Swap PEA UCITS ETF',
        'Investment support annual fees (%)': 0.25,
        'Capital gain tax (%)': social_security_tax,
        'Income tax (€)': 0,
        'PER tax rebate invested net value (€)': 0
    },
    {
        'Account type': 'CTO : Compte Titre Ordinaire',
        'Platform': 'Interactive Brokers',
        'Platform account management fees (%)': 0,
        # 'Platform investment transaction fees (%)': 0.05,
        # 'Platform divestment transaction fees (%)': 0.05,
        'Investment support': 'Amundi Prime Global UCITS ETF DR (C)',
        'Investment support annual fees (%)': 0.05,
        'Capital gain tax (%)': flat_tax,
        'Income tax (€)': 0,
        'PER tax rebate invested net value (€)': 0
    }
]

with st.expander('Platform and fees configuration'):
    st.markdown('''
        By default, we selected a set of platforms + accounts having the best fees on the market.
        
        If on your side you already use a specific platform, you can change, directly in the table below, platform's name, investment support and related fees.  
    ''')

    # TODO : allow to add / remove account type to make easy comparaisons

    data = st.data_editor(data,
                          disabled=[
                              'Account type', 'Capital gain tax (%)', 'Income tax (€)',
                              'PER tax rebate invested net value (€)'
                          ]
                          )

st.divider()
st.subheader('Results')

df = pd.DataFrame(data)

df['Total annual fees (%)'] = df['Platform account management fees (%)'] + df['Investment support annual fees (%)']
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
    'Investment support annual fees (%)',
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

display_mode = st.radio('Results display mode', ['Table', 'Markdown table', 'Dataframe'], horizontal=True)

if display_mode == 'Table':
    st.table(df)
elif display_mode == 'Markdown table':
    st.markdown(df.to_markdown())
elif display_mode == 'Dataframe':
    st.dataframe(df, use_container_width=True, height=527)

st.divider()

st.info('''
    Note : This tool is a V1, I'm planning to implement more features in the next iterations.
    
    If you have any questions or evolution ideas, please contact me at guillaume.kergreis@gmail.com or contribute directly on [GitHub](https://github.com/GuillaumeKergreis/financial-optimizer).
    ''')
