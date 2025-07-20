# nodes/__init__.py

# =========================
# 💉 Import Common
# =========================

from .utils.common import inject_descriptions, NODE_DESCRIPTIONS

# =========================
# 💉 Set JavaScript
# =========================

WEB_DIRECTORY = "./web/"


# =========================
# 🧩 Submodule Imports
# =========================

try:
    from .image_analysis import NODE_CLASS_MAPPINGS as IMG_ANALYSIS_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as IMG_ANALYSIS_NAMES
except ImportError:
    IMG_ANALYSIS_CLASSES, IMG_ANALYSIS_NAMES = {}, {}

try:
    from .image_scorer import NODE_CLASS_MAPPINGS as IMG_SCORER_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as IMG_SCORER_NAMES
except ImportError:
    IMG_SCORER_CLASSES, IMG_SCORER_NAMES = {}, {}

try:
    from .batchers import NODE_CLASS_MAPPINGS as BATCH_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as BATCH_NAMES
except ImportError:
    BATCH_CLASSES, BATCH_NAMES = {}, {}

try:
    from .randomizers import NODE_CLASS_MAPPINGS as RANDOMIZER_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as RANDOMIZER_NAMES
except ImportError:
    RANDOMIZER_CLASSES, RANDOMIZER_NAMES = {}, {}

try:
    from .random_prompt_selectors import NODE_CLASS_MAPPINGS as PROMPT_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as PROMPT_NAMES
except ImportError:
    PROMPT_CLASSES, PROMPT_NAMES = {}, {}

try:
    from .image_saver import NODE_CLASS_MAPPINGS as SAVER_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as SAVER_NAMES
except ImportError:
    SAVER_CLASSES, SAVER_NAMES = {}, {}

try:
    from .image_loader import NODE_CLASS_MAPPINGS as LOADER_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as LOADER_NAMES
except ImportError:
    LOADER_CLASSES, LOADER_NAMES = {}, {}

try:
    from .text_switches import NODE_CLASS_MAPPINGS as TEXT_SWITCH_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as TEXT_SWITCH_NAMES
except ImportError:
    TEXT_SWITCH_CLASSES, TEXT_SWITCH_NAMES = {}, {}

try:
    from .int_switches import NODE_CLASS_MAPPINGS as INT_SWITCH_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as INT_SWITCH_NAMES
except ImportError:
    INT_SWITCH_CLASSES, INT_SWITCH_NAMES = {}, {}

try:
    from .int_switches_widget import NODE_CLASS_MAPPINGS as INT_WIDGET_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as INT_WIDGET_NAMES
except ImportError:
    INT_WIDGET_CLASSES, INT_WIDGET_NAMES = {}, {}

try:
    from .type_converter import NODE_CLASS_MAPPINGS as TYPE_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as TYPE_NAMES
except ImportError:
    TYPE_CLASSES, TYPE_NAMES = {}, {}

try:
    from .embedders.endless_embedder_nodes import NODE_CLASS_MAPPINGS as EMBEDDER_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as EMBEDDER_NAMES
except Exception as e:
    EMBEDDER_CLASSES, EMBEDDER_NAMES = {}, {}

try:
    from .utils import NODE_CLASS_MAPPINGS as UTILS_CLASSES, NODE_DISPLAY_NAME_MAPPINGS as UTILS_NAMES
except Exception as e:
    UTILS_CLASSES, UTILS_NAMES = {}, {}


# =====================
# 📦 Dependency Check (v1.3+)
# =====================


_missing = []
_required = {
    "clip": "CLIP embeddings",
    "ftfy": "CLIP text cleanup",
    "imagehash": "Legacy image hashing",
    "scipy": "Saliency / Structural analysis",
    "sentencepiece": "Tokenizer backend for T5 models",
    "skimage": "Statistical image metrics",
    "transformers": "T5 / HuggingFace model support",
}


for lib, purpose in _required.items():
    try:
        __import__(lib)
    except ImportError:
        _missing.append(f"{lib} ({purpose})")

if _missing:
    print("⚠️ [Endless 🌊✨] Missing dependencies detected:")
    for m in _missing:
        print(f"   ⛔ {m}")
    print("👉 Run this to fix: pip install -r requirements.txt\n")
else:
    print("✅ [Endless 🌊✨] All runtime dependencies detected.")


# =========================
# 🧠 Compose Mappings
# =========================

NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(IMG_ANALYSIS_CLASSES)
NODE_CLASS_MAPPINGS.update(IMG_SCORER_CLASSES)
NODE_CLASS_MAPPINGS.update(BATCH_CLASSES)
NODE_CLASS_MAPPINGS.update(RANDOMIZER_CLASSES)
NODE_CLASS_MAPPINGS.update(PROMPT_CLASSES)
NODE_CLASS_MAPPINGS.update(SAVER_CLASSES)
NODE_CLASS_MAPPINGS.update(LOADER_CLASSES)
NODE_CLASS_MAPPINGS.update(TEXT_SWITCH_CLASSES)
NODE_CLASS_MAPPINGS.update(INT_SWITCH_CLASSES)
NODE_CLASS_MAPPINGS.update(INT_WIDGET_CLASSES)
NODE_CLASS_MAPPINGS.update(TYPE_CLASSES)
NODE_CLASS_MAPPINGS.update(EMBEDDER_CLASSES)
NODE_CLASS_MAPPINGS.update(UTILS_CLASSES)

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(IMG_ANALYSIS_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(IMG_SCORER_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(BATCH_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(RANDOMIZER_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(PROMPT_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(SAVER_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(LOADER_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(TEXT_SWITCH_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(INT_SWITCH_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(INT_WIDGET_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(TYPE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(EMBEDDER_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(UTILS_NAMES)

# =====================
# ✅ Finalization
# =====================

# Inject tooltip descriptions for display names
for cls in NODE_CLASS_MAPPINGS.values():
    inject_descriptions(cls, NODE_DESCRIPTIONS)

# Count only nodes that are meant to be shown (have display names)
visible_node_count = sum(
    1 for k in NODE_CLASS_MAPPINGS
    if NODE_DISPLAY_NAME_MAPPINGS.get(k, "").strip()
)

# Version info
__version__ = "1.3.0"

print("\n===============================")
print(f"Endless Sea of Stars Custom Nodes v{__version__} loaded successfully! 🌠")
print(f"{visible_node_count} nodes available under the 'Endless 🌊✨' menu")
print("🔧 If things are missing, try: pip install -r requirements.txt")
print("===============================\n")