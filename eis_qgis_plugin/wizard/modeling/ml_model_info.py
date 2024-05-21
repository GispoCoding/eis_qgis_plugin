import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class MLModelInfo:
    model_instance_name: str
    model_type: str
    model_kind: str
    model_file: str
    training_time: float
    training_date: str
    tags: List[str]
    evidence_data: List[Tuple[str, str]]
    label_data: Tuple[str, str]
    parameters: Dict[str, Any]
    validation_metrics: Optional[Dict[str, float]] = None

    @classmethod
    def from_dict(cls, dict: Dict):
        field_set = {f.name for f in fields(cls)}
        return cls(**{key: value for key, value in dict.items() if key in field_set})

    @classmethod
    def deserialize(cls, json_str):
        return cls.from_dict(json.loads(json_str))

    def serialize(self):
        return json.dumps(asdict(self))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__dataclass_fields__:
                setattr(self, key, value)
