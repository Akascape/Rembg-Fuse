"""
bg_remover.py
=================
Author: Akascape
License: MIT License - Copyright (c) 2026 Akascape
Script Version: 0.3

Background Remover Script for DaVinci Resolve Fusion
This script uses the rembg library to remove backgrounds from images.
It is designed to be used within the DaVinci Resolve Fusion environment.
"""

import sys
import os
import time
import rembg
from PIL import Image

# Set UTF-8 encoding for better compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class FuseBackgroundRemover:
    def __init__(self, model_name='u2netp'):
        """Initialize rembg with specified model"""

        self.log("="*50)
        self.log(f"Loading background removal model: {model_name}")
        
        # Check GPU availability and configure providers
        self._check_and_configure_gpu()

        try:
            # Use providers parameter to enable GPU if available
            self.session = rembg.new_session(model_name, providers=self.providers)
            self.log("[SUCCESS] Model loaded successfully!")
            self.log(f"[INFO] Using providers: {self.providers}")

        except Exception as e:
            self.log(f"[ERROR] Error loading model {model_name}: {e}")
            self.log("[WARNING] Falling back to u2netp model")
        
            try:
                self.session = rembg.new_session('u2netp', providers=self.providers)
                self.log("[SUCCESS] Fallback model loaded successfully!")
            except Exception as fallback_error:
                self.log(f"[CRITICAL] Critical error: Could not load any model: {fallback_error}")
                raise fallback_error
    
    def _check_and_configure_gpu(self):
        """Check GPU availability and configure ONNX Runtime providers"""
        try:
            import onnxruntime as ort
            available_providers = ort.get_available_providers()
            self.log(f"[INFO] Available ONNX providers: {available_providers}")
            
            # Priority order: TensorRT (best for RTX) > CUDA > ROCm > CPU
            self.providers = []
            gpu_found = False
            
            if 'TensorrtExecutionProvider' in available_providers:
                self.providers.append('TensorrtExecutionProvider')
                self.log("[INFO] GPU detected: TensorRT will be used (FASTEST for RTX GPUs)")
                gpu_found = True
            elif 'CUDAExecutionProvider' in available_providers:
                self.providers.append('CUDAExecutionProvider')
                self.log("[INFO] GPU detected: NVIDIA CUDA will be used")
                gpu_found = True
            elif 'ROCMExecutionProvider' in available_providers:
                self.providers.append('ROCMExecutionProvider')
                self.log("[INFO] GPU detected: AMD ROCm will be used")
                gpu_found = True
            
            # Always add CPU as fallback
            self.providers.append('CPUExecutionProvider')
            
            if not gpu_found:
                self.log("[WARNING] No GPU detected! Using CPU only (slow)")
                self.log("[WARNING] Make sure you have onnxruntime-gpu installed")
                self.log("[WARNING] Run: pip install onnxruntime-gpu")
                
        except ImportError:
            self.log("[WARNING] onnxruntime not properly installed")
            self.providers = None  # Let rembg use default
        except Exception as e:
            self.log(f"[WARNING] GPU configuration error: {e}")
            self.providers = None  # Let rembg use default
    
    def log(self, message):
        """Print log message with timestamp and flush immediately."""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        try:
            print(f"[{timestamp}] {message}")
            sys.stdout.flush()  
        except UnicodeEncodeError:
            # Fallback for encoding issues
            print(f"[{timestamp}] {message.encode('ascii', 'ignore').decode('ascii')}")
            sys.stdout.flush()
    
    def process_image(self, input_path, output_path):
        """Remove background from image file."""
        try:
            # Log processing start
            self.log("-"*50)
            self.log(f"[INPUT] Input path: {input_path}")
            self.log(f"[OUTPUT] Output path: {output_path}")
            
            # Check if input file exists
            if not os.path.exists(input_path):
                self.log(f"[ERROR] Input file does not exist: {input_path}")
                return False
            
            # Load image
            self.log("[STEP 1/4] Loading image...")
            pil_image = Image.open(input_path)
            self.log(f"Image loaded: {pil_image.size[0]}x{pil_image.size[1]} pixels, mode: {pil_image.mode}")
            
            # Ensure RGB mode for processing
            if pil_image.mode != 'RGB':
                self.log(f"[STEP 2/4] Converting from {pil_image.mode} to RGB...")
                pil_image = pil_image.convert('RGB')
            else:
                self.log("[STEP 2/4] Image already in RGB mode")
            
            # Remove background
            self.log("[STEP 3/4] Running background removal AI model...")
            start_time = time.time()
            
            result = rembg.remove(pil_image, session=self.session)
            
            processing_time = time.time() - start_time
            self.log(f"[SUCCESS] Background removal completed in {processing_time:.2f} seconds")
            self.log(f"[INFO] Output image: {result.size[0]}x{result.size[1]} pixels, mode: {result.mode}")
            # Save with transparency (PNG)
            result.save(output_path, "PNG")
            self.log(f"[SUCCESS] Saved with transparency: {os.path.basename(output_path)}")
            # Verify output file was created
            if not os.path.exists(output_path):
                self.log("[ERROR] Output file generation failed!")
                return False
            self.log("-"*50)
            return True
            
        except Exception as e:
            self.log(f"[ERROR] Error processing image: {e}")
            self.log(f"[ERROR] Exception type: {type(e).__name__}")
            return False

def main():

    def log_main(message):
        """Log messages with timestamp for the main script."""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        try:
            print(f"[{timestamp}] MAIN: {message}")
            sys.stdout.flush()
        except UnicodeEncodeError:
            print(f"[{timestamp}] MAIN: {message.encode('ascii', 'ignore').decode('ascii')}")
            sys.stdout.flush()
    
    log_main("[START] REMBG Script Started")

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    model_name = sys.argv[3]
    if not os.path.exists(input_path):
        log_main(f"[ERROR] Input file does not exist: {input_path}")
        sys.exit(1)
    
    # Initialize background remover
    try:
        log_main("[INIT] Initializing REMBG...")
        bg_remover = FuseBackgroundRemover(model_name)
        
        # Process the image
        # Process the image
        success = bg_remover.process_image(input_path, output_path)
        if success:
            log_main("[COMPLETE] Background removal completed successfully!")
            sys.exit(0)
        else:
            log_main("[FAILED] Background removal failed!")
            sys.exit(1)
            
    except Exception as e:
        log_main(f"[FATAL] Fatal error: {e}")
        log_main(f"[FATAL] Exception type: {type(e).__name__}")
        log_main("[CHECK] Check your Python environment and dependencies")
        sys.exit(1)

if __name__ == "__main__":
    main()
