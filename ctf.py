strs = [180, 136, 137, 147, 191, 137, 147, 191,148, 136, 133, 191, 134, 140, 129, 135, 191, 65]
flag = ""
for i in range(0,len(strs)):
    flag += chr(strs[i] - ord('@') ^ 0x20)
print(flag)