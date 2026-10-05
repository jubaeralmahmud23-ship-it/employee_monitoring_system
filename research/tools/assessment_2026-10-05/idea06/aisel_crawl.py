import re, urllib.request, time, json, sys, html
sys.stdout.reconfigure(encoding='utf-8')
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
terms=re.compile(r"language model|\bLLMs?\b|generative AI|generative artificial intelligence|ChatGPT|\bGPT-?[345]|GenAI|foundation model", re.I)
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60) as r: return r.status, r.read().decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code, ""
    except Exception as e: return -1, ""
out={}
for conf in ["icis2024","icis2025","ecis2024","ecis2025"]:
    st,h=get(f"https://aisel.aisnet.org/{conf}/")
    tracks=sorted(set(re.findall(r'href="(https://aisel\.aisnet\.org/%s/[a-z0-9_]+)"'%conf,h)))
    tracks=[t for t in tracks if not t.endswith(".html") or t.endswith(".rss")]
    titles=[]; pages=0; fails=0
    for t in tracks:
        time.sleep(0.8)
        st2,h2=get(t)
        if st2!=200: fails+=1; continue
        pages+=1
        # paper entries: <p class="article-listing"><a href="...">Title</a>
        for m in re.finditer(r'<p class="summary"><a href="([^"]+)"\s*>([^<]+)</a>',h2):
            titles.append((m.group(1),html.unescape(m.group(2)).strip()))
    titles=list(dict.fromkeys(titles))
    hits=[t for t in titles if terms.search(t[1])]
    out[conf]={"landing_http":st,"track_pages_found":len(tracks),"track_pages_fetched_200":pages,"track_fetch_failures":fails,"paper_titles_total":len(titles),"title_term_hits":len(hits),"sample_hits":[t[1][:100] for t in hits[:8]]}
    print(conf,json.dumps({k:v for k,v in out[conf].items() if k!='sample_hits'}),flush=True)
json.dump(out,open("aisel_counts.json","w",encoding='utf-8'),indent=1,ensure_ascii=False)
