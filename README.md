# Which of the G10 currencies is the riskiest to hold for a Swiss resident?

This project aims to address systematic comparisons of G10 currency risks from the perspective of Swiss residents by assessing the exchange rate risk of these currencies against the Swiss Franc (CHF). Several quantitative methods are applied to evaluate the riskiness of holding these currencies for a Swiss investor. The methods include Value-at-Risk (VaR) calculations using various models, the calculation of the historical Expected Shortfall (ES), volatility analysis, and an investigation of the sensitivity of exchange rate returns to interest rate differentials. 

## **Reproducibility**

The user can reproduce our research by using the provided scripts and codes along with the data available here. The data is also generated through the scripts provided here. The process of data generation through the provided scripts will be explained in more detail below.

In this GitHub repository you will find the following content in the folders of the repository:

### **Environmental variables and packages for Python scripts:**

**code/environmental_analyse_script.txt:** lists the necessary packages and their specific versions to ensure the Python scripts for data preservation, data processing, and analysis methodology can be executed successfully. These dependencies are essential for managing, processing, and analyzing data, as well as implementing the required statistical and visualization techniques.

### **Codes to obtain data:**

**code/data_collector_yahoo.py:** Python file used to reproducibly crawl G10 currency exchange rate data against CHF from Yahoo Finance, process it into a long format, and save it as a CSV file for further analysis.

**code/data_collector_interest_rate.py:** Python file used to reproducibly download, process, and combine interest rate data from multiple sources (FRED, Swiss National Bank, and Riksbank) for the period from January 2000 to October 2024. The data is cleaned, formatted, and saved as a CSV file for further analysis

### **Codes to process data:**

**code/data_transformation_yahoo_FX.py:** Python script used to clean and transform the NOKCHF (Norwegian Krone to Swiss Franc) exchange rate data. It specifically removes redundant '00' after the decimal point for NOKCHF values and saves the cleaned data for further use.

**code/merge_FX_interest_yearly.py:** Python script that merges foreign exchange (FX) data with interest rate data on a yearly basis. It calculates the logarithmic returns for the FX rates and then merges these returns with interest rates from the same country. The script also computes the logarithmic interest rate differential between Switzerland and other countries and saves the final merged dataset for further analysis.

### **Codes for methodology and analysis:**

**code/analyse_VAR_Monte_Carlo_fx.py:** Python script that performs a Value-at-Risk (VaR) analysis for various foreign exchange (FX) currency pairs. It calculates daily returns and VaR at the 5% percentile using historical data, and then performs Monte Carlo simulations to estimate future price paths and VaR. The script generates visualizations such as histograms, price simulations, and VaR comparisons, and saves them to a designated folder. It also compares historical VaR values with Monte Carlo VaR simulations, and exports the results to a CSV file for further analysis.

**code/analyse_Regression_FX_Interest_logreturns.py:** Python script for performing linear regressions between foreign exchange (FX) returns and the interest rate differentials for various countries. For each country, the script computes the regression coefficients (alpha and beta), standard errors, t-values, p-values, and confidence intervals. The results are formatted and saved for further analysis.

**code/analyse_basic_risk_measures.py:** Python script for calculating and visualizing basic risk measures for currency pairs, specifically focusing on standard deviation (volatility), Value at Risk (VaR) at the 5% level, and Expected Shortfall (ES) at the 5% level. It uses Yahoo Finance data, resamples it based on a specified frequency (daily, monthly, etc.), and calculates the risk metrics for each currency pair.

### **Notebook for interactive app in the notebooks folder:**

**notebooks/interactive_app.ipynb:** Jupyter notebook designed as the interactive application for visualizing and analyzing overnight interest rate data across multiple countries. It uses Plotly to generate interactive plots that display the overnight rates over time, allowing users to zoom in on specific historical events (e.g., the Dotcom Bubble, the Global Financial Crisis, and the COVID-19 Pandemic) through interactive buttons. The notebook also calculates and visualizes the volatility (standard deviation) of overnight rates for each country, helping to identify which currencies are the riskiest based on their rate fluctuations. This interactive app is essential for Swiss residents to assess currency risk.

