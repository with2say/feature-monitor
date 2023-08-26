import paramiko
import time


host = "172.28.201.169"  # 192.168.35.87
port = 10001
username = "root"
password = "qwer1234"
script = """
    for i in {1..20}; do
        uptime
        sleep 0.2
    done
    """


def read_output(channel):
    def _process_buffer(buffer):
        lines = buffer.split('\n')
        if len(lines) > 1:
            print(lines[:-1])
            return lines[-1]
        return buffer

    output_buffer = ''
    while True:
        if channel.recv_ready():
            output_buffer += channel.recv(1024).decode('utf-8')
            output_buffer = _process_buffer(output_buffer)

        if channel.exit_status_ready():
            if channel.recv_ready():
                output_buffer += channel.recv(1024).decode('utf-8')
                _process_buffer(output_buffer)
            break

        time.sleep(1)  # 3초 대기

    exit_status = channel.recv_exit_status()
    print(f"Exit status: {exit_status}")


def execute_ssh_command(host, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    channel = ssh.get_transport().open_session()
    try:
        channel.exec_command(command)
        read_output(channel)
    finally:
        ssh.close()


if __name__ == "__main__":
    execute_ssh_command(host, port, username, password, script)
    # execute_ssh_command(host, port, username, password, 'uptime')
