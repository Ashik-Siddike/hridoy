from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_content
import time

def main():
    while True:
        print("\n1. নতুন ওয়েবসাইট স্ক্র্যাপ করুন")
        print("2. প্রোগ্রাম বন্ধ করুন")
        
        choice = input("\nআপনার পছন্দ (1-2): ")
        
        if choice == "1":
            # ওয়েবসাইট URL ইনপুট নিন
            website_url = input("\nওয়েবসাইট URL দিন: ")
            
            try:
                # Chrome-এ ওয়েবসাইট খুলুন
                html_content = scrape_website(website_url)
                
                print("\nChrome ব্রাউজারে সাইট খোলা হয়েছে!")
                print("আপনি এখন ব্রাউজারে সাইটটি দেখতে পারবেন")
                print("স্ক্র্যাপিং শেষ হলে ব্রাউজার বন্ধ করে দিন")
                
                # ইউজার ইনপুট অপেক্ষা
                input("\nপরবর্তী ধাপে যেতে এন্টার চাপুন...")
                
                # পার্সিং এবং প্রসেসিং
                if html_content:
                    body_content = extract_body_content(html_content)
                    cleaned_content = clean_body_content(body_content)
                    content_chunks = split_dom_content(cleaned_content)
                    
                    print("\nপার্স করা ডাটা:")
                    for chunk in content_chunks:
                        parsed_data = parse_content(chunk)
                        print(parsed_data)
                        print("-" * 50)
                
            except Exception as e:
                print(f"\nএরর: {str(e)}")
            
        elif choice == "2":
            print("\nপ্রোগ্রাম বন্ধ হচ্ছে...")
            break
        
        else:
            print("\nভুল পছন্দ! আবার চেষ্টা করুন")

if __name__ == "__main__":
    main()
