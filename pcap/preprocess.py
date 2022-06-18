import pyshark
import json

pcap = pyshark.FileCapture('smallFlows.pcap')
print (pcap)

sess_index = list()
src = {}
dst = {}

for pkt in pcap:
    # print (type(pkt.tcp))
    # print (pkt.layers)
    try:
        # pkt.tcp.pretyy_print()
        if pkt.tcp.stream not in sess_index:
            sess_index.append(pkt.tcp.stream)
    except:
        pass

pcap.close()

# for sess in sess_index:
#   print (f"{sess}")
for stream in sess_index:
    display_filter = f"tcp.stream eq {stream}"

    cap = pyshark.FileCapture('smallFlows.pcap', display_filter=display_filter)

    if cap[0].ip.src not in src:
        src[cap[0].ip.src] = [stream]
    else:
        src[cap[0].ip.src].append(stream)
        
    if cap[0].ip.dst not in dst:
        dst[cap[0].ip.dst] = [stream]
    else:
        dst[cap[0].ip.dst].append(stream)

    cap.close()

    # print (f"Stream: {stream}\nSrc: {cap[0].ip.src}\tDst: {cap[0].ip.dst}\n\n\n")

print (src)
print ('\n\n')
print (dst)

src_json = json.dumps(src, indent=4)
dst_json = json.dumps(dst, indent=4)

with open ('src.json', 'w') as json_file:
    json_file.write(src_json)

with open ('dst.json', 'w') as json_file:
    json_file.write(dst_json)














