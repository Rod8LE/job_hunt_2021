import pandas as pd

columns = ["ID", "Name", "Receiving", "Check In", "Pick", "Pack"]
work_df = pd.DataFrame([["A1", "CM", "Si", "Si", "No", "No"],
                        ["A2", "JG", "Si", "Si", "No", "No"],
                        ["A3", "NM", "Si", "Si", "No", "No"],
                        ["A4", "VG", "Si", "Si", "No", "No"],
                        ["A5", "AC", "Si", "Si", "No", "No"],
                        ["A6", "MM", "Si", "Si", "Si", "Si"],
                        ["A7", "EM", "Si", "Si", "Si", "Si"],
                        ["A8", "GM", "No", "Si", "Si", "No"],
                        ["A9", "TC", "No", "No", "Si", "Si"],
                        ["A10", "FA", "No", "No", "Si", "Si"],
                        ["A11", "FM", "No", "No", "Si", "Si"],
                        ["A12", "SC", "Si", "Si", "Si", "Si"],
                        ["A13", "JS", "No", "Si", "Si", "Si"],
                        ["A14", "SS", "Si", "No", "No", "Si"],
                        ["A15", "MA", "Si", "No", "No", "No"],
                        ["A16", "LA", "No", "No", "Si", "No"],
                        ["A17", "PE", "No", "No", "Si", "No"],
                        ["A18", "ES", "No", "No", "Si", "Si"],
                        ["A19", "RP", "No", "No", "Si", "Si"],
                        ["A20", "CR", "No", "No", "Si", "Si"]], columns=columns)

work_update_df = pd.DataFrame([[70, 0, 0],
                               [78, 0, 0],
                               [85, 0, 0],
                               [76, 0, 0],
                               [82, 0, 0],
                               [65, 55, 78],
                               [75, 62, 80],
                               [0, 70, 0],
                               [0, 73, 90],
                               [0, 80, 92],
                               [0, 82, 98],
                               [78, 76, 79],
                               [72, 54, 75],
                               [75, 0, 75],
                               [102, 0, 0],
                               [0, 90, 0],
                               [0, 80, 0],
                               [0, 78, 85],
                               [0, 82, 90],
                               [0, 94, 102]], columns=["Receiving", "Pick", "Pack"])

work_df.update(work_update_df)



print("E1")

e1_df = pd.DataFrame([[200, 250, 300, 400, 800, 850, 600, 550, 600],
                      ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]]).T
e1_df.columns = ["pick", "hour"]
pick_tail = 0
queue_df = pd.DataFrame("IDLE", columns=["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"], index=work_df.ID)

for index in range(len(e1_df)):
    current_queue = []
    pick_current = 0
    pick_goal = e1_df.pick[index] + pick_tail
    hour = e1_df.hour[index]
    while pick_current < pick_goal:
        proposed_df = work_df.loc[(work_df.Pick > 0) & (~work_df.ID.isin(current_queue)), :]
        if len(proposed_df) == 0:
            pick_tail = (pick_goal - pick_current)
            print("tail : %s at %s" % (pick_tail, hour))
            break
        proposed_df["not pick"] = proposed_df["Receiving"] + proposed_df["Pack"]
        proposed_df.sort_values(by="not pick", inplace=True)
        chosen = proposed_df.head(1)
        current_queue.append(chosen.ID.values[0])
        queue_df.loc[chosen.ID.values[0], hour] = "Pick"
        pick_current += chosen.Pick.values[0]

    print(" QUEUE : %s " % current_queue)
    print(hour + ": " + str(pick_current))
print(queue_df)

print("E2")

e1_df = pd.DataFrame([[200, 250, 300, 400, 800, 850, 600, 550, 600],
                      [1000, 1000, 1000, 1000, 1000, 0, 0, 0, 2200],
                      ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]]).T
