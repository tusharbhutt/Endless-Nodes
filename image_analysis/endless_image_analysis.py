import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F
import numpy as np
from PIL import Image, ImageFilter
import os
import hashlib

CLIP_MODEL_NAME = "ViT-B/32"
CLIP_DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), ".cache", "clip")

# Helper to download/load CLIP model from OpenAI
def load_clip_model():
    import clip  # requires `clip` package from OpenAI
    model, preprocess = clip.load(CLIP_MODEL_NAME, device="cpu", download_root=CLIP_DOWNLOAD_PATH)
    return model.eval(), preprocess

# Image Complexity via Edge Density
def compute_edge_density(image: Image.Image) -> float:
    grayscale = image.convert("L")
    edges = grayscale.filter(ImageFilter.FIND_EDGES)
    edge_array = np.asarray(edges, dtype=np.uint8)
    edge_density = np.mean(edge_array > 20)  # percentage of edge pixels
    return round(edge_density * 10, 3)  # scale 0-10

# Image Novelty via distance from reference CLIP embeddings
class ClipImageEmbedder:
    def __init__(self):
        self.model, self.preprocess = load_clip_model()

    def get_embedding(self, image: Image.Image) -> torch.Tensor:
        image_input = self.preprocess(image).unsqueeze(0)
        with torch.no_grad():
            embedding = self.model.encode_image(image_input).float()
        return F.normalize(embedding, dim=-1)

# You could preload this from reference images
REFERENCE_EMBEDDINGS = []

class EndlessNode_ImageNoveltyScorer:
    def __init__(self):
        self.embedder = ClipImageEmbedder()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "reference_images": ("IMAGE", {"default": None, "optional": True}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("novelty_score",)
    FUNCTION = "score_novelty"
    CATEGORY = "Endless 🌊✨/Image Scoring"

    def score_novelty(self, image, reference_images=None):
        img = self._to_pil(image)
        img_emb = self.embedder.get_embedding(img)

        references = REFERENCE_EMBEDDINGS
        if reference_images is not None:
            references = [self.embedder.get_embedding(self._to_pil(ref)) for ref in reference_images]

        if not references:
            return (0.0,)

        sims = [F.cosine_similarity(img_emb, ref_emb).item() for ref_emb in references]
        avg_sim = sum(sims) / len(sims)
        novelty = round((1.0 - avg_sim) * 10, 3)  # higher = more novel
        return (novelty,)

    def _to_pil(self, img):
        if isinstance(img, torch.Tensor):
            img = img.squeeze().detach().cpu().numpy()
        if isinstance(img, np.ndarray):
            if img.max() <= 1.0:
                img = (img * 255).astype(np.uint8)
            else:
                img = img.astype(np.uint8)
            if img.ndim == 3:
                return Image.fromarray(img)
            elif img.ndim == 2:
                return Image.fromarray(img, mode='L')
        elif isinstance(img, Image.Image):
            return img
        else:
            raise ValueError(f"Unsupported image type: {type(img)}")


class EndlessNode_ImageComplexityScorer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("complexity_score",)
    FUNCTION = "score_complexity"
    CATEGORY = "Endless 🌊✨/Image Scoring"

    def score_complexity(self, image):
        img = self._to_pil(image)
        complexity = compute_edge_density(img)
        return (complexity,)

    def _to_pil(self, img):
        if isinstance(img, torch.Tensor):
            img = img.squeeze().detach().cpu().numpy()
        if isinstance(img, np.ndarray):
            if img.max() <= 1.0:
                img = (img * 255).astype(np.uint8)
            else:
                img = img.astype(np.uint8)
            if img.ndim == 3:
                return Image.fromarray(img)
            elif img.ndim == 2:
                return Image.fromarray(img, mode='L')
        elif isinstance(img, Image.Image):
            return img
        else:
            raise ValueError(f"Unsupported image type: {type(img)}")

