import easyocr
import time



class OCRReader:  # Ubah nama class menjadi lebih spesifik
    def __init__(self):
        start_time = time.time()
        self.reader = easyocr.Reader(['en', 'id'], gpu=False)
        end_time = time.time()
        self.installing_model_time = end_time - start_time

    @property
    def debug_message(self):
        debug_msg = f"DEBUG - Total time taken for installing the model: {self.installing_model_time:.2f} seconds"
        print(debug_msg)
        return debug_msg