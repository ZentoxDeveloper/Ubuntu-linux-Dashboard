import os
import shutil
from flask import send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

def get_smb_files(path):
    """Get list of files and directories in SMB path"""
    try:
        if not os.path.exists(path):
            return [{'name': 'SMB path not accessible', 'type': 'error', 'path': ''}]
        
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                items.append({
                    'name': item,
                    'type': 'directory',
                    'path': os.path.relpath(item_path, path),
                    'size': get_directory_size(item_path)
                })
            else:
                items.append({
                    'name': item,
                    'type': 'file',
                    'path': os.path.relpath(item_path, path),
                    'size': os.path.getsize(item_path),
                    'modified': os.path.getmtime(item_path)
                })
        
        # Sort directories first, then files
        items.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))
        return items
        
    except PermissionError:
        return [{'name': 'Access denied to SMB path', 'type': 'error', 'path': ''}]
    except Exception as e:
        return [{'name': f'Error accessing SMB path: {str(e)}', 'type': 'error', 'path': ''}]

def get_directory_size(path):
    """Calculate total size of directory"""
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    continue
        return total_size
    except:
        return 0

def download_smb_file(base_path, filename):
    """Download a file from SMB share"""
    try:
        # Secure the filename
        filename = secure_filename(filename)
        file_path = os.path.join(base_path, filename)
        
        # Check if file exists and is within the base path
        if not os.path.exists(file_path):
            flash('File not found.', 'error')
            return redirect(url_for('main.browse_smb'))
        
        if not os.path.commonpath([base_path, file_path]) == base_path:
            flash('Access denied.', 'error')
            return redirect(url_for('main.browse_smb'))
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('main.browse_smb'))

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_directory(path):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        return False

def copy_file(src, dst):
    """Copy file from source to destination"""
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        return False

def move_file(src, dst):
    """Move file from source to destination"""
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        return False

def delete_file(path):
    """Delete file or directory"""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except Exception as e:
        return False
