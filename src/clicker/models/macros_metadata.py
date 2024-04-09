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
    date: str
    name: str
    macros_dir_path: str
    script_path: str
    metadata_path: str
    img_sources: Dict[str, str]

    def to_dict(self):
        return asdict(self)