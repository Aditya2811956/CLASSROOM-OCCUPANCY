import streamlit as st
import pandas as pd
import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Occupancy Visualizer", layout="wide")
st.title("🏫 Classroom Occupancy Visualizer")

# ----------------------------
# AB-1 Layout
# ----------------------------
ab1_rooms = {
    0: {f"00{i}": {"always_occupied": False} for i in range(1, 11)},
    1: {f"1{i:02d}": {"always_occupied": False} for i in range(1, 40)},
    2: {f"2{i:02d}": {"always_occupied": False} for i in range(1, 36)},
    3: {f"3{i:02d}": {"always_occupied": False} for i in range(1, 34)},
    4: {f"4{i:02d}": {"always_occupied": False} for i in range(1, 39)},
}
# Add always-occupied overrides for AB-1
ab1_rooms[0].update({"001": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "003": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "009": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "010": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}})

ab1_rooms[1].update({"101": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "102": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "114": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "115": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "116": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "122": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}})
for i in range(31, 40):
    ab1_rooms[1][f"1{i}"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}

ab1_rooms[2].update({"201": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "213": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "214": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "215": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "219": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "221": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "223": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}})
for i in range(27, 36):
    ab1_rooms[2][f"2{i}"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}

ab1_rooms[3].update({"304": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "308": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "309": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "LIB": {"always_occupied": True, "label": "Library"}})
for i in range(25, 34):
    ab1_rooms[3][f"3{i}"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}

ab1_rooms[4].update({"401": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "405": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "411": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "413": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "414": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "415": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "420": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"},
                     "421": {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}})
for i in range(30, 39):
    ab1_rooms[4][f"4{i}"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}

