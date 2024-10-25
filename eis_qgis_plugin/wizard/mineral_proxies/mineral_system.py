import json
import os
from dataclasses import dataclass
from typing import List, Optional, Sequence

MINERAL_SYSTEMS_DIR = os.path.join(os.path.dirname(__file__), "mineral_system_libraries")


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
        elif text == "-" or text == "Undefined":
            return ProxyImportance("Undefined", 4, "black", "Importance: Undefined")
        else:
            raise Exception(
                f"Unrecognized proxy importance definition found in JSON: {text}. Importance should be either \
                    'High', 'Moderate', 'Low' or '-'/'Undefined'."
            )

    def __str__(self) -> str:
        return self.description


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
    proxies: List[MineralProxy]

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
            if not proxy_details_for_component:
                continue
            for proxy_details in proxy_details_for_component:
                proxy = MineralProxy.new(proxy_details, component)
                proxies.append(proxy)

        name = source_dict["name"]
        custom = source_dict["custom"].lower() == "true"
        return MineralSystem(name=name, custom=custom, proxies=proxies)

    def add_proxy(self, proxy: MineralProxy):
        self.proxies.append(proxy)

    def to_json_dict(self) -> dict:
        data = {
            "name": self.name,
            "custom": str(self.custom).lower(),
            "mineral_system_components": {}
        }

        for proxy in self.proxies:
            if proxy.mineral_system_component not in data["mineral_system_components"]:
                data["mineral_system_components"][proxy.mineral_system_component] = []
            
            data["mineral_system_components"][proxy.mineral_system_component].append({
                "name": proxy.name,
                "category": proxy.category,
                "workflow": proxy.workflow,
                "importance": {
                    "regional": str(proxy.regional_scale_importance),
                    "camp": str(proxy.camp_scale_importance),
                    "deposit": str(proxy.deposit_scale_importance)
                }
            })

        return data

    def export(self, fp: str):
        json_dict = self.to_json_dict()
        json_dict["custom"] = "true"  # Force to be custom even if exportng predefined system
        with open(fp, "w") as out_file:
            json.dump(json_dict, out_file, indent=4)

    def save(self):        
        fp = os.path.join(MINERAL_SYSTEMS_DIR, f"{self.name}.json")
        json_dict = self.to_json_dict()
        with open(fp, "w") as out_file:
            json.dump(json_dict, out_file, indent=4)

    def delete(self):
        fp = os.path.join(MINERAL_SYSTEMS_DIR, f"{self.name}.json")  
        if os.path.exists(fp):
            os.remove(fp)
