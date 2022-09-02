# Strategy Backtester

This library performs one, but very useful task - it tests the best parameter ratios for the indicator so that you can use them in your trading strategies

## Installation

Install my project with pip

```bash
  pip install numpy
  pip install pandas
```
    
## Demo

#### With specific params

```
/usr/local/bin/python3.10 main.py 

Enter ticker from FTX (Example: BTC-PERP): CRO-PERP

Enter period: 10

Enter multiplier: 3

 ============

SuperTrend Params (ATR Period = 10, Factor = 3.0)
Earning from $1000 is $3419.84 (ROI = 341.98%, Balance = $4419.84)

```

#### Without params

```
Enter ticker from FTX (Example: BTC-PERP): CRO-PERP

Enter period: 0

Enter multiplier: 0

 ============
 
SuperTrend Params (ATR Period = 1, Factor = 7.8)
Earning from $1000 is $718.16 (ROI = 71.82%, Balance = $1718.16)

 ============
SuperTrend Params (ATR Period = 1, Factor = 7.9)
Earning from $1000 is $474.99 (ROI = 47.5%, Balance = $1474.99)

.....

 ============
SuperTrend Params (ATR Period = 1, Factor = 7.9)
Earning from $1000 is $474.99 (ROI = 47.5%, Balance = $1474.99)


SuperTrend Params (ATR Period = 14, Factor = 11.9)

Earning from $1000 is $2124.89 (ROI = 212.49%, Balance = $3124.89)
      ATR_period  Multiplier     ROI
1007          10         2.7  741.67
1117          11         2.7  665.40
1187          11         9.7  626.58
1189          11         9.9  626.58
1188          11         9.8  626.58
1297          12         9.7  616.76
1533          14        11.3  607.29
1298          12         9.8  606.14
1407          13         9.7  596.10
1080          10        10.0  587.56
```

## Roadmap

- Add MAKEFILE

- more ...

