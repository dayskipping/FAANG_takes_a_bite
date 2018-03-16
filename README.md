# FAANG takes a bite out of the S&P
## Survey of mega cap tech stocks and their share of S&amp;P market cap

  As we advance into the future, the growth and dominance of mega-cap technology stocks has emerged as an undeniable trend. With this growth,  these companies have taken an ever increasing share of the overall market capitalization of the US equity market. Over the past few years a popular acronym for these key players has emerged, 'FANG', with its constituents being Facebook, Amazon, Netflix, and Google. I have included Apple in this group as well since it is the currently the largest technology stock by market cap. I have chosen the S&P 500 as a proxy of the US equity market since it is one of the most highly pegged measurements of US equities. This project aims to survey the market cap of these names against the total market cap of the S&P 500 index in order to quantify their current dominance and forecast their potential future share of the total S&P market cap.

## The Data
  The daily stock price and market index data was acquired through querying [Quandl](www.quandl.com). Their extensive API aggregates a variety of data sources that are related to financial markets and economics.  
### Exploring the data
  My first goal was to understand how correlated these stocks are with each other and the S&P. As displayed below, we can clearly see that the entire group is highly correlated with each other, the lowest correlation being **.80**

  **Correlation Matrix:**
  ![corr](/images/correlation.png)

  Next, I set out to understand the distribution of the S&P 500. In order to do this I plotted a histogram of daily market returns from 03-13-2008 to 03-12-2018 against a normal distribution. I utilized a Kolmogorov–Smirnov test of equality in order to see if the observed distribution was equal to the normal or Laplace distribution. As seen in the p-values of ~ 0.0 the returns distribution does not show evidence of being equal to either distributions.  

  **S&P Market Returns:**
  ![returns](/images/normal1.png)

  ![returns](/images/laplace1.png)

  In the financial arena, understanding the way a stock moves in relation to the market can be measured by its beta.
  ![beta](/images/beta.svg)

  This calculation can be done by regressing stock price changes against market index changes. Here is a summary table of the stock betas calculated using returns from 11-03-2017 to 2018-03-12.
  ![fang betas](/images/fangbetas.png)

  ![prices](/images/prices.png)

  Market capitalizations are a measure of the shares outstanding of a company's stock multiplied by its share price. I scraped the shares outstanding from each company's 10-K filings posted to [EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch.html) for years 2014-2017 and took an average of the beginning and ending counts for each year. This data was then used to populate the market caps of each stock. I pulled the overall market cap of the S&P from [SiblisResearch](http://siblisresearch.com/data/total-market-cap-sp-500/), providing semi-annual data. GOOGL was the last company to become a constituent of the S&P on 4/3/2014 therefore the market cap data was populated from that date forward.

  ![market caps](/images/fangcaps.png)

  ![market caps](/images/fangbar.png)









~~~python
this is it
~~~


__Links__:
[**google**](www.google.com)

**Images**:
![correlation](/images/correlation.png)
