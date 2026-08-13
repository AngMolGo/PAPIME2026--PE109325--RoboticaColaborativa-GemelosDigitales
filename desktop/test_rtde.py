import sys
try:
    import rtde.serialize as serialize
    print("Serialize BOOL pack format:", serialize.get_pack_format("BOOL"))
except Exception as e:
    print(e)
