import subprocess
import sys

SCRIPTS = {
    "1": "urlscrapperyt.py",
    "2": "videodownloder.py",
    "3": "shorts_creator.py"
}

def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Script '{script_name}' failed: {e}")

def run_full_pipeline():
    print("\n⚙️ Running Full Pipeline (Downloader ➡️ Shorts Creator)")
    run_script(SCRIPTS["2"])  # Downloader
    run_script(SCRIPTS["3"])  # Shorts Creator
    print("✅ Full pipeline completed.\n")

def main_menu():
    while True:
        print("\n🎬 ShortsMaker Terminal Menu")
        print("1. 🔍 Run URL Scraper")
        print("2. ⬇️  Run Downloader")
        print("3. ✂️  Run Shorts Creator")
        print("4. ❌ Exit")
        print("5. 🤖 Run Full Pipeline (Downloader + Shorts)")

        choice = input("Select an option (1-5): ").strip()

        if choice in SCRIPTS:
            run_script(SCRIPTS[choice])
        elif choice == "4":
            print("👋 Exiting. Goodbye!")
            break
        elif choice == "5":
            run_full_pipeline()
        else:
            print("⚠️ Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main_menu()
