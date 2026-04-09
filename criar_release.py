"""
Script para criar uma nova release no GitHub
"""
import os
import json
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

def create_release_zip(version: str):
    """Cria arquivo ZIP da versão atual"""
    zip_name = f"impressao-3d-pro-v{version}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Arquivos a incluir
        files_to_include = [
            'main.py',
            'calculadora.py',
            'banco_dados.py',
            'interface.py',
            'updater.py',
            'version.json',
            'README.md',
            'LICENSE'
        ]
        
        for file in files_to_include:
            if Path(file).exists():
                zipf.write(file, file)
        
        # Incluir pasta database se existir
        if Path('database').exists():
            for file in Path('database').glob('*'):
                zipf.write(file, f"database/{file.name}")
    
    print(f"✅ ZIP criado: {zip_name}")
    return zip_name

def update_version_file(version: str):
    """Atualiza arquivo version.json"""
    version_data = {
        "version": version,
        "release_date": datetime.now().strftime('%Y-%m-%d'),
        "min_supported_version": "1.0.0",
        "update_url": "https://api.github.com/repos/SEU_USUARIO/impressao-3d-pro-calculator/releases/latest"
    }
    
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Version file atualizado: {version}")

def create_github_release(version: str, zip_file: str, release_notes: str):
    """Cria release no GitHub usando GitHub CLI"""
    commands = [
        f'gh release create v{version} "{zip_file}"',
        f'--title "Versão {version}"',
        f'--notes "{release_notes}"'
    ]
    
    cmd = ' '.join(commands)
    print(f"\nExecute este comando para criar a release:")
    print(cmd)
    print("\nOu use o GitHub Web UI para criar a release manualmente.")

def main():
    print("=== Criar Nova Release ===")
    
    # Ler versão atual
    with open('version.json', 'r') as f:
        current = json.load(f)['version']
    
    print(f"Versão atual: {current}")
    print("\nTipos de bump:")
    print("1 - Patch (1.0.0 -> 1.0.1) [correções de bugs]")
    print("2 - Minor (1.0.0 -> 1.1.0) [novas funcionalidades]")
    print("3 - Major (1.0.0 -> 2.0.0) [grandes mudanças]")
    
    choice = input("\nEscolha: ")
    
    bump_type = {1: 'patch', 2: 'minor', 3: 'major'}.get(int(choice), 'patch')
    
    from updater import VersionHelper
    new_version = VersionHelper.bump_version(current, bump_type)
    
    print(f"\nNova versão: {new_version}")
    confirm = input("Confirmar? (s/n): ")
    
    if confirm.lower() == 's':
        # Atualizar arquivos
        update_version_file(new_version)
        
        # Criar ZIP
        zip_file = create_release_zip(new_version)
        
        # Notas de release (você pode editar isso)
        release_notes = f"""## Versão {new_version}

### 🚀 Novidades
- Implementado sistema de atualizações automáticas
- Melhorias na interface

### 🐛 Correções
- Correções de bugs e melhorias de performance

### 📝 Observações
- Consulte o README para mais informações
"""
        
        # Instruções para criar release
        create_github_release(new_version, zip_file, release_notes)
        
        print(f"\n✅ Preparado para release v{new_version}")

if __name__ == "__main__":
    main()
    