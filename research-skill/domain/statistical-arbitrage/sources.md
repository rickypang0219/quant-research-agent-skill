# Statistical Arbitrage Source Registry

This source registry is curated for a statistical arbitrage skill pack. It prioritizes recognized academia, peer-reviewed journals, SSRN/arXiv/NBER working papers, Wiley/Oxford/ScienceDirect pages, and official institutional research. It deliberately excludes random YouTube/social-media opinions.

## Core Statistical Arbitrage / Pairs Trading

1. Marco Avellaneda and Jeong-Hyun Lee — **Statistical Arbitrage in the U.S. Equities Market**  
   URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1153505  
   Use for: PCA residual stat arb, ETF residual stat arb, s-scores, residual mean reversion, market-neutral backtesting, volume-time adjustment.

2. Evan Gatev, William N. Goetzmann, and K. Geert Rouwenhorst — **Pairs Trading: Performance of a Relative Value Arbitrage Rule**  
   URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=141615  
   Use for: distance-based pairs trading, normalized price path matching, self-financing pair portfolios, conservative cost testing.

3. Christopher Krauss — **Statistical Arbitrage Pairs Trading Strategies: Review and Outlook**  
   URL: https://onlinelibrary.wiley.com/doi/abs/10.1111/joes.12153  
   Use for: pairs trading taxonomy: distance, cointegration, time-series, stochastic-control, and other approaches.

4. Andrew Pole — **Statistical Arbitrage: Algorithmic Trading Insights and Techniques**  
   URL: https://www.wiley.com/en-be/Statistical%2BArbitrage%3A%2BAlgorithmic%2BTrading%2BInsights%2Band%2BTechniques-p-9781119197072  
   Use for: practitioner perspective on statistical arbitrage as a business, not only a signal formula.

## Factor Models and Cross-Sectional Risk

5. Eugene F. Fama and Kenneth R. French — **Common Risk Factors in the Returns on Stocks and Bonds**  
   URL: https://www.sciencedirect.com/science/article/abs/pii/0304405X93900235  
   Use for: market, size, value, bond maturity/default factors; factor-adjusted performance evaluation.

6. Eugene F. Fama and Kenneth R. French — **A Five-Factor Asset Pricing Model**  
   URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2287202  
   Use for: size, value, profitability, investment factor controls.

7. Mark M. Carhart — **On Persistence in Mutual Fund Performance**  
   URL: https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1997.tb03808.x  
   Use for: four-factor model and momentum as a performance attribution control.

8. Clifford S. Asness, Tobias J. Moskowitz, and Lasse H. Pedersen — **Value and Momentum Everywhere**  
   URL: https://www.aqr.com/Insights/Research/Journal-Article/Value-and-Momentum-Everywhere  
   Use for: cross-asset value/momentum, common factor structure, diversified factor portfolios.

9. Andrea Frazzini and Lasse H. Pedersen — **Betting Against Beta**  
   URL: https://www.aqr.com/Insights/Research/Journal-Article/Betting-Against-Beta  
   Use for: leverage constraints, low-beta anomaly, beta-scaled long/short construction.

## Momentum / Reversal / Anomalies

10. Narasimhan Jegadeesh and Sheridan Titman — **Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency**  
    URL: https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html  
    Use for: intermediate-horizon momentum.

11. Louis K. C. Chan, Narasimhan Jegadeesh, and Josef Lakonishok — **Momentum Strategies**  
    URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=225438  
    Use for: momentum and gradual market response to information.

12. Werner F. M. De Bondt and Richard Thaler — **Does the Stock Market Overreact?**  
    URL: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1985.tb05004.x  
    Use for: long-horizon reversal and behavioral overreaction.

13. Zura Kakushadze — **101 Formulaic Alphas**  
    URL: https://arxiv.org/abs/1601.00991  
    Use for: formulaic alpha operators, short-horizon cross-sectional signal templates, alpha correlation and turnover thinking.

## Robustness, Overfitting, and Crowding

14. Andrew W. Lo and A. Craig MacKinlay — **Data-Snooping Biases in Tests of Financial Asset Pricing Models**  
    URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=227465  
    Use for: warning against false discoveries from sorting/searching many characteristics.

15. David H. Bailey and Marcos López de Prado — **The Deflated Sharpe Ratio**  
    URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551  
    Use for: selection bias, multiple testing, non-normality, performance inflation, minimum track record length.

16. Kewei Hou, Chen Xue, and Lu Zhang — **Replicating Anomalies**  
    URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2961979  
    Use for: anomaly replication, microcap control, value-weighting, stricter t-statistics, p-hacking caution.

17. Amir E. Khandani and Andrew W. Lo — **What Happened to the Quants in August 2007?**  
    URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1015987  
    Use for: quant crowding, deleveraging, market-neutral crash risk, common-position liquidation.

18. Andrew W. Lo — **The Adaptive Markets Hypothesis**  
    URL: https://web.mit.edu/Alo/www/Papers/JPM2004_Pub.pdf  
    Use for: markets as adaptive/ecological systems; edge decay under competition and changing regimes.

## Additional Useful References to Add Later

- Johansen cointegration literature for basket spreads.
- Engle-Granger cointegration literature for pair spreads.
- White's Reality Check and Hansen SPA tests for multiple strategy testing.
- Ledoit-Wolf covariance shrinkage for portfolio covariance stability.
- Almgren-Chriss and market-impact literature for execution-aware capacity.
- Exchange-specific API docs for crypto funding, borrow, fee, and contract specifications.
