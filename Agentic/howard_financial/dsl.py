import pandas as pd
from typing import Callable, Optional

# Define the type of a Rule: a function that takes a DataFrame and returns a Series
Rule = Callable[[pd.DataFrame], pd.Series]

def amt(tag: Optional[str] = None, cat: Optional[str] = None, type_: Optional[str] = None) -> Rule:
    """
    Creates a rule that filters transactions by tag, category, and/or type, returning the 'Amount' column.

    Parameters:
    - tag: Substring to match in the 'Tags' column (case-insensitive)
    - cat: Substring to match in the 'Category' column (case-insensitive)
    - type_: Substring to match in the 'Type' column (case-insensitive)

    Returns:
    - A Rule (function) that takes a DataFrame and returns a Series of amounts
      matching the specified filters.
    """
    def _rule(df: pd.DataFrame) -> pd.Series:
        # Start with all rows as True
        mask = pd.Series(True, index=df.index)
        
        # Apply tag filter if provided
        if tag:
            mask &= df["Tags"].str.contains(tag, case=False, na=False)
        
        # Apply category filter if provided
        if cat:
            mask &= df["Category"].str.contains(cat, case=False, na=False)
        
        # Apply type filter if provided
        if type_:
            mask &= df["Type"].str.contains(type_, case=False, na=False)
        
        # Return the filtered 'Amount' Series
        return df.loc[mask, "Amount"]
    
    return _rule

def pct(numerator: Rule, denominator: Rule) -> Rule:
    """
    Creates a rule that computes the ratio of two amount sums (numerator / denominator).

    Parameters:
    - numerator: A Rule that returns a Series of amounts (the top of the fraction)
    - denominator: A Rule that returns a Series of amounts (the bottom of the fraction)

    Returns:
    - A Rule that computes a single float: the ratio of sums of the two Series.
    """
    def _rule(df: pd.DataFrame) -> float:
        num_sum = numerator(df).sum()
        denom_sum = denominator(df).sum()
        # Protect against division by zero
        if denom_sum == 0:
            return float('nan')
        return num_sum / abs(denom_sum)
    
    return _rule
