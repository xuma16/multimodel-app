import pickle
import os

# ---------------- Model File Mapping ----------------
MODEL_FILES = {
    "diabetes":  ("model.pkl",           "vectorizer.pkl"),
    "greetings": ("greetings_model.pkl", "vectorizer_greetings.pkl"),
}

# Keywords that signal a greeting intent
GREETING_KEYWORDS = {
    "hi", "hello", "hey", "hei", "habari", "mambo", "salam", "salaam",
    "good morning", "good afternoon", "good evening", "asubuhi", "alasiri",
    "usiku", "bye", "goodbye", "kwaheri", "asante", "thank", "thanks",
    "how are you", "how r u", "u ok", "ok", "okay", "sure", "yes", "no",
    "ndiyo", "hapana", "sawa", "karibu", "welcome",
}

_models = None  # Module-level cache


def load_models():
    """Load all models once and cache them."""
    global _models
    if _models is not None:
        return _models

    loaded = {}
    for name, (model_path, vec_path) in MODEL_FILES.items():
        # Validate both files exist and are non-empty
        for path in (model_path, vec_path):
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                raise ValueError(f"{path} is missing or empty")

        # ✅ FIX: use model_path and vec_path (not generic variables)
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(vec_path, "rb") as f:
            vectorizer = pickle.load(f)

        loaded[name] = (model, vectorizer)

    _models = loaded
    return _models


def route_question(text: str) -> str:
    """Return 'greetings' or 'diabetes' based on the user's input."""
    lower = text.lower().strip()
    for kw in GREETING_KEYWORDS:
        if kw in lower:
            return "greetings"
    return "diabetes"


def predict(text: str):
    """Route to the right model and return (response, model_key)."""
    models = load_models()
    model_key = route_question(text)
    model, vectorizer = models[model_key]
    X = vectorizer.transform([text])
    response = model.predict(X)[0]
    return response, model_key
