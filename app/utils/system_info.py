import psutil
import subprocess
import socket
import requests
from datetime import datetime, timedelta
import os
import platform

def get_system_info():
    """Get comprehensive system information"""
    try:
        # CPU information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Memory information
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk information
        disk = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        # Network information
        network_io = psutil.net_io_counters()
        
        # System information
        boot_time = psutil.boot_time()
        uptime = str(timedelta(seconds=int(datetime.now().timestamp() - boot_time)))
        
        # Get IP addresses
        hostname = socket.gethostname()
        try:
            private_ip = socket.gethostbyname(hostname)
        except:
            private_ip = "Unable to get IP"
        
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=5).text
        except:
            public_ip = "Unable to get public IP"
        
        # Load average (Linux/Unix only)
        try:
            load_avg = os.getloadavg()
            load_average = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
        except:
            load_average = "N/A"
        
        return {
            'cpu_percent': round(cpu_percent, 2),
            'cpu_count': cpu_count,
            'cpu_freq': round(cpu_freq.current, 2) if cpu_freq else 0,
            'memory_percent': round(memory.percent, 2),
            'memory_total': round(memory.total / (1024**3), 2),  # GB
            'memory_used': round(memory.used / (1024**3), 2),   # GB
            'memory_available': round(memory.available / (1024**3), 2),  # GB
            'swap_percent': round(swap.percent, 2),
            'swap_total': round(swap.total / (1024**3), 2),     # GB
            'disk_percent': round(disk.percent, 2),
            'disk_total': round(disk.total / (1024**3), 2),     # GB
            'disk_used': round(disk.used / (1024**3), 2),       # GB
            'disk_free': round(disk.free / (1024**3), 2),       # GB
            'network_bytes_sent': network_io.bytes_sent if network_io else 0,
            'network_bytes_recv': network_io.bytes_recv if network_io else 0,
            'network_packets_sent': network_io.packets_sent if network_io else 0,
            'network_packets_recv': network_io.packets_recv if network_io else 0,
            'public_ip': public_ip,
            'private_ip': private_ip,
            'hostname': hostname,
            'uptime': uptime,
            'load_average': load_average,
            'platform': platform.platform(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor()
        }
    except Exception as e:
        return {
            'error': f'Failed to get system info: {str(e)}',
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_percent': 0,
            'public_ip': 'Error',
            'private_ip': 'Error',
            'hostname': 'Error',
            'uptime': 'Error'
        }

def get_service_status(service_name):
    """Get the status of a systemd service"""
    try:
        # Check if service is active
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return "active"
        else:
            # Check if service exists but is inactive
            result = subprocess.run(
                ['systemctl', 'status', service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if 'could not be found' in result.stderr.lower():
                return "not-found"
            elif 'inactive' in result.stdout.lower():
                return "inactive"
            elif 'failed' in result.stdout.lower():
                return "failed"
            else:
                return "unknown"
                
    except subprocess.TimeoutExpired:
        return "timeout"
    except Exception as e:
        return f"error: {str(e)}"

def control_service(service_name, action):
    """Control a systemd service (start, stop, restart, enable, disable)"""
    allowed_actions = ['start', 'stop', 'restart', 'enable', 'disable', 'reload']
    
    if action not in allowed_actions:
        return {'success': False, 'error': f'Action {action} not allowed'}
    
    try:
        # Use sudo for service control
        result = subprocess.run(
            ['sudo', 'systemctl', action, service_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {'success': True, 'output': result.stdout}
        else:
            return {'success': False, 'error': result.stderr}
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Command timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_process_list():
    """Get list of running processes"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        return processes[:20]  # Return top 20 processes
        
    except Exception as e:
        return [{'error': f'Failed to get process list: {str(e)}'}]

def get_network_interfaces():
    """Get network interface information"""
    try:
        interfaces = {}
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for interface_name, interface_addresses in net_if_addrs.items():
            interface_info = {
                'addresses': [],
                'stats': {}
            }
            
            for address in interface_addresses:
                interface_info['addresses'].append({
                    'family': str(address.family),
                    'address': address.address,
                    'netmask': address.netmask,
                    'broadcast': address.broadcast
                })
            
            if interface_name in net_if_stats:
                stats = net_if_stats[interface_name]
                interface_info['stats'] = {
                    'isup': stats.isup,
                    'duplex': str(stats.duplex),
                    'speed': stats.speed,
                    'mtu': stats.mtu
                }
            
            interfaces[interface_name] = interface_info
        
        return interfaces
        
    except Exception as e:
        return {'error': f'Failed to get network interfaces: {str(e)}'}

def get_disk_usage():
    """Get disk usage for all mounted filesystems"""
    try:
        disk_usage = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': round(usage.total / (1024**3), 2),  # GB
                    'used': round(usage.used / (1024**3), 2),   # GB
                    'free': round(usage.free / (1024**3), 2),   # GB
                    'percent': round(usage.percent, 2)
                })
            except PermissionError:
                continue
        
        return disk_usage
        
    except Exception as e:
        return [{'error': f'Failed to get disk usage: {str(e)}'}]
