import helper

host_username = helper.get_host_username()

ssh_ip = "127.0.0.1"
ssh_username = "vagrant"
ssh_password = "vagrant"
ssh_key_path = ("/home/%s/.vagrant.d/insecure_private_key" %host_username)
ssh_port = 2222

tmp_login_password = "sifra"

GAME_RPC_USER = 'vagrant'
GAME_RPC_PASS = 'vagrant'
GAME_RPC_PORT = '8332'
