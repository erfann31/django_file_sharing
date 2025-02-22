import os
import sys
import subprocess

def build_for_mac():
    # Ensure you're in the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # Create a virtual environment
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)

    # Activate virtual environment
    activate_this = os.path.join(project_root, 'venv', 'bin', 'activate_this.py')
    exec(open(activate_this).read(), {'__file__': activate_this})

    # Install dependencies
    subprocess.run([sys.executable, '-m', 'pip', 'install',
        'django',
        'waitress',
        'pyinstaller'
    ], check=True)

    # Create spec file
    subprocess.run([
        'pyinstaller',
        '--name=FileSharing',
        '--onefile',  # Combine into single executable
        '--windowed',  # No console window
        '--add-data', 'templates:templates',
        '--add-data', 'file/templates/file:templates/file',
        '--add-data', 'static:static',
        '--hidden-import=django.contrib.admin',
        '--hidden-import=django.contrib.auth',
        '--hidden-import=django.contrib.contenttypes',
        '--hidden-import=django.contrib.sessions',
        '--hidden-import=django.contrib.messages',
        '--hidden-import=django.contrib.staticfiles',
        '--hidden-import=django.template.loader_tags',
        '--hidden-import=file',
        '--hidden-import=waitress',
        '--hidden-import=django.core.wsgi',
        '--hidden-import=django.core.management',
        'run.py'
    ], check=True)

    print("Build completed. Executable is in the 'dist' directory.")

if __name__ == '__main__':
    build_for_mac()