### **Data files:**

**data/raw:** Folder containing the unprocessed raw exchange rate and interest rate data. This includes data collected from sources such as Yahoo Finance, FRED, Swiss National Bank, and Riksbank, without any transformations applied.

**data/modeling_data:** Folder containing transformed and merged exchange rate and interest rate data that has been processed for use in analysis. 

### **Repots and figures:**

**reports/figures:** Contains all PNG files and CSV files generated as outputs for writing the report.

### **Presentation:**

**reports/presentation/presentation.tex** using LaTex via online overleaf.

### **Paper:**

**reports/paper/text_paper.tex** using LaTex via online overleaf.

### **Literature and data References:**

**references/refs.bib**: Folder containing all the literature, academic research papers, and data references relevant to the project. These references are cited throughout the project to support analyses, methodologies, and conclusions, ensuring the use of credible sources for both theoretical and data-driven aspects of the research.

## **Project Structure**

### **Data Source**

We collect overnight interest rates and foreign exchange rate data from multiple sources to compile our dataset, including data for the G10 countries: the Eurozone, the United Kingdom, the United States, Canada, Japan, Australia, New Zealand, Norway, Sweden, and Switzerland.

The daily foreign exchange rate data for these currencies against the Swiss Franc (CHF) were collected using the YFinance library. The data spans from January 1, 2004, to October 21, 2024.

For overnight interest rates, data for Norway, Japan, the United Kingdom, the United States, Germany, Australia, New Zealand, and Canada were obtained from the Federal Reserve Economic Data (FRED) database. Data for Switzerland was retrieved from the Swiss National Bank’s (SNB) official API, specifically using the SARON (Swiss Average Rate Overnight) series. Similarly, overnight interest rate data for Sweden was sourced from the Swedish Riksbank’s Interest Rates and Exchange Rates Statistics. This dataset spans from January 2000 to October 2024 and includes interest rates on a monthly basis.

### **Analysis Structure**

To assess the risk of G10 currencies against the Swiss Franc, we applied various quantitative methods. These include Value-at-Risk (VaR) calculations, Expected Shortfall (ES) analysis, volatility analysis and interest rate regression. The detailed methodology is discussed in the paper.

#### **VaR Calculation**

VaR was calculated using two methods: historical analysis and Monte Carlo simulation. Both methods used a 95% confidence level. The historical method estimated VaR based on the empirical return distribution on a monthly basis, while the Monte Carlo simulation generated forward-looking scenarios to calculate potential losses on a daily basis.

The historical analysis is the simplest method of calculation. For each currency we plot historical return distribution and calculate VaR at 5% level. The highest historical VaR was observed for NOK and NZD, with AUD, JPY and CAD also showing high historical VaR values.

<p align="center">
  <img src="https://github.com/zongcai66/G10_currency_risk_for_Swiss_residents/blob/main/reports/figures/VaR_5_percent_plot.png?raw=true" width="60%" />
</p>


Monte Carlo simulations were conducted to assess the 1-day Value-at-Risk (VaR) for G10 currencies against the Swiss Franc, based on simulated price paths and returns. The VaR, representing the maximum loss not exceeded with 95% probability, was calculated for the final day of each simulation.

Below, we present the price and return simulations for the New Zealand Dollar (NZD), which had one of the highest simulated VaR values.

<p align="center">
  <img src="https://github.com/zongcai66/G10_currency_risk_for_Swiss_residents/blob/main/reports/figures/monte_carlo_price_simulation_NZDCHF_vs_CHF.png?raw=true" width="45%" />
  <img src="https://github.com/zongcai66/G10_currency_risk_for_Swiss_residents/blob/main/reports/figures/monte_carlo_var_simulation_NZDCHF_vs_CHF.png?raw=true" width="45%" />
</p>

