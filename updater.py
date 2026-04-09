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
from typing import Optional, Dict, Tuple

import requests
from PySide6.QtCore import QThread, Signal, QObject
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
    
    def run(self):
        """Verifica por atualizações"""
        try:
            # Fazer requisição à API do GitHub
            response = requests.get(self.check_url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            
            # Comparar versões
            if self._is_newer_version(latest_version, self.current_version):
                # Nova versão disponível
                update_info = {
                    'version': latest_version,
                    'name': release_data.get('name', f'Versão {latest_version}'),
                    'body': release_data.get('body', ''),
                    'download_url': self._get_download_url(release_data),
                    'published_at': release_data.get('published_at', ''),
                    'is_prerelease': release_data.get('prerelease', False)
                }
                self.update_available.emit(update_info)
            else:
                self.no_update.emit()
                
        except requests.RequestException as e:
            self.error_occurred.emit(f"Erro ao verificar atualizações: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Erro inesperado: {str(e)}")
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compara versões no formato X.Y.Z"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Padding com zeros
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)
            
            return latest_parts > current_parts
        except:
            return False
    
    def _get_download_url(self, release_data: dict) -> Optional[str]:
        """Obtém URL do asset para download"""
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
    
    def run(self):
        try:
            # Criar arquivo temporário
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, 'update_temp.zip')
            
            # Download com progresso
            response = requests.get(self.url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.progress.emit(progress)
            
            self.finished.emit(zip_path)
            
        except Exception as e:
            self.error.emit(str(e))


class UpdateManager(QObject):
    """Gerencia o processo completo de atualização"""
    
    def __init__(self, app_path: str):
        super().__init__()
        self.app_path = Path(app_path)
        self.version_file = self.app_path / 'version.json'
        self.current_version = self.load_current_version()
        
        # Configurações do repositório GitHub
        self.repo_owner = "SEU_USUARIO"  # ALTERE PARA SEU USUÁRIO
        self.repo_name = "impressao-3d-pro-calculator"
        
        # Configurações de verificação
        self.last_check_file = self.app_path / '.last_update_check'
    
    def load_current_version(self) -> str:
        """Carrega a versão atual do arquivo"""
        try:
            if self.version_file.exists():
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version', '1.0.0')
        except:
            pass
        return '1.0.0'
    
    def save_current_version(self, version: str):
        """Salva a versão atual"""
        data = {
            'version': version,
            'release_date': datetime.now().strftime('%Y-%m-%d'),
            'update_url': f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        }
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def should_check_for_updates(self) -> bool:
        """Verifica se já passou tempo suficiente desde a última verificação"""
        if not self.last_check_file.exists():
            return True
        
        try:
            with open(self.last_check_file, 'r') as f:
                last_check = datetime.fromtimestamp(float(f.read()))
            
            # Verificar a cada 24 horas
            return datetime.now() - last_check > timedelta(hours=24)
        except:
            return True
    
    def update_last_check_time(self):
        """Atualiza o timestamp da última verificação"""
        with open(self.last_check_file, 'w') as f:
            f.write(str(datetime.now().timestamp()))
    
    def check_for_updates(self, parent_widget=None, show_no_update_msg=False):
        """Verifica por atualizações"""
        checker = UpdateChecker(self.current_version, self.repo_owner, self.repo_name)
        
        def on_update_available(update_info):
            self.update_last_check_time()
            self.prompt_update_dialog(update_info, parent_widget)
        
        def on_no_update():
            self.update_last_check_time()
            if show_no_update_msg and parent_widget:
                QMessageBox.information(parent_widget, "Sem Atualizações", 
                                       "Você já está usando a versão mais recente!")
        
        def on_error(error_msg):
            if show_no_update_msg and parent_widget:
                QMessageBox.warning(parent_widget, "Erro", error_msg)
        
        checker.update_available.connect(on_update_available)
        checker.no_update.connect(on_no_update)
        checker.error_occurred.connect(on_error)
        checker.start()
        
        return checker
    
    def prompt_update_dialog(self, update_info: dict, parent_widget=None):
        """Mostra diálogo perguntando se quer atualizar"""
        msg = QMessageBox(parent_widget)
        msg.setWindowTitle("Atualização Disponível!")
        msg.setIcon(QMessageBox.Information)
        
        # Formatar mensagem
        version = update_info['version']
        name = update_info['name']
        body = update_info['body'][:500]  # Limitar tamanho
        
        message = f"""<h3>Nova versão disponível!</h3>
        <p><b>Versão atual:</b> {self.current_version}<br>
        <b>Nova versão:</b> {version}</p>
        
        <p><b>{name}</b></p>
        <p>{body}</p>
        
        <p>Deseja atualizar agora?</p>
        """
        
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Later | QMessageBox.Ignore)
        
        # Botão "Sim" executa atualização
        if msg.exec() == QMessageBox.Yes:
            self.perform_update(update_info, parent_widget)
    
    def perform_update(self, update_info: dict, parent_widget=None):
        """Executa o processo de atualização"""
        if not update_info.get('download_url'):
            QMessageBox.warning(parent_widget, "Erro", 
                               "URL de download não encontrada!")
            return
        
        # Criar diálogo de progresso
        progress = QProgressDialog("Baixando atualização...", "Cancelar", 0, 100, parent_widget)
        progress.setWindowTitle("Atualizando")
        progress.setWindowModality(2)  # Application Modal
        progress.setMinimumDuration(0)
        
        # Download
        downloader = DownloadWorker(update_info['download_url'])
        
        def on_progress(value):
            progress.setValue(value)
            progress.setLabelText(f"Baixando... {value}%")
        
        def on_finished(zip_path):
            progress.setLabelText("Instalando atualização...")
            self.install_update(zip_path, parent_widget)
            progress.close()
        
        def on_error(error_msg):
            progress.close()
            QMessageBox.critical(parent_widget, "Erro", 
                               f"Falha no download: {error_msg}")
        
        downloader.progress.connect(on_progress)
        downloader.finished.connect(on_finished)
        downloader.error.connect(on_error)
        
        # Cancelar
        progress.canceled.connect(downloader.terminate)
        
        downloader.start()
        progress.exec()
    
    def install_update(self, zip_path: str, parent_widget=None):
        """Instala a atualização baixada"""
        try:
            # Criar diretório temporário para extração
            extract_dir = tempfile.mkdtemp()
            
            # Extrair ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Criar script de atualização
            update_script = self.create_update_script(extract_dir)
            
            # Executar script de atualização
            os.startfile(update_script) if sys.platform == 'win32' else os.system(f'python "{update_script}" &')
            
            # Fechar aplicativo atual
            QApplication.quit()
            
        except Exception as e:
            QMessageBox.critical(parent_widget, "Erro", 
                               f"Falha na instalação: {str(e)}")
    
    def create_update_script(self, extract_dir: str) -> str:
        """Cria script Python para aplicar atualização"""
        script_content = f'''
import os
import sys
import shutil
import time
import subprocess

def main():
    # Aguardar o app fechar completamente
    time.sleep(2)
    
    # Diretórios
    app_dir = r"{self.app_path}"
    update_dir = r"{extract_dir}"
    
    try:
        # Copiar novos arquivos
        for item in os.listdir(update_dir):
            src = os.path.join(update_dir, item)
            dst = os.path.join(app_dir, item)
            
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src) and item not in ['database', '__pycache__']:
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        
        # Limpar arquivos temporários
        shutil.rmtree(update_dir)
        
        # Reiniciar aplicativo
        subprocess.Popen([sys.executable, os.path.join(app_dir, "main.py")])
        
    except Exception as e:
        input(f"Erro na atualização: {{e}}\\nPressione Enter para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        script_path = os.path.join(extract_dir, "update_installer.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path


class VersionHelper:
    """Helper para gerenciar versões do aplicativo"""
    
    @staticmethod
    def bump_version(version: str, bump_type: str = 'patch') -> str:
        """
        Incrementa versão no formato major.minor.patch
        
        bump_type: 'major', 'minor', ou 'patch'
        """
        parts = [int(x) for x in version.split('.')]
        
        if bump_type == 'major':
            parts[0] += 1
            parts[1] = 0
            parts[2] = 0
        elif bump_type == 'minor':
            parts[1] += 1
            parts[2] = 0
        else:  # patch
            parts[2] += 1
        
        return '.'.join(map(str, parts))
    
    @staticmethod
    def create_release_notes(commits: list) -> str:
        """Cria notas de release baseadas nos commits"""
        notes = "## 🚀 Novidades\n\n"
        
        features = []
        fixes = []
        others = []
        
        for commit in commits:
            msg = commit['message'].lower()
            if 'feat' in msg or 'feature' in msg:
                features.append(f"- {commit['message']}")
            elif 'fix' in msg or 'bug' in msg:
                fixes.append(f"- {commit['message']}")
            else:
                others.append(f"- {commit['message']}")
        
        if features:
            notes += "### ✨ Novas Funcionalidades\n" + "\n".join(features) + "\n\n"
        if fixes:
            notes += "### 🐛 Correções\n" + "\n".join(fixes) + "\n\n"
        if others:
            notes += "### 📝 Outras Mudanças\n" + "\n".join(others) + "\n\n"
        
        return notes
    