#!/usr/bin/env python3
"""Generate a plain-English summary of factor mining results."""

import pandas as pd
from pathlib import Path

results_path = Path("data/results/factor_results.csv")

if not results_path.exists():
    print("❌ No results yet. Run evolution first.")
    exit(1)

df = pd.read_csv(results_path)

if df.empty:
    print("❌ Results file is empty. All factors failed.")
    exit(1)

# Sort by IC (best predictor first)
df = df.sort_values('ic', ascending=False)

print("\n" + "="*60)
print("📊 ALPHA MINING RESULTS - PLAIN ENGLISH SUMMARY")
print("="*60 + "\n")

print(f"Total factors tested: {len(df)}")
print(f"Date range: 2018-2025 (7 years of data)")
print(f"Stocks tested: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META\n")

print("="*60)
print("🎯 WHAT THESE METRICS MEAN")
print("="*60)
print("IC (Information Coefficient): How well the factor predicts returns")
print("  • IC > 0.10 = Excellent (publishable research)")
print("  • IC > 0.05 = Good (worth trading)")
print("  • IC > 0.00 = Weak positive signal")
print("  • IC < 0.00 = Predicts backwards (useless)")
print()
print("Sharpe Ratio: Risk-adjusted returns (higher = better)")
print("  • Sharpe > 2.0 = Excellent")
print("  • Sharpe > 1.0 = Good")
print("  • Sharpe < 0.5 = Poor\n")

print("="*60)
print("🏆 TOP 5 FACTORS (Best to Worst)")
print("="*60 + "\n")

for i, row in df.head(5).iterrows():
    ic = row['ic']
    sharpe = row.get('sharpe', 0)
    dsl = row['dsl']
    hypo = row.get('hypothesis', 'No explanation')
    
    # Rating
    if ic > 0.10:
        rating = "🌟 EXCELLENT"
    elif ic > 0.05:
        rating = "✅ GOOD"
    elif ic > 0:
        rating = "⚠️  WEAK"
    else:
        rating = "❌ BAD"
    
    print(f"Factor #{i+1}: {rating}")
    print(f"  Strategy: {hypo}")
    print(f"  Formula: {dsl}")
    print(f"  Predictive Power (IC): {ic:.4f}")
    print(f"  Risk-Adjusted Returns (Sharpe): {sharpe:.2f}")
    
    # Plain English explanation
    if ic > 0.05:
        print(f"  💡 Meaning: This factor can predict stock returns fairly well!")
    elif ic > 0:
        print(f"  💡 Meaning: Weak signal, but better than random guessing.")
    else:
        print(f"  💡 Meaning: This doesn't work - predicts the opposite direction.")
    print()

print("="*60)
print("📈 SUMMARY")
print("="*60 + "\n")

good_factors = df[df['ic'] > 0.05]
weak_factors = df[(df['ic'] > 0) & (df['ic'] <= 0.05)]
bad_factors = df[df['ic'] <= 0]

print(f"✅ Good factors (IC > 0.05): {len(good_factors)}")
print(f"⚠️  Weak factors (0 < IC < 0.05): {len(weak_factors)}")
print(f"❌ Bad factors (IC < 0): {len(bad_factors)}\n")

if len(good_factors) > 0:
    print("🎉 SUCCESS! You found tradeable alpha signals!")
    print(f"Best factor has IC={df.iloc[0]['ic']:.4f}")
    print(f"This means it can predict stock returns with {df.iloc[0]['ic']*100:.1f}% correlation.\n")
else:
    print("🔄 Keep running more generations to find better factors.")
    print("Tip: Most random factors don't work. Need 20-100 tries to find good ones.\n")

print("="*60)
print("💾 Full results saved to:")
print(f"   {results_path.absolute()}")
print("="*60 + "\n")