#### **Volatility Analysis**

Volatility, measured as the standard deviation of monthly returns, was analyzed to assess exchange rate fluctuation intensity. Higher volatility indicates greater risk and uncertainty, helping identify which G10 currencies pose the greatest risk for a Swiss investor. The highest volatility was observed for NZD, USD, and JPY.

<p align="center">   <img src="https://github.com/zongcai66/G10_currency_risk_for_Swiss_residents/blob/main/reports/figures/volatility_plot.png?raw=true" width="60%" /> </p>

#### **ES Calculation**

Historical Expected Shortfall (ES) was calculated as a complement to VaR to assess tail risk, representing the average loss beyond the 5% quantile of the historical return distribution on a monthly basis. This provides insight into potential extreme losses for G10 currencies relative to the Swiss Franc. The highest ES values were observed for NOK and CAD, with NZD and AUD also showing relatively high values.

<p align="center">   <img src="https://github.com/zongcai66/G10_currency_risk_for_Swiss_residents/blob/main/reports/figures/ES_5_percent_plot.png?raw=true" width="60%" /> </p>

#### **Regression to Analyze Interest Rate Differentials**

We analyzed the sensitivity of exchange rate returns to interest rate differentials using linear regression. The logarithmic exchange rate return was regressed against the difference in logarithmic interest rates, comparing each currency's interest rate differential to the Swiss interest rate. The regression provided insights into how much exchange rate returns are influenced by changes in interest rate differentials for each G10 currency relative to the Swiss Franc.

For example, although volatility and VaR are high for the New Zealand Dollar (NZD), the regression results show low sensitivity to changes in interest rate differentials (β=0.13, not significant). This indicates that other factors, such as commodity price fluctuations and speculative behavior, could be contributing to the NZD's market volatility, serving as potential examples of factors not captured in the interest rate regression model. In contrast, the Japanese Yen (JPY), for example, shows a significantly negative sensitivity to changes in interest rate differentials (β = -3.25, highly significant).

<table style="font-size:12px; width:80%; margin:auto;">
  <thead>
    <tr>
      <th>Country</th>
      <th>Alpha</th>
      <th>Beta</th>
      <th>Alpha Std.Err.</th>
      <th>Beta Std.Err.</th>
      <th>Alpha t</th>
      <th>Beta t</th>
      <th>Alpha P>|t|</th>
      <th>Beta P>|t|</th>
      <th>Alpha [0.025</th>
      <th>Alpha 0.975]</th>
      <th>Beta [0.025</th>
      <th>Beta 0.975]</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Australia</td><td>-0.0619</td><td>-1.4626</td><td>0.0200</td><td>0.6324</td><td>-3.0986</td><td>-2.3126</td><td>0.0024</td><td>0.0224</td><td>-0.1015</td><td>-0.0224</td><td>-2.7147</td><td>-0.2105</td></tr>
    <tr><td>Canada</td><td>-0.0281</td><td>-0.7324</td><td>0.0163</td><td>0.8935</td><td>-1.7216</td><td>-0.8196</td><td>0.0877</td><td>0.4140</td><td>-0.0605</td><td>0.0042</td><td>-2.5012</td><td>1.0365</td></tr>
    <tr><td>Germany</td><td>-0.0290</td><td>-0.6740</td><td>0.0077</td><td>0.7651</td><td>-3.7798</td><td>-0.8809</td><td>0.0002</td><td>0.3801</td><td>-0.0442</td><td>-0.0138</td><td>-2.1888</td><td>0.8407</td></tr>
    <tr><td>UK</td><td>-0.0437</td><td>-0.8895</td><td>0.0114</td><td>0.5722</td><td>-3.8264</td><td>-1.5545</td><td>0.0002</td><td>0.1227</td><td>-0.0663</td><td>-0.0211</td><td>-2.0224</td><td>0.2433</td></tr>
    <tr><td>Japan</td><td>-0.0400</td><td>-3.2504</td><td>0.0081</td><td>0.9480</td><td>-4.9300</td><td>-3.4287</td><td>0.0000</td><td>0.0008</td><td>-0.0560</td><td>-0.0239</td><td>-5.1272</td><td>-1.3736</td></tr>
    <tr><td>Norway</td><td>-0.0045</td><td>2.1236</td><td>0.0205</td><td>1.0760</td><td>-0.2183</td><td>1.9736</td><td>0.8276</td><td>0.0507</td><td>-0.0451</td><td>0.0362</td><td>-0.0068</td><td>4.2541</td></tr>
    <tr><td>New Zealand</td><td>-0.0138</td><td>0.1340</td><td>0.0195</td><td>0.5647</td><td>-0.7099</td><td>0.2374</td><td>0.4791</td><td>0.8128</td><td>-0.0524</td><td>0.0247</td><td>-0.9839</td><td>1.2519</td></tr>
    <tr><td>Sweden</td><td>-0.0176</td><td>1.7871</td><td>0.0111</td><td>0.9607</td><td>-1.5787</td><td>1.8602</td><td>0.1170</td><td>0.0653</td><td>-0.0397</td><td>0.0045</td><td>-0.1149</td><td>3.6892</td></tr>
    <tr><td>United States</td><td>-0.0364</td><td>-1.1620</td><td>0.0100</td><td>0.4989</td><td>-3.6296</td><td>-2.3290</td><td>0.0004</td><td>0.0215</td><td>-0.0563</td><td>-0.0166</td><td>-2.1496</td><td>-0.1743</td></tr>
  </tbody>
