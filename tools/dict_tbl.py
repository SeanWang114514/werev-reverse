import json
d=json.load(open('out/reports/dict_fmt.json',encoding='utf-8'))
for x in d:
    print("%-26s %10d t=%-7s dt=%s cell=%d v=%-5s u32=%s mk=%s" % (x['name'],x['size'],x['type'],x['dict_type'],int(x['is_cell']),x['version'],x['u32_0_8'][:6],x.get('markers',{})))
