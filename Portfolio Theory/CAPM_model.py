import numpy as np
import math
import random


class ZeroCouponBond:
    def __init__(self, price, maturity, face_value, compounding_freq):
        """
        express the maturity in year relative terms, examplae:

        - 1 Year: 1
        - 0.5 years : 0.5
        - 25 years : 25

        """

        self.price = price
        self.maturity = maturity
        self.face_value = face_value
        self.r = face_value / price - 1
        self.compounding_freq = compounding_freq

        print(
            f"This a bond with price {self.price}, maturity of {self.maturity} and return of {self.r:.2%}"
        )

    def get_effective_anual_rate(self):
        ear = (1 + self.r) ** (1 / self.maturity) - 1

        return ear

    def get_annual_percentage_rate(self):
        ear = self.get_effective_anual_rate()

        apr = ((1 + ear) ** (1 / self.compounding_freq) - 1) * self.compounding_freq

        return apr

    def get_continuous_compounding_rate(self):
        ear = self.get_effective_anual_rate()
        r_cc = math.log(1 + ear)

        return r_cc

    def get_real_growth(self, inflation_rate):
        """
        Please introduce the inflation of the for the same maturity
        """

        real_growth = (1 + self.r) / (1 + inflation_rate) - 1

        real_face_value = self.price * (1 + real_growth)
        return (real_growth, real_face_value)

    def get_after_tax_rate(self, inflation_rate, tax_rate):
        """
        Returns a tuple with the real_rate after tax and the returned value
        """

        real_after_tax_rate = (1 + self.r * (1 - tax_rate)) / (1 + inflation_rate) - 1
        real_after_tax_value = self.price * (1 + real_after_tax_rate)
        return (real_after_tax_rate, real_after_tax_value)


b = ZeroCouponBond(100 / 1.0580, 1, 100, 1)
print(b.get_effective_anual_rate())
print(b.get_annual_percentage_rate())
print(b.get_continuous_compounding_rate())
print(b.get_after_tax_rate(0.04, 0.3))
print(b.get_real_growth(0.04))
