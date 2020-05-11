import json

def parseSpellJson(filename, jsonobj):
    with open("source/"+filename) as file:
        sourcefile = json.load(file)

    for spell in sourcefile["spell"]:
        spellName = spell["name"]
        print(spellName)
        spellData = []

        #spellname
        spellData.append(f"__**{spellName}:**__")

        #level and ritual
        ritual = ""
        if "meta" in spell:
            if "ritual" in spell["meta"]:
                ritual = " (ritual)"
        spellData.append(f"**Level: **{spell['level']}{ritual}")

        #castingtime
        for castingData in spell["time"]:
            spellData.append(f"**Casting Time: **{castingData['number']} {castingData['unit']}")

        #range
        if spell["range"]["type"] == "special":
            spellData.append(f"**Range: ** special")
        elif "amount" in spell['range']['distance']:
            spellData.append(f"**Range: **{spell['range']['distance']['amount']} {spell['range']['distance']['type']}")
        else:
            spellData.append(f"**Range: **{spell['range']['distance']['type']}")

        #components
        compList = ""
        for k, v in spell["components"].items():
            if k != "m":
                compList += f"{k}, "
            else:
                if type(v) == dict:
                    compList += f"{k} ({v['text']}), "
                else:
                    compList += f"{k} ({v}), "
        #remove final ", " from string
        compList = compList[:-2]
        spellData.append(f"**Components: **{compList}")

        #Duration


        spellDesc =""
        for entries in spell["entries"]:
            if type(entries) == str:
                spellDesc += entries
            if type(entries) == dict:
                spellDesc += "\n"
                #if this is enumeration type spell like "Ceremony"
                if entries["type"]=="entries":
                    dictEntryList = ""
                    for dictEntries in entries["entries"]:
                        if type(dictEntries) == dict:
                            itemList = ""
                            for items in dictEntries["items"]:
                                itemList += f"-{items}\n"
                            dictEntryList +=  itemList
                        else:
                            dictEntryList += dictEntries
                    spellDesc += f"*{entries['name']}*: {dictEntryList}\n"
                #if this is table type like "Chaos Bolt"
                elif entries["type"] == "table":
                    tableEntries = ""
                    for rows in entries["rows"]:
                        for cell in rows:
                            if type(cell) == dict:
                                if "exact" in cell["roll"]:
                                    tableEntries += f"{cell['roll']['exact']}: "
                                else:
                                    tableEntries += f"{cell['roll']['min']}-{cell['roll']['max']}: "
                            else:
                                tableEntries += f"{cell}\n"
                    spellDesc += tableEntries


        if "entriesHigherLevel" in spell:
            spellDesc += "\n"
            for entryHLList in spell["entriesHigherLevel"]:
                for entryHL in entryHLList["entries"]:
                    spellDesc += entryHL
        spellData.append(spellDesc)
        dataJson[spellName] = spellData
        spellNameList.append(spellName)



dataJson = {}
spellNameList = []
filelist = ["spells-phb.json", "spells-xge.json", "spells-scag.json"]

for filesnames in filelist:
    parseSpellJson(filesnames, dataJson)

with open("formated_spells.json", "w") as f:
    json.dump(dataJson, f)

with open("spellindex.json", "w") as si:
    json.dump(spellNameList, si)




