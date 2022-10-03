# %% [markdown]
# # Taxable Income Calculator
#
# I have no idea what rabbit hole I followed to get to this point, but here I am.
# I found myself researching US tax brackets and how they are calculated.
# If you’re not from the US, don’t worry, you will still be able to figure
# it out and get this bad boy to pass.
#
# ## US 2019 Tax Bracket
#
# Here is the break-down on how much a US citizen’s income was taxed in 2019.
#
#         $0 - $9,700   10%
#     $9,701 - $39,475  12%
#     $39,476 - $84,200  22%
#     $84,201 - $160,725 24%
# $160,726 - $204,100 32%
# $204,101 - $510,300 35%
# $510,301 +          37%
#
# The US tax law is pretty complex, so for now, this is all we are going
# to be dealing with. No filing jointly or as head of household.
#
# From looking at that bracket, you would think that someone having $40,000
# of taxable income would be taxed $8,800, which is 22% of 40,000,
# but that is not the case.
#
# ## How taxes are calculated
#
# The actual taxes would be $4,658.50! Each level in the bracket is taxed
# at the amount shown. So the first $9,700 they would be taxed at 10%.
# The amount from $9,701 through $39,475 is taxed at 12%.
# Then the rest is then taxed at 22%.
#
#     9,700.00 x 0.10 =       970.00
#     29,775.00 x 0.12 =     3,573.00
#         525.00 x 0.22 =       115.50
# ----------------------------------
#                 Total =     4,658.50


# %%
"""Tax Bracket Calculator

Here is the break-down on how much a US citizen's income was
taxed in 2019

      $0 - $9,700   10%
  $9,701 - $39,475  12%
 $39,476 - $84,200  22%
 $84,201 - $160,725 24%
$160,726 - $204,100 32%
$204,101 - $510,300 35%
$510,301 +          37%

For example someone earning $40,000 would
pay $4,658.50, not $40,000 x 22% = $8,800!

    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50

More detail can be found here:
https://www.nerdwallet.com/blog/taxes/federal-income-tax-brackets/

Sample output from running the code in the if/main clause:

          Summary Report
==================================
 Taxable Income:        40,000.00
     Taxes Owed:         4,658.50
       Tax Rate:           11.65%

         Taxes Breakdown
==================================
    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50
"""
from dataclasses import dataclass, field
from typing import List, NamedTuple

Bracket = NamedTuple("Bracket", [("end", int), ("rate", float)])
Taxed = NamedTuple("Taxed", [("amount", float), ("rate", float), ("tax", float)])
BRACKET = [
    Bracket(9_700, 0.1),
    Bracket(39_475, 0.12),
    Bracket(84_200, 0.22),
    Bracket(160_725, 0.24),
    Bracket(204_100, 0.32),
    Bracket(510_300, 0.35),
    Bracket(510_301, 0.37),
]


@dataclass
class Taxes:
    """Taxes class

    Given a taxable income and optional tax bracket, it will
    calculate how much taxes are owed to Uncle Sam.

    """

    income: int
    bracket: List[Bracket] = field(default_factory=lambda: BRACKET)

    def __str__(self) -> str:
        """Summary Report

        Returns:
            str -- Summary report

            Example:

                      Summary Report
            ==================================
             Taxable Income:        40,000.00
                 Taxes Owed:         4,658.50
                   Tax Rate:           11.65%
        """

        return (
            "        Summary Report      \n"
            + "==================================\n"
            + f"    Taxable Income:        {self.income:,.2f}\n"
            + f"        Taxes Owed:         {self.taxes:,.2f}\n"
            + f"        Tax Rate:           {self.tax_rate:,.2f}%\n"
        )

    def report(self):
        """Prints taxes breakdown report"""
        print(self)
        taxes = self.taxes
        print("        Taxes Breakdown      \n" + "==================================")
        for taxed in self.tax_amounts:
            print(f"    {taxed.amount:,.2f} x {taxed.rate:.2f} = {taxed.tax:,.2f}")
        print("-" * 32)
        print(f"                Total = {taxes:,.2f}")

    @property
    def tax_amounts(self):

        tax_income = self.income

        tax_amounts = []

        for bracket, prev_bracket in zip(self.bracket, [Bracket(0, 0)] + self.bracket):
            if prev_bracket.end <= self.income:

                if bracket.end <= self.income:
                    amount = bracket.end - prev_bracket.end
                else:
                    amount = self.income - prev_bracket.end

                tax_amounts.append(
                    Taxed(
                        amount=amount,
                        rate=bracket.rate,
                        tax=amount * bracket.rate,
                    )
                )

                tax_income -= bracket.end - prev_bracket.end

        return tax_amounts

    @property
    def taxes(self) -> float:
        """Calculates the taxes owed

        As it's calculating the taxes, it is also populating the tax_amounts list
        which stores the Taxed named tuples.

        Returns:
            float -- The amount of taxes owed
        """

        return sum(tax.tax for tax in self.tax_amounts)

    @property
    def total(self) -> float:
        """Calculates total taxes owed

        Returns:
            float -- Total taxes owed
        """
        return sum(tax.tax for tax in self.tax_amounts)

    @property
    def tax_rate(self) -> float:
        """Calculates the actual tax rate

        Returns:
            float -- Tax rate
        """
        # round to 2 decimal places
        return round(self.taxes / self.income * 100, 2)


if __name__ == "__main__":
    salary = 40_000
    t = Taxes(salary)
    t.report()

