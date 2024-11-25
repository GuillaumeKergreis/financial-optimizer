# Financial Optimizer

This application can be accessed directly at this address : https://financial-optimizer.streamlit.app

Note : if the application is shut down at the moment you want to access it, just click ont the "bring it alive" button and wait for few seconds till the application start.

## Application purpose

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
- PER BoursoBank : https://s.brsimg.com/content/pdf/matla/boursorama-an-financiere.pdf
    - https://www.blackrock.com/fr/particuliers/products/307527/ishares-msci-usa-esg-enhanced-ucits-etf-fund
    - https://www.blackrock.com/fr/intermediaries/products/307564/ishares-msci-europe-esg-enhanced-ucits-etf-eur-acc-fund
- AV BoursoBank : https://api.boursobank.com/services/api/files/public/lifeinsurance-document.phtml?docType=annexe-financiere-libre
    - https://www.blackrock.com/fr/intermediaries/products/290846/ishares-msci-world-sri-ucits-etf
- PEA BoursoBank :
    - https://www.blackrock.com/fr/particuliers/products/335178/ishares-msci-world-swap-pea-ucits-etf
- CTO :
    - https://www.amundietf.fr/fr/professionnels/produits/equity/amundi-prime-global-ucits-etf-dr-c/lu2089238203

## Next features (TODO list)
- French version (translation)
- More precise marginal tax income bracket calculation by taking in account the taxable income.
- Include possibility to add fixed fees in addition to percentage fees
- Include the PER tax deduction cap
- Allow allocation of the PER tax rebate in a selected other account
- Include regular investments calculation
- Add / remove platforms and account type for comparison 