</table>

## **Data Source**

https://finance.yahoo.com/
https://www.riksbank.se/en-gb/statistics/interest-rates-and-exchange-rates/
https://data.snb.ch/
https://fred.stlouisfed.org/

## **References**

[The relationship between exchange rates and international trade: a literature review | World Trade Review | Cambridge Core](https://www.cambridge.org/core/journals/world-trade-review/article/abs/relationship-between-exchange-rates-and-international-trade-a-literature-review/486C5AC908CDBE851869FE8540A3A97A)

[The Dollar Exchange Rate as a Global Risk Factor: Evidence from Investment | IMF Economic Review](https://link.springer.com/article/10.1057/s41308-019-00074-4)

[Triennial Central Bank Survey of foreign exchange and Over-the-counter (OTC) derivatives markets in 2022](https://www.bis.org/statistics/rpfx22.htm)

[Exchange Rates, Interest Rates, and the Risk Premium - American Economic Association](https://www.aeaweb.org/articles?id=10.1257/aer.20121365)

[How Switzerland erdaicates the inflation in 2021 and 2022 - Theseus](https://www.theseus.fi/handle/10024/803553)

[Safe Haven Currencies* | Review of Finance | Oxford Academic](https://academic.oup.com/rof/article-abstract/14/3/385/1592162)

[How big is the premium for currency risk? - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X98000294)

[Strategic Asset Allocation: Portfolio Choice for Long-Term Investors | Oxford Academic](https://academic.oup.com/book/6093)

[The Six Major Puzzles in International Macroeconomics: Is There a Common Cause? | NBER](https://www.nber.org/papers/w7777)

[Currency composition of foreign exchange reserves - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0261560619305832)

[Exchange Rate Policy in Advanced Commodity-Exporting Countries : The Case of Australia and New Zealand | OECD Economics Department Working Papers | OECD iLibrary](https://www.oecd-ilibrary.org/economics/exchange-rate-policy-in-advanced-commodity-exporting-countries_566103428800)

## **Authors**

[xiao.chen@uzh.ch](mailto:xiao.chen@uzh.ch)

[zhi.wang@uzh.ch](mailto:zhi.wang@uzh.ch)

[yannic.laube@ius.uzh.ch](mailto:yannic.laube@ius.uzh.ch)

[bosko.todorovic@uzh.ch](mailto:bosko.todorovic@uzh.ch)
