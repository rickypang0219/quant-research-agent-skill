# Gatheral Mental Models

## 1. Implied Volatility Is a Price Object

It is not the market's literal forecast. It embeds risk premia, supply/demand, hedging pressure, and constraints.

## 2. Surfaces Need Arbitrage Checks

Smooth-looking implied vol surfaces can still imply calendar, butterfly, or vertical spread arbitrage.

## 3. Rough Volatility Is Empirical, Not Decorative

If using rough volatility, estimate scaling behavior and compare against simpler volatility models.

## 4. Impact Models Can Create Fake Arbitrage

An impact model that allows profitable round trips is broken.

## 5. Shape and Decay Are Linked

Do not choose square-root impact and exponential decay independently without checking consistency.

