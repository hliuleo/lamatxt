import sys, os

# 需要检查内部class等内容
def tag_validator(str):
    if len(str)<=2:
        return False
    if str[0] != '<' or str[len(str)-1] != '>':
        return False
    return True
    

def get_tag_name(tag_str):
    #print('get_name_name:' + tag_str)
    space_index = tag_str.find(' ')
    if (space_index > -1):
        return tag_str[1:space_index]
    else:
        return tag_str[1:-1]



class HtmlValidator():
    tag_stack = []
    html_str = ''
    cursorStart = -1
    cursorEnd = 0
    def __init__(self, html_str):
        self.html_str = html_str

    def findNextTag(self):
        nextTagStart = self.html_str.find('<', self.cursorEnd)
        if (nextTagStart >= 0):
            nextTagEnd = self.html_str.find('>', nextTagStart) + 1
        else:
            return False
        self.cursorStart = nextTagStart
        self.cursorEnd = nextTagEnd
    

    def validate(self):
        while (self.findNextTag() != False):
            tag_name = get_tag_name(self.html_str[self.cursorStart:self.cursorEnd])
            if tag_name[0] != '/':
                self.tag_stack.append(tag_name)
            else:
                if (self.tag_stack[-1] == tag_name[1:]):
                    self.tag_stack.pop()
                else:
                    print(self.html_str[0:self.cursorEnd])
                    return False
        return True


if __name__ == '__main__':
    path = sys.argv[1]
    if os.path.isdir(path):
        print('Validate html files in ' + path)
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path.endswith('.html'):
                    continue
                print("Validating file: " + file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                html_validator = HtmlValidator(content)
                if html_validator.validate() == True:
                    print('Correct!')
    elif os.path.isfile(path):
        file_path = path
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("Validating file: " + file_path)
        html_validator = HtmlValidator(content)
        if html_validator.validate() == True:
            print('Correct!')
    else:
        print('Invalid Path, Please make sure input a File path or Directory path')
    
    
