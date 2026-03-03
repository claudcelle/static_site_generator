from textnode import *
from htmlnode import *
  

def main() -> None:
    a = TextNode("aaa",TextType.PLAIN,"www.mypage_doesnt_exist.it")
    print(a)

if __name__ == "__main__":
    main()
