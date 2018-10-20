# FAANG takes a bite out of the S&P
## Survey of mega cap tech stocks and their share of S&amp;P market cap

  The growth and dominance of mega-cap technology stocks has emerged as an undeniable trend. With this growth,  these companies have taken an ever increasing share of the overall market capitalization of the US equity market. Over the past few years a popular acronym for these key players has emerged, "FANG", with its constituents being Facebook, Amazon, Netflix, and Google. I have included Apple in this group as well since it is the currently the largest technology stock by market cap. I have chosen the S&P 500 as a proxy of the US equity market since it is one of the most highly pegged measurements of US equities. This project aims to survey the market cap of these names against the total market cap of the S&P 500 index in order to quantify their current dominance and forecast their potential future share of the total S&P market cap.

## The Data
  The daily stock price and market index data was acquired through querying [IEX API](https://iextrading.com/developer/docs/). The Investors Exchange(IEX) is a newer stock exchange and they have a free API that is very user friendly and offers trading data for most securities.  
### Exploring the data

#### Correlations
  My first goal was to understand how correlated these stocks are with each other and the S&P.  They are all positively correlated with a few pairs showing stronger returns correlations at .6 or higher.

  ![corr](/images/corr.png)
#### Distribution of Returns
  Next, I set out to understand the distribution of the S&P 500. In order to do this I plotted a histogram of daily market returns from 04-14-2014 to 10-19-2018 against a normal and Laplace distribution. I utilized a Kolmogorov–Smirnov test of equality in order to see if the observed distribution was equal to the normal or Laplace distribution. As seen in the p-values of ~ 0.0 we are unable to conclude that the returns distribution is equal to either the normal or the Laplace.   

  ![returns](/images/normal.png)

  ![returns](/images/laplace.png)

#### Stock Betas
  Understanding the way a stock moves in relation to the market can be measured by its beta,

  *x = cov(market, stock) / var(market)*

  and this calculation can also be done by regressing stock price changes against market index changes. Here is a summary table of the stock betas calculated using returns monthly returns of the trailing 3 year period.

  ![prices](/images/beta_changes.png)

#### Market Capitalizations
  Market capitalizations are a measure of the shares outstanding of a company's stock multiplied by its share price. I scraped the shares outstanding from each company's 10-K filings posted to [EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch.html) for years 2014-2017 and took an average of the beginning and ending counts for each year. This data was then used to populate the market caps of each stock. I pulled the overall market cap of the S&P from [YCharts](https://ycharts.com/indicators/sandp_500_market_cap), providing semi-annual data. GOOGL was the last company to become a constituent of the S&P on 4/3/2014 therefore the market cap data was populated from 4/4/2014 forward.

  ![market caps](/images/faangshare.png)

  As of 10-19-2018 the FAANG stocks had an aggregate market cap of \$3.340291 trillion and the S&amp;P 500 at \$24.58 trillion as of 9-30-2018. This puts the FAANG stocks as a percentage of the total S&amp;P at roughly **13.59%**

  ![market caps v sp](/images/faang%.png)

### Forecasting Market Capitalizations

  The Facebook research team published a forecasting package for Python in 2017. The core of its functionality employs an additive regression model comprised of a piecewise linear or logistic growth curve trend and various seasonality components. I utilized their forecasting tool to gain insight on what the market caps of the FAANG stocks and S&P might look like 5 years into the future. Below is a display of the how the model forecasts into the future with uncertainty increasing over time.

  ![Facebook prophet model](/images/fbforecast.png)

  ![prophet caps](/images/faangforecast.png)



### Conclusion
  After running these forecasts on each of the FAANG stocks and S&P I was able to pull out point estimates at the midpoint of each trend 5 years into the future. The total market capitalizations of the FAANG stocks were estimated to reach roughly \$8.97 trillion and the S&P at over $41.21 trillion. This would indicate that the FAANG stocks could reach roughly **21.77%** of the market cap of the S&P 500 by August of 2023.  

  ![forecasts](/images/finalforecast.png)


### Next Steps

  Obviously, these predictions are highly speculative and rely solely on the daily price data given over the past four years. During this timeframe these stocks as well as the S&P 500 have all shown significant growth. This leads to a tremendous amount of bias in the models. The true cyclicality of markets can be observed over longer periods of time. Therefore, moving forward with this project one could make forecasts using additional data covering a longer timeframe in order to improve the value of the forecasts. To better address the major question under consideration, the role of mega cap tech stocks in market, we could use a more comprehensive view of such tech stocks as well as a broader measure of the market. Then, we may want to introduce other features into the models such as GDP in addition to testing other time series analysis techniques like an ARIMA model.       
