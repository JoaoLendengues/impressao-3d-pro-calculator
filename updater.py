"""
Sistema de atualizações automáticas via GitHub
"""
import json
import os
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime, timedelta

import requests
from PySide6.QtCore import QThread, Signal, QObject, QTimer
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QApplication


class UpdateChecker(QThread):
    """Thread para verificar atualizações em background"""
    
    update_available = Signal(dict)
    no_update = Signal()
    error_occurred = Signal(str)
    
    def __init__(self, current_version: str, repo_owner: str, repo_name: str):
        super().__init__()
        self.current_version = current_version
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.check_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self._is_running = True
    
    def run(self):
        """Verifica por atualizações"""
        try:
            response = requests.get(self.check_url, timeout=10)
            response.raise_for_status()
            
            if not self._is_running:
                return
                
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            
            if self._is_newer_version(latest_version, self.current_version):
                update_info = {
                    'version': latest_version,
                    'name': release_data.get('name', f'Versão {latest_version}'),
                    'body': release_data.get('body', ''),
                    'download_url': self._get_download_url(release_data),
                    'published_at': release_data.get('published_at', '')
                }
                self.update_available.emit(update_info)
            else:
                self.no_update.emit()
                
        except Exception as e:
            if self._is_running:
                self.error_occurred.emit(f"Erro: {str(e)}")
    
    def stop(self):
        """Para a thread"""
        self._is_running = False
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compara versões"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)
            
            return latest_parts > current_parts
        except:
            return False
    
    def _get_download_url(self, release_data: dict):
        """Obtém URL do arquivo para download"""
        for asset in release_data.get('assets', []):
            if asset['name'].endswith('.zip'):
                return asset['browser_download_url']
        return None


