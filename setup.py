#!/usr/bin/env python3
"""
Setup script for AI Meeting Summarizer
Helps with initial configuration
"""
import os
import sys
from pathlib import Path
import shutil

def create_env_file():
    """Create .env file from template"""
    if Path('.env').exists():
        response = input('.env file already exists. Overwrite? (y/N): ')
        if response.lower() != 'y':
            print('Skipping .env creation')
            return
    
    template_file = '.env.template' if Path('.env.template').exists() else '.env.example'
    
    if not Path(template_file).exists():
        print(f'Warning: {template_file} not found')
        return
    
    shutil.copy(template_file, '.env')
    print(f'✓ Created .env file from {template_file}')
    print('  Please edit .env and add your API keys')

def create_directories():
    """Create necessary directories"""
    dirs = [
        'data',
        'data/audio',
        'models',
    ]
    
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f'✓ Created directory: {directory}')

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print('❌ Python 3.8+ is required')
        print(f'   Current version: {sys.version}')
        sys.exit(1)
    print(f'✓ Python version: {sys.version_info.major}.{sys.version_info.minor}')

def install_python_deps():
    """Install Python dependencies"""
    print('\nInstalling Python dependencies...')
    response = input('Install Python packages from requirements.txt? (Y/n): ')
    
    if response.lower() != 'n':
        import subprocess
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print('✓ Python dependencies installed')
        except subprocess.CalledProcessError as e:
            print(f'❌ Error installing Python dependencies: {e}')
            return False
    return True

def install_node_deps():
    """Install Node dependencies"""
    print('\nInstalling Node dependencies...')
    response = input('Install Node packages from package.json? (Y/n): ')
    
    if response.lower() != 'n':
        import subprocess
        try:
            subprocess.check_call(['npm', 'install'])
            print('✓ Node dependencies installed')
        except subprocess.CalledProcessError as e:
            print(f'❌ Error installing Node dependencies: {e}')
            print('   Make sure Node.js and npm are installed')
            return False
    return True

def setup_api_keys():
    """Interactive API key setup"""
    print('\n' + '='*50)
    print('API Key Configuration')
    print('='*50)
    print('\nYou need at least ONE of these API keys for AI features:')
    print('1. OpenAI (GPT-4) - https://platform.openai.com/api-keys')
    print('2. Anthropic (Claude) - https://console.anthropic.com/')
    print('3. Or use local models (no API key needed)')
    
    response = input('\nWould you like to configure API keys now? (y/N): ')
    
    if response.lower() == 'y':
        openai_key = input('OpenAI API Key (or press Enter to skip): ').strip()
        anthropic_key = input('Anthropic API Key (or press Enter to skip): ').strip()
        
        if openai_key or anthropic_key:
            # Update .env file
            env_path = Path('.env')
            if env_path.exists():
                content = env_path.read_text()
                
                if openai_key:
                    content = content.replace('OPENAI_API_KEY=', f'OPENAI_API_KEY={openai_key}')
                if anthropic_key:
                    content = content.replace('ANTHROPIC_API_KEY=', f'ANTHROPIC_API_KEY={anthropic_key}')
                
                env_path.write_text(content)
                print('✓ API keys saved to .env')
        else:
            print('No API keys configured. You can use local models or add them later in .env')

def main():
    """Main setup function"""
    print('='*50)
    print('AI Meeting Summarizer - Setup')
    print('='*50)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    print('\nCreating directories...')
    create_directories()
    
    # Create .env file
    print('\nSetting up configuration...')
    create_env_file()
    
    # Install dependencies
    python_ok = install_python_deps()
    node_ok = install_node_deps()
    
    if python_ok and node_ok:
        # Configure API keys
        setup_api_keys()
        
        print('\n' + '='*50)
        print('✅ Setup Complete!')
        print('='*50)
        print('\nNext steps:')
        print('1. Edit .env file with your API keys (if not done)')
        print('2. Run: python test_installation.py')
        print('3. Run: npm start')
        print('\n📖 See README.md for full documentation')
        print('🚀 See QUICKSTART.md for quick start guide')
    else:
        print('\n⚠️  Setup completed with warnings')
        print('Please fix the issues above and try again')

if __name__ == '__main__':
    main()

