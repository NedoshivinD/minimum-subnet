import sys

#считываем IP-адреса из файла
def read_ip_addresses (filename : str) -> list:
    ip_addresses = []
    with open(filename, 'r') as file:
        for line in file:
            ip_addresses.append(line.strip())
    return ip_addresses

#разбиваем каждый IP-адрес на 4 элемента
def parse_IPv4(str_ip : str) -> list:
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
def ip_to_binary(ip_address : list) -> str:
    return "".join(f"{octet:08b}" for octet in ip_address)

# Вычисляем максимальный из ip адресов
def max_IPv4(ip_adresses : list) -> list:
    ar_ind = [x for x in range(0,len(ip_adresses))]
    for j in range(4):
        max_el = ip_adresses[ar_ind[0]][j]
        index_in_ar_ind = 0
        max_ind = ar_ind[0]
        i = ar_ind[0]
        while i in ar_ind:
            index_in_ar_ind += 1
            if ip_adresses[i][j] > max_el:
                max_el = ip_adresses[i][j]
                ar_ind.remove(max_ind)
                max_ind = i
                index_in_ar_ind -= 1
            elif ip_adresses[i][j] < max_el:
                ar_ind.remove(i)
                index_in_ar_ind -= 1
            if index_in_ar_ind<len(ar_ind):
                i = ar_ind[index_in_ar_ind]
            else:
                break
        if len(ar_ind) == 1:
            break
    return ip_adresses[max_ind]

# Вычисляем минимальный IP адрес
def min_IPv4(ip_adresses : list) -> list:
    ar_ind = [x for x in range(0,len(ip_adresses))]
    for j in range(4):
        min_el = ip_adresses[ar_ind[0]][j]
        min_ind = ar_ind[0]
        index_in_ar_ind = 0
        i = ar_ind[0]
        while i in ar_ind:
            index_in_ar_ind += 1
            if ip_adresses[i][j] < min_el:
                min_el = ip_adresses[i][j]
                ar_ind.remove(min_ind)
                min_ind = i
                index_in_ar_ind -= 1
            elif ip_adresses[i][j] > min_el:
                ar_ind.remove(i)
                index_in_ar_ind -= 1
            if index_in_ar_ind<len(ar_ind):
                i = ar_ind[index_in_ar_ind]
            else:
                break
        if len(ar_ind) == 1:
            break
    return ip_adresses[min_ind]

#ищет маску подсети для двух ip
def get_mask(_ip1 : list, _ip2 : list) -> list:
    mask = [0, 0, 0, 0]
    for i in range(0, 4):
        mask[i] = 255 ^ (_ip1[i] ^ _ip2[i])
        if mask[i] < 255:
            string = str(bin(mask[i]))
            if len(string) < 10:
                mask[i] = 0
            else:
                for j in range(2, len(string)):
                    if string[j] == '0':
                        #обрезаем маску после первого нуля
                        string = string[:j]+string[j:].replace('1', '0')
                        break
                mask[i] = int(string, 2)
            break
    return mask

#по маске вычисляет адрес подсети
def get_net(ip1 : list, mask : list) -> list:
    net = [0, 0, 0, 0]
    for i in range(0, 4):
        net[i] = ip1[i] & mask[i]
    return net

#вычисляем подсеть
def calc(*ip : tuple) -> str:
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
        max_ipv4 = max_IPv4(parsed_ip)
        min_ipv4 = min_IPv4(parsed_ip)
        mask = get_mask(max_ipv4, min_ipv4)
        binary_mask = ip_to_binary(mask)

        # Находим общий префикс двоичного представления
        common_prefix = [str(i) for i in binary_mask if i == '1']

        # Находим адрес сети
        network_address = get_net(min_ipv4, mask)

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