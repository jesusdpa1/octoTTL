# %%
import cardiac

test = cardiac.communication.serial.DSICommunications()
# %%

test.start_communications()
print(test.recv_data())
# %%

for n in range(20):
    print(test.recv_data().decode().split(','))

# %%
#
test.start_communications()
print(test.recv_data())
b'\x00\x030;;'
b'0;;'