e1_df.columns = ["pick", "pack", "hour"]
queue_df = pd.DataFrame("IDLE", columns=["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"], index=work_df.ID)
pick_tail = 500  # backlog incial
pack_tail = 0
for index in range(len(e1_df)):
    current_queue = []
    pick_current = 0
    pack_current = 0
    pick_goal = e1_df.pick[index] + pick_tail
    pack_goal = e1_df.pack[index] + pack_tail
    pick_tail = 0
    pack_tail = 0
    hour = e1_df.hour[index]
    while pick_current < pick_goal:
        proposed_df = work_df.loc[(work_df.Pick > 0) & (~work_df.ID.isin(current_queue)), :]
        if len(proposed_df) == 0:
            pick_tail = (pick_goal - pick_current)
            print("pick tail : %s at %s" % (pick_tail, hour))
            break
        proposed_df["not pick"] = proposed_df["Receiving"] + proposed_df["Pack"]
        proposed_df.sort_values(by="not pick", inplace=True)
        chosen = proposed_df.head(1)
        current_queue.append(chosen.ID.values[0])
        queue_df.loc[chosen.ID.values[0], hour] = "Pick"
        pick_current += chosen.Pick.values[0]
    excess = 0
    if pick_current > pick_goal:
        excess = pick_current - pick_goal
    while pack_current < pack_goal:
        proposed_df = work_df.loc[(work_df.Pack > 0) & (~work_df.ID.isin(current_queue)), :]
        if len(proposed_df) == 0:
            pack_tail = (pack_goal - pack_current)
            print("pack tail : %s at %s" % (pack_tail, hour))
            break
        proposed_df["not pack"] = proposed_df["Receiving"] + proposed_df["Pick"]
        proposed_df.sort_values(by="not pack", inplace=True)
        chosen = proposed_df.head(1)
        current_queue.append(chosen.ID.values[0])
        queue_df.loc[chosen.ID.values[0], hour] = "Pack"
        if excess > 0:
            pack_current += (chosen.Pick.values[0] + excess)
            excess = 0
        else:
            pack_current += chosen.Pick.values[0]

    print(" QUEUE : %s " % current_queue)
    print(hour + " - pick: " + str(pick_current) + " - pack: " + str(pack_current))
print(queue_df)


print("E3")

e1_df = pd.DataFrame([[200, 250, 300, 400, 800, 850, 600, 550, 600],
                      [0, 0, 0, 1000, 0, 0, 0, 0, 2200],
                      [450, 450, 450, 200, 200, 200, 200, 200, 200],
                      ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]]).T
e1_df.columns = ["pick", "pack", "receiving", "hour"]
queue_df = pd.DataFrame("IDLE", columns=["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"], index=work_df.ID)
pick_tail = 500  # backlog incial
pack_tail = 0
receiving_tail = 0
for index in range(len(e1_df)):
    current_queue = []
    pick_current = 0
    pack_current = 0
    receiving_current = 0
    pick_goal = e1_df.pick[index] + pick_tail
    pack_goal = e1_df.pack[index] + pack_tail
    receiving_goal = e1_df.receiving[index] + receiving_tail
    pick_tail = 0
    pack_tail = 0
    receiving_tail = 0
    hour = e1_df.hour[index]
    while pick_current < pick_goal:
        proposed_df = work_df.loc[(work_df.Pick > 0) & (~work_df.ID.isin(current_queue)), :]
        if len(proposed_df) == 0:
            pick_tail = (pick_goal - pick_current)
            print("pick tail : %s at %s" % (pick_tail, hour))
            break
        proposed_df["not pick"] = proposed_df["Receiving"] + proposed_df["Pack"]
        proposed_df.sort_values(by="not pick", inplace=True)
        chosen = proposed_df.head(1)
        current_queue.append(chosen.ID.values[0])
        queue_df.loc[chosen.ID.values[0], hour] = "Pick"
        pick_current += chosen.Pick.values[0]
    excess = 0
    if pick_current > pick_goal:
        excess = pick_current - pick_goal
    while pack_current < pack_goal:
        proposed_df = work_df.loc[(work_df.Pack > 0) & (~work_df.ID.isin(current_queue)), :]
        if len(proposed_df) == 0:
            pack_tail = (pack_goal - pack_current)
            print("pack tail : %s at %s" % (pack_tail, hour))
            break
        proposed_df["not pack"] = proposed_df["Receiving"] + proposed_df["Pick"]
        proposed_df.sort_values(by="not pack", inplace=True)
        chosen = proposed_df.head(1)
        current_queue.append(chosen.ID.values[0])
        queue_df.loc[chosen.ID.values[0], hour] = "Pack"
        if excess > 0:
            pack_current += (chosen.Pick.values[0] + excess)
            excess = 0
        else:
            pack_current += chosen.Pick.values[0]
    excess = 0
    if pack_current > pack_goal:
        excess = pack_current - pack_goal
    while receiving_current < receiving_goal:
        proposed_df = work_df.loc[(work_df.Receiving > 0) & (~work_df.ID.isin(current_queue)), :]
        if len(proposed_df) == 0:
            receiving_tail = (receiving_goal - receiving_current)
            print("pack tail : %s at %s" % (receiving_tail, hour))
            break
        proposed_df["not receiving"] = proposed_df["Pack"] + proposed_df["Pick"]
        proposed_df.sort_values(by="not receiving", inplace=True)
        chosen = proposed_df.head(1)
        current_queue.append(chosen.ID.values[0])
        queue_df.loc[chosen.ID.values[0], hour] = "Rece."
        if excess > 0:
            receiving_current += (chosen.Receiving.values[0] + excess)
            excess = 0
        else:
            receiving_current += chosen.Receiving.values[0]
    print(" QUEUE : %s " % current_queue)
    print(hour + " - pick: " + str(pick_current) + " - pack: " + str(pack_current) + " - receiving: " + str(receiving_current))
print(queue_df)

