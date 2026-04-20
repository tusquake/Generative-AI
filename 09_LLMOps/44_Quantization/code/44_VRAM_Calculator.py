def calculate_vram_usage(params_billions: float, bits: int):
    """
    Calculates theoretical VRAM usage.
    params_billions: Model size in B (e.g. 7, 70)
    bits: Precision (4, 8, 16)
    """
    # Bytes per parameter
    bytes_per_param = bits / 8
    
    # Base model size
    model_size_gb = params_billions * bytes_per_param
    
    # 25% overhead for KV Cache and Context
    total_vram_gb = model_size_gb * 1.25
    
    return model_size_gb, total_vram_gb

if __name__ == "__main__":
    # Example: Llama 3 70B in 4-bit quantization
    p = 70  # Llama-70B
    b = 4   # 4-bit
    base, total = calculate_vram_usage(p, b)
    
    print("-" * 30)
    print(f"📊 VRAM ESTIMATOR")
    print("-" * 30)
    print(f"Model Size: {p}B Parameters")
    print(f"Precision:  {b}-bit")
    print(f"Base Weights: {base:.2f} GB")
    print(f"Recommended VRAM: {total:.2f} GB")
    print("-" * 30)
    print("[Senior Note] Always account for context length (KV Cache). "
          "A large context window (128k+) can easily double the VRAM "
          "required beyond just the base weights.")
