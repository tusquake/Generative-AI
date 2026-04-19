import numpy as np

def run_lora_parameter_analysis():
    """
    Demonstrates the mathematical efficiency of LoRA (Low-Rank Adaptation).
    We compare a standard 7B parameter model's weight updates 
    against a LoRA adapter with Rank 8.
    """
    
    # Configuration for a Llama-3 7B style model
    model_name = "Llama-3 7B"
    hidden_dimension = 4096
    num_attention_layers = 32
    
    print("-" * 50)
    print(f"PEFT ANALYSIS: {model_name}")
    print("-" * 50)

    # 1. Full Fine-Tuning Math
    # In Full FT, we update every single weight in the weight matrices
    # For simplicity, let's look at the Query/Value matrices in attention
    weights_per_layer = (hidden_dimension * hidden_dimension) * 2 # Q and V
    total_full_ft_params = weights_per_layer * num_attention_layers
    
    print(f"Full FT Trainable Parameters (Q/V only): {total_full_ft_params:,}")

    # 2. LoRA Math (Rank = 8)
    # Instead of updating Dim x Dim, we train two small matrices:
    # Matrix A: Dim x Rank
    # Matrix B: Rank x Dim
    rank = 8
    lora_params_per_layer = (hidden_dimension * rank) * 2 * 2 # (A+B) * (Q and V)
    total_lora_params = lora_params_per_layer * num_attention_layers
    
    print(f"LoRA Trainable Parameters (Rank={rank}): {total_lora_params:,}")

    # 3. Efficiency Calculation
    savings = (1 - (total_lora_params / total_full_ft_params)) * 100
    footprint_mb = (total_lora_params * 4) / (1024 * 1024) # Assuming FP32 (4 bytes per param)

    print("-" * 50)
    print(f"PARAMETER REDUCTION: {savings:.2f}%")
    print(f"ADAPTER DISK SIZE: ~{footprint_mb:.2f} MB")
    print("-" * 50)

    # 4. Simulation of Rank-Decomposition
    print("Visualizing Rank-Decomposition (Dimension Compression):")
    # Original Matrix (4096 x 4096) -> 16.7 Million items
    # LoRA A (4096 x 8) + LoRA B (8 x 4096) -> 65,536 items
    print(f"  [4096 x 4096] Weight Matrix")
    print(f"  REPLACED BY")
    print(f"  [4096 x {rank}] Matrix A  +  [{rank} x 4096] Matrix B")
    print("-" * 50)

    print("INSIGHT:")
    print("Because the 'Base' model weights are frozen, we don't need")
    print("to store their gradients or optimizer states. This reduces")
    print("VRAM requirements by up to 80%, allowing 7B models to be")
    print("fine-tuned on a single consumer GPU.")
    print("-" * 50)

if __name__ == "__main__":
    run_lora_parameter_analysis()
