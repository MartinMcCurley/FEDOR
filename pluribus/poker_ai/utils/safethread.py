from typing import Optional, Iterable, Callable

import ctypes
import multiprocessing
import time
import platform
from multiprocessing.shared_memory import SharedMemory

import numpy as np
from tqdm import tqdm

# Try to import CuPy for GPU acceleration
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print(f"GPU detected: {cp.cuda.runtime.getDeviceCount()} devices")
except ImportError:
    GPU_AVAILABLE = False
    cp = None
    print("CuPy not available, using CPU only")

# Move the nested function outside to make it picklable on Windows
def _process_all_worker(batch, cursor, result_size, result_width, tasker):
    """Worker function for multiprocessing that can be pickled."""
    sm = SharedMemory("result_sm")
    result = np.ndarray(
        (result_size, result_width), dtype=np.double, buffer=sm.buf
    )
    tasker(batch, cursor, result)
    sm.close()

def multiprocess_ehs_calc(
    source_iter: Iterable[any],
    tasker: Callable[[Iterable[any], int, int], None],
    result_size: int = None,
    result_width: int = 3,
):
    result_size = result_size or len(source_iter)
    
    # GPU acceleration option - try this first
    if GPU_AVAILABLE and platform.system() == "Windows":
        try:
            print("Attempting GPU-accelerated processing...")
            result = cp.zeros((result_size, result_width), dtype=cp.float64)
            
            # Convert iterator to list if needed
            if hasattr(source_iter, '__iter__') and not hasattr(source_iter, '__len__'):
                source_list = list(source_iter)
            else:
                source_list = source_iter
                
            # Process all items using GPU when possible
            batch_size = 1000  # Process in batches to avoid memory issues
            
            with tqdm(total=result_size, ascii=" >=", desc="GPU Processing") as pbar:
                for i in range(0, len(source_list), batch_size):
                    batch_end = min(i + batch_size, len(source_list))
                    batch = source_list[i:batch_end]
                    
                    # Create temporary CPU result for this batch
                    temp_result = np.zeros((len(batch), result_width), dtype=np.float64)
                    
                    # Process the batch (CPU operations that could be parallelized)
                    for j, item in enumerate(batch):
                        single_batch = [item]
                        cursor = i + j
                        tasker(single_batch, cursor, temp_result[j:j+1])
                    
                    # Copy batch result to GPU memory
                    gpu_batch_result = cp.asarray(temp_result)
                    result[i:batch_end] = gpu_batch_result
                    
                    pbar.update(len(batch))
                    
            # Convert back to CPU for compatibility
            result_cpu = cp.asnumpy(result)
            return result_cpu, None
            
        except Exception as e:
            print(f"GPU processing failed ({e}), falling back to CPU...")
            # Fall through to CPU processing
    
    # Fallback to single-threaded processing on Windows due to pickling issues
    if platform.system() == "Windows":
        print("Using single-threaded CPU processing on Windows...")
        result = np.zeros((result_size, result_width), dtype=np.double)
        
        # Convert iterator to list if needed
        if hasattr(source_iter, '__iter__') and not hasattr(source_iter, '__len__'):
            source_list = list(source_iter)
        else:
            source_list = source_iter
            
        # Process all items in a single thread
        with tqdm(total=result_size, ascii=" >=", desc="CPU Processing") as pbar:
            for i, item in enumerate(source_list):
                # Create a single-item batch and process it
                batch = [item]
                cursor = i
                # Call the tasker function directly
                tasker(batch, cursor, result)
                pbar.update(1)
                
        # Create a dummy shared memory object for compatibility
        result_sm = None
        return result, result_sm
    
    # Original multiprocessing code for non-Windows systems
    result_bytes = result_size * result_width * 8
    result_sm = SharedMemory(
        name="result_sm", create=True, size=result_bytes
    )
    result = np.ndarray(
        (result_size, result_width), dtype=np.double, buffer=result_sm.buf
    )
    
    worker_count = multiprocessing.cpu_count()
    batch_size = min(10_000, result_size // worker_count)
    cursor = 0
    max_batch_seconds = None
    batch_failed = False
    total = result_size
    if total is None:
        try:
            total = len(source_iter)
        except:
            pass

    with tqdm(total=total, ascii=" >=") as pbar:
        while True:
            task_done = False
            
            if batch_failed:
                batches = cached_batches
            else:
                batches = []
                for _ in range(worker_count):
                    batch = []
                    for _ in range(batch_size):
                        try:
                            batch.append(next(source_iter))
                        except StopIteration:
                            task_done = True
                            break
                    if len(batch) > 0:
                        batches.append(batch)
            
            cached_batches = batches
            batch_failed = False
            
            total_batch_size = 0
            processes = []

            start = time.time()
            for batch in batches:
                process = multiprocessing.Process(
                    target=_process_all_worker, 
                    args=(batch, cursor, result_size, result_width, tasker)
                )
                process.start()
                processes.append(process)
                total_batch_size += len(batch)
                cursor += len(batch)
        
            for process in processes:
                if max_batch_seconds is None:
                    process.join()
                    continue
                process.join(timeout=max_batch_seconds)

                if process.is_alive():
                    # Failed to handle this batch.
                    batch_failed = True
                    cursor -= total_batch_size
                    break

            if batch_failed:
                continue

            end = time.time()
            if max_batch_seconds is None:
                duration = end - start
                max_batch_seconds = int(duration * 3)
                
            pbar.update(total_batch_size)
            
            if task_done:
                break
    
    return result, result_sm


def batch_process(
    source_iter: Iterable[any],
    batch_process: Callable[[Iterable[any], int, multiprocessing.Array], None],
    result_type: ctypes._SimpleCData = ctypes.c_float,
    result_size: int = None,
    worker_count: Optional[int] = None,
    max_batch_size: Optional[int] = None,
):
    result_array = multiprocessing.Array(
        result_type, result_size
    )

    worker_count = worker_count or multiprocessing.cpu_count()
    batch_size = min(max_batch_size or 10_000, result_size // worker_count)
    cursor = 0
    max_batch_seconds = None
    batch_failed = False
    total = result_size
    if total is None:
        try:
            total = len(source_iter)
        except:
            pass

    with tqdm(total=total, ascii=" >=") as pbar:
        while True:
            task_done = False
            
            if batch_failed:
                batches = cached_batches
            else:
                batches = []
                for _ in range(worker_count):
                    batch = []
                    for _ in range(batch_size):
                        try:
                            batch.append(next(source_iter))
                        except StopIteration:
                            task_done = True
                            break
                    if len(batch) > 0:
                        batches.append(batch)
            
            cached_batches = batches
            batch_failed = False
            
            total_batch_size = 0
            processes = []

            start = time.time()
            for batch in batches:
                process = multiprocessing.Process(
                    target=batch_process, args=(batch, cursor, result_array)
                )
                process.start()
                processes.append(process)
                total_batch_size += len(batch)
                cursor += len(batch)
        
            for process in processes:
                if max_batch_seconds is None:
                    process.join()
                    continue
                process.join(timeout=max_batch_seconds)

                if process.is_alive():
                    # Failed to handle this batch.
                    batch_failed = True
                    cursor -= total_batch_size
                    break

            if batch_failed:
                continue

            end = time.time()
            if max_batch_seconds is None:
                duration = end - start
                max_batch_seconds = int(duration * 3)
                
            pbar.update(total_batch_size)
            
            if task_done:
                break
    
    return result_array
