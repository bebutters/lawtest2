import sqlite3 as sqlite
import random
import datetime
import uuid
import threading

sqlite.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite.register_adapter(uuid.UUID, lambda u: u.bytes_le)
connection = sqlite.connect("Database.db", detect_types = sqlite.PARSE_DECLTYPES)
cursor = connection.cursor()
ecursor = connection.cursor()

def QueryLawyer(FirstName, LastName, PostCode, Language, State):
    Language = Language.title()
    args = [FirstName, LastName, PostCode, State]
    results = cursor.execute("""select FirmID, LawyerID from Lawyer inner join FirmLawyers
        on Lawyer.ID = Firmlawyers.LawyerID inner join Firm on Firm.ID = FirmLawyers.FirmID
        inner join Suburb on Firm.SuburbID = Suburb.ID
        where FirstName like ? and LastName like ? and PostCode like ? and State like ?""", args).fetchall()
    json = {"flag": 0, "data": []}
    count = 0
    for result in results:
        if count > 20:
            json["flag"] = 1
            break
        FirstName, LastName = cursor.execute("select FirstName, LastName from Lawyer where ID = ?", [result[1].bytes_le]).fetchall()[0]
        name = FirstName + " " + LastName
        FirmName, PostCode = cursor.execute("""select FirmName, PostCode from Firm inner join
            Suburb on Firm.SuburbID = Suburb.ID where Firm.ID = ?""", [result[0].bytes_le]).fetchall()[0]
        Languages = [language[0] for language in cursor.execute("""select LanguageName from Lawyer inner join LawyerLanguages
            on Lawyer.ID = LawyerLanguages.LawyerID inner join Language on Language.ID = LawyerLanguages.LanguageID
            where Lawyer.ID = ?""", [result[1].bytes_le])]
        if Language:
            if Language in Languages:
                json["data"].append({"name": name, "firm": FirmName, "postcode": PostCode, "languages": list(Languages)})
                count += 1
        else:
            json["data"].append({"name": name, "firm": FirmName, "postcode": PostCode, "languages": list(Languages)})
            count += 1
    return(json)

def QueryFirm(Name, PostCode, Language, State):
    Language = Language.title()
    args = [Name, PostCode, State]
    results = cursor.execute("""select Firm.ID, Firmname, PostCode from
                                Firm inner join Suburb on Firm.SuburbID = Suburb.ID
                                where FirmName like ? and PostCode like ? and State like ?""", args)
    json = {"flag": 0, "data": []}
    count = 0
    for result in results:
        print(result)
        if count > 20:
            print(count, "Broke")
            json["flag"] = 1
            break
        FirmID, Name, PostCode = result
        print(Name, PostCode)
        Languages = [language[0] for language in ecursor.execute("""select distinct LanguageName from
            (select ID from Firm where ID = ?) as FQ inner join FirmLawyers on FQ.ID = FirmLawyers.FirmID inner join Lawyer on
            Lawyer.ID = FirmLawyers.LawyerID inner join LawyerLanguages on
            Lawyer.ID = LawyerLanguages.LawyerID inner join Language on Language.ID = LawyerLanguages.LanguageID""", [FirmID.bytes_le])]
##        Languages = [language[0] for language in ecursor.execute("""select distinct LanguageName from
##            (select ID from Firm where ID = ?) as FQ inner join FirmLawyers on FQ.ID = FirmLawyers.FirmID inner join (select * from Language where LanguageName like ?) Lawyer on
##            Lawyer.ID = FirmLawyers.LawyerID inner join LawyerLanguages on
##            Lawyer.ID = LawyerLanguages.LawyerID inner join  as LQ on LQ.ID = LawyerLanguages.LanguageID""", [FirmID.bytes_le], Language)]
        if Language:
            if Language in Languages:
                json["data"].append({"firm": Name, "postcode": PostCode, "languages": list(Languages)})
                count += 1
        else:
            json["data"].append({"firm": Name, "postcode": PostCode, "languages": list(Languages)})
            count += 1
    return(json)

def AddCookie(cookie, state):
    query = "insert into Cookies values (?, ?, ?)"
    try:
        cursor.execute(query, [cookie, state, datetime.datetime.now()])
    except Exception as e:
        return(str(e) + "The Line")
    connection.commit()

def ClearCookies():
    prevtime = datetime.datetime.now() - datetime.timedelta(hours = 8)
    cursor.execute("delete from Cookies where Time > ?", (prevtime,))
    threading.Timer(60, ClearCookies)

def CheckCookie(cookie):
    return(cursor.execute("select State from Cookies where Cookie = ?", (cookie,)).fetchall()[0][0])


