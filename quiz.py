from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdGryVG9q--lZmQ60k2ih8BPI2NDBHsEkWqJ-qXJDpTZn8AopGE6IT9BUzk657PXjKj_Em_LjnAo9nZMiG3efu_GTlu44xgypG3yr_w7VPNmvxBtAY1DRBVYwVvdn9g_onv1F6X5KNwgP4Z4BYns640tEOpaAIHkRcQIxCpStIdDXc-Yw='

def main():
    f = Fernet(key)
    print(f.decrypt(message))

if __name__ == "__main__":
    main()