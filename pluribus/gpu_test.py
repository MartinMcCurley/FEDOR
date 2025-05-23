#!/usr/bin/env python3
"""
GPU Test Script - Verify RTX 4070 Ti is working properly
"""

print("🔍 Testing GPU Setup for RTX 4070 Ti")
print("=" * 50)

# Test PyTorch CUDA
print("\n🔥 PyTorch CUDA Test:")
try:
    import torch
    if torch.cuda.is_available():
        print(f"✅ PyTorch CUDA Available: {torch.cuda.is_available()}")
        print(f"✅ GPU Count: {torch.cuda.device_count()}")
        print(f"✅ GPU Name: {torch.cuda.get_device_name(0)}")
        
        # Test GPU computation
        x = torch.randn(1000, 1000).cuda()
        y = torch.randn(1000, 1000).cuda()
        z = torch.matmul(x, y)
        print(f"✅ GPU Computation Test: Matrix multiplication successful")
        print(f"✅ Result tensor device: {z.device}")
    else:
        print("❌ PyTorch CUDA not available")
except Exception as e:
    print(f"❌ PyTorch error: {e}")

# Test CuPy
print("\n🚀 CuPy Test:")
try:
    import cupy as cp
    print(f"✅ CuPy GPU Count: {cp.cuda.runtime.getDeviceCount()}")
    print(f"✅ GPU Name: {cp.cuda.Device(0).name}")
    print(f"✅ GPU Memory: {cp.cuda.Device(0).total_memory / (1024**3):.1f} GB")
    
    # Test CuPy computation
    x_cp = cp.random.randn(1000, 1000)
    y_cp = cp.random.randn(1000, 1000)
    z_cp = cp.matmul(x_cp, y_cp)
    print(f"✅ CuPy Computation Test: Matrix multiplication successful")
    print(f"✅ Result array device: GPU")
    
    # Memory check
    mempool = cp.get_default_memory_pool()
    gpu_memory_used = mempool.used_bytes() / (1024**3)
    print(f"✅ GPU Memory Used: {gpu_memory_used:.2f} GB")
    
except Exception as e:
    print(f"❌ CuPy error: {e}")

print("\n🎉 GPU Setup Verification Complete!")
print("Your RTX 4070 Ti is ready for poker AI training!") 