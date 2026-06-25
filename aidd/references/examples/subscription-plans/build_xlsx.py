import openpyxl, os
wb = openpyxl.Workbook(); wb.remove(wb.active)
def sheet(name, rows):
    ws = wb.create_sheet(name)
    for r in rows: ws.append(r)
# Self-describing header: r1=table, r2=type, r3=key, r4=description, r5+=data
sheet("plan", [
    ["plan"],
    ["int","int","int","int","int"],
    ["id","name","tier","priceMonthly","trialDays"],
    ["Plan id","Name text id","Tier","Monthly price (cents)","Trial days"],
    [1,9001,1,0,14],
    [2,9002,2,1900,14],
    [3,9003,3,9900,0],
])
sheet("planTier", [
    ["planTier"],
    ["int","int","int","int","int"],
    ["tier","seats","projects","storageGb","apiPerDay"],
    ["Tier","Seats","Projects","Storage GB","API calls/day"],
    [1,3,3,5,1000],
    [2,10,25,100,50000],
    [3,100,500,1000,1000000],
])
sheet("feature", [
    ["feature"],
    ["int","int"],
    ["id","name"],
    ["Feature id","Name text id"],
    [201,9201],
    [202,9202],
    [203,9203],
])
sheet("planFeature", [
    ["planFeature"],
    ["int","int","int"],
    ["id","plan","feature"],
    ["Row id","Plan","Feature"],
    [1,2,203],
    [2,3,201],
    [3,3,202],
    [4,3,203],
])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subscription.xlsx")
wb.save(out); print("wrote", out)
