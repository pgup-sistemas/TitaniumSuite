import os
from PIL import Image
import shutil

class ImageTools:
    def __init__(self, logger_callback=None):
        self.log = logger_callback if logger_callback else print

    def _get_output_path(self, input_path, output_dir, suffix=""):
        """Gera o caminho de saída, garantindo que o diretório exista."""
        if not output_dir:
            output_dir = os.path.dirname(input_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        base, ext = os.path.splitext(os.path.basename(input_path))
        
        # Garante que a extensão seja minúscula para consistência
        ext = ext.lower()
        
        # Se o sufixo for vazio, tenta evitar sobrescrever o original
        if not suffix:
            suffix = "_processed"
            
        return os.path.join(output_dir, f"{base}{suffix}{ext}")

    def redimensionar_imagem(self, input_path, output_dir, width=None, height=None, percent=None, quality=90):
        """Redimensiona uma imagem, mantendo a proporção."""
        try:
            img = Image.open(input_path)
            original_width, original_height = img.size
            
            if percent:
                new_width = int(original_width * (percent / 100))
                new_height = int(original_height * (percent / 100))
            elif width and height:
                new_width = width
                new_height = height
            elif width:
                new_width = width
                new_height = int(original_height * (width / original_width))
            elif height:
                new_height = height
                new_width = int(original_width * (height / original_height))
            else:
                self.log(f"⚠️ {os.path.basename(input_path)}: Nenhum parâmetro de redimensionamento fornecido.")
                return False

            # Redimensiona com filtro de alta qualidade (ANTIALIAS)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            output_path = self._get_output_path(input_path, output_dir, suffix=f"_{new_width}x{new_height}")
            
            # Salva a imagem
            img_resized.save(output_path, quality=quality, optimize=True)
            self.log(f"✅ Redimensionado: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
            return True
            
        except Exception as e:
            self.log(f"❌ Erro ao redimensionar {os.path.basename(input_path)}: {e}")
            return False

    def converter_imagem(self, input_path, output_dir, target_format, quality=90):
        """Converte uma imagem para um formato específico."""
        try:
            img = Image.open(input_path)
            
            # Garante que o formato alvo seja minúsculo e sem o ponto
            target_format = target_format.upper().replace(".", "")
            
            base, _ = os.path.splitext(os.path.basename(input_path))
            output_path = os.path.join(output_dir, f"{base}.{target_format.lower()}")
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Salva a imagem no novo formato
            if target_format == "JPG" or target_format == "JPEG":
                img.save(output_path, "JPEG", quality=quality, optimize=True)
            elif target_format == "PNG":
                # PNG não usa qualidade, mas pode usar otimização
                img.save(output_path, "PNG", optimize=True)
            elif target_format == "WEBP":
                img.save(output_path, "WEBP", quality=quality, optimize=True)
            else:
                img.save(output_path, target_format)
                
            self.log(f"✅ Convertido: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
            return True
            
        except Exception as e:
            self.log(f"❌ Erro ao converter {os.path.basename(input_path)}: {e}")
            return False

    def comprimir_imagem(self, input_path, output_dir, quality=70):
        """Comprime uma imagem (principalmente JPG) para reduzir o tamanho do arquivo."""
        try:
            img = Image.open(input_path)
            
            # A compressão é feita ao salvar com uma qualidade menor
            output_path = self._get_output_path(input_path, output_dir, suffix="_compressed")
            
            # Se for PNG, a compressão é feita pela otimização (não usa quality)
            if img.format == "PNG":
                img.save(output_path, "PNG", optimize=True)
            else:
                # Para JPG e outros, usa o parâmetro quality
                img.save(output_path, quality=quality, optimize=True)
                
            self.log(f"✅ Comprimido: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
            return True
            
        except Exception as e:
            self.log(f"❌ Erro ao comprimir {os.path.basename(input_path)}: {e}")
            return False
