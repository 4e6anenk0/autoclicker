from dataclasses import dataclass, asdict
from typing import Dict

@dataclass()
class MacrosMetadata:
    """
    Представлення метаданих у вигляді класу даних

    Returns:
        MacrosMetadata: клас даних для метаданих
    """
    uuid: str
    name: str
    macros_dir_path: str
    script_path: str
    metadata_path: str
    data: Dict[str, str]

    def to_dict(self):
        return asdict(self)