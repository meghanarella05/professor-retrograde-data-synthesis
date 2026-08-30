import json
from pathlib import Path
from .models import TRAITS, Chart

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())

def _scale(values, weights):
    return {trait: values[trait] * weight for trait, weight in zip(TRAITS, weights)}

class POSEngine:
    """Deterministic POS transformation engine.

    The supplied specification treats every operator as independent
    component-wise scaling, preserving all 20 latent dimensions.
    """

    def __init__(self, config=None):
        self.config = config or CONFIG

    def apply_operator(self, values, weights):
        return _scale(values, weights)

    def context_vector(self, base_traits, zodiac=None, planet=None,
                       house=None, dchart=None):
        values = dict(base_traits)

        if zodiac:
            values = self.apply_operator(values, self._zodiac(zodiac))
        if planet:
            values = self.apply_operator(values, self._planet(planet))
        if house:
            values = self.apply_operator(values, self._house(house))
        if dchart:
            values = self.apply_operator(values, self._dchart(dchart))
        return values

    def pos_matrix(self, base_traits, lagna, bhava_chalit, d9, d60):
        """POS = component-wise product of the four specified chart operators."""
        values = dict(base_traits)
        for chart_name in ("lagna", "bhava_chalit", "D9", "D60"):
            values = self.apply_operator(values, self._dchart(
                {"lagna":"lagna","bhava_chalit":"bhava_chalit","D9":"D9","D60":"D60"}[chart_name]
            ))
        return values

    def interpret_chart(self, chart: Chart, base_traits):
        """Return structured representations; narrative generation is intentionally separate."""
        out = {
            "model_version": self.config["model_version"],
            "base_traits": dict(base_traits),
            "ascendant": chart.ascendant,
            "planet_contexts": {},
            "house_contexts": {},
            "divisional_contexts": {},
        }

        for planet, placement in chart.planets.items():
            out["planet_contexts"][planet] = self.context_vector(
                base_traits, zodiac=placement.sign, planet=planet, house=placement.house
            )

        for house, placement in chart.houses.items():
            out["house_contexts"][str(house)] = self.context_vector(
                base_traits, zodiac=placement.sign, house=house
            )

        for dchart, data in chart.divisional_charts.items():
            if dchart in self.config["dchart_operators"]:
                out["divisional_contexts"][dchart] = self.apply_operator(
                    base_traits, self._dchart(dchart)
                )

        return out

    def _planet(self, name):
        key = name.lower().replace(" ", "_")
        if key not in self.config["planet_operators"]:
            raise ValueError(f"Unsupported planet/operator: {name}")
        return self.config["planet_operators"][key]

    def _zodiac(self, sign):
        key = sign.lower().replace(" ", "_")
        if key not in self.config["zodiac_operators"]:
            raise ValueError(f"Unsupported zodiac sign: {sign}")
        return self.config["zodiac_operators"][key]

    def _house(self, house):
        key = str(house)
        if key not in self.config["house_operators"]:
            raise ValueError(f"Unsupported house: {house}")
        return self.config["house_operators"][key]

    def _dchart(self, name):
        key = name.upper() if name.upper() in self.config["dchart_operators"] else name.lower()
        # config contains canonical keys such as D9, D60, lagna, bhava_chalit
        if key not in self.config["dchart_operators"]:
            raise ValueError(f"Unsupported D-chart/operator: {name}")
        return self.config["dchart_operators"][key]
