import datetime


scan_history = []

 # FUNCTION TO LOG SCAN ENTRY
def log_scan(caption, user_command):
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
    entry = {
        "timestamp": timestamp,       # Key = "timestamp", value = current time
        "caption": caption,           # Key = "caption", value = passed caption
        "user_command": user_command  # Key = "user_command", value = passed command
    }
    scan_history.append(entry)
    print("✅ Logged entry successfully!")

#  FUNCTION TO SHOW ALL HISTORY (DEFINED OUTSIDE log_scan)
def show_history():
    if not scan_history:
        print("\n📭 No scan history available.")
        return

    print("\n📜 Scan History:")
    for i, entry in enumerate(scan_history, start=1):
        print(f"\n🔹 Entry {i}")
        print(f"   🕒 Time: {entry['timestamp']}")
        print(f"   🖼️ Caption: {entry['caption']}")
        print(f"   💬 User Command: {entry['user_command']}")

# DEMO — WRAPPED IN if __name__ == "__main__"
if __name__ == "__main__":
    log_scan("A man passing the main road", "Alert User")
    log_scan("A family roaming in a busy market", "Describe the surroundings")
    log_scan("Animal moving freely in the zoo", "Describe the surroundings")

    show_history()
