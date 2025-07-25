import datetime


scan_history=[]



def log_scan(caption, user_command):
    timestamp=datetime.datetime.now().strftime('%d-%m-%Y,%H:%M:%S')
    entry={
        timestamp:"timestamp",
        caption: "caption",
        user_command:"user_command",

    }
    

    scan_history.append(entry)
    print("Logged time and data")

    def show_history():
        print("Scan History")
        for i,entry in enumerate(scan_history,start=1):
         print(f"\n🔹 Entry {i}")
        print("\n Time:{Entry[timestamp]}")
        print("\n Caption:{Entry[caption]}")
        print("\n User Command:{Entry[user_command]}")




    #Demonstrating with examples:
    log_scan("A Man passing the main road", "Alert User")
    log_scan("A family roaming in a busy market","Describe the surroundings")
    log_scan("Animal moving freely in the zoo","Describe the surroundings")


    
    #Logs

    show_history()