import requests

def main():
    response = requests.get("http://google.com")
    print ("Status Code : ",response.status_code)
    print ("Headers : ", response.headers)
    print ("Content type : ", response.headers['Content-Type'])
    print ("Content : ", response.content)



if __name__ == "__main__":
    main()