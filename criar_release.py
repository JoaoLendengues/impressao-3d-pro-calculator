"""
Script para criar uma nova versão
"""
import json
import subprocess
from datetime import datetime

def update_version(version_type='patch'):
    """Atualiza versão no version.json"""
    
    # Ler versão atual
    with open('version.json', 'r') as f:
        data = json.load(f)
    
    current = data['version']
    parts = [int(x) for x in current.split('.')]
    
    if version_type == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif version_type == 'minor':
        parts[1] += 1
        parts[2] = 0
    else:  # patch
        parts[2] += 1
    
    new_version = '.'.join(map(str, parts))
    
    # Atualizar arquivo
    data['version'] = new_version
    data['release_date'] = datetime.now().strftime('%Y-%m-%d')
    
    with open('version.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Versão atualizada: {current} → {new_version}")
    return new_version

def criar_release():
    """Cria tag e push para o GitHub"""
    print("\n=== CRIAR NOVA RELEASE ===\n")
    print("1 - Patch (correções) 1.0.0 → 1.0.1")
    print("2 - Minor (novidades) 1.0.0 → 1.1.0")
    print("3 - Major (grandes)   1.0.0 → 2.0.0")
    
    choice = input("\nEscolha: ")
    
    types = {'1': 'patch', '2': 'minor', '3': 'major'}
    version_type = types.get(choice, 'patch')
    
    new_version = update_version(version_type)
    
    print(f"\n📦 Nova versão: v{new_version}")
    confirm = input("Confirmar release? (s/n): ")
    
    if confirm.lower() == 's':
        # Commit da mudança
        subprocess.run(['git', 'add', 'version.json'])
        subprocess.run(['git', 'commit', '-m', f'Bump version to {new_version}'])
        subprocess.run(['git', 'push'])
        
        # Criar tag
        subprocess.run(['git', 'tag', f'v{new_version}'])
        subprocess.run(['git', 'push', 'origin', f'v{new_version}'])
        
        print(f"\n✅ Release v{new_version} criada!")
        print("📝 O GitHub Actions vai criar o release automaticamente")
        print("🔗 Acompanhe em: Actions -> Seu repositório no GitHub")

if __name__ == "__main__":
    criar_release()
    