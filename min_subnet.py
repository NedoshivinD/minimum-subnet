import sys

#считываем IP-адреса из файла
def read_ip_addresses (filename):
    ip_addresses = []
    with open(filename, 'r') as file:
        for line in file:
            ip_addresses.append(line.strip())
    return ip_addresses

#разбиваем каждый IP-адрес на 4 элемента
def parse_IPv4(str_ip):
    parts_ip = str_ip.split('.')
    try:
        parts_ip = [int(x) for x in parts_ip]
    except:
        raise TypeError("The IP address contains data that is not convertible to an integer type")
    if len(parts_ip) != 4:
        raise ValueError("In one or more IP addresses, the number of blocks does not correspond to it's type")
    for i in parts_ip:
        if i > 255 or i < 0:
            raise ValueError("You have entered an incorrect IP address")
    return parts_ip

# Разбиваем IP-адрес на отдельные части и конвертируем их в двоичное представление
def ip_to_binary(ip_address):
    return "".join(f"{octet:08b}" for octet in ip_address)

#формируем ответ в префиксном виде
def get_answer_ipv4(ip,mask):
    elements_network_adress = [ip[i] & mask[i] for i in range(4)]
    network_adress = '.'.join(map(str, elements_network_adress))
    prefix = 0
    for i in range(4):
        prefix += bin(mask[i])[2:].count('1')
    return network_adress + '/' + str(prefix)

#вычисляем подсеть
def calc(*ip):
    ip_addresses = ip[:-1]
    ip_version = ip[-1]
    if len(ip_addresses) == 0:
        raise ValueError("File is empty")
    if len(ip_addresses) < 2:
        raise ValueError("To find the minimum subnet I need more IP addresses")
    if ip_version == 4:
        parsed_ip = []
        for i in range(len(ip_addresses)):
            parsed_ip.append(parse_IPv4(ip_addresses[i]))
        max_ipv4 = max(parsed_ip, key=sum)
        min_ipv4 = min(parsed_ip, key=sum)
        binary_max_ip = ip_to_binary(max_ipv4)
        binary_min_ip = ip_to_binary(min_ipv4)

        # Находим общий префикс двоичного представления
        common_prefix = [a for a, b in zip(binary_max_ip, binary_min_ip) if a == b]

        # Находим адрес сети
        network_address_binary = binary_max_ip[:len(common_prefix)] + "0" * (32 - len(common_prefix))
        network_address = [int(network_address_binary[i:i+8], 2) for i in range(0, 32, 8)]

        res = ".".join(map(str, network_address)) + "/{}".format(len(common_prefix))
    elif ip_version == 6:
        raise ValueError("Unfortunately, support for this IP version is in development :(")
    else:
        raise ValueError("This IP version is not supported, please choose another one")
    return res

def main():
    filename = sys.argv[1]
    try:
        ip_version = int(sys.argv[2])
    except:
        raise ValueError("IP version must be an integer")
    ip_addresses = read_ip_addresses(filename)
    print('Result net:', calc(*ip_addresses, ip_version))

if __name__ == "__main__":
    main()