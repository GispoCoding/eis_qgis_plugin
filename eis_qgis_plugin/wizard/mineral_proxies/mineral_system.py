from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class ProxyImportance:
    description: str
    value: int
    color_coding: str
    tooltip_text: str

    @classmethod
    def from_description(self, text: str):
        if text == "High":
            return ProxyImportance(text, 1, "red", "Importance: High")
        elif text == "Moderate":
            return ProxyImportance(text, 2, "orange", "Importance: Moderate")
        elif text == "Low":
            return ProxyImportance(text, 3, "green", "Importance: Low")
        elif text == "-":
            return ProxyImportance(text, 4, "black", "Importance: Undefined")
        else:
            raise Exception(
                f"Unrecognized proxy importance definition found in JSON: {text}. Importance should be either \
                    'High', 'Moderate', 'Low' or '-'."
            )


@dataclass
class MineralProxy:
    name: str
    custom: bool
    mineral_system_component: str
    category: str
    workflow: Sequence[str]
    regional_scale_importance: ProxyImportance
    camp_scale_importance: ProxyImportance
    deposit_scale_importance: ProxyImportance

    @classmethod
    def new(self, source_dict: dict, mineral_system_component: str):
        importances = source_dict.pop("importance")
        custom = False
        return MineralProxy(
            custom=custom,
            mineral_system_component=mineral_system_component,
            regional_scale_importance=ProxyImportance.from_description(importances["regional"]),
            camp_scale_importance=ProxyImportance.from_description(importances["camp"]),
            deposit_scale_importance=ProxyImportance.from_description(importances["deposit"]),
            **source_dict
        )

    def importance_from_scale(self, scale: str) -> Optional[ProxyImportance]:
        if scale == "regional":
            return self.regional_scale_importance
        elif scale == "camp":
            return self.camp_scale_importance
        elif scale == "deposit":
            return self.deposit_scale_importance
        else:
            print("Unrecognized scale!")
            return None  # NOTE: Check


@dataclass
class MineralSystem:
    name: str
    custom: bool
    proxies: Sequence[MineralProxy]

    @classmethod
    def new(
        self,
        source_dict: dict,
        components: Sequence[str] = ["source", "pathway", "depositional", "mineralisation"]
    ):
        proxies = []
        try:
            components_dict = source_dict.pop("mineral_system_components")
        except KeyError:
            print(f"Mineral system initialization failed as 'mineral_system_components' were not \
                found for source dict {source_dict}")
        for component in components:
            proxy_details_for_component = components_dict.get(component)
            for proxy_details in proxy_details_for_component:
                proxy = MineralProxy.new(proxy_details, component)
                proxies.append(proxy)

        return MineralSystem(proxies=proxies, **source_dict)

    def to_json():
        pass
