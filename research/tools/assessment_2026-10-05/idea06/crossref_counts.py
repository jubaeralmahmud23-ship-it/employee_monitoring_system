import json, urllib.request, urllib.parse, time, re, sys
sys.stdout.reconfigure(encoding='utf-8')
MAILTO="<contact email of the repository owner>"  # Crossref polite-pool contact; replaced before committing
journals={
 "Business & Information Systems Engineering":["2363-7005","1867-0202"],
 "Information Systems Frontiers":["1387-3326","1572-9419"],
 "Electronic Markets":["1019-6781","1422-8890"],
 "Information & Management":["0378-7206"],
 "Decision Support Systems":["0167-9236"],
 "MIS Quarterly":["0276-7783","2162-9730"],
 "Information Systems Research":["1047-7047","1526-5536"],
 "Journal of Management Information Systems":["0742-1222","1557-928X"],
 "Journal of the Association for Information Systems":["1536-9323"],
 "European Journal of Information Systems":["0960-085X","1476-9344"],
 "Information Systems Journal":["1350-1917","1365-2575"],
}
terms=re.compile(r"language model|\bLLMs?\b|generative AI|generative artificial intelligence|ChatGPT|GPT-?[34]", re.I)
out={}
for name,issns in journals.items():
    items=[]
    for issn in issns:
        cursor="*"
        while True:
            url=("https://api.crossref.org/works?filter=issn:%s,from-pub-date:2023-01-01,type:journal-article&rows=1000&select=DOI,title,abstract,container-title,issued,license&cursor=%s&mailto=%s"
                 %(issn,urllib.parse.quote(cursor),MAILTO))
            for attempt in range(4):
                try:
                    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"feas06/1.0 (mailto:%s)"%MAILTO}),timeout=120) as r:
                        d=json.load(r); break
                except Exception as e:
                    print("retry",name,issn,e,file=sys.stderr); time.sleep(3)
            else:
                d={"message":{"items":[],"next-cursor":None}}
            its=d["message"]["items"]; items+=its
            cursor=d["message"].get("next-cursor")
            if not its or not cursor: break
            time.sleep(0.5)
    seen={}
    for it in items: seen[it["DOI"]]=it
    items=list(seen.values())
    total=len(items); with_abs=sum(1 for it in items if it.get("abstract"))
    title_hits=[it for it in items if terms.search(" ".join(it.get("title",[])))]
    ta_hits=[it for it in items if terms.search(" ".join(it.get("title",[]))+" "+it.get("abstract",""))]
    byyear={}
    for it in ta_hits:
        y=it.get("issued",{}).get("date-parts",[[None]])[0][0]; byyear[y]=byyear.get(y,0)+1
    def cc(it): return any('creativecommons' in (l.get('URL') or '') for l in it.get('license',[]))
    cc_hits=sum(1 for it in ta_hits if cc(it)); cc_all=sum(1 for it in items if cc(it))
    out[name]={"cc_license_all":cc_all,"cc_license_hits":cc_hits,"total_articles_2023plus":total,"with_crossref_abstract":with_abs,"title_hits":len(title_hits),"title_or_abstract_hits":len(ta_hits),"ta_hits_by_year":byyear,
               "sample_titles":[" ".join(it["title"])[:110] for it in ta_hits[:6]]}
    print(name,out[name],flush=True)
json.dump(out,open("crossref_counts.json","w"),indent=1)