class DownloadWorker(QThread):
    """Thread para download da atualização"""
    
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self._is_running = True
    
    def run(self):
        try:
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, 'update_temp.zip')
            
            response = requests.get(self.url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk and self._is_running:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.progress.emit(progress)
            
            if self._is_running:
                self.finished.emit(zip_path)
            
        except Exception as e:
            if self._is_running:
                self.error.emit(str(e))
    
    def stop(self):
        """Para a thread"""
        self._is_running = False


class UpdateManager(QObject):
    """Gerencia o processo de atualização"""
    
    def __init__(self, app_path: str, repo_owner: str, repo_name: str):
        super().__init__()
        self.app_path = Path(app_path)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.version_file = self.app_path / 'version.json'
        self.current_version = self.load_current_version()
        self.checker = None
        self.downloader = None
    
    def load_current_version(self) -> str:
        """Carrega a versão atual"""
        try:
            if self.version_file.exists():
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version', '1.0.0')
        except:
            pass
        return '1.0.0'
    
    def check_for_updates(self, parent_widget=None, show_no_update_msg=False):
        """Verifica por atualizações"""
        # Limpar checker anterior se existir
        if self.checker is not None:
            self.checker.stop()
            self.checker.quit()
            self.checker.wait()
        
        self.checker = UpdateChecker(self.current_version, self.repo_owner, self.repo_name)
        
        def on_update_available(update_info):
            self.prompt_update_dialog(update_info, parent_widget)
        
        def on_no_update():
            if show_no_update_msg and parent_widget:
                QMessageBox.information(parent_widget, "Sem Atualizações", 
                                       "Você já está usando a versão mais recente!")
        
        def on_error(error_msg):
            if show_no_update_msg and parent_widget:
                QMessageBox.warning(parent_widget, "Erro", error_msg)
        
        self.checker.update_available.connect(on_update_available)
        self.checker.no_update.connect(on_no_update)
        self.checker.error_occurred.connect(on_error)
        self.checker.finished.connect(self.checker.deleteLater)
        self.checker.start()
        
        return self.checker
    
    def prompt_update_dialog(self, update_info: dict, parent_widget=None):
        """Mostra diálogo de atualização"""
        msg = QMessageBox(parent_widget)
        msg.setWindowTitle("Atualização Disponível!")
        msg.setIcon(QMessageBox.Information)
        
        message = f"""<h3>Nova versão disponível!</h3>
        <p><b>Versão atual:</b> {self.current_version}<br>
        <b>Nova versão:</b> {update_info['version']}</p>
        
        <p><b>{update_info['name']}</b></p>
        <p>{update_info['body'][:300]}</p>
        
        <p>Deseja atualizar agora?</p>
        """
        
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Later)
        
        if msg.exec() == QMessageBox.Yes:
            self.perform_update(update_info, parent_widget)
    
    def perform_update(self, update_info: dict, parent_widget=None):
        """Executa o download e instalação"""
        if not update_info.get('download_url'):
            QMessageBox.warning(parent_widget, "Erro", "URL de download não encontrada!")
            return
        
        progress = QProgressDialog("Baixando atualização...", "Cancelar", 0, 100, parent_widget)
        progress.setWindowTitle("Atualizando")
        progress.setWindowModality(2)
        progress.setMinimumDuration(0)
        
        # Limpar downloader anterior
        if self.downloader is not None:
            self.downloader.stop()
            self.downloader.quit()
            self.downloader.wait()
        
        self.downloader = DownloadWorker(update_info['download_url'])
        
        def on_progress(value):
            progress.setValue(value)
            progress.setLabelText(f"Baixando... {value}%")
        
        def on_finished(zip_path):
            progress.setLabelText("Instalando...")
            self.install_update(zip_path, parent_widget)
            progress.close()
        
        def on_error(error_msg):
            progress.close()
            QMessageBox.critical(parent_widget, "Erro", f"Falha no download: {error_msg}")
        
        self.downloader.progress.connect(on_progress)
        self.downloader.finished.connect(on_finished)
        self.downloader.error.connect(on_error)
        self.downloader.finished.connect(self.downloader.deleteLater)
        
        progress.canceled.connect(self.cancel_download)
        self.downloader.start()
        progress.exec()
    
    def cancel_download(self):
        """Cancela o download em andamento"""
        if self.downloader is not None:
            self.downloader.stop()
            self.downloader.quit()
            self.downloader.wait()
    
    def install_update(self, zip_path: str, parent_widget=None):
        """Instala a atualização"""
        try:
            extract_dir = tempfile.mkdtemp()
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Criar script de atualização
            script_path = self.create_update_script(extract_dir)
            
            # Executar script
            if sys.platform == 'win32':
                os.startfile(script_path)
            else:
                os.system(f'python "{script_path}" &')
            
            # Fechar aplicativo
            QApplication.quit()
            
        except Exception as e:
            QMessageBox.critical(parent_widget, "Erro", f"Falha na instalação: {str(e)}")
    
    def create_update_script(self, extract_dir: str) -> str:
        """Cria script para aplicar atualização"""
        script_content = f'''import os
import sys
import shutil
import time
import subprocess

def main():
    time.sleep(2)
    
    app_dir = r"{self.app_path}"
    update_dir = r"{extract_dir}"
    
    try:
        for item in os.listdir(update_dir):
            src = os.path.join(update_dir, item)
            dst = os.path.join(app_dir, item)
            
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src) and item not in ['database', '__pycache__', '.git']:
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        
        shutil.rmtree(update_dir)
        subprocess.Popen([sys.executable, os.path.join(app_dir, "main.py")])
        
    except Exception as e:
        with open(os.path.join(app_dir, "update_error.log"), 'w') as f:
            f.write(str(e))
        input(f"Erro na atualização: {{e}}\\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
'''
        script_path = os.path.join(extract_dir, "update_installer.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path
    
    def __del__(self):
        """Destrutor para limpar threads"""
        if self.checker is not None:
            self.checker.stop()
            self.checker.quit()
            self.checker.wait()
        if self.downloader is not None:
            self.downloader.stop()
            self.downloader.quit()
            self.downloader.wait()
            