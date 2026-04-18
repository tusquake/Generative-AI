import os
import torch
import logging
import base64
from io import BytesIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("StableDiffusionService")

app = FastAPI(title="Stable Diffusion Production API")

# --- Model Configuration ---
# Use runwayml/stable-diffusion-v1-5 for broad compatibility
MODEL_ID = os.getenv("MODEL_ID", "runwayml/stable-diffusion-v1-5")
# Hardware detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Use float16 on GPU for speed and lower VRAM usage
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

logger.info(f"Loading model '{MODEL_ID}' on device '{DEVICE}'...")

# Global pipeline instance
pipe = None

@app.on_event("startup")
def load_model():
    global pipe
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=TORCH_DTYPE,
            use_safetensors=True
        )
        pipe.to(DEVICE)
        
        # PERFORMANCE OPTIMIZATIONS
        if DEVICE == "cuda":
            logger.info("Enabling GPU optimizations (Attention Slicing)...")
            pipe.enable_attention_slicing()
            # If you have < 4GB VRAM, uncomment the line below:
            # pipe.enable_model_cpu_offload()
        else:
            logger.warning("Running on CPU. Generation will be slow.")
            
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Critical error loading model: {e}")
        # In a real production app, you might want to retry or crash
        pass

# --- API Models ---
class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = "blurry, low quality, distorted, bad anatomy"
    steps: int = 30
    guidance_scale: float = 7.5

# --- Endpoints ---
@app.post("/generate")
async def generate(request: ImageRequest):
    if pipe is None:
        raise HTTPException(status_code=503, detail="Model is still loading or failed to load.")

    try:
        logger.info(f"Generating image for prompt: {request.prompt}")
        
        # Run inference
        # Use autocast for FP16 inference on GPU
        with torch.autocast(DEVICE) if DEVICE == "cuda" else torch.no_grad():
            output = pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                num_inference_steps=request.steps,
                guidance_scale=request.guidance_scale
            )
        
        image = output.images[0]
        
        # Convert PIL image to base64 string
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {
            "status": "success",
            "device": DEVICE,
            "image_b64": img_str
        }

    except torch.cuda.OutOfMemoryError:
        logger.error("GPU Out of Memory error caught.")
        raise HTTPException(status_code=507, detail="GPU out of memory. Try reducing steps or complexity.")
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {
        "status": "healthy" if pipe else "loading",
        "device": DEVICE,
        "model": MODEL_ID
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