# ----------------------------
# AB-2 Layout (your existing one)
# ----------------------------
ab2_rooms = {
   0: {  # 0th floor
        "001": {"always_occupied": True, "label": "Library"},
        "002": {"always_occupied": True, "label": "Always Occupied"},
        "003": {"always_occupied": False},
        "004": {"always_occupied": False},
    },
    1: {  # 1st floor - 14 rooms
        **{f"1{i:02d}": {"always_occupied": False} for i in range(1, 15)},
        "105": {"always_occupied": True, "label": "Teacher Cabin"},
        "106": {"always_occupied": True, "label": "Teacher Cabin"},
        "107": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    2: {  # 2nd floor
        "201": {"always_occupied": False},
        "202": {"always_occupied": False},
        "203": {"always_occupied": False},
        "204": {"always_occupied": False},
        "205": {"always_occupied": True, "label": "Teacher Cabin"},
        "206": {"always_occupied": False, "label": "SBG Hall"},
    },
    3: {  # 3rd floor - 8 rooms
        **{f"3{i:02d}": {"always_occupied": False} for i in range(1, 9)},
        "305": {"always_occupied": True, "label": "Teacher Cabin"},
        "306": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    4: {  # 4th floor - 14 rooms
        **{f"4{i:02d}": {"always_occupied": False} for i in range(1, 15)},
        "405": {"always_occupied": True, "label": "Teacher Cabin"},
        "407": {"always_occupied": True, "label": "Teacher Cabin"},
        "408": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    5: {  # 5th floor - 12 rooms
        **{f"5{i:02d}": {"always_occupied": False} for i in range(1, 13)},
        "505": {"always_occupied": True, "label": "Teacher Cabin"},
        "506": {"always_occupied": True, "label": "Teacher Cabin"},
        "507": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    6: {  # 6th floor - 13 rooms
        **{f"6{i:02d}": {"always_occupied": False} for i in range(1, 14)},
        "605": {"always_occupied": True, "label": "Teacher Cabin"},
        "606": {"always_occupied": True, "label": "Teacher Cabin"},
        "607": {"always_occupied": True, "label": "Teacher Cabin"},
        "612": {"always_occupied": True, "label": "Teacher Cabin"},
        "613": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    7: {  # 7th floor - 12 rooms
        **{f"7{i:02d}": {"always_occupied": False} for i in range(1, 13)},
        "705": {"always_occupied": True, "label": "Teacher Cabin"},
        "706": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    8: {  # 8th floor - 13 rooms
        **{f"8{i:02d}": {"always_occupied": False} for i in range(1, 14)},
        "805": {"always_occupied": True, "label": "Teacher Cabin"},
        "806": {"always_occupied": True, "label": "Teacher Cabin"},
        "807": {"always_occupied": True, "label": "Teacher Cabin"},
    },
    9: {  # 9th floor - NB rooms
        **{f"NB{i}": {"always_occupied": False} for i in range(1, 13)},
    }
}

# ----------------------------
# AB-3 Layout (Updated)
# ----------------------------
ab3_rooms = {
    0: {"000": {"always_occupied": True, "label": "Inactive"}},  # 0th floor (red block)
    1: {"100": {"always_occupied": True, "label": "Inactive"}},  # 1st floor (red block)

    2: {f"2{i:02d}": {"always_occupied": False} for i in range(1, 8)},  # 7 rooms
    3: {f"3{i:02d}": {"always_occupied": False} for i in range(1, 7)},  # 6 rooms
    4: {f"4{i:02d}": {"always_occupied": False} for i in range(1, 8)},  # 7 rooms
    5: {f"5{i:02d}": {"always_occupied": False} for i in range(1, 8)},  # 7 rooms
    6: {f"6{i:02d}": {"always_occupied": False} for i in range(1, 9)},  # 8 rooms

    7: {"700": {"always_occupied": True, "label": "Inactive"}},  # 7th floor (red block)

    8: {f"8{i:02d}": {"always_occupied": False} for i in range(1, 8)},  # 7 rooms
    9: {f"9{i:02d}": {"always_occupied": False} for i in range(1, 8)},  # 7 rooms
    10: {f"10{i:02d}": {"always_occupied": False} for i in range(1, 9)},  # 8 rooms (depends on timetable)
}

# Teacher's cabins (always occupied)
ab3_rooms[2]["205"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}
ab3_rooms[3]["304"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}
ab3_rooms[4]["405"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}
ab3_rooms[5]["505"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}
ab3_rooms[6]["603"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}
ab3_rooms[8]["805"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}
ab3_rooms[9]["905"] = {"always_occupied": True, "label": "Teacher's Cabin Always Occupied"}

# ----------------------------
# Choose Building
# ----------------------------
building_choice = st.radio("🏢 Select Building", ["AB-1", "AB-2", "AB-3"])
if building_choice == "AB-1":
    building_rooms = ab1_rooms
elif building_choice == "AB-2":
    building_rooms = ab2_rooms
else:
    building_rooms = ab3_rooms

# ----------------------------
# File Uploader
# ----------------------------
uploaded_file = st.file_uploader("Upload your cleaned timetable (Excel/CSV)", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = [c.strip() for c in df.columns]

    # Current Day + Day Selector
    now = datetime.datetime.now()
    today_day = now.strftime("%a").upper()
    days_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    selected_day = st.selectbox("📅 Select Day", options=days_list, index=days_list.index(today_day))
    st.info(f"📌 Showing schedule for: {selected_day}")

    # Manual Time Selector
    col1, col2, col3 = st.columns([1, 1, 1])
    hour = col1.selectbox("Hour", options=[i for i in range(1, 13)],
                          index=(now.hour % 12) - 1 if now.hour % 12 != 0 else 11)
    minute = col2.selectbox("Minute", options=[f"{i:02d}" for i in range(0, 60)], index=now.minute)
    am_pm = col3.selectbox("AM/PM", options=["AM", "PM"], index=0 if now.hour < 12 else 1)

    selected_hour = hour % 12
    if am_pm == "PM":
        selected_hour += 12
    selected_time = datetime.time(hour=selected_hour, minute=int(minute))
    st.markdown(f"⏱ Selected Time: **{selected_time.strftime('%I:%M %p')}**")

    # Filter classes
    today_classes = df[df["Day"].str.upper().str.startswith(selected_day)]

    # Display Floor-wise
    for floor, rooms in building_rooms.items():
        st.subheader(f"🏢 Floor {floor}")
        room_list = list(rooms.items())

        for chunk in range(0, len(room_list), 10):  # rows of 10
            cols = st.columns(10)
            for j, (room, info) in enumerate(room_list[chunk:chunk+10]):
                occupied, subject, teacher = False, "", ""
                if info.get("always_occupied", False):
                    occupied = True
                    subject = info.get("label", "Occupied")
                else:
                    room_classes = today_classes[today_classes["Room Number"].astype(str) == room]
                    for _, row in room_classes.iterrows():
                        try:
                            start = pd.to_datetime(str(row["Start Time"])).time()
                            end = pd.to_datetime(str(row["End Time"])).time()
                            if start <= selected_time < end:
                                occupied = True
                                subject = row.get("Subject/Lab", "")
                                teacher = row.get("Teacher", "")
                                break
                        except Exception as e:
                            st.warning(f"⚠️ Error parsing time for room {room}: {e}")

                # Determine color based on occupancy
                if info.get("label") == "Inactive":
                   color = "red"
                   occupied = True  # force it to show as occupied
                   subject = "Inactive"
                elif occupied:  # includes timetable-based occupancy and always_occupied
                   color = "yellow"
                else:
                   color = "green"

                text = f"<b>{room}</b><br>{'📚 ' + subject if subject else '🟢 Free'}"
                if teacher:
                    text += f"<br>👨‍🏫 {teacher}"

                cols[j].markdown(
                    f"""
                    <div style='background:{color};
                                padding:15px;
                                border-radius:10px;
                                text-align:center;
                                font-weight:bold;
                                color:black;
                                margin:5px;
                                min-height:90px'>
                        {text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
else:
    st.info("📂 Please upload your cleaned timetable (Excel/CSV) to visualize occupancy.")
