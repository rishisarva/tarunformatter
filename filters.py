# filters.py

playerMap = {
     "messi": ["messi", "leo", "lionel"],      
  "ronaldo": ["ronaldo", "cr7", "cristiano"],      
  "neymar": ["neymar", "neymar jr"],      
  "mbappe": ["mbappe", "kylian"],      
  "haaland": ["haaland", "erling"],      
  "benzema": ["benzema", "karim"],      
  "modric": ["modric", "luka"],      
  "salah": ["salah", "mo"],      
  "lewandowski": ["lewandowski", "lewa"],      
  "ronaldinho": ["ronaldinho", "dinho"],      
  "zidane": ["zidane", "zizou"],      
  "beckham": ["beckham", "david"],      
  "kaka": ["kaka", "ricardo"],      
  "suarez": ["suarez", "luis"],      
  "ibrahimovic": ["ibrahimovic", "zlatan"],      
  "de bruyne": ["de bruyne", "kdb"],      
  "griezmann": ["griezmann", "antoine"],      
  "bellingham": ["bellingham", "jude"],      
  "vinicius": ["vinicius", "vini", "vinijr"],      
  "haaland": ["haaland", "erling"],      
      
  "ramos": ["ramos", "sergio"],      
  "van dijk": ["van dijk", "virgil"],      
  "kane": ["kane", "harry"],      
  "son": ["son", "heungmin"],      
  "rashford": ["rashford", "marcus"],      
  "saka": ["saka", "bukayo"],      
  "foden": ["foden", "phil"],      
  "musiala": ["musiala", "jamal"],      
  "pedri": ["pedri"],      
  "gavi": ["gavi"],      
      
  "osimhen": ["osimhen", "victor"],      
  "leao": ["leao", "rafael"],      
  "valverde": ["valverde", "fede"],      
  "rodrygo": ["rodrygo"],      
  "camavinga": ["camavinga", "eduardo"],      
  "tchouameni": ["tchouameni", "aurelien"],      
  "odegaard": ["odegaard", "martin"],      
  "bruno fernandes": ["bruno", "fernandes"],      
  "bernardo silva": ["bernardo", "silva"],      
  "kroos": ["kroos", "toni"],      
  "kimmich": ["kimmich", "joshua"],      
      
  "neuer": ["neuer", "manuel"],      
  "alisson": ["alisson"],      
  "courtois": ["courtois", "thibaut"],      
  "ederson": ["ederson"],      
  "oblak": ["oblak", "jan"],      
      
  "buffon": ["buffon", "gigi"],      
  "casillas": ["casillas", "iker"],      
  "cannavaro": ["cannavaro", "fabio"],      
  "pirlo": ["pirlo", "andrea"],      
  "gattuso": ["gattuso", "rino"],      
  "lampard": ["lampard", "frank"],      
  "gerrard": ["gerrard", "steven"],      
  "drogba": ["drogba", "didier"],      
  "eto'o": ["etoo", "samuel"],      
  "rooney": ["rooney", "wayne"],      
      
  "mbappe": ["mbappe"],      
  "hakimi": ["hakimi", "achraf"],      
  "cancelo": ["cancelo", "joao"],      
  "davies": ["davies", "alphonso"],      
  "walker": ["walker", "kyle"],      
  "reece james": ["reece", "james"],      
      
  "martinez": ["martinez", "lautaro"],      
  "dybala": ["dybala", "paulo"],      
  "lukaku": ["lukaku", "romelu"],      
  "dimaria": ["di maria", "angel"],      
  "mahrez": ["mahrez", "riyad"],      
  "kante": ["kante", "ngolo"],      
  "koulibaly": ["koulibaly", "kalidou"],      
      
  "rivaldo": ["rivaldo"],      
  "ronaldo nazario": ["ronaldo", "r9"],      
  "pele": ["pele"],      
  "maradona": ["maradona", "diego"],      
  "garrincha": ["garrincha"],      
  "zola": ["zola", "gianfranco"],      
  "shearer": ["shearer", "alan"],      
  "henry": ["henry", "thierry"],      
  "bergkamp": ["bergkamp", "dennis"],      
  "seedorf": ["seedorf", "clarence"],      
      
  "foden": ["foden"],      
  "grealish": ["grealish", "jack"],      
  "mount": ["mount", "mason"],      
  "rice": ["rice", "declan"],      
  "odegaard": ["odegaard"],      
  "nunez": ["nunez", "darwin"],      
  "felix": ["felix", "joao"],      
  "chiesa": ["chiesa", "federico"],      
  "barella": ["barella", "nicolo"],      
  "tonali": ["tonali", "sandro"],      
      
  "donnarumma": ["donnarumma", "gigi"],      
  "maignan": ["maignan", "mike"],      
  "navas": ["navas", "keylor"],      
  "bounou": ["bounou", "bono"],      
  "martinez": ["martinez", "emi"],      
      
  "vlahovic": ["vlahovic", "dusan"],      
  "scamacca": ["scamacca", "gianluca"],      
  "pjanic": ["pjanic", "miralem"],      
  "mkhitaryan": ["mkhitaryan", "henrikh"],      
  "calhanoglu": ["calhanoglu", "hakan"],      
  "onana": ["onana", "andre"],      
  "goretzka": ["goretzka", "leon"],      
  "sancho": ["sancho", "jadon"],      
  "hummels": ["hummels", "mats"],      
  "upamecano": ["upamecano", "dayot"]      
}

sleeves = ["short sleeve", "full sleeve", "polo", "five sleeve"]
techniques = ["sublimation", "embroidery", "signature"]

def clubs(rows):
    return sorted(set(r["club"] for r in rows if r["club"]))

def players(rows):
    found = set()
    for p, keys in playerMap.items():
        for r in rows:
            if any(k in r["title"] for k in keys):
                found.add(p)
    return sorted(found)

def by_club(rows, club):
    return [r for r in rows if r["club"] == club]

def by_player(rows, player):
    keys = playerMap[player]
    return [r for r in rows if any(k in r["title"] for k in keys)]

def smart(rows, club=None, player=None, sleeve=None, tech=None):
    out = rows
    if club:
        out = [r for r in out if r["club"] == club]
    if player:
        out = by_player(out, player)
    if sleeve:
        out = [r for r in out if sleeve in r["title"]]
    if tech:
        out = [r for r in out if tech in r["title"] or tech in r.get("techniques","")]
    return out